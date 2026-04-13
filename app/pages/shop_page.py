import reflex as rx
from app.states.checkout_state import CheckoutState
from app.states.medicine_state import MedicineState
from app.components.navbar import navbar
from app.components.footer import footer
from app.components.chat_widget import chat_widget
from app.components.auth_modal import auth_modal
from app.components.cart_drawer import cart_drawer


def category_pill(cat: str) -> rx.Component:
    is_selected = CheckoutState.shop_category_filter == cat
    return rx.el.button(
        cat,
        on_click=lambda: CheckoutState.set_shop_category(cat),
        class_name=rx.cond(
            is_selected,
            "px-4 py-2 bg-blue-600 text-white text-sm font-bold rounded-full whitespace-nowrap shadow-sm transition-all",
            "px-4 py-2 bg-gray-100 text-gray-600 hover:bg-blue-50 hover:text-blue-600 text-sm font-medium rounded-full whitespace-nowrap transition-all",
        ),
    )


def product_card(med: dict) -> rx.Component:
    savings_amt = med["brand_price"].to(float) - med["generic_price"].to(float)
    savings_pct = rx.cond(
        med["brand_price"].to(float) > 0,
        (savings_amt / med["brand_price"].to(float) * 100).to(int),
        0,
    )
    cat_color = rx.match(
        med["category"].to(str),
        ("Analgesic", "blue"),
        ("Antibiotic", "red"),
        ("Antacid", "purple"),
        ("Anti-Diabetic", "amber"),
        ("Vitamin", "green"),
        "gray",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                med["category"],
                class_name=f"px-2 py-1 bg-{cat_color}-100 text-{cat_color}-700 text-[10px] font-bold uppercase tracking-wider rounded-full",
            ),
            rx.el.span(
                f"Save {savings_pct}%",
                class_name="px-2 py-1 bg-green-50 text-green-700 text-[10px] font-bold uppercase tracking-wider rounded-md border border-green-200",
            ),
            class_name="flex justify-between items-start mb-4",
        ),
        rx.el.div(
            rx.el.h3(
                med["brand_name"],
                class_name="text-xl font-extrabold text-gray-900 mb-1",
            ),
            rx.el.p(
                med["generic_name"], class_name="text-xs text-gray-500 font-medium mb-3"
            ),
            rx.el.p(
                rx.el.span("Salt: ", class_name="font-semibold text-gray-700"),
                med["salt_composition"],
                class_name="text-xs text-gray-600 truncate mb-1",
            ),
            rx.el.p(
                rx.el.span("By: ", class_name="font-semibold text-gray-700"),
                med["manufacturer"],
                class_name="text-xs text-gray-600",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    f"₹{med['brand_price']}",
                    class_name="text-sm text-gray-400 line-through font-medium",
                ),
                rx.icon("arrow-right", class_name="h-4 w-4 text-gray-300 mx-2"),
                rx.el.p(
                    f"₹{med['generic_price']}",
                    class_name="text-3xl font-black text-green-600",
                ),
                class_name="flex items-center mb-1",
            ),
            rx.el.p(
                f"Save ₹{savings_amt} per strip",
                class_name="text-xs font-bold text-green-600 bg-green-50 px-2 py-1 rounded w-fit",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.button(
                "Compare",
                on_click=lambda: MedicineState.select_medicine(med["id"]),
                class_name="flex-1 bg-white border-2 border-blue-100 hover:border-blue-300 hover:bg-blue-50 text-blue-600 text-sm font-bold py-2.5 rounded-xl transition-all text-center",
            ),
            rx.el.button(
                rx.icon("shopping-cart", class_name="h-4 w-4 mr-2"),
                "Add to Cart",
                on_click=lambda: CheckoutState.add_to_cart(
                    med["generic_name"].to(str), med["generic_price"].to(float), 1
                ),
                class_name="flex-1 flex items-center justify-center bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold py-2.5 rounded-xl shadow-lg shadow-blue-200 transition-all",
            ),
            class_name="flex gap-3",
        ),
        class_name="bg-white border border-gray-100 p-6 rounded-3xl shadow-sm hover:shadow-xl transition-all duration-300 flex flex-col justify-between h-full",
    )


