import reflex as rx
from app.states.auth_state import AuthState


def login_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Welcome Back", class_name="text-2xl font-bold text-gray-900 mb-1"
            ),
            rx.el.p(
                "Sign in to your MediSmart account", class_name="text-sm text-gray-500"
            ),
            class_name="mb-6",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "mail",
                        class_name="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Email Address",
                        type="email",
                        name="email",
                        class_name="w-full pl-12 pr-4 py-3 border-2 border-gray-100 rounded-xl focus:border-blue-500 focus:ring-0 transition-colors bg-gray-50 focus:bg-white outline-none",
                        default_value=AuthState.login_email,
                    ),
                    class_name="relative mb-4",
                ),
                rx.el.div(
                    rx.icon(
                        "lock",
                        class_name="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Password",
                        type=rx.cond(AuthState.show_login_password, "text", "password"),
                        name="password",
                        class_name="w-full pl-12 pr-12 py-3 border-2 border-gray-100 rounded-xl focus:border-blue-500 focus:ring-0 transition-colors bg-gray-50 focus:bg-white outline-none",
                        default_value=AuthState.login_password,
                    ),
                    rx.el.button(
                        rx.cond(
                            AuthState.show_login_password,
                            rx.icon(
                                "eye-off",
                                class_name="h-5 w-5 text-gray-400 hover:text-gray-600",
                            ),
                            rx.icon(
                                "eye",
                                class_name="h-5 w-5 text-gray-400 hover:text-gray-600",
                            ),
                        ),
                        type="button",
                        on_click=AuthState.toggle_login_password,
                        class_name="absolute right-4 top-1/2 -translate-y-1/2",
                    ),
                    class_name="relative mb-6",
                ),
                rx.cond(
                    AuthState.login_error != "",
                    rx.el.div(
                        rx.icon("circle-alert", class_name="h-4 w-4 mr-2"),
                        rx.el.span(AuthState.login_error),
                        class_name="flex items-center text-sm text-red-600 bg-red-50 p-3 rounded-lg mb-6",
                    ),
                ),
                rx.el.button(
                    rx.cond(
                        AuthState.login_loading,
                        rx.icon("loader", class_name="h-5 w-5 animate-spin mx-auto"),
                        "Sign In",
                    ),
                    type="submit",
                    disabled=AuthState.login_loading,
                    class_name="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl transition-colors shadow-lg shadow-blue-200 disabled:opacity-70",
                ),
                class_name="flex flex-col",
            ),
            on_submit=AuthState.handle_login,
        ),
        rx.el.div(
            rx.el.p(
                "Don't have an account? ",
                rx.el.button(
                    "Sign up",
                    on_click=AuthState.open_signup_modal,
                    class_name="text-blue-600 hover:text-blue-700 font-semibold",
                ),
                class_name="text-sm text-gray-500",
            ),
            class_name="mt-6 text-center",
        ),
    )


