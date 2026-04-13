import reflex as rx


def footer_section(title: str, links: list[tuple[str, str]]) -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            title,
            class_name="text-sm font-semibold text-gray-900 uppercase tracking-wider mb-4",
        ),
        rx.el.ul(
            rx.foreach(
                links,
                lambda link: rx.el.li(
                    rx.el.a(
                        link[0],
                        href=link[1],
                        class_name="text-base text-gray-500 hover:text-blue-600 transition-colors",
                    ),
                    class_name="mb-2",
                ),
            ),
            class_name="mt-4",
        ),
    )


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("shield-plus", class_name="h-6 w-6 text-blue-600 mr-2"),
                        rx.el.span(
                            "MediSmart", class_name="text-xl font-bold text-gray-900"
                        ),
                        class_name="flex items-center mb-6",
                    ),
                    rx.el.p(
                        "Empowering patients with information to find affordable generic alternatives without compromising on quality.",
                        class_name="text-gray-500 text-sm max-w-xs mb-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon("award", class_name="h-5 w-5 text-green-500 mr-2"),
                            rx.el.span(
                                "Verified Data Sources",
                                class_name="text-xs text-gray-600 font-medium",
                            ),
                            class_name="flex items-center",
                        ),
                        class_name="p-3 bg-gray-50 rounded-lg inline-block",
                    ),
                    class_name="col-span-1 md:col-span-2",
                ),
                footer_section(
                    "Platform",
                    [
                        ("Search Medicines", "/"),
                        ("Upload Prescription", "#"),
                        ("Pharmacy Locator", "#"),
                    ],
                ),
                footer_section(
                    "Information",
                    [("How it works", "#"), ("Medicine Safety", "#"), ("FAQ", "#")],
                ),
                footer_section(
                    "Legal",
                    [
                        ("Privacy Policy", "#"),
                        ("Terms of Service", "#"),
                        ("Disclaimer", "#"),
                    ],
                ),
                class_name="grid grid-cols-2 md:grid-cols-5 gap-8",
            ),
            rx.el.div(
                rx.el.p(
                    "Disclaimer: This platform provides informational comparisons for educational purposes. Always consult a licensed medical professional before changing medications or dosages. All health claims should be verified with your doctor.",
                    class_name="text-xs text-gray-400 text-center italic",
                ),
                rx.el.div(
                    rx.el.p(
                        f"© 2024 MediSmart Health Intelligence. All rights reserved.",
                        class_name="text-sm text-gray-500",
                    ),
                    class_name="mt-8 border-t border-gray-100 pt-8 flex justify-center items-center",
                ),
                class_name="mt-12 pt-8 border-t border-gray-200",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12",
        ),
        class_name="bg-white border-t mt-20",
    )