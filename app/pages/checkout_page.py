import reflex as rx
import reflex_enterprise as rxe
from reflex_enterprise.components.map.types import latlng
from app.states.checkout_state import CheckoutState, CITY_PHARMACIES
from app.components.navbar import navbar
from app.components.footer import footer
from app.components.chat_widget import chat_widget
from app.components.auth_modal import auth_modal
from app.components.cart_drawer import cart_drawer


def cart_item_row(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h4(item["name"], class_name="text-sm font-semibold text-gray-900"),
            rx.el.div(
                rx.el.button(
                    rx.icon("minus", class_name="h-3 w-3"),
                    on_click=lambda: CheckoutState.update_qty(
                        item["name"], item["qty"].to(int) - 1
                    ),
                    class_name="bg-gray-100 hover:bg-gray-200 text-gray-600 rounded p-1",
                ),
                rx.el.span(
                    item["qty"].to(str), class_name="text-xs font-bold w-4 text-center"
                ),
                rx.el.button(
                    rx.icon("plus", class_name="h-3 w-3"),
                    on_click=lambda: CheckoutState.update_qty(
                        item["name"], item["qty"].to(int) + 1
                    ),
                    class_name="bg-gray-100 hover:bg-gray-200 text-gray-600 rounded p-1",
                ),
                rx.el.span(
                    f"× ₹{item['price']}", class_name="text-xs text-gray-500 ml-2"
                ),
                class_name="flex items-center gap-2 mt-1",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.p(
                f"₹{item['price'].to(float) * item['qty'].to(float)}",
                class_name="text-sm font-bold text-gray-900 mr-3",
            ),
            rx.el.button(
                rx.icon("x", class_name="h-4 w-4 text-gray-400 hover:text-red-500"),
                on_click=lambda: CheckoutState.remove_from_cart(item["name"]),
                class_name="p-1",
            ),
            class_name="flex items-center",
        ),
        class_name="flex justify-between items-center py-3 border-b border-gray-50 last:border-0",
    )