def signup_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                "Create Account", class_name="text-2xl font-bold text-gray-900 mb-1"
            ),
            rx.el.p(
                "Join MediSmart to start saving", class_name="text-sm text-gray-500"
            ),
            class_name="mb-6",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "user",
                            class_name="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                        ),
                        rx.el.input(
                            placeholder="Full Name",
                            name="name",
                            class_name=rx.cond(
                                AuthState.signup_field_errors.contains("name"),
                                "w-full pl-12 pr-4 py-3 border-2 border-red-300 rounded-xl focus:border-red-500 focus:ring-0 transition-colors bg-red-50 outline-none",
                                "w-full pl-12 pr-4 py-3 border-2 border-gray-100 rounded-xl focus:border-blue-500 focus:ring-0 transition-colors bg-gray-50 focus:bg-white outline-none",
                            ),
                            default_value=AuthState.signup_name,
                        ),
                        class_name="relative",
                    ),
                    rx.cond(
                        AuthState.signup_field_errors.contains("name"),
                        rx.el.div(
                            rx.icon("circle-alert", class_name="h-3 w-3 mr-1"),
                            rx.el.span(AuthState.signup_field_errors["name"]),
                            class_name="flex items-center text-xs text-red-500 mt-1",
                        ),
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "mail",
                            class_name="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                        ),
                        rx.el.input(
                            placeholder="Email Address",
                            type="email",
                            name="email",
                            class_name=rx.cond(
                                AuthState.signup_field_errors.contains("email"),
                                "w-full pl-12 pr-4 py-3 border-2 border-red-300 rounded-xl focus:border-red-500 focus:ring-0 transition-colors bg-red-50 outline-none",
                                "w-full pl-12 pr-4 py-3 border-2 border-gray-100 rounded-xl focus:border-blue-500 focus:ring-0 transition-colors bg-gray-50 focus:bg-white outline-none",
                            ),
                            default_value=AuthState.signup_email,
                        ),
                        class_name="relative",
                    ),
                    rx.cond(
                        AuthState.signup_field_errors.contains("email"),
                        rx.el.div(
                            rx.icon("circle-alert", class_name="h-3 w-3 mr-1"),
                            rx.el.span(AuthState.signup_field_errors["email"]),
                            class_name="flex items-center text-xs text-red-500 mt-1",
                        ),
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "lock",
                            class_name="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                        ),
                        rx.el.input(
                            placeholder="Password (min 6 characters)",
                            type=rx.cond(
                                AuthState.show_signup_password, "text", "password"
                            ),
                            name="password",
                            class_name=rx.cond(
                                AuthState.signup_field_errors.contains("password"),
                                "w-full pl-12 pr-12 py-3 border-2 border-red-300 rounded-xl focus:border-red-500 focus:ring-0 transition-colors bg-red-50 outline-none",
                                "w-full pl-12 pr-12 py-3 border-2 border-gray-100 rounded-xl focus:border-blue-500 focus:ring-0 transition-colors bg-gray-50 focus:bg-white outline-none",
                            ),
                            default_value=AuthState.signup_password,
                        ),
                        rx.el.button(
                            rx.cond(
                                AuthState.show_signup_password,
                                rx.icon(
                                    "eye-off",
                                    class_name="h-5 w-5 text-gray-400 hover:text-gray-600",
                                ),
                                rx.icon(
                                    "eye",
                                    class_name="h-5 w-5 text-gray-400 hover:text-gray-600",
                                ),
                            ),
                            type="button",
                            on_click=AuthState.toggle_signup_password,
                            class_name="absolute right-4 top-1/2 -translate-y-1/2",
                        ),
                        class_name="relative",
                    ),
                    rx.cond(
                        AuthState.signup_field_errors.contains("password"),
                        rx.el.div(
                            rx.icon("circle-alert", class_name="h-3 w-3 mr-1"),
                            rx.el.span(AuthState.signup_field_errors["password"]),
                            class_name="flex items-center text-xs text-red-500 mt-1",
                        ),
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "shield-check",
                            class_name="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                        ),
                        rx.el.input(
                            placeholder="Confirm Password",
                            type=rx.cond(
                                AuthState.show_signup_confirm, "text", "password"
                            ),
                            name="confirm_password",
                            class_name=rx.cond(
                                AuthState.signup_field_errors.contains(
                                    "confirm_password"
                                ),
                                "w-full pl-12 pr-12 py-3 border-2 border-red-300 rounded-xl focus:border-red-500 focus:ring-0 transition-colors bg-red-50 outline-none",
                                "w-full pl-12 pr-12 py-3 border-2 border-gray-100 rounded-xl focus:border-blue-500 focus:ring-0 transition-colors bg-gray-50 focus:bg-white outline-none",
                            ),
                            default_value=AuthState.signup_confirm_password,
                        ),
                        rx.el.button(
                            rx.cond(
                                AuthState.show_signup_confirm,
                                rx.icon(
                                    "eye-off",
                                    class_name="h-5 w-5 text-gray-400 hover:text-gray-600",
                                ),
                                rx.icon(
                                    "eye",
                                    class_name="h-5 w-5 text-gray-400 hover:text-gray-600",
                                ),
                            ),
                            type="button",
                            on_click=AuthState.toggle_signup_confirm,
                            class_name="absolute right-4 top-1/2 -translate-y-1/2",
                        ),
                        class_name="relative",
                    ),
                    rx.cond(
                        AuthState.signup_field_errors.contains("confirm_password"),
                        rx.el.div(
                            rx.icon("circle-alert", class_name="h-3 w-3 mr-1"),
                            rx.el.span(
                                AuthState.signup_field_errors["confirm_password"]
                            ),
                            class_name="flex items-center text-xs text-red-500 mt-1",
                        ),
                    ),
                    class_name="mb-6",
                ),
                rx.el.button(
                    rx.cond(
                        AuthState.signup_loading,
                        rx.icon("loader", class_name="h-5 w-5 animate-spin mx-auto"),
                        "Create Account",
                    ),
                    type="submit",
                    disabled=AuthState.signup_loading,
                    class_name="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl transition-colors shadow-lg shadow-blue-200 disabled:opacity-70",
                ),
                class_name="flex flex-col",
            ),
            on_submit=AuthState.handle_signup,
        ),
        rx.el.div(
            rx.el.p(
                "Already have an account? ",
                rx.el.button(
                    "Sign in",
                    on_click=AuthState.open_login_modal,
                    class_name="text-blue-600 hover:text-blue-700 font-semibold",
                ),
                class_name="text-sm text-gray-500",
            ),
            class_name="mt-6 text-center",
        ),
    )


def auth_modal() -> rx.Component:
    return rx.cond(
        AuthState.show_login_modal | AuthState.show_signup_modal,
        rx.el.div(
            rx.el.div(
                on_click=AuthState.close_modals,
                class_name="absolute inset-0 bg-black/60 backdrop-blur-sm",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("x", class_name="h-5 w-5"),
                    on_click=AuthState.close_modals,
                    class_name="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors p-2",
                ),
                rx.cond(AuthState.show_login_modal, login_form(), signup_form()),
                class_name="relative bg-white rounded-3xl shadow-2xl max-w-md w-full mx-4 p-8 animate-in fade-in zoom-in duration-200",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center",
        ),
    )