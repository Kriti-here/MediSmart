import reflex as rx
from app.states.medos_state import MedOSState, SAVINGS_CHART_DATA
from app.components.auth_modal import auth_modal
from app.components.cart_drawer import cart_drawer


def stat_card(value: str, label: str, accent: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(value, class_name=f"text-4xl font-bold text-{accent}-400 mb-1"),
            rx.el.p(
                label,
                class_name="text-gray-400 text-sm uppercase tracking-wider font-medium",
            ),
            class_name="flex flex-col items-center justify-center h-full",
        ),
        class_name=f"bg-gray-900 border border-gray-800 rounded-2xl p-6 shadow-lg shadow-{accent}-900/20",
    )


def pillar_card(
    title: str, description: str, icon_name: str, accent: str, stat: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon_name, class_name=f"h-6 w-6 text-{accent}-400"),
            class_name=f"bg-{accent}-500/10 p-3 rounded-full mb-4 w-fit",
        ),
        rx.el.h4(title, class_name="text-lg font-bold text-gray-100 mb-2"),
        rx.el.p(description, class_name="text-sm text-gray-400 mb-6 flex-1"),
        rx.el.div(
            rx.el.span(
                stat,
                class_name=f"text-xs font-bold text-{accent}-400 bg-{accent}-500/10 px-3 py-1 rounded-full uppercase tracking-wider",
            )
        ),
        class_name=f"flex flex-col bg-gray-900 border border-gray-800 rounded-2xl p-6 transition-all duration-300 hover:border-{accent}-500/50 hover:shadow-lg hover:shadow-{accent}-500/10",
    )


def features_tab() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            pillar_card(
                "Generic Intelligence Engine",
                "AI-powered salt matching across 15,000+ medicines. Identifies exact bioequivalent generics with regulatory verification.",
                "brain",
                "green",
                "15,000+ Medicines Indexed",
            ),
            pillar_card(
                "Adherence Engine",
                "Visual dosage tracking with smart reminders. Tap-to-log interface increases medication compliance by 3.1× over paper methods.",
                "heart-pulse",
                "cyan",
                "3.1× Compliance Lift",
            ),
            pillar_card(
                "Expiry Shield",
                "Proactive expiry monitoring with color-coded countdowns. Auto-triggers reorder alerts before medicines expire.",
                "shield-alert",
                "amber",
                "Zero Waste Target",
            ),
            pillar_card(
                "Emergency Access",
                "Real-time pharmacy stock tracking with 28-minute emergency delivery coordination across partner networks.",
                "siren",
                "red",
                "28-min Emergency ETA",
            ),
            pillar_card(
                "Drug Interaction Guard",
                "Cross-checks all active medications for dangerous interactions. Flags NSAID stacking, contraindicated combinations, and dosage conflicts.",
                "triangle-alert",
                "orange",
                "500+ Interaction Rules",
            ),
            pillar_card(
                "Community Intelligence",
                "Crowdsourced medicine availability reports from real patients. Real-time stock updates, price verification, and pharmacy ratings.",
                "users",
                "purple",
                "10,000+ Reports/Month",
            ),
            pillar_card(
                "AI Health Assistant",
                "Natural language interface for medicine queries. Understands brand names, salts, symptoms, and prescription terminology.",
                "bot",
                "blue",
                "24/7 Instant Answers",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 max-w-7xl mx-auto",
        ),
        class_name="py-12 px-4 sm:px-6 lg:px-8",
    )


def symptom_chip(symptom: str) -> rx.Component:
    is_selected = MedOSState.selected_symptoms.contains(symptom)
    return rx.el.button(
        rx.cond(
            is_selected,
            rx.icon("check", class_name="h-3 w-3 mr-1 inline-block"),
            rx.fragment(),
        ),
        symptom,
        on_click=lambda: MedOSState.toggle_symptom(symptom),
        class_name=rx.cond(
            is_selected,
            "flex items-center bg-green-500/20 border border-green-500 text-green-400 px-4 py-2 rounded-full text-sm font-bold transition-all shadow-[0_0_10px_rgba(74,222,128,0.2)]",
            "flex items-center bg-gray-800 border border-gray-700 text-gray-400 hover:border-gray-500 hover:text-gray-200 px-4 py-2 rounded-full text-sm font-bold transition-all",
        ),
    )


