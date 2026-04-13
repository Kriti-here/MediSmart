import reflex as rx
from app.components.navbar import navbar
from app.components.footer import footer
from app.components.search_bar import search_section
from app.components.chat_widget import chat_widget
from app.components.expiry_badge import expiry_badge
from app.components.auth_modal import auth_modal
from app.components.cart_drawer import cart_drawer
from app.states.medicine_state import MedicineState, Medicine
from app.states.auth_state import AuthState


def stat_card(value: str, label: str, icon_name: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon_name, class_name="h-6 w-6 text-blue-600"),
            class_name="p-3 bg-blue-50 rounded-xl mb-4",
        ),
        rx.el.h4(value, class_name="text-2xl font-bold text-gray-900"),
        rx.el.p(label, class_name="text-sm text-gray-500 font-medium"),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm flex flex-col items-center text-center",
    )


def feature_card(
    title: str, description: str, icon_name: str, color: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon_name, class_name=f"h-6 w-6 text-{color}-600"),
            class_name=f"p-3 bg-{color}-50 rounded-xl mb-6 w-fit",
        ),
        rx.el.h3(title, class_name="text-xl font-bold text-gray-900 mb-2"),
        rx.el.p(description, class_name="text-gray-500 text-sm leading-relaxed"),
        class_name="bg-white p-8 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow",
    )


def expiring_medicine_item(med: Medicine) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(med["brand_name"], class_name="font-bold text-gray-900"),
            rx.el.p(
                med["salt_composition"],
                class_name="text-xs text-gray-400 truncate w-32",
            ),
            class_name="flex-1",
        ),
        expiry_badge(med["expiry_date"]),
        class_name="bg-white p-4 rounded-xl border border-gray-100 shadow-sm min-w-[280px] flex items-center justify-between",
    )


def index_page() -> rx.Component:
    return rx.el.main(
        navbar(),
        cart_drawer(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Smart Healthcare Savings",
                        class_name="px-4 py-1.5 rounded-full bg-blue-50 text-blue-600 text-sm font-bold mb-6 inline-block uppercase tracking-wider",
                    ),
                    rx.el.h1(
                        "Find High-Quality ",
                        rx.el.span(
                            "Affordable Alternatives", class_name="text-blue-600"
                        ),
                        " for Your Medicines",
                        class_name="text-4xl md:text-6xl font-extrabold text-gray-900 leading-tight mb-8",
                    ),
                    rx.el.p(
                        "Up to 80% savings on your medical bills. Compare brand-name prescriptions with verified generic substitutes containing the exact same ingredients.",
                        class_name="text-xl text-gray-600 max-w-2xl mx-auto mb-12",
                    ),
                    search_section(),
                    class_name="text-center",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24",
            ),
            class_name="bg-gradient-to-b from-blue-50/50 to-white",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    stat_card("15,000+", "Medicines Indexed", "database"),
                    stat_card("₹12Cr+", "Annual Savings", "trending-down"),
                    stat_card("100%", "Verified Substitutes", "message_circle_check"),
                    stat_card("500+", "Partner Pharmacies", "map-pin"),
                    class_name="grid grid-cols-2 lg:grid-cols-4 gap-6",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-12",
            )
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Advanced Healthcare Intelligence",
                        class_name="text-3xl font-bold text-gray-900 mb-4",
                    ),
                    rx.el.p(
                        "Everything you need to manage your medical expenses smarter.",
                        class_name="text-gray-500 max-w-md mx-auto mb-12",
                    ),
                    class_name="text-center",
                ),
                rx.el.div(
                    rx.el.a(
                        feature_card(
                            "Search & Compare AI",
                            "7-step deep analysis of medicines and generic alternatives.",
                            "search",
                            "blue",
                        ),
                        href="/compare",
                        class_name="block",
                    ),
                    feature_card(
                        "Prescription Scan",
                        "Upload a photo of your prescription and let our AI extract medicine names for you.",
                        "camera",
                        "indigo",
                    ),
                    feature_card(
                        "Pharmacy Locator",
                        "Find nearby pharmacies that stock generic alternatives at the lowest prices.",
                        "map-pin",
                        "green",
                    ),
                    feature_card(
                        "Community Reports",
                        "Real-time updates on medicine availability from users in your local area.",
                        "users",
                        "purple",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24",
            )
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "⚠️ Check Your Medicine Cabinet",
                        class_name="text-2xl font-bold text-gray-900 mb-2",
                    ),
                    rx.el.p(
                        "These commonly purchased medicines may be nearing expiry in our database.",
                        class_name="text-gray-500 mb-8",
                    ),
                    class_name="text-center md:text-left",
                ),
                rx.el.div(
                    rx.foreach(
                        MedicineState.expiring_soon_medicines, expiring_medicine_item
                    ),
                    class_name="flex gap-4 overflow-x-auto pb-4 scrollbar-hide",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-24",
            )
        ),
        footer(),
        chat_widget(),
        auth_modal(),
        on_mount=AuthState.init_auth,
        class_name="bg-white min-h-screen",
    )