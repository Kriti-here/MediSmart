import reflex as rx
from app.components.navbar import navbar
from app.components.footer import footer
from app.components.chat_widget import chat_widget
from app.components.expiry_badge import expiry_badge
from app.components.auth_modal import auth_modal
from app.components.cart_drawer import cart_drawer
from app.states.medicine_state import MedicineState, ExtractedMedicine

UPLOAD_ID = "prescription_upload"


def processing_indicator() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    class_name="h-2 bg-blue-600 rounded-full transition-all duration-300",
                    style={"width": f"{MedicineState.ocr_progress}%"},
                ),
                class_name="w-full h-2 bg-gray-100 rounded-full overflow-hidden mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("loader", class_name="h-5 w-5 text-blue-600 animate-spin"),
                    rx.el.span(
                        MedicineState.processing_step,
                        class_name="text-sm font-medium text-gray-700",
                    ),
                    class_name="flex items-center gap-3 justify-center",
                ),
                rx.el.span(
                    f"{MedicineState.ocr_progress}%",
                    class_name="text-sm font-bold text-blue-600",
                ),
                class_name="flex justify-between items-center",
            ),
            class_name="max-w-md mx-auto",
        ),
        class_name="py-12 px-6 bg-white rounded-3xl border border-blue-100 shadow-sm animate-pulse",
    )


def extracted_medicine_card(med: ExtractedMedicine) -> rx.Component:
    savings_amt = med["brand_price"].to(int) - med["generic_price"].to(int)
    savings_pct = rx.cond(
        med["brand_price"].to(int) > 0,
        (med["brand_price"].to(int) - med["generic_price"].to(int))
        * 100
        // med["brand_price"].to(int),
        0,
    )
    return rx.el.div(
        rx.cond(
            med["needs_review"],
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        class_name="h-2 w-2 rounded-full bg-amber-500 animate-pulse mr-2"
                    ),
                    rx.el.span(
                        "☐ Needs Manual Review",
                        class_name="text-[10px] font-bold uppercase tracking-widest text-amber-800",
                    ),
                    class_name="flex items-center justify-center py-2 bg-amber-100/50 border-b border-amber-200",
                )
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h4(
                            med["name"], class_name="text-xl font-bold text-gray-900"
                        ),
                        rx.el.div(
                            rx.el.span(
                                rx.el.span(med["confidence"].to(str)),
                                rx.el.span("% Confidence"),
                                class_name=rx.cond(
                                    med["confidence"] >= 90,
                                    "text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-green-100 text-green-700",
                                    rx.cond(
                                        med["confidence"] >= 75,
                                        "text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-yellow-100 text-yellow-700",
                                        "text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-red-100 text-red-700",
                                    ),
                                ),
                            ),
                            rx.cond(
                                med["confidence"] < 75,
                                rx.el.div(
                                    "Unclear Handwriting Detected",
                                    class_name="text-[10px] font-bold text-red-500 uppercase mt-1",
                                ),
                                rx.fragment(),
                            ),
                            class_name="mt-1",
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.div(
                        expiry_badge(med["expiry_date"]),
                        rx.el.p(
                            "Extracted Item",
                            class_name="text-[10px] text-gray-400 font-bold uppercase mt-2",
                        ),
                        class_name="text-right",
                    ),
                    class_name="flex justify-between items-start border-b border-gray-100 pb-4",
                ),
                rx.cond(
                    med["needs_review"],
                    rx.el.div(
                        rx.icon(
                            "info",
                            class_name="h-4 w-4 text-amber-600 mr-2 shrink-0 mt-0.5",
                        ),
                        rx.el.p(
                            med["review_reason"],
                            class_name="text-xs text-amber-800 font-medium",
                        ),
                        class_name="bg-amber-50 p-3 rounded-xl border border-amber-100 my-4",
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Dosage",
                            class_name="text-[10px] text-gray-400 font-bold uppercase",
                        ),
                        rx.el.p(
                            med["dosage"],
                            class_name="text-sm font-semibold text-gray-700",
                        ),
                        class_name="flex flex-col",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Frequency",
                            class_name="text-[10px] text-gray-400 font-bold uppercase",
                        ),
                        rx.el.p(
                            med["frequency"],
                            class_name="text-sm font-semibold text-gray-700",
                        ),
                        class_name="flex flex-col",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Duration",
                            class_name="text-[10px] text-gray-400 font-bold uppercase",
                        ),
                        rx.el.p(
                            med["duration"],
                            class_name="text-sm font-semibold text-gray-700",
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="grid grid-cols-3 gap-4 py-4 border-b border-gray-50",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Verified Generic Alternative",
                            class_name="text-xs text-blue-600 font-bold uppercase tracking-tight mb-1",
                        ),
                        rx.el.p(
                            med["generic_name"],
                            class_name="text-lg font-extrabold text-gray-900",
                        ),
                        rx.el.p(
                            med["salt_composition"],
                            class_name="text-sm text-gray-500 italic",
                        ),
                        class_name="py-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                rx.el.span("‹"),
                                rx.el.span(med["brand_price"].to(str)),
                                class_name="text-sm font-bold text-gray-400 line-through",
                            ),
                            rx.icon(
                                "arrow-right", class_name="h-4 w-4 text-gray-300 mx-2"
                            ),
                            rx.el.p(
                                rx.el.span("‹"),
                                rx.el.span(med["generic_price"].to(str)),
                                class_name="text-3xl font-black text-green-600",
                            ),
                            class_name="flex items-center",
                        ),
                        rx.el.div(
                            rx.el.div(
                                "Save ₹",
                                rx.el.span(savings_amt.to(str), class_name="font-bold"),
                                class_name="text-xs text-green-700",
                            ),
                            rx.el.div(
                                "(",
                                rx.el.span(savings_pct.to(str)),
                                "% Off)",
                                class_name="text-[10px] font-medium text-green-600",
                            ),
                            class_name="bg-green-50 px-2 py-1 rounded-lg border border-green-100 mt-1 w-fit",
                        ),
                        class_name="mb-6",
                    ),
                    class_name="",
                ),
                rx.el.div(
                    rx.cond(
                        med["matched_id"] != "",
                        rx.el.button(
                            "View Full Comparison",
                            on_click=lambda: MedicineState.select_medicine(
                                med["matched_id"]
                            ),
                            class_name="w-full flex items-center justify-center gap-2 bg-blue-50 hover:bg-blue-100 text-blue-600 font-bold py-3 rounded-xl transition-all",
                        ),
                        rx.el.div(
                            rx.icon(
                                "search-x", class_name="h-4 w-4 text-gray-400 mr-2"
                            ),
                            rx.el.span(
                                "No exact match in database",
                                class_name="text-sm font-bold text-gray-400",
                            ),
                            class_name="w-full flex items-center justify-center py-3 bg-gray-50 rounded-xl border border-dashed border-gray-200",
                        ),
                    ),
                    class_name="mt-2 pt-4 border-t border-gray-50",
                ),
                class_name="p-6",
            )
        ),
        class_name=rx.cond(
            med["needs_review"],
            "bg-amber-50/50 rounded-[2rem] border border-amber-200 shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden",
            "bg-white rounded-[2rem] border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden",
        ),
    )


