import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise.components.map.types import latlng
from app.components.navbar import navbar
from app.components.footer import footer
from app.components.chat_widget import chat_widget
from app.components.auth_modal import auth_modal
from app.components.cart_drawer import cart_drawer
from app.states.pharmacy_state import PharmacyState, Pharmacy, CommunityReport


def pharmacy_marker(pharmacy: Pharmacy) -> rx.Component:
    return rxe.map.marker(
        rxe.map.popup(
            rx.el.div(
                rx.el.h4(
                    pharmacy["name"], class_name="font-bold text-gray-900 m-0 text-sm"
                ),
                rx.el.p(
                    pharmacy["address"], class_name="text-xs text-gray-600 m-0 mt-1"
                ),
                rx.el.p(
                    f"{pharmacy['distance']} km away",
                    class_name="text-xs font-semibold text-blue-600 m-0 mt-1",
                ),
                class_name="min-w-[150px]",
            )
        ),
        position=latlng(lat=pharmacy["lat"], lng=pharmacy["lng"]),
    )


def map_section() -> rx.Component:
    return rx.el.div(
        rxe.map(
            rxe.map.tile_layer(
                url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            ),
            rx.foreach(PharmacyState.filtered_pharmacies, pharmacy_marker),
            id="pharmacy-map",
            center=PharmacyState.map_center,
            zoom=PharmacyState.map_zoom,
            height="600px",
            width="100%",
            class_name="rounded-2xl shadow-lg border border-gray-200 z-10 relative",
        ),
        class_name="w-full h-full",
    )


def pharmacy_card(pharmacy: Pharmacy) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        pharmacy["name"],
                        class_name="font-bold text-lg text-gray-900 flex items-center gap-2",
                    ),
                    rx.el.div(
                        rx.cond(
                            pharmacy["status"] != "",
                            rx.cond(
                                pharmacy["status"] == "Open Now",
                                rx.el.span(
                                    "Open Now",
                                    class_name="text-[10px] font-bold uppercase tracking-wider text-green-700 bg-green-100 px-2 py-0.5 rounded-full mt-1 inline-block mr-2",
                                ),
                                rx.el.span(
                                    pharmacy["status"],
                                    class_name="text-[10px] font-bold uppercase tracking-wider text-red-700 bg-red-100 px-2 py-0.5 rounded-full mt-1 inline-block mr-2",
                                ),
                            ),
                        ),
                        rx.cond(
                            pharmacy["brand"] != "",
                            rx.el.span(
                                pharmacy["brand"],
                                class_name="text-[10px] font-bold uppercase tracking-wider text-blue-700 bg-blue-100 px-2 py-0.5 rounded-full mt-1 inline-block",
                            ),
                        ),
                        class_name="flex items-center flex-wrap",
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.div(
                    rx.el.span(
                        f"{pharmacy['distance']} km",
                        class_name="text-sm font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded-lg",
                    )
                ),
                class_name="flex justify-between items-start mb-3",
            ),
            rx.el.p(
                pharmacy["address"],
                class_name="text-sm text-gray-500 mb-4 leading-relaxed",
            ),
            rx.el.div(
                rx.cond(
                    pharmacy["opening_hours"] != "",
                    rx.el.div(
                        rx.icon(
                            "clock",
                            class_name="h-4 w-4 text-gray-400 mr-2 flex-shrink-0",
                        ),
                        rx.el.span(
                            pharmacy["opening_hours"],
                            class_name="text-sm text-gray-600 truncate",
                        ),
                        class_name="flex items-center",
                    ),
                ),
                rx.cond(
                    pharmacy["phone"] != "",
                    rx.el.a(
                        rx.icon(
                            "phone",
                            class_name="h-4 w-4 text-gray-400 mr-2 flex-shrink-0",
                        ),
                        rx.el.span(
                            pharmacy["phone"],
                            class_name="text-sm text-gray-600 hover:text-blue-600 truncate",
                        ),
                        href=f"tel:{pharmacy['phone']}",
                        class_name="flex items-center",
                    ),
                ),
                class_name="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-6",
            ),
            rx.el.a(
                "Get Directions",
                href=f"https://www.google.com/maps/dir/?api=1&destination={pharmacy['lat']},{pharmacy['lng']}",
                target="_blank",
                rel="noopener noreferrer",
                class_name="block w-full text-center bg-blue-50 hover:bg-blue-100 text-blue-600 font-semibold py-2.5 rounded-xl transition-colors",
            ),
            class_name="p-6",
        ),
        class_name="bg-white rounded-2xl shadow-sm border border-gray-200 hover:shadow-md transition-all hover:border-blue-200 mb-4",
    )


