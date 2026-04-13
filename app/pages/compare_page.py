import reflex as rx
from app.states.compare_state import CompareState
from app.components.navbar import navbar
from app.components.footer import footer
from app.components.chat_widget import chat_widget
from app.components.auth_modal import auth_modal
from app.components.cart_drawer import cart_drawer


def alternative_row(alt: dict) -> rx.Component:
    is_best_value = alt["price"].to(float) == CompareState.med_price_cheapest_safe
    savings_amt = CompareState.med_price_original - alt["price"].to(float)
    savings_pct = rx.cond(
        CompareState.med_price_original > 0,
        (savings_amt / CompareState.med_price_original * 100).to(int),
        0,
    )
    return rx.el.tr(
        rx.el.td(
            rx.cond(
                is_best_value,
                rx.icon("star", class_name="h-4 w-4 text-amber-500 fill-amber-500"),
                "-",
            ),
            class_name="py-4 px-4 text-center",
        ),
        rx.el.td(
            rx.el.p(alt["name"].to(str), class_name="font-bold text-gray-900"),
            rx.el.p(alt["manufacturer"].to(str), class_name="text-xs text-gray-500"),
            class_name="py-4 px-4",
        ),
        rx.el.td(
            rx.match(
                alt["type"],
                (
                    "Jan Aushadhi",
                    rx.el.span(
                        "Jan Aushadhi",
                        class_name="px-2 py-1 bg-green-100 text-green-700 text-xs font-bold rounded-full",
                    ),
                ),
                (
                    "Generic Brand",
                    rx.el.span(
                        "Generic Brand",
                        class_name="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-bold rounded-full",
                    ),
                ),
                (
                    "Original Brand",
                    rx.el.span(
                        "Original Brand",
                        class_name="px-2 py-1 bg-gray-100 text-gray-700 text-xs font-bold rounded-full",
                    ),
                ),
                rx.el.span(
                    alt["type"],
                    class_name="px-2 py-1 bg-indigo-100 text-indigo-700 text-xs font-bold rounded-full",
                ),
            ),
            class_name="py-4 px-4",
        ),
        rx.el.td(
            alt["salt_match"].to(str), class_name="py-4 px-4 text-sm text-gray-600"
        ),
        rx.el.td(
            alt["dosage_match"].to(str), class_name="py-4 px-4 text-sm text-gray-600"
        ),
        rx.el.td(f"₹{alt['price']}", class_name="py-4 px-4 font-bold text-gray-900"),
        rx.el.td(
            rx.el.span(
                alt["regulatory_badge"].to(str),
                class_name="text-xs text-gray-500 border border-gray-200 px-2 py-1 rounded",
            ),
            class_name="py-4 px-4",
        ),
        rx.el.td(
            rx.el.span(
                f"Save ₹{savings_amt}", class_name="text-sm font-bold text-green-600"
            ),
            class_name="py-4 px-4",
        ),
        class_name=rx.cond(
            is_best_value,
            "bg-green-50/50 hover:bg-green-50 border-b",
            "border-b hover:bg-gray-50 transition-colors",
        ),
    )