def results_summary() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "message_circle_check", class_name="h-10 w-10 text-green-500"
                    ),
                    class_name="p-3 bg-green-50 rounded-2xl",
                ),
                rx.el.div(
                    rx.el.h3(
                        rx.cond(
                            MedicineState.items_needing_review > 0,
                            "Manual Review Required",
                            "Analysis Complete",
                        ),
                        class_name="text-2xl font-extrabold text-gray-900",
                    ),
                    rx.el.p(
                        rx.el.span(
                            f"{MedicineState.extracted_medicines.length()} medicines identified "
                        ),
                        rx.cond(
                            MedicineState.items_needing_review > 0,
                            rx.el.span(
                                f"({MedicineState.items_needing_review} flagged)",
                                class_name="font-bold text-amber-600",
                            ),
                            rx.el.span(
                                "verified by AI", class_name="font-bold text-blue-600"
                            ),
                        ),
                        class_name="text-sm text-gray-500",
                    ),
                ),
                class_name="flex items-center gap-5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Total Potential Savings",
                        class_name="text-[10px] font-bold text-green-700 uppercase tracking-widest",
                    ),
                    rx.el.p(
                        f"‹{MedicineState.total_savings}",
                        class_name="text-3xl font-black text-green-600",
                    ),
                    rx.el.p(
                        "per treatment cycle",
                        class_name="text-[10px] text-gray-400 font-medium text-right",
                    ),
                    class_name="text-right",
                ),
                class_name="bg-green-50/50 px-8 py-5 rounded-[2rem] border-2 border-green-100 shadow-inner",
            ),
            class_name="flex flex-col md:flex-row md:items-center justify-between gap-8",
        ),
        class_name="bg-white rounded-[2.5rem] border border-gray-100 shadow-lg p-10 mb-8",
    )