def medicine_recommendation_row(med: dict) -> rx.Component:
    savings_amt = med["brand_price"].to(int) - med["generic_price"].to(int)
    savings_pct = rx.cond(
        med["brand_price"].to(int) > 0,
        (savings_amt / med["brand_price"].to(int) * 100).to(int),
        0,
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    med["brand"],
                    class_name="line-through text-gray-500 text-sm font-medium",
                ),
                rx.icon("arrow-right", class_name="h-4 w-4 text-gray-600 mx-2"),
                rx.el.p(med["generic"], class_name="text-green-400 font-bold"),
                class_name="flex items-center flex-wrap",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        f"₹{med['brand_price']}",
                        class_name="line-through text-gray-500 text-xs font-medium text-right",
                    ),
                    rx.el.p(
                        f"₹{med['generic_price']}",
                        class_name="text-green-400 font-bold text-xl text-right",
                    ),
                    class_name="mr-4",
                ),
                rx.el.div(
                    rx.el.span(
                        f"Save ₹{savings_amt}",
                        class_name="block text-xs text-green-300 font-bold",
                    ),
                    rx.el.span(
                        f"{savings_pct}%",
                        class_name="block text-[10px] text-green-500/70 font-mono",
                    ),
                    class_name="bg-green-500/10 border border-green-500/20 rounded-lg px-2 py-1 text-right",
                ),
                class_name="flex items-center mt-2 md:mt-0",
            ),
            class_name="flex flex-col md:flex-row md:items-center justify-between",
        ),
        rx.cond(
            med["interaction"] != "",
            rx.el.div(
                rx.icon("triangle-alert", class_name="h-3 w-3 text-amber-400 mr-1.5"),
                rx.el.span(
                    med["interaction"], class_name="text-amber-400 text-xs font-medium"
                ),
                class_name="flex items-center mt-3 pt-3 border-t border-gray-800",
            ),
        ),
        class_name="bg-gray-900 border border-gray-800 p-4 rounded-xl mb-3 shadow-lg",
    )


def interaction_warning_card(warning: str) -> rx.Component:
    is_critical = warning.contains("CRITICAL")
    return rx.el.div(
        rx.icon(
            "triangle-alert",
            class_name=rx.cond(
                is_critical,
                "h-5 w-5 text-red-400 mr-3 flex-shrink-0",
                "h-5 w-5 text-amber-400 mr-3 flex-shrink-0",
            ),
        ),
        rx.el.p(
            warning,
            class_name=rx.cond(
                is_critical,
                "text-red-300 text-sm font-medium",
                "text-amber-300 text-sm font-medium",
            ),
        ),
        class_name=rx.cond(
            is_critical,
            "flex items-start bg-red-950/40 border border-red-500/50 p-4 rounded-xl mb-3 animate-pulse shadow-[0_0_15px_rgba(248,113,113,0.15)]",
            "flex items-start bg-amber-950/20 border border-amber-800/50 p-4 rounded-xl mb-3",
        ),
    )


def pill_button(pill: dict) -> rx.Component:
    status = pill["status"].to(str)
    return rx.el.button(
        rx.match(
            status,
            ("pending", rx.icon("circle", class_name="h-5 w-5 text-gray-500")),
            ("taken", rx.icon("check", class_name="h-5 w-5 text-green-400")),
            ("missed", rx.icon("x", class_name="h-5 w-5 text-red-400")),
            rx.icon("circle", class_name="h-5 w-5 text-gray-500"),
        ),
        on_click=lambda: MedOSState.toggle_pill(
            pill["day_idx"].to(int), pill["dose_idx"].to(int)
        ),
        class_name=rx.match(
            status,
            (
                "pending",
                "h-12 w-full flex items-center justify-center rounded-xl bg-gray-700 border border-gray-600 hover:bg-gray-600 transition-all duration-200",
            ),
            (
                "taken",
                "h-12 w-full flex items-center justify-center rounded-xl bg-green-500/20 border border-green-500 hover:bg-green-500/30 transition-all duration-200 shadow-[0_0_10px_rgba(74,222,128,0.1)]",
            ),
            (
                "missed",
                "h-12 w-full flex items-center justify-center rounded-xl bg-red-500/20 border border-red-500 hover:bg-red-500/30 transition-all duration-200",
            ),
            "h-12 w-full flex items-center justify-center rounded-xl bg-gray-700 border border-gray-600 hover:bg-gray-600 transition-all duration-200",
        ),
    )