def shop_page() -> rx.Component:
    return rx.el.main(
        navbar(),
        cart_drawer(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "MediSmart Online Pharmacy",
                    class_name="text-4xl md:text-5xl font-extrabold text-white mb-4 drop-shadow-md",
                ),
                rx.el.p(
                    "Browse verified generic medicines at up to 80% savings",
                    class_name="text-xl text-blue-100 font-medium max-w-2xl mx-auto mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon("package", class_name="h-5 w-5 text-blue-200 mr-2"),
                        rx.el.span(
                            "15 medicines", class_name="text-sm font-bold text-white"
                        ),
                        class_name="flex items-center bg-white/10 backdrop-blur-md px-4 py-2 rounded-full",
                    ),
                    rx.el.div(
                        rx.icon(
                            "shield-check", class_name="h-5 w-5 text-blue-200 mr-2"
                        ),
                        rx.el.span(
                            "Verified generics",
                            class_name="text-sm font-bold text-white",
                        ),
                        class_name="flex items-center bg-white/10 backdrop-blur-md px-4 py-2 rounded-full",
                    ),
                    rx.el.div(
                        rx.icon(
                            "trending-down", class_name="h-5 w-5 text-blue-200 mr-2"
                        ),
                        rx.el.span(
                            "Save up to 80%", class_name="text-sm font-bold text-white"
                        ),
                        class_name="flex items-center bg-white/10 backdrop-blur-md px-4 py-2 rounded-full",
                    ),
                    class_name="flex flex-wrap justify-center gap-4",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10",
            ),
            class_name="bg-gradient-to-r from-blue-700 to-indigo-800 pt-20 pb-24 relative overflow-hidden",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Search medicines...",
                        on_change=CheckoutState.set_shop_search.debounce(300),
                        default_value=CheckoutState.shop_search_query,
                        class_name="w-full md:w-64 lg:w-80 pl-11 pr-4 py-3 border border-gray-200 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all",
                    ),
                    class_name="relative w-full md:w-auto shrink-0",
                ),
                rx.el.div(
                    rx.foreach(CheckoutState.available_categories, category_pill),
                    class_name="flex gap-2 overflow-x-auto pb-2 md:pb-0 scrollbar-hide flex-1 items-center px-2",
                ),
                rx.el.div(
                    rx.icon(
                        "filter",
                        class_name="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
                    ),
                    rx.el.select(
                        rx.el.option("Best Savings", value="savings"),
                        rx.el.option("Price: Low to High", value="price_low"),
                        rx.el.option("Price: High to Low", value="price_high"),
                        rx.el.option("Name A-Z", value="name"),
                        on_change=CheckoutState.set_shop_sort,
                        value=CheckoutState.shop_sort_by,
                        class_name="w-full md:w-48 pl-10 pr-10 py-3 border border-gray-200 rounded-xl focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none appearance-none bg-white text-sm font-semibold text-gray-700",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="absolute right-4 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
                    ),
                    class_name="relative w-full md:w-auto shrink-0",
                ),
                class_name="flex flex-col md:flex-row gap-4 items-center justify-between p-4 bg-white rounded-2xl shadow-lg border border-gray-100 max-w-7xl mx-auto -mt-10 relative z-20",
            ),
            class_name="px-4 sm:px-6 lg:px-8 mb-12",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    rx.el.span("Showing "),
                    rx.el.span(
                        CheckoutState.filtered_shop_medicines.length(),
                        class_name="font-bold text-gray-900",
                    ),
                    rx.el.span(" medicines"),
                    class_name="text-sm text-gray-500 mb-6",
                ),
                rx.cond(
                    CheckoutState.filtered_shop_medicines.length() > 0,
                    rx.el.div(
                        rx.foreach(CheckoutState.filtered_shop_medicines, product_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
                    ),
                    rx.el.div(
                        rx.icon(
                            "search-x",
                            class_name="h-16 w-16 text-gray-300 mx-auto mb-4",
                        ),
                        rx.el.h3(
                            "No medicines found",
                            class_name="text-xl font-bold text-gray-900 mb-2",
                        ),
                        rx.el.p(
                            "Try adjusting your filters or search query.",
                            class_name="text-gray-500 mb-6",
                        ),
                        rx.el.button(
                            "Clear Filters",
                            on_click=[
                                CheckoutState.set_shop_search(""),
                                CheckoutState.set_shop_category("All"),
                            ],
                            class_name="bg-white border-2 border-gray-200 text-gray-700 hover:bg-gray-50 px-6 py-2 rounded-xl font-bold transition-colors",
                        ),
                        class_name="text-center py-20 bg-white rounded-3xl border border-dashed border-gray-200",
                    ),
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-24",
            )
        ),
        footer(),
        chat_widget(),
        auth_modal(),
        class_name="bg-gray-50 min-h-screen",
    )