def order_summary() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("shopping-cart", class_name="h-5 w-5 text-blue-600 mr-2"),
                rx.el.h3("Order Summary", class_name="text-lg font-bold text-gray-900"),
                class_name="flex items-center",
            ),
            rx.el.span(
                f"{CheckoutState.cart_item_count} items",
                class_name="text-xs font-bold bg-blue-50 text-blue-600 px-2 py-1 rounded-full",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.cond(
            CheckoutState.cart_items.length() > 0,
            rx.el.div(
                rx.foreach(CheckoutState.cart_items, cart_item_row), class_name="mb-4"
            ),
            rx.el.div(
                rx.el.p(
                    "Your cart is empty",
                    class_name="text-sm text-gray-500 text-center py-4",
                ),
                rx.el.a(
                    "Back to Search",
                    href="/",
                    class_name="text-xs text-blue-600 hover:underline block text-center mb-4",
                ),
            ),
        ),
        rx.el.div(
            rx.el.p("Total", class_name="font-bold text-gray-900"),
            rx.el.p(
                f"₹{CheckoutState.cart_total}",
                class_name="text-xl font-extrabold text-blue-600",
            ),
            class_name="flex justify-between items-center pt-4 border-t border-gray-100",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-6",
    )


def address_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("map-pin", class_name="h-5 w-5 text-blue-600 mr-2"),
                rx.el.h3(
                    "Delivery Address", class_name="text-lg font-bold text-gray-900"
                ),
                class_name="flex items-center",
            ),
            rx.el.button(
                rx.cond(
                    CheckoutState.is_gps_loading,
                    rx.icon("loader", class_name="h-4 w-4 animate-spin"),
                    rx.el.div(
                        rx.icon("crosshair", class_name="h-4 w-4 mr-1"),
                        "Use GPS",
                        class_name="flex items-center",
                    ),
                ),
                on_click=CheckoutState.use_gps_location,
                disabled=CheckoutState.is_gps_loading,
                class_name="text-sm font-semibold text-blue-600 border border-blue-200 px-3 py-1.5 rounded-lg hover:bg-blue-50 transition-colors disabled:opacity-70",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.cond(
            CheckoutState.address_error != "",
            rx.el.div(
                rx.icon("triangle-alert", class_name="h-4 w-4 text-red-500 mr-2"),
                rx.el.span(
                    CheckoutState.address_error,
                    class_name="text-sm text-red-700 font-medium",
                ),
                class_name="flex items-center bg-red-50 p-3 rounded-xl mb-4",
            ),
        ),
        rx.cond(
            CheckoutState.geocode_status != "",
            rx.el.div(
                rx.icon("loader", class_name="h-4 w-4 text-blue-500 animate-spin mr-2"),
                rx.el.span(
                    CheckoutState.geocode_status,
                    class_name="text-sm text-blue-700 font-medium",
                ),
                class_name="flex items-center bg-blue-50 p-3 rounded-xl mb-4",
            ),
            rx.fragment(),
        ),
        rx.el.form(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "building",
                            class_name="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 pointer-events-none",
                        ),
                        rx.el.select(
                            rx.foreach(
                                list(CITY_PHARMACIES.keys()),
                                lambda city: rx.el.option(city, value=city),
                            ),
                            value=CheckoutState.selected_city,
                            on_change=CheckoutState.set_city,
                            class_name="w-full pl-12 pr-10 py-3 border-2 border-gray-100 rounded-xl focus:border-blue-500 focus:ring-0 bg-gray-50 focus:bg-white outline-none transition-colors appearance-none font-semibold text-gray-800",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="absolute right-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400 pointer-events-none",
                        ),
                        class_name="relative mb-2",
                    ),
                    rx.el.p(
                        f"{CheckoutState.shop_name} — {CheckoutState.shop_address}",
                        class_name="text-xs text-gray-500 ml-1 mb-6",
                    ),
                ),
                rx.el.div(
                    rx.icon(
                        "home",
                        class_name="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="House No / Flat / Building",
                        name="house_no",
                        default_value=CheckoutState.house_no,
                        key=CheckoutState.house_no,
                        class_name="w-full pl-12 pr-4 py-3 border-2 border-gray-100 rounded-xl focus:border-blue-500 focus:ring-0 bg-gray-50 focus:bg-white outline-none transition-colors",
                    ),
                    class_name="relative mb-4",
                ),
                rx.el.div(
                    rx.icon(
                        "map",
                        class_name="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Area / Street (Required)",
                        name="area",
                        default_value=CheckoutState.area,
                        key=CheckoutState.area,
                        class_name="w-full pl-12 pr-4 py-3 border-2 border-gray-100 rounded-xl focus:border-blue-500 focus:ring-0 bg-gray-50 focus:bg-white outline-none transition-colors",
                    ),
                    class_name="relative mb-4",
                ),
                rx.el.div(
                    rx.icon(
                        "landmark",
                        class_name="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Landmark (Optional)",
                        name="landmark",
                        default_value=CheckoutState.landmark,
                        key=CheckoutState.landmark,
                        class_name="w-full pl-12 pr-4 py-3 border-2 border-gray-100 rounded-xl focus:border-blue-500 focus:ring-0 bg-gray-50 focus:bg-white outline-none transition-colors",
                    ),
                    class_name="relative mb-4",
                ),
                rx.el.div(
                    rx.icon(
                        "hash",
                        class_name="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Pincode (Required)",
                        name="pincode",
                        max_length=6,
                        default_value=CheckoutState.pincode,
                        key=CheckoutState.pincode,
                        class_name="w-full pl-12 pr-4 py-3 border-2 border-gray-100 rounded-xl focus:border-blue-500 focus:ring-0 bg-gray-50 focus:bg-white outline-none transition-colors",
                    ),
                    class_name="relative mb-6",
                ),
                rx.el.button(
                    rx.cond(
                        CheckoutState.is_geocoding,
                        rx.icon("loader", class_name="h-5 w-5 animate-spin mx-auto"),
                        rx.el.div(
                            rx.icon("map-pin", class_name="h-5 w-5 mr-2"),
                            "Locate & Set Address",
                            class_name="flex items-center justify-center",
                        ),
                    ),
                    type="submit",
                    disabled=CheckoutState.is_geocoding,
                    class_name="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl transition-colors shadow-lg shadow-blue-200 disabled:opacity-70",
                ),
                class_name="flex flex-col",
            ),
            on_submit=CheckoutState.geocode_address,
            reset_on_submit=True,
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
    )