def expiry_card(med: dict) -> rx.Component:
    status = med["status"].to(str)
    days_left = med["days_left"].to(int)
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(med["name"], class_name="text-gray-100 font-bold"),
                rx.el.p(med["expiry"], class_name="text-xs font-mono text-gray-500"),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.cond(
                    days_left < 0,
                    rx.el.p(
                        "EXPIRED",
                        class_name="text-red-500 font-black text-lg tracking-widest",
                    ),
                    rx.el.div(
                        rx.el.span(
                            med["days_left"],
                            class_name=rx.match(
                                status,
                                ("critical", "text-2xl font-black text-red-400"),
                                ("warning", "text-2xl font-black text-amber-400"),
                                "text-2xl font-black text-green-400",
                            ),
                        ),
                        rx.el.span(
                            " days left",
                            class_name="text-xs ml-1 text-gray-500 uppercase",
                        ),
                        class_name="flex items-baseline",
                    ),
                ),
                class_name="flex justify-end",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.match(
            status,
            (
                "critical",
                rx.el.button(
                    rx.icon("shopping-cart", class_name="h-4 w-4 mr-2"),
                    "REORDER NOW",
                    class_name="w-full flex items-center justify-center py-2 bg-red-500/20 text-red-400 border border-red-500/50 rounded-lg text-sm font-bold uppercase tracking-wider hover:bg-red-500/30 transition-colors",
                ),
            ),
            (
                "warning",
                rx.el.button(
                    rx.icon("shopping-cart", class_name="h-4 w-4 mr-2"),
                    "Reorder Soon",
                    class_name="w-full flex items-center justify-center py-2 bg-amber-500/20 text-amber-400 border border-amber-500/50 rounded-lg text-sm font-bold hover:bg-amber-500/30 transition-colors",
                ),
            ),
            rx.fragment(),
        ),
        class_name=rx.match(
            status,
            (
                "critical",
                "bg-red-950/30 border border-red-500/80 p-4 rounded-xl shadow-[0_0_15px_rgba(248,113,113,0.1)] relative overflow-hidden animate-pulse",
            ),
            ("warning", "bg-amber-950/20 border border-amber-800 p-4 rounded-xl"),
            "bg-green-950/10 border border-green-800/30 p-4 rounded-xl opacity-70",
        ),
    )


def pharmacy_card(pharmacy: dict) -> rx.Component:
    stock = pharmacy["stock"].to(str)
    return rx.el.div(
        rx.el.div(
            rx.el.h4(
                pharmacy["name"],
                class_name=rx.cond(
                    stock == "Out of Stock",
                    "text-gray-500 font-bold",
                    "text-gray-200 font-bold",
                ),
            ),
            rx.el.p(f"{pharmacy['distance']} away", class_name="text-xs text-gray-500"),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.span(
                pharmacy["stock"],
                class_name=rx.match(
                    stock,
                    (
                        "In Stock",
                        "bg-green-500/20 text-green-400 text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wider block text-center mb-1",
                    ),
                    (
                        "Low Stock",
                        "bg-amber-500/20 text-amber-400 text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wider block text-center mb-1",
                    ),
                    "bg-red-500/20 text-red-400 text-[10px] font-bold px-2 py-1 rounded-full uppercase tracking-wider block text-center mb-1",
                ),
            ),
            rx.el.div(
                rx.cond(
                    pharmacy["price"] != "",
                    rx.el.span(
                        pharmacy["price"],
                        class_name=rx.cond(
                            stock == "Out of Stock",
                            "text-gray-600 font-mono text-sm mr-2",
                            "text-gray-300 font-mono text-sm mr-2",
                        ),
                    ),
                ),
                rx.cond(
                    pharmacy["eta"] != "—",
                    rx.el.span(
                        pharmacy["eta"], class_name="text-cyan-400 text-xs font-bold"
                    ),
                ),
                class_name="flex items-center justify-end",
            ),
            class_name="text-right",
        ),
        class_name=rx.cond(
            stock == "Out of Stock",
            "flex items-center p-4 bg-gray-900/50 border border-gray-800 rounded-xl opacity-60",
            "flex items-center p-4 bg-gray-900 border border-gray-700 rounded-xl hover:border-gray-600 transition-colors",
        ),
    )