def compare_page() -> rx.Component:
    quick_meds = [
        "Crocin",
        "Pan 40",
        "Augmentin 625",
        "Thyronorm 50",
        "Glycomet 500",
        "Combiflam",
        "Allegra",
        "Dolo 650",
    ]
    return rx.el.main(
        navbar(),
        cart_drawer(),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "MediCompare AI",
                    class_name="px-3 py-1.5 bg-blue-100 text-blue-700 text-xs font-bold uppercase tracking-widest rounded-full mb-4 inline-block",
                ),
                rx.el.h1(
                    "Pharmaceutical Intelligence Engine",
                    class_name="text-4xl md:text-5xl font-extrabold text-gray-900 mb-4",
                ),
                rx.el.p(
                    "Enter any medicine name for a comprehensive 7-step safety and savings analysis",
                    class_name="text-gray-600 text-lg max-w-2xl mx-auto",
                ),
                class_name="max-w-4xl mx-auto text-center px-4 py-16",
            ),
            class_name="bg-gradient-to-b from-blue-50 to-white border-b border-gray-100",
        ),
        rx.el.div(
            rx.cond(
                ~CompareState.analysis_complete,
                rx.el.div(
                    rx.el.form(
                        rx.el.div(
                            rx.icon(
                                "search",
                                class_name="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 h-6 w-6",
                            ),
                            rx.el.input(
                                name="medicine_query",
                                placeholder="Enter medicine name (e.g., Crocin, Pan 40, Augmentin...)",
                                class_name="w-full pl-14 pr-4 py-5 bg-white border-2 border-gray-200 rounded-2xl focus:border-blue-500 focus:ring-0 text-xl shadow-sm transition-all",
                                default_value=CompareState.medicine_query,
                                key=CompareState.medicine_query,
                            ),
                            rx.el.button(
                                rx.cond(
                                    CompareState.is_analyzing,
                                    rx.icon(
                                        "loader", class_name="h-6 w-6 animate-spin"
                                    ),
                                    "Analyze Medicine",
                                ),
                                type="submit",
                                disabled=CompareState.is_analyzing,
                                class_name="absolute right-2 top-1/2 -translate-y-1/2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-bold transition-all disabled:opacity-70 flex items-center justify-center min-w-[160px]",
                            ),
                            class_name="relative",
                        ),
                        on_submit=CompareState.analyze_medicine,
                        class_name="mb-8",
                    ),
                    rx.cond(
                        CompareState.error_message != "",
                        rx.el.div(
                            rx.icon(
                                "circle-alert", class_name="h-5 w-5 text-red-500 mr-2"
                            ),
                            rx.el.span(
                                CompareState.error_message,
                                class_name="text-red-700 font-medium",
                            ),
                            class_name="flex items-center p-4 bg-red-50 rounded-xl mb-8",
                        ),
                    ),
                    rx.cond(
                        CompareState.is_analyzing,
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    class_name="h-full bg-blue-600 animate-pulse w-full"
                                ),
                                class_name="w-full h-2 bg-blue-100 rounded-full overflow-hidden",
                            ),
                            rx.el.p(
                                f"Analyzing {CompareState.medicine_query}...",
                                class_name="text-center text-sm font-medium text-gray-500 mt-2",
                            ),
                            class_name="mb-8",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Quick Analyze:",
                            class_name="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3",
                        ),
                        rx.el.div(
                            rx.foreach(
                                quick_meds,
                                lambda m: rx.el.button(
                                    m,
                                    on_click=lambda: CompareState.analyze_quick(m),
                                    class_name="px-4 py-2 bg-white border border-gray-200 rounded-full text-sm font-medium text-gray-700 hover:border-blue-500 hover:text-blue-600 transition-colors shadow-sm",
                                ),
                            ),
                            class_name="flex flex-wrap gap-2",
                        ),
                    ),
                    class_name="max-w-3xl mx-auto px-4 py-8",
                ),
            ),
            rx.cond(
                CompareState.analysis_complete,
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Step 1: Medicine Identification",
                            class_name="text-sm font-bold text-blue-600 uppercase tracking-widest mb-4",
                        ),
                        rx.el.div(
                            rx.el.h3(
                                CompareState.med_brand_name,
                                class_name="text-3xl font-extrabold text-gray-900 mb-6",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "flask-conical",
                                        class_name="h-5 w-5 text-blue-500 mr-3",
                                    ),
                                    rx.el.div(
                                        rx.el.p(
                                            "Active Ingredient",
                                            class_name="text-xs text-gray-500 font-bold uppercase",
                                        ),
                                        rx.el.p(
                                            CompareState.med_active_ingredients,
                                            class_name="font-semibold text-gray-900",
                                        ),
                                    ),
                                    class_name="flex items-center p-4 bg-white rounded-xl shadow-sm border border-gray-100",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "pill",
                                        class_name="h-5 w-5 text-indigo-500 mr-3",
                                    ),
                                    rx.el.div(
                                        rx.el.p(
                                            "Dosage Form",
                                            class_name="text-xs text-gray-500 font-bold uppercase",
                                        ),
                                        rx.el.p(
                                            CompareState.med_dosage_form,
                                            class_name="font-semibold text-gray-900",
                                        ),
                                    ),
                                    class_name="flex items-center p-4 bg-white rounded-xl shadow-sm border border-gray-100",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "activity",
                                        class_name="h-5 w-5 text-green-500 mr-3",
                                    ),
                                    rx.el.div(
                                        rx.el.p(
                                            "Category",
                                            class_name="text-xs text-gray-500 font-bold uppercase",
                                        ),
                                        rx.el.p(
                                            CompareState.med_therapeutic_category,
                                            class_name="font-semibold text-gray-900",
                                        ),
                                    ),
                                    class_name="flex items-center p-4 bg-white rounded-xl shadow-sm border border-gray-100",
                                ),
                                class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6",
                            ),
                            rx.el.div(
                                rx.el.h4(
                                    "How it works:",
                                    class_name="font-bold text-gray-900 text-sm mb-1",
                                ),
                                rx.el.p(
                                    CompareState.med_mechanism,
                                    class_name="text-gray-700 text-sm mb-4",
                                ),
                                rx.el.h4(
                                    "Standard Use:",
                                    class_name="font-bold text-gray-900 text-sm mb-1",
                                ),
                                rx.el.p(
                                    CompareState.med_standard_use,
                                    class_name="text-gray-700 text-sm",
                                ),
                                class_name="bg-white p-6 rounded-xl border border-gray-100 shadow-sm",
                            ),
                            class_name="bg-blue-50/50 p-6 md:p-8 rounded-3xl border border-blue-100",
                        ),
                        class_name="mb-12",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "Step 2: Regulatory Verification",
                            class_name="text-sm font-bold text-blue-600 uppercase tracking-widest mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.p(
                                        "CDSCO Approved",
                                        class_name="text-sm font-medium text-gray-500 mb-2",
                                    ),
                                    rx.cond(
                                        CompareState.med_cdsco_approved,
                                        rx.el.div(
                                            rx.icon(
                                                "message_circle_check",
                                                class_name="h-5 w-5 text-green-600 mr-2",
                                            ),
                                            rx.el.span(
                                                "Approved",
                                                class_name="font-bold text-green-700",
                                            ),
                                            class_name="flex items-center bg-green-50 px-3 py-2 rounded-lg w-fit",
                                        ),
                                        rx.el.div(
                                            rx.icon(
                                                "message_circle_x",
                                                class_name="h-5 w-5 text-red-600 mr-2",
                                            ),
                                            rx.el.span(
                                                "Not Approved",
                                                class_name="font-bold text-red-700",
                                            ),
                                            class_name="flex items-center bg-red-50 px-3 py-2 rounded-lg w-fit",
                                        ),
                                    ),
                                    class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "NLEM Listed",
                                        class_name="text-sm font-medium text-gray-500 mb-2",
                                    ),
                                    rx.cond(
                                        CompareState.med_nlem_listed,
                                        rx.el.div(
                                            rx.icon(
                                                "message_circle_check",
                                                class_name="h-5 w-5 text-green-600 mr-2",
                                            ),
                                            rx.el.span(
                                                "Listed",
                                                class_name="font-bold text-green-700",
                                            ),
                                            class_name="flex items-center bg-green-50 px-3 py-2 rounded-lg w-fit",
                                        ),
                                        rx.el.div(
                                            rx.icon(
                                                "circle_minus",
                                                class_name="h-5 w-5 text-gray-500 mr-2",
                                            ),
                                            rx.el.span(
                                                "Not Listed",
                                                class_name="font-bold text-gray-700",
                                            ),
                                            class_name="flex items-center bg-gray-50 px-3 py-2 rounded-lg w-fit",
                                        ),
                                    ),
                                    class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Jan Aushadhi",
                                        class_name="text-sm font-medium text-gray-500 mb-2",
                                    ),
                                    rx.el.div(
                                        rx.icon(
                                            "store",
                                            class_name="h-5 w-5 mr-2 text-blue-600",
                                        ),
                                        rx.el.span(
                                            CompareState.med_jan_aushadhi,
                                            class_name="font-bold text-blue-700",
                                        ),
                                        class_name="flex items-center bg-blue-50 px-3 py-2 rounded-lg w-fit",
                                    ),
                                    class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Manufacturing",
                                        class_name="text-sm font-medium text-gray-500 mb-2",
                                    ),
                                    rx.el.div(
                                        rx.icon(
                                            "shield",
                                            class_name="h-5 w-5 text-purple-600 mr-2",
                                        ),
                                        rx.el.span(
                                            CompareState.med_manufacturing_tier,
                                            class_name="font-bold text-purple-700",
                                        ),
                                        class_name="flex items-center bg-purple-50 px-3 py-2 rounded-lg w-fit",
                                    ),
                                    class_name="bg-white p-4 rounded-xl shadow-sm border border-gray-100",
                                ),
                                class_name="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "triangle_alert",
                                        class_name="h-6 w-6 text-amber-500 mr-3 mt-1 flex-shrink-0",
                                    ),
                                    rx.el.div(
                                        rx.el.h4(
                                            "Regulatory Warnings",
                                            class_name="font-bold text-amber-900",
                                        ),
                                        rx.el.p(
                                            CompareState.med_regulatory_warnings,
                                            class_name="text-amber-800 text-sm mt-1",
                                        ),
                                    ),
                                    class_name="flex items-start bg-amber-50 border border-amber-200 p-4 rounded-xl flex-1",
                                ),
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.span(
                                            CompareState.med_safety_score,
                                            class_name=rx.cond(
                                                CompareState.med_safety_score >= 95,
                                                "text-3xl font-black text-green-600",
                                                "text-3xl font-black text-amber-600",
                                            ),
                                        ),
                                        rx.el.span(
                                            "/100",
                                            class_name="text-sm text-gray-400 font-bold ml-1",
                                        ),
                                        class_name="flex items-baseline",
                                    ),
                                    rx.el.p(
                                        "Safety Score",
                                        class_name="text-xs text-gray-500 font-bold uppercase tracking-wider",
                                    ),
                                    class_name="bg-white p-4 rounded-xl border border-gray-100 shadow-sm flex flex-col items-center justify-center min-w-[150px]",
                                ),
                                class_name="flex flex-col md:flex-row gap-4",
                            ),
                            class_name="bg-gray-50 p-6 md:p-8 rounded-3xl border border-gray-200",
                        ),
                        class_name="mb-12",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "Step 3: Generic Alternatives",
                            class_name="text-sm font-bold text-blue-600 uppercase tracking-widest mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th(
                                                "", class_name="py-4 px-4 text-center"
                                            ),
                                            rx.el.th(
                                                "Name & Manufacturer",
                                                class_name="text-left py-4 px-4 text-xs font-bold text-gray-500 uppercase",
                                            ),
                                            rx.el.th(
                                                "Type",
                                                class_name="text-left py-4 px-4 text-xs font-bold text-gray-500 uppercase",
                                            ),
                                            rx.el.th(
                                                "Salt Match",
                                                class_name="text-left py-4 px-4 text-xs font-bold text-gray-500 uppercase",
                                            ),
                                            rx.el.th(
                                                "Dosage Match",
                                                class_name="text-left py-4 px-4 text-xs font-bold text-gray-500 uppercase",
                                            ),
                                            rx.el.th(
                                                "Price",
                                                class_name="text-left py-4 px-4 text-xs font-bold text-gray-500 uppercase",
                                            ),
                                            rx.el.th(
                                                "Regulatory",
                                                class_name="text-left py-4 px-4 text-xs font-bold text-gray-500 uppercase",
                                            ),
                                            rx.el.th(
                                                "Savings",
                                                class_name="text-left py-4 px-4 text-xs font-bold text-gray-500 uppercase",
                                            ),
                                            class_name="border-b bg-gray-50",
                                        )
                                    ),
                                    rx.el.tbody(
                                        rx.foreach(
                                            CompareState.med_alternatives,
                                            alternative_row,
                                        )
                                    ),
                                    class_name="w-full table-auto",
                                ),
                                class_name="overflow-x-auto",
                            ),
                            class_name="bg-white rounded-3xl border border-gray-200 shadow-sm overflow-hidden",
                        ),
                        class_name="mb-12",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "Step 4: Price Intelligence",
                            class_name="text-sm font-bold text-blue-600 uppercase tracking-widest mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.p(
                                        "Original Brand Price",
                                        class_name="text-sm font-bold text-gray-500 uppercase",
                                    ),
                                    rx.el.p(
                                        f"₹{CompareState.med_price_original}",
                                        class_name="text-3xl font-bold text-gray-400 line-through mt-2",
                                    ),
                                    class_name="bg-white p-6 rounded-2xl border border-gray-100 flex-1 text-center",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "arrow-right",
                                        class_name="h-8 w-8 text-gray-300 transform rotate-90 md:rotate-0",
                                    )
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Cheapest Safe Generic",
                                        class_name="text-sm font-bold text-green-700 uppercase",
                                    ),
                                    rx.el.p(
                                        f"₹{CompareState.med_price_cheapest_safe}",
                                        class_name="text-5xl font-black text-green-600 mt-2",
                                    ),
                                    class_name="bg-green-50 p-6 rounded-2xl border border-green-200 flex-1 text-center shadow-inner",
                                ),
                                class_name="flex flex-col md:flex-row items-center gap-6 mb-8",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.p(
                                        "You Save",
                                        class_name="text-sm text-green-800 font-medium",
                                    ),
                                    rx.el.h3(
                                        f"₹{CompareState.savings_amount} ({CompareState.savings_percent}%)",
                                        class_name="text-2xl font-bold text-green-900",
                                    ),
                                    class_name="flex flex-col",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Est. Annual Savings",
                                        class_name="text-sm text-green-800 font-medium",
                                    ),
                                    rx.el.h3(
                                        f"₹{CompareState.med_annual_savings}",
                                        class_name="text-2xl font-bold text-green-900",
                                    ),
                                    class_name="flex flex-col text-right",
                                ),
                                class_name="flex justify-between items-center bg-green-100 p-6 rounded-2xl",
                            ),
                            rx.cond(
                                CompareState.savings_percent > 50,
                                rx.el.div(
                                    rx.icon(
                                        "triangle-alert",
                                        class_name="h-5 w-5 text-amber-600 mr-2",
                                    ),
                                    rx.el.span(
                                        f"⚠️ A verified equivalent exists at {CompareState.savings_percent}% lower cost!",
                                        class_name="text-amber-800 font-bold",
                                    ),
                                    class_name="mt-4 p-4 bg-amber-100 rounded-xl flex items-center justify-center",
                                ),
                            ),
                            class_name="bg-white p-6 md:p-8 rounded-3xl border border-gray-200 shadow-sm",
                        ),
                        class_name="mb-12",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                "Step 5: Pharmacy Availability",
                                class_name="text-sm font-bold text-blue-600 uppercase tracking-widest mb-4",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "map-pin", class_name="h-12 w-12 text-blue-500 mb-4"
                                ),
                                rx.el.h3(
                                    f"Find {CompareState.best_value_name} Near You",
                                    class_name="text-xl font-bold text-gray-900 mb-2",
                                ),
                                rx.el.p(
                                    "Search our map for pharmacies currently stocking this alternative.",
                                    class_name="text-gray-600 mb-6",
                                ),
                                rx.el.a(
                                    "Open Pharmacy Locator →",
                                    href="/locator",
                                    class_name="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-bold transition-colors inline-block",
                                ),
                                class_name="bg-blue-50 p-8 rounded-3xl border border-blue-100 flex flex-col items-center text-center h-full",
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.div(
                            rx.el.h2(
                                "Step 6: Substitution Safety",
                                class_name="text-sm font-bold text-blue-600 uppercase tracking-widest mb-4",
                            ),
                            rx.el.div(
                                rx.match(
                                    CompareState.med_substitution_safety,
                                    (
                                        "🟢 GREEN",
                                        rx.el.div(
                                            rx.icon(
                                                "circle_check",
                                                class_name="h-12 w-12 text-green-500 mb-4",
                                            ),
                                            rx.el.h3(
                                                "Direct Substitution Safe",
                                                class_name="text-xl font-bold text-green-900 mb-2",
                                            ),
                                            class_name="bg-green-100 p-8 rounded-t-3xl border-b border-green-200 flex flex-col items-center text-center",
                                        ),
                                    ),
                                    (
                                        "🟡 YELLOW",
                                        rx.el.div(
                                            rx.icon(
                                                "circle_alert",
                                                class_name="h-12 w-12 text-amber-500 mb-4",
                                            ),
                                            rx.el.h3(
                                                "Consult Pharmacist",
                                                class_name="text-xl font-bold text-amber-900 mb-2",
                                            ),
                                            class_name="bg-amber-100 p-8 rounded-t-3xl border-b border-amber-200 flex flex-col items-center text-center",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.icon(
                                            "octagon_x",
                                            class_name="h-12 w-12 text-red-500 mb-4",
                                        ),
                                        rx.el.h3(
                                            "Doctor Approval Required",
                                            class_name="text-xl font-bold text-red-900 mb-2",
                                        ),
                                        class_name="bg-red-100 p-8 rounded-t-3xl border-b border-red-200 flex flex-col items-center text-center",
                                    ),
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        CompareState.med_substitution_note,
                                        class_name="text-gray-700 text-center font-medium",
                                    ),
                                    rx.cond(
                                        CompareState.med_narrow_therapeutic_index,
                                        rx.el.div(
                                            rx.icon(
                                                "triangle-alert",
                                                class_name="h-4 w-4 mr-2 text-red-600",
                                            ),
                                            rx.el.span(
                                                "NARROW THERAPEUTIC INDEX DRUG",
                                                class_name="text-xs font-bold text-red-700",
                                            ),
                                            class_name="flex items-center justify-center mt-4 p-2 bg-red-50 rounded-lg",
                                        ),
                                    ),
                                    class_name="p-6 bg-white rounded-b-3xl",
                                ),
                                class_name="border border-gray-200 rounded-3xl shadow-sm h-full flex flex-col",
                            ),
                            class_name="flex-1",
                        ),
                        class_name="flex flex-col md:flex-row gap-8 mb-12",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "Step 7: Patient Summary",
                            class_name="text-sm font-bold text-blue-600 uppercase tracking-widest mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "file-text",
                                        class_name="h-6 w-6 text-indigo-600 mr-2",
                                    ),
                                    rx.el.h3(
                                        "Summary for Your Records",
                                        class_name="text-xl font-bold text-gray-900",
                                    ),
                                    class_name="flex items-center",
                                ),
                                rx.el.button(
                                    rx.cond(
                                        CompareState.copied_summary,
                                        rx.icon(
                                            "check", class_name="h-5 w-5 text-green-600"
                                        ),
                                        rx.icon(
                                            "copy", class_name="h-5 w-5 text-gray-500"
                                        ),
                                    ),
                                    rx.cond(
                                        CompareState.copied_summary,
                                        rx.el.span(
                                            "Copied!",
                                            class_name="text-sm font-bold text-green-600",
                                        ),
                                        rx.el.span(
                                            "Copy",
                                            class_name="text-sm font-bold text-gray-600",
                                        ),
                                    ),
                                    on_click=CompareState.copy_summary,
                                    class_name="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors shadow-sm",
                                ),
                                class_name="flex justify-between items-center mb-6",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "pill",
                                        class_name="h-5 w-5 text-gray-400 mt-0.5",
                                    ),
                                    rx.el.p(
                                        rx.el.span(
                                            f"{CompareState.med_therapeutic_category}",
                                            class_name="font-bold",
                                        ),
                                        f" medication for {CompareState.med_standard_use.split('.')[0].lower()}.",
                                    ),
                                    class_name="flex items-start gap-3 mb-4",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "indian-rupee",
                                        class_name="h-5 w-5 text-green-500 mt-0.5",
                                    ),
                                    rx.el.p(
                                        rx.el.span(
                                            "Cheapest safe alternative:",
                                            class_name="font-bold",
                                        ),
                                        f" {CompareState.best_value_name} at ₹{CompareState.med_price_cheapest_safe} (save ₹{CompareState.savings_amount})",
                                    ),
                                    class_name="flex items-start gap-3 mb-4",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "map-pin",
                                        class_name="h-5 w-5 text-blue-500 mt-0.5",
                                    ),
                                    rx.el.p(
                                        "Find it at your nearest Jan Aushadhi Kendra or verified pharmacy."
                                    ),
                                    class_name="flex items-start gap-3 mb-4",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "triangle_alert",
                                        class_name="h-5 w-5 text-amber-500 mt-0.5",
                                    ),
                                    rx.el.p(
                                        rx.el.span("Caution:", class_name="font-bold"),
                                        f" {CompareState.med_regulatory_warnings.split('.')[0]}.",
                                    ),
                                    class_name="flex items-start gap-3 mb-4",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "bell-ring",
                                        class_name="h-5 w-5 text-purple-500 mt-0.5",
                                    ),
                                    rx.el.p(
                                        "Always confirm substitutions with your doctor or pharmacist before switching.",
                                        class_name="font-bold text-gray-900",
                                    ),
                                    class_name="flex items-start gap-3 p-4 bg-purple-50 rounded-xl mt-6",
                                ),
                                class_name="text-gray-700 bg-white p-6 rounded-2xl border border-gray-100",
                            ),
                            class_name="bg-indigo-50/50 p-6 md:p-8 rounded-3xl border border-indigo-100 shadow-md",
                        ),
                        class_name="mb-12",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("rotate-ccw", class_name="h-5 w-5 mr-2"),
                            "Analyze Another Medicine",
                            on_click=CompareState.reset_analysis,
                            class_name="flex items-center mx-auto bg-gray-900 hover:bg-gray-800 text-white px-8 py-4 rounded-xl font-bold transition-colors shadow-lg",
                        ),
                        class_name="py-8",
                    ),
                    class_name="max-w-5xl mx-auto px-4 py-8 animate-in fade-in slide-in-from-bottom-8 duration-500",
                ),
            ),
            class_name="min-h-[60vh]",
        ),
        footer(),
        chat_widget(),
        auth_modal(),
        class_name="bg-gray-50 min-h-screen",
    )