def resolved_address_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "message_circle_check", class_name="h-6 w-6 text-green-500 mr-2"
                ),
                rx.el.h3(
                    "Delivery Location Set",
                    class_name="text-lg font-bold text-gray-900",
                ),
                class_name="flex items-center",
            ),
            rx.el.button(
                "Change Address",
                on_click=CheckoutState.clear_user_location,
                class_name="text-xs text-blue-600 font-semibold hover:underline",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.el.div(
            rx.el.p(
                CheckoutState.user_address_resolved,
                class_name="text-sm text-gray-700 font-medium mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("route", class_name="h-4 w-4 text-blue-500 mr-1"),
                    rx.el.span(
                        f"{CheckoutState.delivery_distance_km} km",
                        class_name="text-xs font-bold text-blue-700",
                    ),
                    class_name="flex items-center bg-blue-50 px-3 py-1.5 rounded-lg",
                ),
                rx.el.div(
                    rx.icon("clock", class_name="h-4 w-4 text-amber-500 mr-1"),
                    rx.el.span(
                        f"{CheckoutState.estimated_delivery_time}",
                        class_name="text-xs font-bold text-amber-700",
                    ),
                    class_name="flex items-center bg-amber-50 px-3 py-1.5 rounded-lg",
                ),
                class_name="flex gap-3",
            ),
            class_name="bg-gray-50 p-4 rounded-xl border border-gray-200",
        ),
        rx.el.button(
            rx.cond(
                CheckoutState.order_loading,
                rx.icon("loader", class_name="h-5 w-5 animate-spin mx-auto"),
                f"Place Order — ₹{CheckoutState.cart_total}",
            ),
            on_click=CheckoutState.submit_order,
            disabled=CheckoutState.order_loading
            | (CheckoutState.cart_items.length() == 0),
            class_name="w-full mt-6 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-bold py-4 px-4 rounded-xl transition-all shadow-lg shadow-green-200 disabled:opacity-70",
        ),
        class_name="bg-white p-6 rounded-2xl shadow-sm border border-green-200",
    )


def order_confirmation() -> rx.Component:
    return rx.el.div(
        rx.icon("circle_check", class_name="h-16 w-16 text-green-500 mx-auto mb-4"),
        rx.el.h2(
            "Order Confirmed!",
            class_name="text-2xl font-extrabold text-gray-900 text-center mb-2",
        ),
        rx.el.p(
            "Your medicines are on the way. Our delivery partner has been assigned.",
            class_name="text-gray-500 text-center text-sm mb-8",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Delivery To",
                    class_name="text-xs font-bold text-gray-400 uppercase tracking-widest mb-1",
                ),
                rx.el.p(
                    CheckoutState.user_address_resolved,
                    class_name="text-sm text-gray-800 font-medium",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "ETA",
                        class_name="text-xs font-bold text-gray-400 uppercase tracking-widest mb-1",
                    ),
                    rx.el.p(
                        CheckoutState.estimated_delivery_time,
                        class_name="font-bold text-gray-900",
                    ),
                    class_name="flex-1",
                ),
                rx.el.div(
                    rx.el.p(
                        "Total Paid",
                        class_name="text-xs font-bold text-gray-400 uppercase tracking-widest mb-1",
                    ),
                    rx.el.p(
                        f"₹{CheckoutState.cart_total}",
                        class_name="font-bold text-green-600",
                    ),
                    class_name="flex-1 text-right",
                ),
                class_name="flex justify-between",
            ),
            class_name="bg-gray-50 p-5 rounded-xl border border-gray-100 mb-8",
        ),
        rx.el.button(
            "Place Another Order",
            on_click=CheckoutState.reset_checkout,
            class_name="w-full bg-white border-2 border-gray-200 text-gray-700 hover:bg-gray-50 font-bold py-3 px-4 rounded-xl transition-colors",
        ),
        class_name="bg-white p-8 rounded-2xl shadow-xl border border-gray-100 max-w-md mx-auto",
    )