def search_form() -> rx.Component:
    return rx.el.div(
        rx.el.form(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 h-5 w-5",
                        ),
                        rx.el.input(
                            name="city_query",
                            placeholder="Enter city, town, or area name...",
                            class_name="w-full pl-12 pr-4 py-4 bg-white border-2 border-gray-100 rounded-2xl focus:border-blue-500 focus:ring-0 text-lg transition-all",
                            default_value=PharmacyState.city_query,
                            key=PharmacyState.city_query,
                        ),
                        class_name="relative flex-1",
                    ),
                    rx.el.button(
                        rx.cond(
                            PharmacyState.is_geolocating,
                            rx.icon("loader", class_name="h-5 w-5 animate-spin"),
                            rx.el.span("📍 Use My Location"),
                        ),
                        type="button",
                        on_click=PharmacyState.use_current_location,
                        disabled=PharmacyState.is_geolocating,
                        class_name="bg-white border-2 border-blue-100 hover:bg-blue-50 text-blue-600 px-4 py-4 rounded-2xl font-bold transition-all flex items-center justify-center whitespace-nowrap",
                    ),
                    class_name="flex gap-2 w-full flex-1",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("1 km radius", value="1"),
                        rx.el.option("2 km radius", value="2"),
                        rx.el.option("5 km radius", value="5"),
                        rx.el.option("10 km radius", value="10"),
                        rx.el.option("20 km radius", value="20"),
                        on_change=PharmacyState.set_search_radius,
                        class_name="w-full md:w-48 px-4 py-4 bg-white border-2 border-gray-100 rounded-2xl focus:border-blue-500 focus:ring-0 text-gray-700 font-medium appearance-none",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="absolute right-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 pointer-events-none",
                    ),
                    class_name="relative",
                ),
                rx.el.button(
                    rx.cond(
                        PharmacyState.is_loading,
                        rx.icon("loader", class_name="h-5 w-5 animate-spin"),
                        "Search Pharmacies",
                    ),
                    type="submit",
                    disabled=PharmacyState.is_loading,
                    class_name="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-2xl font-bold shadow-lg shadow-blue-200 transition-all active:scale-95 flex items-center justify-center min-w-[200px] disabled:opacity-70",
                ),
                class_name="flex flex-col md:flex-row gap-4 max-w-4xl mx-auto",
            ),
            on_submit=PharmacyState.search_pharmacies,
        ),
        rx.cond(
            PharmacyState.geolocation_status != "",
            rx.el.div(
                rx.icon("map-pin", class_name="h-4 w-4 mr-1"),
                rx.el.span(PharmacyState.geolocation_status),
                class_name="flex items-center text-sm text-blue-600 font-medium mt-2 max-w-4xl mx-auto animate-in fade-in",
            ),
        ),
        rx.el.div(
            rx.el.span(
                "Popular Cities:",
                class_name="text-sm text-gray-500 font-medium mb-2 md:mb-0 mr-3",
            ),
            rx.el.div(
                rx.foreach(
                    PharmacyState.popular_cities,
                    lambda city: rx.el.button(
                        city,
                        on_click=lambda: PharmacyState.search_popular_city(city),
                        class_name="text-xs font-medium bg-white border border-gray-200 text-gray-600 px-3 py-1.5 rounded-full hover:bg-blue-50 hover:text-blue-600 hover:border-blue-200 transition-colors whitespace-nowrap",
                    ),
                ),
                class_name="flex flex-wrap gap-2",
            ),
            class_name="flex flex-col md:flex-row items-start md:items-center justify-center mt-6 max-w-4xl mx-auto",
        ),
        class_name="py-8 px-4",
    )


def pharmacy_skeleton() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(class_name="w-48 h-5 bg-gray-200 rounded animate-pulse mb-2"),
            rx.el.div(class_name="w-64 h-4 bg-gray-200 rounded animate-pulse mb-4"),
            rx.el.div(class_name="w-32 h-4 bg-gray-200 rounded animate-pulse"),
            class_name="p-6",
        ),
        class_name="bg-white rounded-2xl shadow-sm border border-gray-200 mb-4",
    )


