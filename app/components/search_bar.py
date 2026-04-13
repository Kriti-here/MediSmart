import reflex as rx
from app.states.medicine_state import MedicineState
from app.components.expiry_badge import expiry_badge


def search_suggestion(medicine: dict) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        medicine["brand_name"], class_name="font-bold text-gray-900"
                    ),
                    rx.el.span(
                        f" ({medicine['generic_name']})",
                        class_name="text-gray-500 text-sm",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.div(
                    rx.el.span(
                        medicine["salt_composition"],
                        class_name="text-xs text-blue-600 font-medium",
                    ),
                    class_name="mt-0.5",
                ),
                class_name="text-left flex-1",
            ),
            expiry_badge(medicine["expiry_date"]),
            class_name="flex items-center justify-between gap-4 w-full",
        ),
        on_click=lambda: MedicineState.select_medicine(medicine["id"]),
        class_name="w-full px-4 py-3 hover:bg-blue-50 transition-colors border-b last:border-0 flex items-center",
    )


def search_section() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 h-5 w-5",
                ),
                rx.el.input(
                    placeholder="Search by Brand, Salt, or Generic Name (e.g. Crocin, Pantoprazole...)",
                    on_change=MedicineState.set_search_query.debounce(300),
                    class_name="w-full pl-12 pr-4 py-4 md:py-5 bg-white border-2 border-gray-100 rounded-2xl focus:border-blue-500 focus:ring-0 shadow-xl text-lg transition-all",
                ),
                class_name="relative",
            ),
            rx.cond(
                MedicineState.search_results.length() > 0,
                rx.el.div(
                    rx.foreach(MedicineState.search_results, search_suggestion),
                    class_name="absolute top-full left-0 right-0 mt-2 bg-white rounded-xl shadow-2xl border border-gray-100 overflow-hidden z-40 animate-in fade-in slide-in-from-top-2",
                ),
            ),
            class_name="relative w-full max-w-3xl mx-auto",
        ),
        class_name="px-4 py-8",
    )