def map_section() -> rx.Component:
    return rx.el.div(
        rxe.map(
            rxe.map.tile_layer(
                url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
            ),
            rxe.map.marker(
                rxe.map.popup(
                    rx.el.div(
                        rx.el.p(
                            CheckoutState.shop_name,
                            class_name="font-bold text-sm text-gray-900 m-0",
                        ),
                        rx.el.p(
                            "Pharmacy Location",
                            class_name="text-xs text-red-600 font-medium m-0",
                        ),
                    )
                ),
                position=latlng(lat=CheckoutState.shop_lat, lng=CheckoutState.shop_lng),
            ),
            rx.cond(
                CheckoutState.has_user_location,
                rxe.map.marker(
                    rxe.map.popup(
                        rx.el.div(
                            rx.el.p(
                                "Your Delivery Address",
                                class_name="font-bold text-sm text-blue-600 m-0",
                            ),
                            rx.el.p(
                                CheckoutState.user_address_resolved,
                                class_name="text-xs text-gray-700 font-medium mt-1 mb-0",
                            ),
                        )
                    ),
                    position=latlng(
                        lat=CheckoutState.user_lat, lng=CheckoutState.user_lng
                    ),
                ),
            ),
            rx.cond(
                CheckoutState.has_user_location,
                rxe.map.polyline(
                    positions=CheckoutState.route_positions,
                    path_options=rxe.map.path_options(
                        color="#3b82f6", weight=4, dash_array="8, 8"
                    ),
                ),
            ),
            id="checkout-map",
            center=CheckoutState.map_center,
            zoom=CheckoutState.map_zoom,
            height="600px",
            width="100%",
            class_name="rounded-2xl shadow-lg border border-gray-200 z-10 relative",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    class_name="w-3 h-3 rounded-full bg-red-500 mr-2 border border-white shadow-sm"
                ),
                rx.el.span(
                    "Pharmacy", class_name="text-xs font-semibold text-gray-700"
                ),
                class_name="flex items-center mb-2",
            ),
            rx.el.div(
                rx.el.div(
                    class_name="w-3 h-3 rounded-full bg-blue-500 mr-2 border border-white shadow-sm"
                ),
                rx.el.span(
                    "Your Address", class_name="text-xs font-semibold text-gray-700"
                ),
                class_name="flex items-center",
            ),
            class_name="absolute bottom-6 left-6 bg-white/90 backdrop-blur-sm p-3 rounded-xl shadow-md border border-gray-100 z-20",
        ),
        class_name="w-full h-full relative",
    )


def checkout_page() -> rx.Component:
    return rx.el.main(
        navbar(),
        cart_drawer(),
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.icon("arrow-left", class_name="h-4 w-4 mr-2"),
                    "Back to Home",
                    href="/",
                    class_name="flex items-center text-sm font-semibold text-gray-500 hover:text-blue-600 transition-colors mb-4 w-fit",
                ),
                rx.el.h1(
                    "Checkout & Delivery",
                    class_name="text-3xl md:text-4xl font-extrabold text-gray-900 mb-8",
                ),
                rx.cond(
                    CheckoutState.order_submitted,
                    order_confirmation(),
                    rx.el.div(
                        rx.el.div(
                            order_summary(),
                            rx.cond(
                                CheckoutState.has_user_location,
                                resolved_address_view(),
                                address_form(),
                            ),
                            class_name="w-full lg:w-5/12 flex flex-col",
                        ),
                        rx.el.div(
                            map_section(), class_name="w-full lg:w-7/12 mt-8 lg:mt-0"
                        ),
                        class_name="flex flex-col lg:flex-row gap-8",
                    ),
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12",
            ),
            class_name="bg-gray-50 min-h-screen",
        ),
        footer(),
        chat_widget(),
        auth_modal(),
        class_name="bg-gray-50 min-h-screen",
    )