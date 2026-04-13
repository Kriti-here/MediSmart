import reflex as rx
from app.states.medicine_state import MedicineState
from app.states.checkout_state import CheckoutState
from app.components.navbar import navbar
from app.components.footer import footer
from app.components.chat_widget import chat_widget
from app.components.auth_modal import auth_modal
from app.components.cart_drawer import cart_drawer
from app.components.expiry_badge import expiry_badge, expiry_countdown_card


def medicine_header() -> rx.Component:
    med = MedicineState.selected_medicine
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.icon("arrow-left", class_name="h-4 w-4 mr-2"),
                "Back to Search",
                on_click=rx.redirect("/"),
                class_name="flex items-center text-blue-600 font-semibold mb-8 hover:translate-x-[-4px] transition-transform",
            ),
            rx.cond(
                MedicineState.selected_medicine,
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                med["category"],
                                class_name="text-xs font-bold text-blue-600 uppercase tracking-widest bg-blue-50 px-3 py-1 rounded-full mb-4 inline-block",
                            ),
                            rx.el.h1(
                                med["brand_name"],
                                class_name="text-3xl md:text-5xl font-extrabold text-gray-900 mb-2",
                            ),
                            rx.el.p(
                                f"By {med['manufacturer']}",
                                class_name="text-gray-500 font-medium",
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.div(
                            expiry_countdown_card(med["expiry_date"]),
                            rx.el.div(
                                rx.el.p(
                                    "Current Brand Price",
                                    class_name="text-sm text-gray-400 font-medium mb-1",
                                ),
                                rx.el.p(
                                    f"₹{med['brand_price']}",
                                    class_name="text-3xl font-bold text-gray-900",
                                ),
                                class_name="bg-gray-50 p-6 rounded-2xl border border-gray-100 text-right min-w-[200px]",
                            ),
                            class_name="flex flex-col md:flex-row gap-4 mt-6 md:mt-0",
                        ),
                        class_name="flex flex-col md:flex-row md:items-center justify-between",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "flask-conical", class_name="h-5 w-5 text-gray-400 mr-3"
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Salt Composition",
                                    class_name="text-xs text-gray-400 font-bold uppercase",
                                ),
                                rx.el.p(
                                    med["salt_composition"],
                                    class_name="text-lg text-gray-700 font-semibold",
                                ),
                            ),
                            class_name="flex items-start bg-white p-6 rounded-2xl border border-gray-100 shadow-sm mt-8",
                        )
                    ),
                ),
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
        ),
        class_name="bg-white border-b py-12",
    )


def alternative_row(med: dict) -> rx.Component:
    savings_amt = med["brand_price"].to(float) - med["generic_price"].to(float)
    savings_pct = rx.cond(
        med["brand_price"].to(float) > 0,
        (savings_amt / med["brand_price"].to(float) * 100).to(int),
        0,
    )
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    med["brand_name"].to(str), class_name="font-bold text-gray-900"
                ),
                rx.el.p(
                    med["generic_name"].to(str), class_name="text-xs text-gray-500"
                ),
                class_name="py-4",
            )
        ),
        rx.el.td(med["manufacturer"].to(str), class_name="text-gray-600"),
        rx.el.td(f"₹{med['generic_price']}", class_name="font-bold text-gray-900"),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    f"Save ₹{savings_amt}", class_name="block font-bold text-green-600"
                ),
                rx.el.span(
                    f"{savings_pct}% cheaper",
                    class_name="block text-xs text-green-500 font-medium",
                ),
                class_name="bg-green-50 px-3 py-2 rounded-lg",
            )
        ),
        rx.el.td(expiry_badge(med["expiry_date"])),
        rx.el.td(
            rx.el.div(
                rx.icon("shield-check", class_name="h-4 w-4 text-blue-500 mr-2"),
                rx.el.span(
                    "Verified", class_name="text-sm font-semibold text-blue-600"
                ),
                class_name="flex items-center",
            )
        ),
        rx.el.td(
            rx.el.button(
                rx.icon("shopping-cart", class_name="h-4 w-4 mr-2"),
                "Add to Cart",
                on_click=lambda: CheckoutState.add_to_cart(
                    med["generic_name"].to(str), med["generic_price"].to(float), 1
                ),
                class_name="flex items-center bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-bold text-sm transition-colors",
            )
        ),
        class_name="border-b last:border-0 hover:bg-gray-50/50 transition-colors",
    )


def results_page() -> rx.Component:
    return rx.el.main(
        navbar(),
        cart_drawer(),
        medicine_header(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Recommended Generic Alternatives",
                        class_name="text-2xl font-bold text-gray-900 mb-2",
                    ),
                    rx.el.p(
                        "These medicines have the exact same chemical composition and efficacy.",
                        class_name="text-gray-500 mb-8",
                    ),
                    rx.cond(
                        MedicineState.filtered_alternatives.length() > 0,
                        rx.el.div(
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th(
                                                "Generic Brand",
                                                class_name="text-left py-4 px-4 text-xs font-bold text-gray-400 uppercase tracking-widest",
                                            ),
                                            rx.el.th(
                                                "Manufacturer",
                                                class_name="text-left py-4 px-4 text-xs font-bold text-gray-400 uppercase tracking-widest",
                                            ),
                                            rx.el.th(
                                                "Price",
                                                class_name="text-left py-4 px-4 text-xs font-bold text-gray-400 uppercase tracking-widest",
                                            ),
                                            rx.el.th(
                                                "Potential Savings",
                                                class_name="text-left py-4 px-4 text-xs font-bold text-gray-400 uppercase tracking-widest",
                                            ),
                                            rx.el.th(
                                                "Expiry",
                                                class_name="text-left py-4 px-4 text-xs font-bold text-gray-400 uppercase tracking-widest",
                                            ),
                                            rx.el.th(
                                                "Status",
                                                class_name="text-left py-4 px-4 text-xs font-bold text-gray-400 uppercase tracking-widest",
                                            ),
                                            rx.el.th("", class_name="py-4 px-4"),
                                            class_name="border-b",
                                        )
                                    ),
                                    rx.el.tbody(
                                        rx.foreach(
                                            MedicineState.filtered_alternatives,
                                            alternative_row,
                                        )
                                    ),
                                    class_name="w-full table-auto",
                                ),
                                class_name="overflow-x-auto",
                            ),
                            class_name="bg-white rounded-3xl border border-gray-100 shadow-xl p-4 md:p-8",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "search-x",
                                    class_name="h-16 w-16 text-gray-200 mb-6 mx-auto",
                                ),
                                rx.el.h3(
                                    "No exact generic alternatives found",
                                    class_name="text-xl font-bold text-gray-900 mb-2",
                                ),
                                rx.el.p(
                                    "We couldn't find a cheaper generic for this specific brand in our database yet. Try searching by the salt name directly.",
                                    class_name="text-gray-500 max-w-sm mx-auto mb-8",
                                ),
                                rx.el.button(
                                    "Try New Search",
                                    on_click=rx.redirect("/"),
                                    class_name="bg-blue-600 text-white px-8 py-3 rounded-xl font-bold shadow-lg shadow-blue-200",
                                ),
                                class_name="text-center py-20",
                            ),
                            class_name="bg-gray-50 rounded-3xl border-2 border-dashed border-gray-200",
                        ),
                    ),
                    class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12",
                )
            ),
            class_name="bg-white min-h-screen",
        ),
        footer(),
        chat_widget(),
        auth_modal(),
        class_name="bg-gray-50 min-h-screen",
    )