def html_legend(items: list[tuple[str, str]]) -> rx.Component:
    return rx.el.div(
        rx.foreach(
            items,
            lambda item: rx.el.div(
                rx.el.div(class_name=f"w-3 h-3 rounded-full {item[1]} mr-2"),
                rx.el.span(item[0], class_name="text-xs text-gray-400"),
                class_name="flex items-center",
            ),
        ),
        class_name="flex justify-center gap-6 mt-4",
    )


def demo_tab() -> rx.Component:
    symptoms = ["Headache", "Fever", "Acidity", "Allergy", "Joint Pain", "Diabetes"]
    adherence_trend = [
        {"week": "W1", "adherence": 45, "target": 80},
        {"week": "W2", "adherence": 62, "target": 80},
        {"week": "W3", "adherence": 71, "target": 80},
        {"week": "W4", "adherence": 78, "target": 80},
        {"week": "W5", "adherence": 85, "target": 80},
        {"week": "W6", "adherence": 82, "target": 80},
        {"week": "W7", "adherence": 91, "target": 80},
    ]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "SYMPTOM INTELLIGENCE",
                    class_name="text-xs font-mono uppercase tracking-widest text-green-400 mb-1",
                ),
                rx.el.p(
                    "Select active patient symptoms for real-time generic substitution mapping.",
                    class_name="text-sm text-gray-500 mb-6",
                ),
                rx.el.div(
                    rx.foreach(symptoms, symptom_chip),
                    class_name="flex flex-wrap gap-3 mb-8",
                ),
                rx.cond(
                    MedOSState.selected_symptoms.length() > 0,
                    rx.el.div(
                        rx.el.p(
                            "RECOMMENDED ALTERNATIVES",
                            class_name="text-xs font-mono uppercase tracking-widest text-gray-500 mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(
                                MedOSState.recommended_medicines,
                                medicine_recommendation_row,
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                        ),
                        class_name="mt-8",
                    ),
                ),
                rx.cond(
                    MedOSState.interaction_warnings.length() > 0,
                    rx.el.div(
                        rx.el.p(
                            "⚠ DRUG INTERACTION ALERTS",
                            class_name="text-xs font-mono uppercase tracking-widest text-red-400 mb-4 mt-8",
                        ),
                        rx.el.div(
                            rx.foreach(
                                MedOSState.interaction_warnings,
                                interaction_warning_card,
                            ),
                            class_name="flex flex-col gap-2",
                        ),
                    ),
                ),
                class_name="py-10 border-b border-gray-800",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "SAVINGS INTELLIGENCE",
                        class_name="text-xs font-mono uppercase tracking-widest text-green-400 mb-1",
                    ),
                    rx.el.p(
                        "12-month branded vs generic spending analysis.",
                        class_name="text-sm text-gray-500 mb-6",
                    ),
                    rx.recharts.area_chart(
                        rx.recharts.cartesian_grid(
                            stroke_dasharray="3 3", stroke="#374151"
                        ),
                        rx.recharts.graphing_tooltip(
                            content_style={
                                "backgroundColor": "#1f2937",
                                "border": "1px solid #374151",
                                "borderRadius": "12px",
                                "color": "#f3f4f6",
                            },
                            label_style={"color": "#9ca3af"},
                            separator="",
                        ),
                        rx.recharts.area(
                            data_key="branded",
                            stroke="#ef4444",
                            fill="url(#brandedGradient)",
                            type_="monotone",
                            name="Branded Cost",
                        ),
                        rx.recharts.area(
                            data_key="generic",
                            stroke="#22c55e",
                            fill="url(#genericGradient)",
                            type_="monotone",
                            name="Generic Cost",
                        ),
                        rx.recharts.x_axis(
                            data_key="month",
                            stroke="#6b7280",
                            tick_line=False,
                            axis_line=False,
                        ),
                        rx.recharts.y_axis(
                            stroke="#6b7280", tick_line=False, axis_line=False
                        ),
                        rx.el.defs(
                            rx.el.svg.linear_gradient(
                                rx.el.stop(
                                    offset="5%", stop_color="#ef4444", stop_opacity=0.3
                                ),
                                rx.el.stop(
                                    offset="95%", stop_color="#ef4444", stop_opacity=0.0
                                ),
                                id="brandedGradient",
                                x1="0",
                                y1="0",
                                x2="0",
                                y2="1",
                            ),
                            rx.el.svg.linear_gradient(
                                rx.el.stop(
                                    offset="5%", stop_color="#22c55e", stop_opacity=0.4
                                ),
                                rx.el.stop(
                                    offset="95%", stop_color="#22c55e", stop_opacity=0.0
                                ),
                                id="genericGradient",
                                x1="0",
                                y1="0",
                                x2="0",
                                y2="1",
                            ),
                        ),
                        data=SAVINGS_CHART_DATA,
                        height=300,
                        width="100%",
                    ),
                    html_legend(
                        [
                            ("Branded Cost", "bg-red-500"),
                            ("Generic Cost", "bg-green-500"),
                        ]
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Total Branded:",
                                class_name="text-xs text-gray-500 uppercase tracking-widest",
                            ),
                            rx.el.p(
                                "₹30,000/yr",
                                class_name="text-lg font-bold text-red-400",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Total Generic:",
                                class_name="text-xs text-gray-500 uppercase tracking-widest",
                            ),
                            rx.el.p(
                                "₹6,000/yr",
                                class_name="text-lg font-bold text-green-400",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Annual Savings:",
                                class_name="text-xs text-green-500/70 uppercase tracking-widest",
                            ),
                            rx.el.p(
                                "₹24,000",
                                class_name="text-2xl font-black text-green-400 drop-shadow-[0_0_8px_rgba(74,222,128,0.5)]",
                            ),
                        ),
                        class_name="flex flex-col sm:flex-row items-center justify-between mt-6 pt-6 border-t border-gray-800 gap-4 text-center sm:text-left",
                    ),
                    class_name="bg-gray-900/50 border border-gray-800 rounded-2xl p-6",
                ),
                class_name="py-10 border-b border-gray-800",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "ADHERENCE ENGINE",
                            class_name="text-xs font-mono uppercase tracking-widest text-cyan-400 mb-1",
                        ),
                        rx.el.p(
                            "Interactive compliance tracking with automated refill triggers.",
                            class_name="text-sm text-gray-500",
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.div(
                        rx.el.p(
                            rx.el.span(
                                MedOSState.adherence_percent,
                                class_name="text-4xl font-black text-cyan-400",
                            ),
                            rx.el.span(
                                "%", class_name="text-xl font-bold text-cyan-400/50"
                            ),
                            class_name="text-right leading-none",
                        ),
                        rx.el.p(
                            f"{MedOSState.total_taken} taken · {MedOSState.total_missed} missed",
                            class_name="text-xs text-gray-500 mt-1 font-mono",
                        ),
                        class_name="text-right mt-4 md:mt-0",
                    ),
                    class_name="flex flex-col md:flex-row md:items-center justify-between mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(class_name="w-12 shrink-0"),
                        rx.foreach(
                            MedOSState.dosage_days,
                            lambda day: rx.el.div(
                                day,
                                class_name="text-center text-xs font-mono text-gray-500 w-full min-w-[3rem]",
                            ),
                        ),
                        class_name="flex gap-2 mb-3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            "☀",
                            class_name="flex items-center justify-center h-12 w-12 text-xl shrink-0",
                        ),
                        rx.foreach(
                            MedOSState.morning_pills,
                            lambda pill: rx.el.div(
                                pill_button(pill), class_name="w-full min-w-[3rem]"
                            ),
                        ),
                        class_name="flex gap-2 mb-3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            "🌤",
                            class_name="flex items-center justify-center h-12 w-12 text-xl shrink-0",
                        ),
                        rx.foreach(
                            MedOSState.afternoon_pills,
                            lambda pill: rx.el.div(
                                pill_button(pill), class_name="w-full min-w-[3rem]"
                            ),
                        ),
                        class_name="flex gap-2 mb-3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            "🌙",
                            class_name="flex items-center justify-center h-12 w-12 text-xl shrink-0",
                        ),
                        rx.foreach(
                            MedOSState.night_pills,
                            lambda pill: rx.el.div(
                                pill_button(pill), class_name="w-full min-w-[3rem]"
                            ),
                        ),
                        class_name="flex gap-2 mb-6",
                    ),
                    class_name="bg-gray-900/50 border border-gray-800 rounded-2xl p-6 overflow-x-auto",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="h-full bg-cyan-400 rounded-full transition-all duration-500",
                        style={"width": f"{MedOSState.adherence_percent}%"},
                    ),
                    class_name="h-2 w-full bg-gray-800 rounded-full overflow-hidden mt-6 mb-8 shadow-inner",
                ),
                rx.el.div(
                    rx.el.p(
                        "ADHERENCE TREND",
                        class_name="text-xs font-mono uppercase tracking-widest text-cyan-400 mb-6",
                    ),
                    rx.recharts.area_chart(
                        rx.recharts.cartesian_grid(
                            stroke_dasharray="3 3", stroke="#374151"
                        ),
                        rx.recharts.graphing_tooltip(
                            content_style={
                                "backgroundColor": "#1f2937",
                                "border": "1px solid #374151",
                                "borderRadius": "12px",
                                "color": "#f3f4f6",
                            },
                            separator="",
                        ),
                        rx.recharts.area(
                            data_key="adherence",
                            stroke="#06b6d4",
                            fill="url(#adherenceGradient)",
                            type_="monotone",
                            name="Adherence %",
                        ),
                        rx.recharts.reference_line(
                            y=80,
                            stroke="#f59e0b",
                            stroke_dasharray="5 5",
                            label="Target (80%)",
                        ),
                        rx.recharts.x_axis(
                            data_key="week",
                            stroke="#6b7280",
                            tick_line=False,
                            axis_line=False,
                        ),
                        rx.recharts.y_axis(
                            stroke="#6b7280",
                            tick_line=False,
                            axis_line=False,
                            domain=[0, 100],
                        ),
                        rx.el.defs(
                            rx.el.svg.linear_gradient(
                                rx.el.stop(
                                    offset="5%", stop_color="#06b6d4", stop_opacity=0.3
                                ),
                                rx.el.stop(
                                    offset="95%", stop_color="#06b6d4", stop_opacity=0.0
                                ),
                                id="adherenceGradient",
                                x1="0",
                                y1="0",
                                x2="0",
                                y2="1",
                            )
                        ),
                        data=adherence_trend,
                        height=200,
                        width="100%",
                    ),
                    html_legend(
                        [("Adherence %", "bg-cyan-500"), ("Target", "bg-amber-500")]
                    ),
                    class_name="bg-gray-900/50 border border-gray-800 rounded-2xl p-6",
                ),
                class_name="py-10 border-b border-gray-800",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "EXPIRY SHIELD",
                        class_name="text-xs font-mono uppercase tracking-widest text-amber-400 mb-1",
                    ),
                    rx.el.p(
                        "Predictive stock degradation monitoring.",
                        class_name="text-sm text-gray-500 mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(MedOSState.expiry_medicines, expiry_card),
                        class_name="grid grid-cols-1 gap-4",
                    ),
                    class_name="flex-1",
                ),
                rx.el.div(
                    rx.el.p(
                        "EMERGENCY ACCESS",
                        class_name="text-xs font-mono uppercase tracking-widest text-red-400 mb-1",
                    ),
                    rx.el.p(
                        "Real-time local inventory telemetry.",
                        class_name="text-sm text-gray-500 mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(MedOSState.nearby_pharmacies, pharmacy_card),
                        class_name="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            class_name="absolute inset-0 bg-red-600 blur-xl opacity-30 rounded-full animate-pulse"
                        ),
                        rx.el.button(
                            "⚡ EMERGENCY — Get Medicines in 30 min",
                            on_click=rx.redirect("/locator"),
                            class_name="relative w-full py-5 bg-red-600 hover:bg-red-500 text-white font-bold text-lg rounded-2xl shadow-[0_0_20px_rgba(220,38,38,0.4)] transition-all",
                        ),
                        class_name="relative mt-4",
                    ),
                    class_name="flex-1",
                ),
                class_name="grid grid-cols-1 lg:grid-cols-2 gap-12 py-10",
            ),
            class_name="max-w-7xl mx-auto",
        ),
        class_name="py-6 px-4 sm:px-6 lg:px-8",
    )


