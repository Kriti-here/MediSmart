import reflex as rx
from typing import TypedDict
from reflex_enterprise.components.map.types import LatLng, latlng
import math
import urllib.parse
import httpx
import logging


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


class Pharmacy(TypedDict):
    id: str
    name: str
    address: str
    lat: float
    lng: float
    phone: str
    distance: float
    rating: float
    opening_hours: str
    brand: str
    status: str


class CommunityReport(TypedDict):
    id: str
    medicine_name: str
    pharmacy_name: str
    status: str
    time_ago: str


class PharmacyState(rx.State):
    pharmacies: list[Pharmacy] = []
    city_query: str = ""
    search_radius: int = 5
    is_loading: bool = False
    search_error: str = ""
    searched_city: str = ""
    total_results: int = 0
    popular_cities: list[str] = [
        "Mumbai",
        "Delhi",
        "Bangalore",
        "Chennai",
        "Kolkata",
        "Hyderabad",
        "Pune",
        "Ahmedabad",
        "Jaipur",
        "Lucknow",
        "Chandigarh",
        "Kochi",
    ]
    reports: list[CommunityReport] = [
        {
            "id": "r1",
            "medicine_name": "Crocin 500mg",
            "pharmacy_name": "Apollo Pharmacy",
            "status": "In Stock",
            "time_ago": "2 hours ago",
        },
        {
            "id": "r2",
            "medicine_name": "Augmentin 625",
            "pharmacy_name": "MedPlus",
            "status": "Out of Stock",
            "time_ago": "5 hours ago",
        },
        {
            "id": "r3",
            "medicine_name": "Pan 40",
            "pharmacy_name": "Jan Aushadhi Kendra",
            "status": "Low Stock",
            "time_ago": "1 day ago",
        },
    ]
    search_medicine: str = ""
    sort_by: str = "distance"
    map_center: LatLng = latlng(lat=20.5937, lng=78.9629)
    map_zoom: float = 4.0
    report_medicine: str = ""
    report_pharmacy: str = ""
    report_status: str = "In Stock"
    report_price: str = ""
    report_notes: str = ""
    retry_message: str = ""
    is_using_cached: bool = False
    cached_pharmacies: list[Pharmacy] = []
    cached_city: str = ""
    is_geolocating: bool = False
    geolocation_status: str = ""

    @rx.var
    def filtered_pharmacies(self) -> list[Pharmacy]:
        filtered = self.pharmacies
        if self.sort_by == "distance":
            filtered = sorted(filtered, key=lambda x: x["distance"])
        elif self.sort_by == "name":
            filtered = sorted(filtered, key=lambda x: x["name"])
        return filtered

    @rx.event
    def set_search_medicine(self, value: str):
        self.search_medicine = value

    @rx.event
    def set_sort_by(self, value: str):
        self.sort_by = value

    @rx.event
    def set_search_radius(self, value: str):
        self.search_radius = int(value)

    @rx.event
    def set_city_query(self, value: str):
        self.city_query = value

    @rx.event
    def search_popular_city(self, city: str):
        self.city_query = city
        yield PharmacyState.search_pharmacies({"city_query": city})

    async def _fetch_with_retry(self, client, method, url, max_retries=3, **kwargs):
        import asyncio
        import httpx

        for attempt in range(1, max_retries + 1):
            try:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except (httpx.TimeoutException, httpx.HTTPStatusError) as e:
                logging.exception("Unexpected error")
                if attempt == max_retries:
                    logging.error(f"All {max_retries} retries failed for {url}: {e}")
                    raise e
                logging.warning(f"Retry {attempt}/{max_retries} for {url}: {e}")
                async with self:
                    self.retry_message = (
                        f"Server busy, retrying... (attempt {attempt}/{max_retries})"
                    )
                await asyncio.sleep(2 ** (attempt - 1))

    def _parse_opening_status(self, opening_hours_str: str) -> str:
        if not opening_hours_str:
            return ""
        oh = opening_hours_str.lower()
        if "24/7" in oh or "24 hours" in oh or "00:00-24:00" in oh:
            return "Open Now"
        from datetime import datetime

        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
            curr_day = days[now.weekday()]
            if "-" in opening_hours_str and ":" in opening_hours_str:
                parts = opening_hours_str.split(" ")
                if len(parts) >= 2:
                    day_part = parts[0]
                    time_part = parts[1]
                    if "-" in day_part:
                        d_start, d_end = day_part.split("-")[:2]
                        if d_start in days and d_end in days:
                            start_idx = days.index(d_start)
                            end_idx = days.index(d_end)
                            if start_idx <= now.weekday() <= end_idx:
                                if "-" in time_part:
                                    t_start, t_end = time_part.split("-")[:2]
                                    if t_start <= current_time <= t_end:
                                        return "Open Now"
                                    else:
                                        return "Closed"
            return ""
        except Exception:
            logging.exception("Unexpected error")
            return ""

    def _handle_search_failure(self, error_msg: str):
        self.retry_message = ""
        if len(self.cached_pharmacies) > 0:
            self.pharmacies = self.cached_pharmacies
            self.is_using_cached = True
            self.total_results = len(self.cached_pharmacies)
            self.searched_city = self.cached_city
            self.is_loading = False
        else:
            self.search_error = error_msg
            self.is_loading = False

    @rx.event(background=True)
    async def search_pharmacies(self, form_data: dict):
        async with self:
            self.is_loading = True
            self.search_error = ""
            self.retry_message = ""
            self.is_using_cached = False
            self.pharmacies = []
            city_query = form_data.get("city_query", self.city_query)
            if not city_query and (not (form_data.get("lat") and form_data.get("lng"))):
                self.is_loading = False
                self.search_error = "Please enter a city name."
                return
            self.city_query = city_query
        try:
            import httpx

            async with httpx.AsyncClient() as client:
                if form_data.get("lat") and form_data.get("lng"):
                    lat = float(form_data["lat"])
                    lon = float(form_data["lng"])
                else:
                    try:
                        geo_r = await self._fetch_with_retry(
                            client,
                            "GET",
                            "https://nominatim.openstreetmap.org/search",
                            params={
                                "q": f"{city_query}, India",
                                "format": "json",
                                "limit": 1,
                            },
                            headers={"User-Agent": "MediSmart/1.0"},
                            timeout=10.0,
                        )
                    except httpx.TimeoutException as e:
                        logging.exception("Unexpected error")
                        logging.warning(f"Geocoding timed out for {city_query}: {e}")
                        async with self:
                            self._handle_search_failure(
                                "Search timed out. The pharmacy database may be under heavy load. Please try again in a moment."
                            )
                        return
                    except httpx.HTTPStatusError as e:
                        logging.exception("Unexpected error")
                        logging.warning(
                            f"Geocoding HTTP error {e.response.status_code} for {city_query}: {e}"
                        )
                        async with self:
                            self._handle_search_failure(
                                "Network error — please check your internet connection and try again."
                            )
                        return
                    except Exception:
                        logging.exception("Unexpected error")
                        async with self:
                            self._handle_search_failure(
                                "Network error — please check your internet connection and try again."
                            )
                        return
                    geo_data = geo_r.json()
                    if not geo_data:
                        async with self:
                            self._handle_search_failure(
                                f"No location found for '{city_query}'. Try a more specific city name like 'Andheri, Mumbai'"
                            )
                        return
                    lat = float(geo_data[0]["lat"])
                    lon = float(geo_data[0]["lon"])
                async with self:
                    self.map_center = latlng(lat=lat, lng=lon)
                    if self.search_radius <= 2:
                        self.map_zoom = 13.0
                    elif self.search_radius <= 5:
                        self.map_zoom = 12.0
                    elif self.search_radius <= 10:
                        self.map_zoom = 11.0
                    else:
                        self.map_zoom = 10.0
                delta_lat = self.search_radius / 111.0
                delta_lon = self.search_radius / (111.0 * math.cos(math.radians(lat)))
                south = lat - delta_lat
                west = lon - delta_lon
                north = lat + delta_lat
                east = lon + delta_lon
                query = f'\n                [out:json][timeout:25];\n                (\n                  node["amenity"="pharmacy"]({south:.4f},{west:.4f},{north:.4f},{east:.4f});\n                  way["amenity"="pharmacy"]({south:.4f},{west:.4f},{north:.4f},{east:.4f});\n                );\n                out center tags;\n                '
                async with self:
                    self.retry_message = ""
                try:
                    op_r = await self._fetch_with_retry(
                        client,
                        "POST",
                        "https://overpass-api.de/api/interpreter",
                        data={"data": query},
                        headers={"User-Agent": "MediSmart/1.0"},
                        timeout=30.0,
                    )
                except httpx.TimeoutException as e:
                    logging.exception("Unexpected error")
                    logging.warning(
                        f"Pharmacy search timed out for {self.city_query}: {e}"
                    )
                    async with self:
                        self._handle_search_failure(
                            "Search timed out. The pharmacy database may be under heavy load. Please try again in a moment."
                        )
                    return
                except httpx.HTTPStatusError as e:
                    logging.exception("Unexpected error")
                    logging.warning(
                        f"Pharmacy search HTTP error {e.response.status_code} for {self.city_query}: {e}"
                    )
                    async with self:
                        if e.response.status_code in [429, 503, 504]:
                            self._handle_search_failure(
                                "Pharmacy database is busy, retrying..."
                            )
                        else:
                            self._handle_search_failure(
                                "Network error — please check your internet connection and try again."
                            )
                    return
                except Exception:
                    logging.exception("Unexpected error")
                    async with self:
                        self._handle_search_failure(
                            "Network error — please check your internet connection and try again."
                        )
                    return
                try:
                    op_data = op_r.json()
                except Exception as e:
                    logging.exception(f"Error parsing Overpass JSON: {e}")
                    async with self:
                        self._handle_search_failure(
                            "Received an invalid response from the search service. Please try again."
                        )
                    return
                results = []
                for el in op_data.get("elements", [])[:50]:
                    tags = el.get("tags", {})
                    if el["type"] == "node":
                        plat, plon = (el.get("lat"), el.get("lon"))
                    else:
                        center = el.get("center", {})
                        plat, plon = (center.get("lat"), center.get("lon"))
                    addr_parts = [
                        tags.get("addr:housenumber", ""),
                        tags.get("addr:street", ""),
                        tags.get("addr:suburb", ""),
                        tags.get("addr:city", ""),
                        tags.get("addr:postcode", ""),
                    ]
                    address = (
                        tags.get("addr:full")
                        or ", ".join((p for p in addr_parts if p))
                        or "Address unavailable"
                    ).strip(", ")
                    distance = round(haversine(lat, lon, plat, plon), 1)
                    oh = tags.get("opening_hours") or ""
                    status = self._parse_opening_status(oh)
                    results.append(
                        {
                            "id": str(el.get("id", "")),
                            "name": tags.get("name")
                            or tags.get("name:en")
                            or "Pharmacy",
                            "address": address,
                            "lat": plat,
                            "lng": plon,
                            "phone": tags.get("phone")
                            or tags.get("contact:phone")
                            or "",
                            "distance": distance,
                            "rating": 0.0,
                            "opening_hours": oh,
                            "brand": tags.get("brand") or "",
                            "status": status,
                        }
                    )
                results.sort(key=lambda x: x["distance"])
                async with self:
                    if len(results) == 0:
                        self._handle_search_failure(
                            f"No pharmacies found within {self.search_radius}km of {self.city_query}. Try increasing the search radius."
                        )
                    else:
                        self.pharmacies = results
                        self.total_results = len(results)
                        self.searched_city = self.city_query
                        self.cached_pharmacies = results
                        self.cached_city = self.city_query
                        self.is_loading = False
                        self.retry_message = ""
        except Exception as e:
            logging.exception(f"Error fetching pharmacies: {e}")
            async with self:
                self._handle_search_failure(
                    "Network error — please check your internet connection and try again."
                )

    @rx.event
    def use_current_location(self):
        self.is_geolocating = True
        self.search_error = ""
        self.geolocation_status = "Getting your location..."
        return rx.call_script(
            """
            return new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(
                    (pos) => resolve([pos.coords.latitude, pos.coords.longitude]),
                    (err) => {
                        let msg;
                        if (err.code === 1) msg = "Permission denied. Please allow location access in your browser settings.";
                        else if (err.code === 2) msg = "Location unavailable. Your device could not determine your position.";
                        else if (err.code === 3) msg = "Location request timed out. Please try again or search manually.";
                        else msg = "Unknown geolocation error: " + err.message;
                        resolve(["error", msg]);
                    },
                    {enableHighAccuracy: true, timeout: 10000, maximumAge: 0}
                );
            });
            """,
            callback=PharmacyState.receive_geolocation,
        )

    @rx.event(background=True)
    async def receive_geolocation(self, result):
        if not result or (
            isinstance(result, list) and len(result) > 0 and (result[0] == "error")
        ):
            async with self:
                self.is_geolocating = False
                self.geolocation_status = ""
                err_msg = (
                    result[1]
                    if isinstance(result, list) and len(result) > 1
                    else "Unknown error"
                )
                yield rx.toast(f"Could not get your location: {err_msg}", level="error")
            return
        lat, lon = result
        async with self:
            self.geolocation_status = "Location found! Resolving address..."
            self.map_center = latlng(lat=lat, lng=lon)
        try:
            import httpx

            async with httpx.AsyncClient() as client:
                geo_r = await self._fetch_with_retry(
                    client,
                    "GET",
                    f"https://nominatim.openstreetmap.org/reverse",
                    params={"lat": lat, "lon": lon, "format": "json"},
                    headers={"User-Agent": "MediSmart/1.0"},
                    timeout=10.0,
                )
                geo_data = geo_r.json()
                address = geo_data.get("address", {})
                city = (
                    address.get("city")
                    or address.get("town")
                    or address.get("suburb")
                    or address.get("village")
                    or "Current Location"
                )
                async with self:
                    self.city_query = city
                    self.geolocation_status = ""
                    self.is_geolocating = False
                yield PharmacyState.search_pharmacies(
                    {"city_query": city, "lat": lat, "lng": lon}
                )
        except Exception:
            logging.exception("Unexpected error")
            async with self:
                self.is_geolocating = False
                self.geolocation_status = ""
                yield rx.toast(
                    "Found your location but couldn't resolve the address. Searching nearby...",
                    level="info",
                )
                yield PharmacyState.search_pharmacies(
                    {"city_query": "Current Location", "lat": lat, "lng": lon}
                )

    @rx.event
    def submit_report(self, form_data: dict):
        if not form_data.get("medicine") or not form_data.get("pharmacy"):
            yield rx.toast("Please fill all required fields", level="error")
            return
        new_report: CommunityReport = {
            "id": f"r{len(self.reports) + 1}",
            "medicine_name": form_data["medicine"],
            "pharmacy_name": form_data["pharmacy"],
            "status": form_data["status"],
            "time_ago": "Just now",
        }
        self.reports.insert(0, new_report)
        yield rx.toast("Thank you! Your report helps the community", duration=3000)