import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.navbar import navbar
from app.components.footer import footer
from app.components.chat_widget import chat_widget
from app.components.auth_modal import auth_modal
from app.components.cart_drawer import cart_drawer


def member_avatar(member: dict, idx: int) -> rx.Component:
    return rx.el.button(
        rx.image(
            src=f"https://api.dicebear.com/9.x/initials/svg?seed={member['avatar_seed']}",
            class_name="h-12 w-12 rounded-full border-2 "
            + rx.cond(
                DashboardState.active_member_index == idx,
                "border-blue-600 shadow-md",
                "border-transparent opacity-70 hover:opacity-100",
            ),
        ),
        rx.el.span(
            member["name"],
            class_name="text-xs font-medium mt-1 "
            + rx.cond(
                DashboardState.active_member_index == idx,
                "text-blue-600",
                "text-gray-500",
            ),
        ),
        on_click=lambda: DashboardState.set_active_member(idx),
        class_name="flex flex-col items-center",
    )


def dashboard_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        cart_drawer(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.icon("heart-pulse", class_name="h-10 w-10 text-blue-600 mr-4"),
                    rx.el.div(
                        rx.el.h1(
                            "Family Health Dashboard",
                            class_name="text-3xl font-extrabold text-gray-900",
                        ),
                        rx.el.p(
                            "Manage your family's health, track medications, and monitor vitals",
                            class_name="text-gray-500",
                        ),
                    ),
                    class_name="flex items-center mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.foreach(
                            DashboardState.family_members,
                            lambda m, i: member_avatar(m, i),
                        ),
                        rx.el.button(
                            rx.el.div(
                                rx.icon("plus", class_name="h-6 w-6 text-gray-400"),
                                class_name="h-12 w-12 rounded-full border-2 border-dashed border-gray-300 flex items-center justify-center hover:bg-gray-50 transition-colors",
                            ),
                            rx.el.span(
                                "Add Member",
                                class_name="text-xs font-medium mt-1 text-gray-500",
                            ),
                            on_click=DashboardState.toggle_add_member,
                            class_name="flex flex-col items-center",
                        ),
                        class_name="flex gap-6 overflow-x-auto pb-4 scrollbar-hide items-start",
                    ),
                    class_name="border-b border-gray-200 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "pill", class_name="h-5 w-5 text-blue-600 mr-2"
                                ),
                                rx.el.h2(
                                    "Daily Medicines",
                                    class_name="text-lg font-bold text-gray-900",
                                ),
                                class_name="flex items-center mb-4",
                            ),
                            rx.el.div(
                                rx.foreach(
                                    DashboardState.active_member_medicines,
                                    lambda med: rx.el.div(
                                        rx.el.div(
                                            rx.el.p(
                                                med["name"],
                                                class_name="font-bold text-gray-900",
                                            ),
                                            rx.el.p(
                                                med["dosage"],
                                                class_name="text-sm text-gray-500",
                                            ),
                                        ),
                                        rx.el.div(
                                            rx.el.span(
                                                med["time"],
                                                class_name="text-xs font-medium text-blue-700 bg-blue-50 px-2 py-1 rounded-md",
                                            ),
                                            class_name="mt-2",
                                        ),
                                        class_name="p-4 border border-gray-100 rounded-xl mb-3 hover:shadow-sm transition-shadow",
                                    ),
                                )
                            ),
                            rx.el.a(
                                "Buy on Shop →",
                                href="/shop",
                                class_name="text-sm font-semibold text-blue-600 hover:text-blue-700 block mt-4",
                            ),
                            class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.h2(
                                    "Weekly Adherence",
                                    class_name="text-lg font-bold text-gray-900",
                                ),
                                rx.el.span(
                                    f"{DashboardState.adherence_percent}%",
                                    class_name="px-2 py-1 bg-green-100 text-green-700 font-bold rounded-lg text-sm",
                                ),
                                class_name="flex justify-between items-center mb-6",
                            ),
                            rx.el.div(
                                class_name="h-2 bg-gray-100 rounded-full w-full mb-4 overflow-hidden"
                            ),
                            class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mt-6",
                        ),
                        class_name="col-span-1 flex flex-col",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    "activity",
                                    class_name="h-5 w-5 text-indigo-600 mr-2",
                                ),
                                rx.el.h2(
                                    "Health Vitals",
                                    class_name="text-lg font-bold text-gray-900",
                                ),
                                class_name="flex items-center mb-6",
                            ),
                            rx.recharts.area_chart(
                                rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                                rx.recharts.graphing_tooltip(),
                                rx.recharts.area(
                                    data_key="BP Systolic",
                                    stroke="#3b82f6",
                                    fill="#3b82f6",
                                    fill_opacity=0.3,
                                ),
                                rx.recharts.area(
                                    data_key="Sugar",
                                    stroke="#f59e0b",
                                    fill="#f59e0b",
                                    fill_opacity=0.3,
                                ),
                                rx.recharts.x_axis(data_key="date"),
                                rx.recharts.y_axis(),
                                data=DashboardState.vitals_chart_data,
                                height=250,
                                width="100%",
                            ),
                            class_name="bg-white p-6 rounded-2xl shadow-sm border border-gray-100",
                        ),
                        class_name="col-span-1 flex flex-col gap-6",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12",
            ),
            class_name="bg-gray-50 min-h-screen",
        ),
        footer(),
        chat_widget(),
        auth_modal(),
    )