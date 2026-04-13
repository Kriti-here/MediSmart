import reflex as rx
from app.states.medicine_state import MedicineState
from app.states.auth_state import AuthState
from app.states.checkout_state import CheckoutState


def nav_link(label: str, href: str) -> rx.Component:
    return rx.el.a(
        label,
        href=href,
        class_name="text-gray-600 hover:text-blue-600 font-medium transition-colors",
    )


def profile_dropdown() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AuthState.show_profile_dropdown,
            rx.el.div(
                on_click=AuthState.close_profile_dropdown,
                class_name="fixed inset-0 z-40",
            ),
        ),
        rx.cond(
            AuthState.show_profile_dropdown,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            AuthState.user_initial,
                            class_name="h-12 w-12 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center text-lg",
                        ),
                        rx.el.div(
                            rx.el.p(
                                AuthState.current_user["name"],
                                class_name="font-bold text-gray-900 truncate",
                            ),
                            rx.el.p(
                                AuthState.current_user["email"],
                                class_name="text-xs text-gray-500 truncate",
                            ),
                            class_name="flex-1 min-w-0",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    rx.el.div(class_name="border-t border-gray-100 my-3"),
                    rx.el.button(
                        rx.icon("log-out", class_name="h-4 w-4"),
                        "Sign Out",
                        on_click=AuthState.handle_logout,
                        class_name="w-full flex items-center gap-2 text-red-600 hover:bg-red-50 rounded-xl px-3 py-2 font-medium transition-colors",
                    ),
                    class_name="bg-white rounded-2xl shadow-2xl border border-gray-100 w-64 p-4 animate-in fade-in slide-in-from-top-2",
                ),
                class_name="absolute right-0 top-full mt-2 z-50",
            ),
        ),
        class_name="relative",
    )


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("shield-plus", class_name="h-8 w-8 text-blue-600"),
                        rx.el.span(
                            "MediSmart",
                            class_name="text-2xl font-bold text-gray-900 tracking-tight",
                        ),
                        class_name="flex items-center gap-2 cursor-pointer",
                        on_click=MedicineState.go_home,
                    ),
                    class_name="flex-shrink-0",
                ),
                rx.el.div(
                    nav_link("Home", "/"),
                    nav_link("Dashboard", "/dashboard"),
                    nav_link("MediCompare", "/compare"),
                    nav_link("Upload Prescription", "/upload"),
                    nav_link("Pharmacy Locator", "/locator"),
                    nav_link("Community", "#"),
                    nav_link("Shop", "/shop"),
                    rx.el.button(
                        rx.el.div(
                            rx.icon("shopping-cart", class_name="h-5 w-5"),
                            rx.cond(
                                CheckoutState.cart_item_count > 0,
                                rx.el.span(
                                    CheckoutState.cart_item_count,
                                    class_name="absolute -top-2 -right-2 bg-red-500 text-white text-[10px] font-bold h-4 w-4 rounded-full flex items-center justify-center",
                                ),
                            ),
                            class_name="relative flex items-center",
                        ),
                        on_click=CheckoutState.toggle_cart_drawer,
                        class_name="text-gray-600 hover:text-blue-600 transition-colors",
                    ),
                    rx.el.a(
                        "MedOS ",
                        rx.el.span(
                            "PRO",
                            class_name="text-[8px] bg-green-100 text-green-700 px-1 py-0.5 rounded font-bold ml-1 align-top",
                        ),
                        href="/medos",
                        class_name="text-green-600 hover:text-green-700 font-bold transition-colors",
                    ),
                    class_name="hidden lg:flex items-center space-x-8",
                ),
                rx.el.div(
                    rx.cond(
                        AuthState.is_logged_in,
                        rx.el.div(
                            rx.el.button(
                                AuthState.user_initial,
                                on_click=AuthState.toggle_profile_dropdown,
                                class_name="h-10 w-10 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center cursor-pointer shadow-sm hover:bg-blue-700 transition-colors",
                            ),
                            profile_dropdown(),
                            class_name="flex items-center",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Login",
                                on_click=AuthState.open_login_modal,
                                class_name="border border-blue-200 text-blue-600 hover:bg-blue-50 px-5 py-2 rounded-xl font-semibold transition-colors",
                            ),
                            rx.el.button(
                                "Sign Up",
                                on_click=AuthState.open_signup_modal,
                                class_name="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-xl font-semibold shadow-sm transition-colors",
                            ),
                            class_name="flex items-center gap-3",
                        ),
                    ),
                    class_name="hidden lg:flex items-center gap-4",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("menu", class_name="h-6 w-6"),
                        on_click=MedicineState.toggle_menu,
                        class_name="lg:hidden p-2 text-gray-600 hover:text-blue-600",
                    ),
                    class_name="lg:hidden flex items-center",
                ),
                class_name="flex justify-between h-20",
            ),
            rx.cond(
                MedicineState.is_menu_open,
                rx.el.div(
                    rx.el.div(
                        rx.el.a(
                            "Home",
                            href="/",
                            class_name="block px-3 py-2 text-base font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-md",
                        ),
                        rx.el.a(
                            "Dashboard",
                            href="/dashboard",
                            class_name="block px-3 py-2 text-base font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-md",
                        ),
                        rx.el.a(
                            "MediCompare",
                            href="/compare",
                            class_name="block px-3 py-2 text-base font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-md",
                        ),
                        rx.el.a(
                            "Upload",
                            href="/upload",
                            class_name="block px-3 py-2 text-base font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-md",
                        ),
                        rx.el.a(
                            "Locator",
                            href="/locator",
                            class_name="block px-3 py-2 text-base font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-md",
                        ),
                        rx.el.a(
                            "Shop",
                            href="/shop",
                            class_name="block px-3 py-2 text-base font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-md",
                        ),
                        rx.el.button(
                            rx.el.div(
                                "Cart",
                                rx.cond(
                                    CheckoutState.cart_item_count > 0,
                                    rx.el.span(
                                        CheckoutState.cart_item_count,
                                        class_name="ml-2 bg-blue-100 text-blue-600 text-xs font-bold px-2 py-0.5 rounded-full",
                                    ),
                                ),
                                class_name="flex items-center",
                            ),
                            on_click=CheckoutState.toggle_cart_drawer,
                            class_name="block w-full text-left px-3 py-2 text-base font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-600 rounded-md",
                        ),
                        rx.el.a(
                            "MedOS ",
                            rx.el.span(
                                "PRO",
                                class_name="text-[8px] bg-green-100 text-green-700 px-1 py-0.5 rounded font-bold ml-1 align-top",
                            ),
                            href="/medos",
                            class_name="block px-3 py-2 text-base font-bold text-green-600 hover:bg-green-50 hover:text-green-700 rounded-md",
                        ),
                        rx.el.div(class_name="border-t border-gray-100 my-2"),
                        rx.cond(
                            AuthState.is_logged_in,
                            rx.el.div(
                                rx.el.div(
                                    rx.el.div(
                                        AuthState.user_initial,
                                        class_name="h-10 w-10 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center",
                                    ),
                                    rx.el.div(
                                        rx.el.p(
                                            AuthState.current_user["name"],
                                            class_name="font-bold text-gray-900",
                                        ),
                                        rx.el.p(
                                            AuthState.current_user["email"],
                                            class_name="text-xs text-gray-500",
                                        ),
                                        class_name="flex-1",
                                    ),
                                    class_name="flex items-center gap-3 px-3 py-2",
                                ),
                                rx.el.button(
                                    rx.icon("log-out", class_name="h-4 w-4 mr-2"),
                                    "Sign Out",
                                    on_click=AuthState.handle_logout,
                                    class_name="w-full flex items-center px-3 py-2 text-base font-medium text-red-600 hover:bg-red-50 rounded-md",
                                ),
                                class_name="space-y-1",
                            ),
                            rx.el.div(
                                rx.el.button(
                                    "Login",
                                    on_click=AuthState.open_login_modal,
                                    class_name="w-full text-center py-2 px-3 text-base font-medium text-blue-600 border border-blue-100 rounded-md hover:bg-blue-50",
                                ),
                                rx.el.button(
                                    "Sign Up",
                                    on_click=AuthState.open_signup_modal,
                                    class_name="w-full text-center py-2 px-3 text-base font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700",
                                ),
                                class_name="space-y-2 p-2",
                            ),
                        ),
                        class_name="px-2 pt-2 pb-3 space-y-1 bg-white border-b",
                    ),
                    class_name="lg:hidden",
                ),
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
        ),
        class_name="bg-white border-b sticky top-0 z-50 shadow-sm",
    )