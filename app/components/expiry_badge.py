import reflex as rx
from app.states.medicine_state import MedicineState


def expiry_badge(expiry_date_str: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("clock", class_name="h-3 w-3 mr-1"),
            rx.el.span("Expires: ", class_name="font-bold mr-1"),
            rx.moment(date=expiry_date_str, from_now=True),
            class_name="flex items-center text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded-lg bg-gray-100 text-gray-700 whitespace-nowrap",
        ),
        rx.el.p(expiry_date_str, class_name="text-[9px] text-gray-400 mt-0.5 ml-1"),
        class_name="flex flex-col",
    )


def expiry_countdown_card(expiry_date_str: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("triangle_alert", class_name="h-6 w-6 text-amber-500 mb-2"),
                rx.el.h4(
                    "Expiration Warning", class_name="text-sm font-bold text-gray-900"
                ),
                rx.el.div(
                    rx.el.p(
                        "This batch expires ", class_name="text-xs text-gray-500 inline"
                    ),
                    rx.moment(
                        date=expiry_date_str,
                        from_now=True,
                        class_name="text-xs font-bold text-amber-600",
                    ),
                    class_name="mt-1",
                ),
                rx.el.p(
                    f"Official Expiry: {expiry_date_str}",
                    class_name="text-[10px] text-gray-400 mt-2",
                ),
                class_name="flex-1",
            ),
            rx.el.div(
                rx.el.div(
                    class_name="h-12 w-12 rounded-full border-4 border-amber-100 border-t-amber-500 animate-spin-slow"
                ),
                class_name="flex items-center justify-center",
            ),
            class_name="flex items-start gap-4",
        ),
        class_name="bg-amber-50/50 p-6 rounded-2xl border border-amber-100 shadow-sm",
    )