def pharmacy_list() -> rx.Component:
    return rx.el.div(
        rx.cond(
            PharmacyState.retry_message != "",
            rx.el.div(
                rx.icon(
                    "loader", class_name="h-4 w-4 text-amber-600 animate-spin mr-2"
                ),
                rx.el.span(
                    PharmacyState.retry_message,
                    class_name="text-sm font-medium text-amber-800",
                ),
                class_name="flex items-center p-3 bg-amber-50 border border-amber-200 rounded-xl mb-4",
            ),
        ),
        rx.cond(
            PharmacyState.is_using_cached,
            rx.el.div(
                rx.icon("info", class_name="h-5 w-5 text-indigo-600 mr-2"),
                rx.el.span(
                    f"Showing last available results for {PharmacyState.cached_city}. Live search is temporarily unavailable.",
                    class_name="text-sm font-medium text-indigo-800",
                ),
                class_name="flex items-center p-4 bg-indigo-50 border border-indigo-200 rounded-xl mb-4",
            ),
        ),
        rx.el.div(
            rx.cond(
                PharmacyState.searched_city != "",
                rx.el.div(
                    rx.el.h2(
                        f"Found {PharmacyState.total_results} pharmacies near {PharmacyState.searched_city}",
                        class_name="text-lg font-bold text-gray-900",
                    ),
                    rx.el.div(
                        rx.el.span("Sort by:", class_name="text-sm text-gray-500 mr-2"),
                        rx.el.div(
                            rx.el.select(
                                rx.el.option("Distance", value="distance"),
                                rx.el.option("Name", value="name"),
                                value=PharmacyState.sort_by,
                                on_change=PharmacyState.set_sort_by,
                                class_name="text-sm bg-gray-50 border border-gray-200 rounded-lg px-3 py-1.5 focus:ring-blue-500 focus:border-blue-500 outline-none appearance-none pr-8 relative",
                            ),
                            rx.icon(
                                "chevron-down",
                                class_name="absolute right-2 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
                            ),
                            class_name="relative",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex justify-between items-center bg-white p-4 rounded-2xl shadow-sm border border-gray-200 mb-6 sticky top-0 z-20",
                ),
            )
        ),
        rx.cond(
            PharmacyState.is_loading,
            rx.el.div(
                rx.foreach(rx.Var.create([1, 2, 3, 4]), lambda x: pharmacy_skeleton()),
                class_name="pr-4 pb-4",
            ),
            rx.cond(
                PharmacyState.search_error != "",
                rx.el.div(
                    rx.icon(
                        "circle_alert", class_name="h-12 w-12 text-red-400 mx-auto mb-4"
                    ),
                    rx.el.h3(
                        "Search Information",
                        class_name="text-lg font-bold text-gray-900 mb-2",
                    ),
                    rx.el.p(PharmacyState.search_error, class_name="text-gray-500"),
                    class_name="text-center py-20 bg-white rounded-3xl border border-gray-100 shadow-sm",
                ),
                rx.cond(
                    PharmacyState.filtered_pharmacies.length() > 0,
                    rx.scroll_area(
                        rx.el.div(
                            rx.foreach(
                                PharmacyState.filtered_pharmacies, pharmacy_card
                            ),
                            class_name="pr-4 pb-4",
                        ),
                        type="hover",
                        scrollbars="vertical",
                        class_name="h-[600px]",
                    ),
                    rx.el.div(
                        rx.icon(
                            "map", class_name="h-16 w-16 text-blue-200 mx-auto mb-4"
                        ),
                        rx.el.h3(
                            "Explore Local Pharmacies",
                            class_name="text-lg font-bold text-gray-900 mb-2",
                        ),
                        rx.el.p(
                            "Search for a city above to find nearby pharmacies.",
                            class_name="text-gray-500 max-w-xs mx-auto",
                        ),
                        class_name="text-center py-20 bg-white rounded-3xl border border-gray-100 shadow-sm border-dashed border-2",
                    ),
                ),
            ),
        ),
        class_name="w-full lg:w-1/2 flex flex-col",
    )


def community_report_item(report: CommunityReport) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed={report['id']}",
                class_name="h-10 w-10 rounded-full bg-gray-100",
            ),
            rx.el.div(
                rx.el.p(
                    rx.el.span(
                        report["medicine_name"], class_name="font-bold text-gray-900"
                    ),
                    " at ",
                    rx.el.span(
                        report["pharmacy_name"], class_name="font-medium text-gray-700"
                    ),
                    class_name="text-sm",
                ),
                rx.el.div(
                    rx.match(
                        report["status"],
                        (
                            "In Stock",
                            rx.el.span(
                                "In Stock",
                                class_name="text-[10px] font-bold uppercase tracking-wider text-green-700 bg-green-100 px-2 py-0.5 rounded-full mr-2",
                            ),
                        ),
                        (
                            "Low Stock",
                            rx.el.span(
                                "Low Stock",
                                class_name="text-[10px] font-bold uppercase tracking-wider text-yellow-700 bg-yellow-100 px-2 py-0.5 rounded-full mr-2",
                            ),
                        ),
                        (
                            "Out of Stock",
                            rx.el.span(
                                "Out of Stock",
                                class_name="text-[10px] font-bold uppercase tracking-wider text-red-700 bg-red-100 px-2 py-0.5 rounded-full mr-2",
                            ),
                        ),
                        rx.el.span(
                            report["status"],
                            class_name="text-[10px] font-bold uppercase tracking-wider text-gray-700 bg-gray-100 px-2 py-0.5 rounded-full mr-2",
                        ),
                    ),
                    rx.el.span(report["time_ago"], class_name="text-xs text-gray-400"),
                    class_name="mt-1 flex items-center",
                ),
                class_name="ml-3",
            ),
            class_name="flex items-center",
        ),
        class_name="py-4 border-b border-gray-100 last:border-0",
    )


