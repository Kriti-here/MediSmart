import reflex as rx
from reflex_enterprise.components.map.types import LatLng, latlng
import httpx
import asyncio
import math
import logging

CITY_PHARMACIES = {
    "Jamshedpur": {
        "name": "MediSmart Pharmacy, Bistupur",
        "lat": 22.8046,
        "lng": 86.2029,
        "address": "Main Road, Bistupur, Jamshedpur 831001",
    },
    "Mumbai": {
        "name": "MediSmart Pharmacy, Andheri",
        "lat": 19.1197,
        "lng": 72.8464,
        "address": "SV Road, Andheri West, Mumbai 400058",
    },
    "Delhi": {
        "name": "MediSmart Pharmacy, Connaught Place",
        "lat": 28.6315,
        "lng": 77.2167,
        "address": "Block A, Connaught Place, New Delhi 110001",
    },
    "Bangalore": {
        "name": "MediSmart Pharmacy, Koramangala",
        "lat": 12.9352,
        "lng": 77.6245,
        "address": "80 Feet Road, Koramangala, Bangalore 560034",
    },
    "Kolkata": {
        "name": "MediSmart Pharmacy, Park Street",
        "lat": 22.551,
        "lng": 88.3521,
        "address": "Park Street, Kolkata 700016",
    },
    "Chennai": {
        "name": "MediSmart Pharmacy, T Nagar",
        "lat": 13.0418,
        "lng": 80.2341,
        "address": "Usman Road, T Nagar, Chennai 600017",
    },
    "Hyderabad": {
        "name": "MediSmart Pharmacy, Banjara Hills",
        "lat": 17.4156,
        "lng": 78.4347,
        "address": "Road No 12, Banjara Hills, Hyderabad 500034",
    },
    "Pune": {
        "name": "MediSmart Pharmacy, FC Road",
        "lat": 18.5273,
        "lng": 73.8407,
        "address": "Fergusson College Road, Pune 411004",
    },
}
SHOP_MEDICINES = [
    {
        "id": "1",
        "brand_name": "Crocin",
        "generic_name": "Paracetamol",
        "salt_composition": "Paracetamol 500mg",
        "brand_price": 40.0,
        "generic_price": 12.0,
        "manufacturer": "GSK",
        "dosage": "Tablet",
        "verified": True,
        "category": "Analgesic",
        "expiry_date": "2025-08-15",
    },
    {
        "id": "2",
        "brand_name": "Augmentin 625",
        "generic_name": "Amoxycillin + Clavulanic Acid",
        "salt_composition": "Amoxycillin (500mg) + Clavulanic Acid (125mg)",
        "brand_price": 200.0,
        "generic_price": 85.0,
        "manufacturer": "GSK",
        "dosage": "Tablet",
        "verified": True,
        "category": "Antibiotic",
        "expiry_date": "2025-10-15",
    },
    {
        "id": "3",
        "brand_name": "Combiflam",
        "generic_name": "Ibuprofen + Paracetamol",
        "salt_composition": "Ibuprofen (400mg) + Paracetamol (325mg)",
        "brand_price": 45.0,
        "generic_price": 15.0,
        "manufacturer": "Sanofi",
        "dosage": "Tablet",
        "verified": True,
        "category": "Analgesic",
        "expiry_date": "2025-06-01",
    },
    {
        "id": "4",
        "brand_name": "Allegra 120mg",
        "generic_name": "Fexofenadine",
        "salt_composition": "Fexofenadine (120mg)",
        "brand_price": 180.0,
        "generic_price": 60.0,
        "manufacturer": "Sanofi",
        "dosage": "Tablet",
        "verified": True,
        "category": "Antihistamine",
        "expiry_date": "2025-12-01",
    },
    {
        "id": "5",
        "brand_name": "Pan 40",
        "generic_name": "Pantoprazole",
        "salt_composition": "Pantoprazole (40mg)",
        "brand_price": 150.0,
        "generic_price": 40.0,
        "manufacturer": "Alkem",
        "dosage": "Tablet",
        "verified": True,
        "category": "Antacid",
        "expiry_date": "2025-08-01",
    },
    {
        "id": "6",
        "brand_name": "Calpol 500",
        "generic_name": "Paracetamol",
        "salt_composition": "Paracetamol 500mg",
        "brand_price": 35.0,
        "generic_price": 12.0,
        "manufacturer": "GSK",
        "dosage": "Tablet",
        "verified": True,
        "category": "Analgesic",
        "expiry_date": "2026-03-20",
    },
    {
        "id": "7",
        "brand_name": "Glycomet 500",
        "generic_name": "Metformin",
        "salt_composition": "Metformin (500mg)",
        "brand_price": 60.0,
        "generic_price": 18.0,
        "manufacturer": "USV",
        "dosage": "Tablet",
        "verified": True,
        "category": "Anti-Diabetic",
        "expiry_date": "2025-08-20",
    },
    {
        "id": "8",
        "brand_name": "Telma 40",
        "generic_name": "Telmisartan",
        "salt_composition": "Telmisartan (40mg)",
        "brand_price": 110.0,
        "generic_price": 35.0,
        "manufacturer": "Glenmark",
        "dosage": "Tablet",
        "verified": True,
        "category": "Hypertension",
        "expiry_date": "2026-06-15",
    },
    {
        "id": "9",
        "brand_name": "Voveran SR 100",
        "generic_name": "Diclofenac",
        "salt_composition": "Diclofenac (100mg)",
        "brand_price": 95.0,
        "generic_price": 30.0,
        "manufacturer": "Novartis",
        "dosage": "Tablet",
        "verified": True,
        "category": "Pain Relief",
        "expiry_date": "2025-09-15",
    },
    {
        "id": "10",
        "brand_name": "Taxim-O 200",
        "generic_name": "Cefixime",
        "salt_composition": "Cefixime (200mg)",
        "brand_price": 160.0,
        "generic_price": 70.0,
        "manufacturer": "Alkem",
        "dosage": "Tablet",
        "verified": True,
        "category": "Antibiotic",
        "expiry_date": "2025-11-20",
    },
    {
        "id": "11",
        "brand_name": "Dolo 650",
        "generic_name": "Paracetamol",
        "salt_composition": "Paracetamol 650mg",
        "brand_price": 30.0,
        "generic_price": 15.0,
        "manufacturer": "Micro Labs",
        "dosage": "Tablet",
        "verified": True,
        "category": "Analgesic",
        "expiry_date": "2025-07-25",
    },
    {
        "id": "12",
        "brand_name": "Limcee",
        "generic_name": "Vitamin C",
        "salt_composition": "Vitamin C (500mg)",
        "brand_price": 25.0,
        "generic_price": 10.0,
        "manufacturer": "Abbott",
        "dosage": "Chewable Tablet",
        "verified": True,
        "category": "Vitamin",
        "expiry_date": "2026-12-31",
    },
    {
        "id": "13",
        "brand_name": "Azithral 500",
        "generic_name": "Azithromycin",
        "salt_composition": "Azithromycin (500mg)",
        "brand_price": 120.0,
        "generic_price": 55.0,
        "manufacturer": "Alembic",
        "dosage": "Tablet",
        "verified": True,
        "category": "Antibiotic",
        "expiry_date": "2025-10-10",
    },
    {
        "id": "14",
        "brand_name": "Thyronorm 50",
        "generic_name": "Levothyroxine",
        "salt_composition": "Levothyroxine (50mcg)",
        "brand_price": 140.0,
        "generic_price": 50.0,
        "manufacturer": "Abbott",
        "dosage": "Tablet",
        "verified": True,
        "category": "Thyroid",
        "expiry_date": "2026-01-15",
    },
    {
        "id": "15",
        "brand_name": "Atorva 10",
        "generic_name": "Atorvastatin",
        "salt_composition": "Atorvastatin (10mg)",
        "brand_price": 85.0,
        "generic_price": 25.0,
        "manufacturer": "Zydus",
        "dosage": "Tablet",
        "verified": True,
        "category": "Cholesterol",
        "expiry_date": "2026-05-10",
    },
]