def upload_page() -> rx.Component:
    return rx.el.main(
        navbar(),
        cart_drawer(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "AI Powered Extraction",
                        class_name="px-3 py-1 bg-indigo-50 text-indigo-600 text-[10px] font-bold uppercase tracking-widest rounded-full mb-4 inline-block",
                    ),
                    rx.el.h1(
                        "Prescription ",
                        rx.el.span("Smart Scan", class_name="text-indigo-600"),
                        class_name="text-4xl md:text-5xl font-extrabold text-gray-900 mb-6",
                    ),
                    rx.el.p(
                        "Upload your handwritten or printed prescription. Our medical AI will identify the salts and find the most affordable verified generic alternatives.",
                        class_name="text-gray-500 max-w-2xl mx-auto text-lg",
                    ),
                    class_name="text-center mb-16",
                ),
                rx.cond(
                    ~MedicineState.is_processing & ~MedicineState.ocr_complete,
                    rx.el.div(
                        rx.upload.root(
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "cloud-upload",
                                        class_name="h-12 w-12 text-blue-500 mb-4",
                                    ),
                                    rx.el.p(
                                        "Drag & drop your prescription image",
                                        class_name="text-lg font-bold text-gray-900 mb-1",
                                    ),
                                    rx.el.p(
                                        "or click to browse your files",
                                        class_name="text-gray-500",
                                    ),
                                    rx.el.div(
                                        rx.el.span(
                                            "JPG, PNG up to 10MB",
                                            class_name="text-xs text-gray-400 bg-gray-50 px-3 py-1 rounded-full mt-6",
                                        ),
                                        class_name="flex justify-center",
                                    ),
                                    class_name="flex flex-col items-center justify-center py-16",
                                ),
                                class_name="border-4 border-dashed border-blue-100 rounded-[2rem] hover:border-blue-300 hover:bg-blue-50/30 transition-all cursor-pointer",
                            ),
                            id=UPLOAD_ID,
                            accept={
                                "image/jpeg": [".jpg", ".jpeg"],
                                "image/png": [".png"],
                            },
                            max_files=1,
                        ),
                        rx.el.div(
                            rx.foreach(
                                rx.selected_files(UPLOAD_ID),
                                lambda f: rx.el.div(
                                    rx.icon(
                                        "file-image", class_name="h-4 w-4 text-blue-500"
                                    ),
                                    rx.el.span(
                                        f,
                                        class_name="text-sm font-medium text-gray-700",
                                    ),
                                    class_name="flex items-center gap-2 mt-4 px-4 py-2 bg-blue-50 rounded-lg border border-blue-100 w-fit mx-auto animate-in fade-in slide-in-from-top-1",
                                ),
                            )
                        ),
                        rx.cond(
                            rx.selected_files(UPLOAD_ID).length() > 0,
                            rx.el.div(
                                rx.el.button(
                                    "Analyze Prescription",
                                    on_click=MedicineState.analyze_prescription,
                                    class_name="bg-blue-600 hover:bg-blue-700 text-white px-12 py-4 rounded-2xl font-bold shadow-xl shadow-blue-200 transition-all active:scale-95",
                                ),
                                class_name="flex justify-center mt-12",
                            ),
                        ),
                        class_name="max-w-3xl mx-auto",
                    ),
                ),
                rx.cond(MedicineState.is_processing, processing_indicator()),
                rx.cond(
                    MedicineState.ocr_complete,
                    rx.el.div(
                        results_summary(),
                        rx.cond(
                            MedicineState.items_needing_review > 0,
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "triangle-alert",
                                        class_name="h-6 w-6 text-amber-600 mr-4 shrink-0",
                                    ),
                                    rx.el.div(
                                        rx.el.p(
                                            rx.el.span("☐ "),
                                            rx.el.span(
                                                MedicineState.items_needing_review.to(
                                                    str
                                                )
                                            ),
                                            rx.el.span(
                                                " item(s) flagged for manual review"
                                            ),
                                            class_name="font-bold text-amber-900",
                                        ),
                                        rx.el.p(
                                            "Some medicine names could not be read with high confidence. Please verify the flagged items with your pharmacist or doctor before switching to generics.",
                                            class_name="text-sm text-amber-800 mt-1",
                                        ),
                                    ),
                                    class_name="flex items-start",
                                ),
                                class_name="bg-amber-50 border-2 border-amber-200 rounded-3xl p-6 mb-8 animate-in fade-in slide-in-from-top-2",
                            ),
                            rx.fragment(),
                        ),
                        rx.el.div(
                            rx.foreach(
                                MedicineState.extracted_medicines,
                                extracted_medicine_card,
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("refresh-ccw", class_name="h-4 w-4 mr-2"),
                                "Upload Another Prescription",
                                on_click=MedicineState.reset_upload,
                                class_name="bg-gray-900 text-white px-8 py-3 rounded-xl font-bold shadow-lg mt-12 hover:bg-gray-800 transition-colors",
                            ),
                            class_name="flex justify-center",
                        ),
                    ),
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24",
            ),
            class_name="bg-white min-h-screen",
        ),
        footer(),
        chat_widget(),
        auth_modal(),
        class_name="bg-gray-50 min-h-screen",
    )