def medos_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    "← Back to MediSmart",
                    href="/",
                    class_name="text-gray-400 hover:text-gray-200 text-sm font-medium transition-colors absolute left-4 top-4 md:left-8 md:top-8",
                ),
                rx.el.div(
                    rx.el.span(
                        "MedOS",
                        class_name="font-mono text-green-400 font-bold tracking-widest absolute right-4 top-4 md:right-8 md:top-8",
                    )
                ),
                rx.el.div(
                    rx.el.h1(
                        "MedOS",
                        class_name="text-6xl md:text-8xl font-black bg-clip-text text-transparent bg-gradient-to-r from-green-400 to-cyan-400 mb-4",
                    ),
                    rx.el.p(
                        "Pharmaceutical Intelligence Operating System",
                        class_name="text-gray-400 uppercase tracking-widest text-sm md:text-base font-bold mb-6",
                    ),
                    rx.el.p(
                        "Advanced command center for automated healthcare savings, adherence tracking, and safety monitoring.",
                        class_name="text-gray-500 max-w-xl mx-auto",
                    ),
                    class_name="text-center pt-24 pb-16 px-4",
                ),
            ),
            class_name="bg-gradient-to-b from-gray-950 to-gray-900 border-b border-gray-800 relative",
        ),
        rx.el.div(
            rx.el.div(
                stat_card("62%", "Average Savings", "green"),
                stat_card("28 min", "Emergency Delivery", "cyan"),
                stat_card("3.1×", "Adherence Lift", "amber"),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto -mt-10 px-4 relative z-10",
            )
        ),
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    "FEATURES",
                    on_click=lambda: MedOSState.set_active_tab("features"),
                    class_name=rx.cond(
                        MedOSState.active_tab == "features",
                        "font-mono text-green-400 font-bold border-b-2 border-green-400 px-8 py-4 bg-gray-800/80 uppercase tracking-widest",
                        "font-mono text-gray-500 hover:text-gray-300 font-bold border-b-2 border-transparent px-8 py-4 uppercase tracking-widest transition-colors",
                    ),
                ),
                rx.el.button(
                    "LIVE DEMO",
                    on_click=lambda: MedOSState.set_active_tab("demo"),
                    class_name=rx.cond(
                        MedOSState.active_tab == "demo",
                        "font-mono text-green-400 font-bold border-b-2 border-green-400 px-8 py-4 bg-gray-800/80 uppercase tracking-widest",
                        "font-mono text-gray-500 hover:text-gray-300 font-bold border-b-2 border-transparent px-8 py-4 uppercase tracking-widest transition-colors",
                    ),
                ),
                class_name="flex justify-center border-b border-gray-800 mt-12 bg-gray-950",
            )
        ),
        rx.cond(MedOSState.active_tab == "features", features_tab(), demo_tab()),
        auth_modal(),
        cart_drawer(),
        class_name="bg-gray-950 min-h-screen text-gray-100 font-sans",
    )