class CheckoutState(rx.State):
    house_no: str = ""
    area: str = ""
    landmark: str = ""
    pincode: str = ""
    address_error: str = ""
    is_geocoding: bool = False
    geocode_status: str = ""
    selected_city: str = "Jamshedpur"
    shop_lat: float = 22.8046
    shop_lng: float = 86.2029
    shop_name: str = "MediSmart Pharmacy, Bistupur"
    shop_address: str = "Main Road, Bistupur, Jamshedpur 831001"
    user_lat: float = 0.0
    user_lng: float = 0.0
    user_address_resolved: str = ""
    has_user_location: bool = False
    map_center: LatLng = latlng(lat=22.8046, lng=86.2029)
    map_zoom: float = 13.0
    route_positions: list[LatLng] = []
    order_submitted: bool = False
    order_loading: bool = False
    saved_order: dict = {}
    cart_items: list[dict] = []
    is_gps_loading: bool = False
    shop_search_query: str = ""
    shop_category_filter: str = "All"
    shop_sort_by: str = "savings"
    show_cart_drawer: bool = False

    @rx.var
    def available_categories(self) -> list[str]:
        cats = set((m["category"] for m in SHOP_MEDICINES))
        return ["All"] + sorted(list(cats))

    @rx.var
    def filtered_shop_medicines(self) -> list[dict]:
        query = self.shop_search_query.lower()
        filtered = []
        for m in SHOP_MEDICINES:
            if query and (
                not (
                    query in m["brand_name"].lower()
                    or query in m["generic_name"].lower()
                    or query in m["salt_composition"].lower()
                )
            ):
                continue
            if (
                self.shop_category_filter != "All"
                and m["category"] != self.shop_category_filter
            ):
                continue
            filtered.append(m)
        if self.shop_sort_by == "savings":
            filtered.sort(
                key=lambda x: x["brand_price"] - x["generic_price"], reverse=True
            )
        elif self.shop_sort_by == "price_low":
            filtered.sort(key=lambda x: x["generic_price"])
        elif self.shop_sort_by == "price_high":
            filtered.sort(key=lambda x: x["generic_price"], reverse=True)
        elif self.shop_sort_by == "name":
            filtered.sort(key=lambda x: x["brand_name"])
        return filtered

    @rx.event
    def set_shop_search(self, query: str):
        self.shop_search_query = query

    @rx.event
    def set_shop_category(self, category: str):
        self.shop_category_filter = category

    @rx.event
    def set_shop_sort(self, sort: str):
        self.shop_sort_by = sort

    @rx.event
    def toggle_cart_drawer(self):
        self.show_cart_drawer = not self.show_cart_drawer

    @rx.event
    def close_cart_drawer(self):
        self.show_cart_drawer = False

    @rx.event
    def open_cart_drawer(self):
        self.show_cart_drawer = True

    @rx.var
    def cart_total(self) -> float:
        return sum((item["price"] * item["qty"] for item in self.cart_items))

    @rx.var
    def cart_item_count(self) -> int:
        return sum((item["qty"] for item in self.cart_items))

    @rx.event
    def set_city(self, city: str):
        self.selected_city = city
        if city in CITY_PHARMACIES:
            pharmacy = CITY_PHARMACIES[city]
            self.shop_name = pharmacy["name"]
            self.shop_address = pharmacy["address"]
            self.shop_lat = pharmacy["lat"]
            self.shop_lng = pharmacy["lng"]
            self.map_center = latlng(lat=self.shop_lat, lng=self.shop_lng)
            self.map_zoom = 13.0
            self.has_user_location = False
            self.user_lat = 0.0
            self.user_lng = 0.0
            self.user_address_resolved = ""
            self.route_positions = []

    @rx.event
    def add_to_cart(self, name: str, price: float, qty: int = 1):
        for item in self.cart_items:
            if item["name"] == name:
                item["qty"] += qty
                yield rx.toast(f"Added another {name} to cart", duration=2000)
                return
        self.cart_items.append({"name": name, "qty": qty, "price": float(price)})
        yield rx.toast(f"Added {name} to cart", duration=2000)

    @rx.event
    def remove_from_cart(self, name: str):
        self.cart_items = [item for item in self.cart_items if item["name"] != name]

    @rx.event
    def update_qty(self, name: str, qty: int):
        for item in self.cart_items:
            if item["name"] == name:
                item["qty"] = max(1, qty)
                break

    @rx.var
    def full_address(self) -> str:
        parts = [self.house_no, self.area, self.landmark, self.pincode]
        return ", ".join((p for p in parts if p.strip()))

    @rx.var
    def delivery_distance_km(self) -> float:
        if not self.has_user_location:
            return 0.0
        R = 6371.0
        dlat = math.radians(self.user_lat - self.shop_lat)
        dlon = math.radians(self.user_lng - self.shop_lng)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(self.shop_lat))
            * math.cos(math.radians(self.user_lat))
            * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round(R * c, 1)

    @rx.var
    def estimated_delivery_time(self) -> str:
        d = self.delivery_distance_km
        if d == 0:
            return "—"
        mins = max(15, int(d * 3))
        if mins >= 60:
            return f"{mins // 60}h {mins % 60}min"
        return f"{mins} min"

    def _generate_route_points(self):
        """Generate intermediate points between shop and user for a polyline route."""
        if not self.has_user_location:
            self.route_positions = []
            return
        num_points = 8
        points = []
        for i in range(num_points + 1):
            t = i / num_points
            lat = self.shop_lat + t * (self.user_lat - self.shop_lat)
            lng = self.shop_lng + t * (self.user_lng - self.shop_lng)
            if 0 < t < 1:
                offset = math.sin(t * math.pi) * 0.003
                lat += offset
            points.append(latlng(lat=lat, lng=lng))
        self.route_positions = points

    @rx.event(background=True)
    async def geocode_address(self, form_data: dict):
        """Geocode the address using Nominatim and update map."""
        async with self:
            self.house_no = form_data.get("house_no", "").strip()
            self.area = form_data.get("area", "").strip()
            self.landmark = form_data.get("landmark", "").strip()
            self.pincode = form_data.get("pincode", "").strip()
            self.address_error = ""
            if not self.area:
                self.address_error = "Area/Street is required"
                return
            if (
                not self.pincode
                or len(self.pincode) != 6
                or (not self.pincode.isdigit())
            ):
                self.address_error = "Valid 6-digit pincode is required"
                return
            self.is_geocoding = True
            self.geocode_status = "Locating your address..."
        try:
            query_parts = [
                self.house_no,
                self.area,
                self.landmark,
                self.pincode,
                "Jamshedpur",
                "India",
            ]
            query = ", ".join((p for p in query_parts if p))
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={"q": query, "format": "json", "limit": 1},
                    headers={"User-Agent": "MediSmart/1.0"},
                    timeout=10.0,
                )
                resp.raise_for_status()
                data = resp.json()
                if not data:
                    resp2 = await client.get(
                        "https://nominatim.openstreetmap.org/search",
                        params={
                            "q": f"{self.area}, {self.pincode}, Jamshedpur, India",
                            "format": "json",
                            "limit": 1,
                        },
                        headers={"User-Agent": "MediSmart/1.0"},
                        timeout=10.0,
                    )
                    data = resp2.json()
                if data:
                    lat = float(data[0]["lat"])
                    lng = float(data[0]["lon"])
                    display = data[0].get("display_name", self.full_address)
                    async with self:
                        self.user_lat = lat
                        self.user_lng = lng
                        self.user_address_resolved = display
                        self.has_user_location = True
                        center_lat = (self.shop_lat + lat) / 2
                        center_lng = (self.shop_lng + lng) / 2
                        self.map_center = latlng(lat=center_lat, lng=center_lng)
                        dist = self.delivery_distance_km
                        if dist < 2:
                            self.map_zoom = 14.0
                        elif dist < 5:
                            self.map_zoom = 13.0
                        elif dist < 15:
                            self.map_zoom = 12.0
                        elif dist < 50:
                            self.map_zoom = 10.0
                        else:
                            self.map_zoom = 8.0
                        self._generate_route_points()
                        self.is_geocoding = False
                        self.geocode_status = ""
                else:
                    async with self:
                        self.address_error = "Could not locate this address. Please check the details or use GPS."
                        self.is_geocoding = False
                        self.geocode_status = ""
        except Exception as e:
            logging.exception(f"Geocoding error: {e}")
            async with self:
                self.address_error = (
                    "Network error while locating address. Please try again."
                )
                self.is_geocoding = False
                self.geocode_status = ""

    @rx.event
    def use_gps_location(self):
        """Trigger browser geolocation."""
        self.is_gps_loading = True
        self.address_error = ""
        self.geocode_status = "Getting your GPS location..."
        return rx.call_script(
            """
            return new Promise((resolve) => {
                navigator.geolocation.getCurrentPosition(
                    (pos) => resolve([pos.coords.latitude, pos.coords.longitude]),
                    (err) => {
                        let msg = "Location unavailable";
                        if (err.code === 1) msg = "Permission denied";
                        else if (err.code === 3) msg = "Timed out";
                        resolve(["error", msg]);
                    },
                    {enableHighAccuracy: true, timeout: 10000}
                );
            });
            """,
            callback=CheckoutState.receive_gps,
        )

    @rx.event(background=True)
    async def receive_gps(self, result):
        if not result or (
            isinstance(result, list) and len(result) > 0 and (result[0] == "error")
        ):
            async with self:
                self.is_gps_loading = False
                self.geocode_status = ""
                err = (
                    result[1]
                    if isinstance(result, list) and len(result) > 1
                    else "Unknown error"
                )
                self.address_error = (
                    f"GPS failed: {err}. Please enter address manually."
                )
            return
        lat, lon = (float(result[0]), float(result[1]))
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    "https://nominatim.openstreetmap.org/reverse",
                    params={"lat": lat, "lon": lon, "format": "json"},
                    headers={"User-Agent": "MediSmart/1.0"},
                    timeout=10.0,
                )
                data = resp.json()
                address = data.get("address", {})
                display = data.get("display_name", "Your Location")
                async with self:
                    self.user_lat = lat
                    self.user_lng = lon
                    self.user_address_resolved = display
                    self.has_user_location = True
                    self.is_gps_loading = False
                    self.geocode_status = ""
                    self.house_no = address.get("house_number", "")
                    self.area = (
                        address.get("road", "")
                        or address.get("suburb", "")
                        or address.get("neighbourhood", "")
                    )
                    self.landmark = address.get("suburb", "") or address.get(
                        "city_district", ""
                    )
                    self.pincode = address.get("postcode", "")
                    center_lat = (self.shop_lat + lat) / 2
                    center_lng = (self.shop_lng + lon) / 2
                    self.map_center = latlng(lat=center_lat, lng=center_lng)
                    dist = self.delivery_distance_km
                    if dist < 2:
                        self.map_zoom = 14.0
                    elif dist < 5:
                        self.map_zoom = 13.0
                    elif dist < 15:
                        self.map_zoom = 12.0
                    elif dist < 50:
                        self.map_zoom = 10.0
                    else:
                        self.map_zoom = 8.0
                    self._generate_route_points()
                    yield rx.toast(
                        "📍 Location detected! Address auto-filled.", duration=3000
                    )
        except Exception:
            logging.exception("Reverse geocode error")
            async with self:
                self.user_lat = lat
                self.user_lng = lon
                self.user_address_resolved = f"{lat:.4f}, {lon:.4f}"
                self.has_user_location = True
                self.is_gps_loading = False
                self.geocode_status = ""
                center_lat = (self.shop_lat + lat) / 2
                center_lng = (self.shop_lng + lon) / 2
                self.map_center = latlng(lat=center_lat, lng=center_lng)
                self.map_zoom = 12.0
                self._generate_route_points()

    @rx.event
    def submit_order(self):
        """Save order with address + coordinates."""
        if not self.has_user_location:
            self.address_error = "Please set your delivery address first."
            return
        self.order_loading = True
        yield
        self.saved_order = {
            "address": {
                "house_no": self.house_no,
                "area": self.area,
                "landmark": self.landmark,
                "pincode": self.pincode,
                "full_address": self.full_address,
                "resolved_address": self.user_address_resolved,
                "lat": self.user_lat,
                "lng": self.user_lng,
            },
            "shop": {
                "name": self.shop_name,
                "address": self.shop_address,
                "lat": self.shop_lat,
                "lng": self.shop_lng,
            },
            "items": self.cart_items,
            "total": self.cart_total,
            "distance_km": self.delivery_distance_km,
            "estimated_delivery": self.estimated_delivery_time,
        }
        self.order_submitted = True
        self.order_loading = False
        yield rx.toast(
            "🎉 Order placed successfully! Your medicines are on the way.",
            duration=5000,
        )

    @rx.event
    def reset_checkout(self):
        self.house_no = ""
        self.area = ""
        self.landmark = ""
        self.pincode = ""
        self.address_error = ""
        self.user_lat = 0.0
        self.user_lng = 0.0
        self.user_address_resolved = ""
        self.has_user_location = False
        self.route_positions = []
        self.order_submitted = False
        self.saved_order = {}
        self.map_center = latlng(lat=22.8046, lng=86.2029)
        self.map_zoom = 13.0

    @rx.event
    def clear_user_location(self):
        self.has_user_location = False