def community_reporting_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Community Reports",
                    class_name="text-2xl font-bold text-gray-900 mb-2",
                ),
                rx.el.p(
                    "Help others by reporting medicine availability and prices in your area.",
                    class_name="text-gray-500 mb-8",
                ),
                class_name="text-center md:text-left",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Report Medicine Availability",
                        class_name="text-lg font-bold text-gray-900 mb-6",
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.el.label(
                                "Medicine Name",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                name="medicine",
                                placeholder="e.g. Crocin 500mg",
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Pharmacy",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.select(
                                rx.el.option(
                                    "Select a pharmacy", value="", disabled=True
                                ),
                                rx.foreach(
                                    PharmacyState.pharmacies,
                                    lambda p: rx.el.option(p["name"], value=p["name"]),
                                ),
                                name="pharmacy",
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 appearance-none",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Availability Status",
                                class_name="block text-sm font-medium text-gray-700 mb-2",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    rx.el.input(
                                        type="radio",
                                        name="status",
                                        value="In Stock",
                                        default_checked=True,
                                        class_name="mr-2 text-blue-600 focus:ring-blue-500 h-4 w-4",
                                    ),
                                    "In Stock",
                                    class_name="flex items-center text-sm text-gray-700 cursor-pointer",
                                ),
                                rx.el.label(
                                    rx.el.input(
                                        type="radio",
                                        name="status",
                                        value="Low Stock",
                                        class_name="mr-2 text-blue-600 focus:ring-blue-500 h-4 w-4",
                                    ),
                                    "Low Stock",
                                    class_name="flex items-center text-sm text-gray-700 cursor-pointer",
                                ),
                                rx.el.label(
                                    rx.el.input(
                                        type="radio",
                                        name="status",
                                        value="Out of Stock",
                                        class_name="mr-2 text-blue-600 focus:ring-blue-500 h-4 w-4",
                                    ),
                                    "Out of Stock",
                                    class_name="flex items-center text-sm text-gray-700 cursor-pointer",
                                ),
                                class_name="flex flex-wrap gap-4",
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Price Seen (₹) - Optional",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="number",
                                name="price",
                                placeholder="0.00",
                                class_name="w-full px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.button(
                            "Submit Report",
                            type="submit",
                            class_name="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl transition-colors shadow-md shadow-blue-200",
                        ),
                        on_submit=PharmacyState.submit_report,
                        reset_on_submit=True,
                    ),
                    class_name="bg-white p-6 md:p-8 rounded-3xl shadow-sm border border-gray-200 lg:col-span-3",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Recent Reports in Mumbai",
                        class_name="text-lg font-bold text-gray-900 mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(PharmacyState.reports, community_report_item),
                        class_name="bg-white p-6 rounded-3xl shadow-sm border border-gray-200 h-full",
                    ),
                    class_name="lg:col-span-2",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-5 gap-8",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16",
        ),
        class_name="bg-gray-50 border-t border-gray-200",
    )


def locator_page() -> rx.Component:
    return rx.el.main(
        navbar(),
        cart_drawer(),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "All-India Locator",
                    class_name="px-3 py-1 bg-green-50 text-green-600 text-[10px] font-bold uppercase tracking-widest rounded-full mb-4 inline-block",
                ),
                rx.el.h1(
                    "Find Pharmacies ",
                    rx.el.span("Near You", class_name="text-green-600"),
                    class_name="text-3xl md:text-5xl font-extrabold text-gray-900 mb-4",
                ),
                rx.el.p(
                    "Search across India for local pharmacies using real-time OpenStreetMap data.",
                    class_name="text-gray-500 max-w-2xl mx-auto text-lg",
                ),
                class_name="text-center py-12 md:py-16 px-4",
            ),
            class_name="bg-gradient-to-b from-green-50/40 to-white",
        ),
        rx.el.div(
            rx.el.p(
                "Powered by OpenStreetMap • Real-time pharmacy data • Covering all of India",
                class_name="text-xs font-bold uppercase tracking-widest text-center text-gray-400 mb-6",
            ),
            search_form(),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    pharmacy_list(),
                    rx.el.div(
                        map_section(),
                        class_name="w-full lg:w-1/2 h-[500px] lg:h-auto mb-8 lg:mb-0",
                    ),
                    class_name="flex flex-col lg:flex-row gap-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
                )
            ),
            class_name="pb-16",
        ),
        community_reporting_section(),
        footer(),
        chat_widget(),
        auth_modal(),
        class_name="bg-white min-h-screen",
    )