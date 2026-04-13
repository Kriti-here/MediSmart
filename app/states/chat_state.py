import reflex as rx
import asyncio
from typing import TypedDict
from app.states.medicine_state import MedicineState

SYMPTOM_MEDICINE_MAP = {
    "headache": [
        {
            "brand": "Crocin 500mg",
            "generic": "Paracetamol 500mg",
            "price_brand": 40,
            "price_generic": 8,
            "dosage": "1-2 tablets every 4-6 hours, max 8/day",
            "note": "First-line treatment. Safe for most patients.",
        },
        {
            "brand": "Combiflam",
            "generic": "Ibuprofen+Paracetamol",
            "price_brand": 45,
            "price_generic": 12,
            "dosage": "1 tablet after meals, max 3/day",
            "note": "Better for pain with inflammation. Avoid on empty stomach.",
        },
    ],
    "fever": [
        {
            "brand": "Dolo 650",
            "generic": "Paracetamol 650mg",
            "price_brand": 30,
            "price_generic": 10,
            "dosage": "1 tablet every 6-8 hours, max 4/day",
            "note": "Higher dose for moderate to high fever.",
        },
        {
            "brand": "Crocin 500mg",
            "generic": "Paracetamol 500mg",
            "price_brand": 40,
            "price_generic": 8,
            "dosage": "1-2 tablets every 4-6 hours",
            "note": "Standard dose for mild fever.",
        },
    ],
    "acidity": [
        {
            "brand": "Pan 40",
            "generic": "Pantoprazole 40mg",
            "price_brand": 150,
            "price_generic": 18,
            "dosage": "1 tablet 30 min before breakfast",
            "note": "PPI — best taken on empty stomach.",
        }
    ],
    "allergy": [
        {
            "brand": "Allegra 120mg",
            "generic": "Fexofenadine 120mg",
            "price_brand": 180,
            "price_generic": 30,
            "dosage": "1 tablet daily",
            "note": "Non-drowsy. Avoid fruit juices (reduces absorption).",
        }
    ],
    "joint pain": [
        {
            "brand": "Voveran SR 100",
            "generic": "Diclofenac SR 100mg",
            "price_brand": 95,
            "price_generic": 14,
            "dosage": "1 tablet after meals, max 2/day",
            "note": "Do NOT crush SR tablets. Take with food.",
        },
        {
            "brand": "Combiflam",
            "generic": "Ibuprofen+Paracetamol",
            "price_brand": 45,
            "price_generic": 12,
            "dosage": "1 tablet after meals",
            "note": "Lighter option for mild joint pain.",
        },
    ],
    "diabetes": [
        {
            "brand": "Glycomet 500",
            "generic": "Metformin 500mg",
            "price_brand": 60,
            "price_generic": 10,
            "dosage": "1 tablet twice daily with meals",
            "note": "First-line for Type 2 diabetes. Monitor B12 long-term.",
        }
    ],
    "cold": [
        {
            "brand": "Crocin 500mg",
            "generic": "Paracetamol 500mg",
            "price_brand": 40,
            "price_generic": 8,
            "dosage": "1-2 tablets every 4-6 hours",
            "note": "For body ache and mild fever from cold.",
        },
        {
            "brand": "Allegra 120mg",
            "generic": "Fexofenadine 120mg",
            "price_brand": 180,
            "price_generic": 30,
            "dosage": "1 tablet daily",
            "note": "For runny nose and sneezing.",
        },
    ],
    "stomach pain": [
        {
            "brand": "Pan 40",
            "generic": "Pantoprazole 40mg",
            "price_brand": 150,
            "price_generic": 18,
            "dosage": "1 tablet before breakfast",
            "note": "If acid-related. Consult doctor if persistent.",
        }
    ],
    "high blood pressure": [
        {
            "brand": "Telma 40",
            "generic": "Telmisartan 40mg",
            "price_brand": 110,
            "price_generic": 15,
            "dosage": "1 tablet daily",
            "note": "Do not use during pregnancy. Monitor BP regularly.",
        }
    ],
    "cholesterol": [
        {
            "brand": "Atorva 10",
            "generic": "Atorvastatin 10mg",
            "price_brand": 85,
            "price_generic": 12,
            "dosage": "1 tablet at bedtime",
            "note": "Report unexplained muscle pain. Avoid grapefruit.",
        }
    ],
    "thyroid": [
        {
            "brand": "Thyronorm 50",
            "generic": "Levothyroxine 50mcg",
            "price_brand": 140,
            "price_generic": 15,
            "dosage": "1 tablet empty stomach in morning, 30min before food",
            "note": "⚠️ Narrow Therapeutic Index — do NOT switch brands without doctor approval.",
        }
    ],
}
DRUG_INTERACTIONS = [
    {
        "drugs": ["ibuprofen", "diclofenac", "combiflam", "voveran", "nsaid"],
        "warning": "⚠️ CRITICAL: Do NOT combine multiple NSAIDs (Ibuprofen, Diclofenac, Combiflam, Voveran). Risk of stomach bleeding and kidney damage.",
    },
    {
        "drugs": ["ibuprofen", "aspirin", "blood thinner", "warfarin"],
        "warning": "⚠️ CRITICAL: NSAIDs + Blood thinners increase bleeding risk significantly. Consult doctor immediately.",
    },
    {
        "drugs": ["paracetamol", "crocin", "dolo", "calpol"],
        "warning": "⚠️ WARNING: Do not combine multiple paracetamol products (Crocin + Dolo + Calpol all contain Paracetamol). Max 4g/day to avoid liver damage.",
    },
    {
        "drugs": ["metformin", "alcohol"],
        "warning": "⚠️ WARNING: Metformin + Alcohol increases risk of lactic acidosis. Avoid alcohol with diabetes medication.",
    },
    {
        "drugs": ["pantoprazole", "clopidogrel"],
        "warning": "⚠️ WARNING: Pantoprazole may reduce the effectiveness of Clopidogrel (blood thinner). Use Ranitidine instead if needed.",
    },
    {
        "drugs": ["fexofenadine", "fruit juice", "grapefruit"],
        "warning": "ℹ️ NOTE: Fruit juices (especially grapefruit) reduce Fexofenadine absorption by up to 36%. Take with water only.",
    },
    {
        "drugs": ["levothyroxine", "thyronorm", "calcium", "iron"],
        "warning": "⚠️ WARNING: Take Levothyroxine at least 4 hours apart from Calcium or Iron supplements — they block absorption.",
    },
    {
        "drugs": ["atorvastatin", "grapefruit"],
        "warning": "⚠️ WARNING: Grapefruit increases Atorvastatin levels in blood, raising risk of muscle damage. Avoid large amounts.",
    },
]
SIDE_EFFECTS_DB = {
    "paracetamol": {
        "common": "Nausea, rash (rare)",
        "serious": "Liver damage with overdose (>4g/day)",
        "avoid": "Alcohol, other paracetamol products",
    },
    "ibuprofen": {
        "common": "Stomach pain, nausea, dizziness",
        "serious": "Stomach ulcers, kidney problems with long-term use",
        "avoid": "Empty stomach, other NSAIDs, blood thinners",
    },
    "pantoprazole": {
        "common": "Headache, diarrhea, flatulence",
        "serious": "B12/Magnesium deficiency with prolonged use",
        "avoid": "Taking after meals (take 30min before food)",
    },
    "fexofenadine": {
        "common": "Headache, nausea (rare)",
        "serious": "Very safe profile — rarely causes drowsiness",
        "avoid": "Fruit juices (reduces absorption)",
    },
    "metformin": {
        "common": "Nausea, diarrhea, metallic taste",
        "serious": "Lactic acidosis (very rare), B12 deficiency",
        "avoid": "Alcohol, skipping meals",
    },
    "diclofenac": {
        "common": "Stomach pain, nausea, headache",
        "serious": "GI bleeding, cardiovascular risk with long-term use",
        "avoid": "Empty stomach, other NSAIDs, blood thinners",
    },
    "telmisartan": {
        "common": "Dizziness, back pain",
        "serious": "Hyperkalemia (high potassium)",
        "avoid": "Pregnancy, potassium supplements",
    },
    "atorvastatin": {
        "common": "Muscle aches, headache",
        "serious": "Rhabdomyolysis (severe muscle breakdown — rare)",
        "avoid": "Grapefruit, heavy alcohol",
    },
    "levothyroxine": {
        "common": "Hair loss initially, weight changes",
        "serious": "Heart palpitations if dose too high",
        "avoid": "Calcium, iron, soy within 4 hours",
    },
    "azithromycin": {
        "common": "Nausea, diarrhea, stomach pain",
        "serious": "QT prolongation (heart rhythm — rare)",
        "avoid": "Antacids within 2 hours",
    },
    "cefixime": {
        "common": "Diarrhea, nausea",
        "serious": "Severe allergic reaction (rare)",
        "avoid": "Stopping course early",
    },
    "amoxicillin": {
        "common": "Diarrhea, rash, nausea",
        "serious": "Severe allergic reaction, C. diff colitis",
        "avoid": "Stopping course early, allergy to penicillin",
    },
}


class ChatMessage(TypedDict):
    role: str
    content: str


class ChatState(rx.State):
    messages: list[ChatMessage] = [
        {
            "role": "bot",
            "content": "👋 Hi there! I'm your MediSmart Assistant. I can help you understand generic medicines, prescription terms, or find affordable alternatives. What would you like to know?",
        }
    ]
    is_chat_open: bool = False
    current_message: str = ""
    is_typing: bool = False
    suggested_questions: list[str] = [
        "I have headache and fever",
        "Side effects of Paracetamol?",
        "Can I take Combiflam with Voveran?",
        "Best medicine for acidity",
        "Dosage for Pan 40",
        "I have joint pain and diabetes",
        "Analyze Crocin 500mg",
        "What are generic medicines?",
    ]

    @rx.event
    def toggle_chat(self):
        self.is_chat_open = not self.is_chat_open
        if self.is_chat_open:
            yield rx.call_script(
                "setTimeout(() => { const el = document.getElementById('chat-messages'); if(el) el.scrollTop = el.scrollHeight; }, 100);"
            )

    @rx.event
    def set_current_message(self, message: str):
        self.current_message = message

    async def _generate_response(self, user_text: str) -> str:
        """Helper to generate a response based on user input."""
        await asyncio.sleep(0.8)
        lower_text = user_text.lower()
        response = ""
        is_substitution_query = any(
            (
                w in lower_text
                for w in [
                    "unavailable",
                    "not available",
                    "out of stock",
                    "alternative for",
                    "substitute for",
                    "replacement for",
                    "instead of",
                ]
            )
        )
        if is_substitution_query:
            from app.states.medicine_state import MEDICINE_DATABASE

            found_med_key = None
            for key, data in MEDICINE_DATABASE.items():
                if data["brand_name"].lower() in lower_text or key in lower_text:
                    found_med_key = key
                    break
            if found_med_key:
                med = MEDICINE_DATABASE[found_med_key]
                best_alt = min(med["alternatives"], key=lambda x: x["price"])
                jan_aushadhi = [
                    a for a in med["alternatives"] if "Jan Aushadhi" in a["type"]
                ]
                response = f"🔄 Smart Substitution: {med['brand_name']} Unavailable?\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n✅ BEST ALTERNATIVE: {best_alt['name']}\n• Type: {best_alt['type']}\n• Salt Match: {best_alt['salt_match']}\n• Price: ₹{best_alt['price']} (Save ₹{med['price_original'] - best_alt['price']})\n• Regulatory: {best_alt['regulatory_badge']}\n\n🚦 Substitution Safety: {med['substitution_safety']}\n{med['substitution_note']}\n"
                if jan_aushadhi:
                    ja = jan_aushadhi[0]
                    response += f"\n🏥 JAN AUSHADHI OPTION: {ja['name']}\n• Price: ₹{ja['price']} (Cheapest verified option)\n• Available at 9,000+ Jan Aushadhi Kendras across India\n"
                response += f"\n📍 Find nearby: Use our Pharmacy Locator → /locator\n🛒 Buy generic online → /shop\n\n⚠️ Always confirm substitutions with your doctor or pharmacist."
                return response
        found_symptoms = []
        for symptom in SYMPTOM_MEDICINE_MAP.keys():
            if symptom in lower_text:
                found_symptoms.append(symptom)
        if found_symptoms:
            response_lines = [
                f"🩺 Symptom Analysis: {' + '.join((s.title() for s in found_symptoms))}"
            ]
            response_lines.append("""━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
            response_lines.append("""Based on your symptoms, here are recommended medicines:
""")
            suggested_meds = []
            for symptom in found_symptoms:
                response_lines.append(f"💊 For {symptom.title()}:")
                for med in SYMPTOM_MEDICINE_MAP[symptom]:
                    savings_pct = (
                        int(
                            (med["price_brand"] - med["price_generic"])
                            / med["price_brand"]
                            * 100
                        )
                        if med["price_brand"]
                        else 0
                    )
                    response_lines.append(f"┌─────────────────────────────────────┐")
                    response_lines.append(
                        f"│ Brand: {med['brand']} → Generic: {med['generic']}"
                    )
                    response_lines.append(
                        f"│ 💰 ₹{med['price_brand']} → ₹{med['price_generic']} (Save {savings_pct}%)"
                    )
                    response_lines.append(f"│ 📋 Dosage: {med['dosage']}")
                    response_lines.append(f"│ ℹ️ {med['note']}")
                    response_lines.append(f"└─────────────────────────────────────┘")
                    suggested_meds.append(med["generic"].split()[0].lower())
                    suggested_meds.append(med["brand"].split()[0].lower())
            warnings = []
            for interaction in DRUG_INTERACTIONS:
                matched_drugs = [
                    d
                    for d in interaction["drugs"]
                    if any((d in sm for sm in suggested_meds))
                ]
                if len(matched_drugs) >= 2:
                    warnings.append(interaction["warning"])
            if warnings:
                warnings = list(dict.fromkeys(warnings))
                response_lines.append("""
⚠️ DRUG INTERACTION ALERTS:""")
                for w in warnings:
                    response_lines.append(f"• {w}")
            response_lines.append("""
🏥 Find these at your nearest pharmacy → /locator""")
            response_lines.append("🛒 Buy online from our shop → /shop")
            response_lines.append("""
⚠️ Always consult a doctor before starting any medication.""")
            return """
""".join(response_lines)
        is_interaction_query = any(
            (
                w in lower_text
                for w in ["interaction", "combine", "mix", "together", "with"]
            )
        )
        if is_interaction_query:
            warnings = []
            for interaction in DRUG_INTERACTIONS:
                matched = [d for d in interaction["drugs"] if d in lower_text]
                if len(matched) >= 1:
                    warnings.append(interaction["warning"])
            if warnings:
                warnings = list(dict.fromkeys(warnings))
                return (
                    """⚠️ DRUG INTERACTION ALERTS:
"""
                    + """
""".join((f"• {w}" for w in warnings))
                    + """

⚠️ Always consult a doctor before starting any medication."""
                )
        is_side_effect_query = any(
            (w in lower_text for w in ["side effect", "reaction", "adverse", "risk"])
        )
        if is_side_effect_query:
            for drug, info in SIDE_EFFECTS_DB.items():
                if drug in lower_text:
                    return f"📋 Side Effects Profile: {drug.title()}\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n🔹 Common: {info['common']}\n🔸 Serious: {info['serious']}\n⛔ Avoid: {info['avoid']}\n\n⚠️ Always consult a doctor before starting any medication."
            for symptoms, meds in SYMPTOM_MEDICINE_MAP.items():
                for med in meds:
                    brand_lower = med["brand"].lower()
                    if brand_lower.split()[0] in lower_text:
                        generic_key = med["generic"].split()[0].lower()
                        if generic_key in SIDE_EFFECTS_DB:
                            info = SIDE_EFFECTS_DB[generic_key]
                            return f"📋 Side Effects Profile: {med['brand']} ({generic_key.title()})\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n🔹 Common: {info['common']}\n🔸 Serious: {info['serious']}\n⛔ Avoid: {info['avoid']}\n\n⚠️ Always consult a doctor before starting any medication."
        is_dosage_query = any(
            (
                w in lower_text
                for w in ["dose", "dosage", "how much", "how many", "how to take"]
            )
        )
        if is_dosage_query:
            for symptoms, meds in SYMPTOM_MEDICINE_MAP.items():
                for med in meds:
                    brand_lower = med["brand"].lower()
                    generic_lower = med["generic"].lower()
                    if (
                        brand_lower.split()[0] in lower_text
                        or generic_lower.split()[0] in lower_text
                    ):
                        return f"📋 Dosage Information: {med['brand']}\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n💊 Recommended Dosage: {med['dosage']}\nℹ️ Note: {med['note']}\n\n⚠️ Always consult a doctor before starting any medication."
        from app.states.medicine_state import MEDICINE_DATABASE

        found_med_key = None
        for key, data in MEDICINE_DATABASE.items():
            if data["brand_name"].lower() in lower_text or key in lower_text:
                found_med_key = key
                break
        if found_med_key:
            med = MEDICINE_DATABASE[found_med_key]
            alt_lines = []
            for i, alt in enumerate(med["alternatives"], 1):
                savings_val = med["price_original"] - alt["price"]
                alt_lines.append(
                    f"│ {i} │ {alt['name'][:15].ljust(15)} │ {alt['type'][:14].ljust(14)} │ ₹{str(alt['price'])[:5].ljust(5)} │ ₹{str(savings_val)[:5].ljust(5)} │"
                )
            alts_table = """
""".join(alt_lines)
            best_value = min(med["alternatives"], key=lambda x: x["price"])
            savings = med["price_original"] - med["price_cheapest_safe"]
            pct = (
                round(savings / med["price_original"] * 100)
                if med["price_original"]
                else 0
            )
            savings_warning = (
                f"\n   ⚠️ A verified equivalent exists at {pct}% lower cost!"
                if pct > 50
                else ""
            )
            response = f"🔬 MediCompare AI Analysis: {med['brand_name']}\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n📋 STEP 1 — MEDICINE IDENTIFICATION\n• Brand: {med['brand_name']}\n• Active Ingredient: {med['active_ingredients']}\n• Form: {med['dosage_form']} | Category: {med['therapeutic_category']}\n• How it works: {med['mechanism']}\n• Standard use: {med['standard_use']}\n\n✅ STEP 2 — REGULATORY VERIFICATION\n• CDSCO Approved: {('✅ Yes' if med['cdsco_approved'] else '❌ No')}\n• NLEM Listed: {('✅' if med['nlem_listed'] else '❌')}\n• Jan Aushadhi: {med['jan_aushadhi_available']}\n• Manufacturing: {med['manufacturing_tier']}\n• ⚠️ Warnings: {med['regulatory_warnings']}\n• Safety Score: {med['safety_score']}/100\n\n💊 STEP 3 — GENERIC ALTERNATIVES\n┌────────────────────────────────────────────────────────┐\n│ # │ Name            │ Type           │ Price   │ Savings │\n{alts_table}\n│ ⭐ Best Value: {best_value['name']} \n└────────────────────────────────────────────────────────┘\n\n💰 STEP 4 — PRICE INTELLIGENCE\n• Original Price: ₹{med['price_original']}/strip\n• Cheapest Safe Generic: ₹{med['price_cheapest_safe']}/strip\n• You Save: ₹{savings} per strip ({pct}%)\n• Annual Savings: ₹{med['annual_savings_estimate']} (for regular use)\n• {med['affordability_tier']}{savings_warning}\n\n🏥 STEP 5 — PHARMACY AVAILABILITY\nSearch for nearby pharmacies stocking this generic on our Pharmacy Locator page → /locator\n\n🚦 STEP 6 — SUBSTITUTION SAFETY\n{med['substitution_safety']}\n{med['substitution_note']}\n\n📝 STEP 7 — PATIENT SUMMARY\n━━━━━━━━━━━━━━━━━━━━━━━━━━━\n💊 {med['therapeutic_category']} medication for {med['standard_use'].split('.')[0].lower()}.\n💰 Cheapest safe alternative: {best_value['name']} at ₹{best_value['price']} (save ₹{savings})\n🏥 Find it at your nearest Jan Aushadhi Kendra or pharmacy\n⚠️ {med['regulatory_warnings'].split('.')[0]}\n🔔 Always confirm substitutions with your doctor or pharmacist before switching."
            return response
        if "generic" in lower_text and (
            "what" in lower_text or "brand" in lower_text or "difference" in lower_text
        ):
            response = "Generics contain the exact same active ingredient (API/salt), same dosage, and same route of administration as brand-name drugs. They differ only in brand name, packaging, and price. For example, Crocin and generic Paracetamol both contain 500mg of Paracetamol, but have very different prices! 💊"
        elif any(
            (
                w in lower_text
                for w in ["save", "cost", "price", "cheap", "expensive", "savings"]
            )
        ):
            response = "💰 You can typically save 30% to 80% by switching to generic medicines! Jan Aushadhi Kendras offer medicines at 50-90% less than market rates. Fun fact: India's pharmaceutical industry is the world's largest generic supplier!"
        elif any(
            (
                w in lower_text
                for w in ["safe", "quality", "cdsco", "fda", "who", "trust"]
            )
        ):
            response = "✅ Yes, generic medicines are equally safe and effective! They are strictly regulated by CDSCO (India's drug regulator), must pass bioequivalence tests, and are manufactured in WHO-GMP certified facilities. They are widely endorsed by doctors worldwide."
        elif (
            "prescription" in lower_text
            or "read" in lower_text
            or "od" in lower_text
            or ("bd" in lower_text)
            or ("tds" in lower_text)
        ):
            response = """Here are common prescription terms to know:
• OD: Once daily
• BD/BID: Twice daily
• TDS/TID: Three times daily
• QID: Four times daily
• SOS: As needed
• AC: Before food
• PC: After food
• HS: At bedtime 📝"""
        elif "salt" in lower_text or "api" in lower_text or "composition" in lower_text:
            response = "The 'salt' or API (Active Pharmaceutical Ingredient) is the actual chemical that treats your condition. For example, Paracetamol is the salt, while Crocin, Dolo, and Calpol are just different brand names selling the exact same salt! 🧪"
        elif (
            "jan aushadhi" in lower_text
            or "pmbjp" in lower_text
            or "government" in lower_text
        ):
            response = "🏥 The Pradhan Mantri Bhartiya Janaushadhi Pariyojana (PMBJP) is a government initiative providing high-quality generic medicines at affordable prices. There are over 9,000+ dedicated Jan Aushadhi stores across India where you can buy these medicines."
        elif "bioequivalence" in lower_text:
            response = "🔬 Bioequivalence means that the generic drug delivers the exact same amount of active ingredient into your bloodstream, at the exact same rate, as the original brand-name drug. This ensures it works exactly the same way in your body!"
        elif "online" in lower_text or "buy" in lower_text or "internet" in lower_text:
            response = """🛒 Tips for buying medicines online:
1. Always check the expiry date on delivery.
2. Verify the platform has a valid drug license.
3. Compare prices across multiple apps.
4. Stick to well-known generic manufacturers."""
        elif (
            "store" in lower_text or "storage" in lower_text or "sunlight" in lower_text
        ):
            response = "Proper medicine storage is crucial! 🌡️ Store most medicines in a cool, dry place away from direct sunlight and moisture (avoid the bathroom cabinet). Always check the label for specific temperature requirements, and keep them out of children's reach."
        elif (
            "side effect" in lower_text
            or "reaction" in lower_text
            or "allergy" in lower_text
        ):
            response = "⚠️ All medicines (whether brand or generic) can have side effects. Always read the information leaflet and consult your doctor if you experience unusual symptoms. Never self-medicate, especially with antibiotics!"
        elif any((w in lower_text for w in ["hello", "hi", "hey", "greetings"])):
            response = "Hello! 👋 I'm here to help you navigate the world of affordable medicines. You can ask me about generic alternatives, how to read prescriptions, or medicine safety."
        elif any((w in lower_text for w in ["thank", "thanks", "helpful", "great"])):
            response = "You're very welcome! 😊 Feel free to use the Search or Upload Prescription features to find specific affordable alternatives. Stay healthy!"
        else:
            response = "I can help with questions about generic medicines, savings, prescription reading, medicine safety, and finding affordable alternatives. Could you rephrase your question? 🩺"
        return response

    @rx.event
    async def send_suggested_question(self, question: str):
        """Send a suggested question directly without relying on form submission."""
        self.messages.append({"role": "user", "content": question})
        self.current_message = ""
        self.is_typing = True
        yield
        yield rx.call_script(
            "setTimeout(() => { const el = document.getElementById('chat-messages'); if(el) el.scrollTop = el.scrollHeight; }, 50);"
        )
        response = await self._generate_response(question)
        self.messages.append({"role": "bot", "content": response})
        self.is_typing = False
        yield
        yield rx.call_script(
            "setTimeout(() => { const el = document.getElementById('chat-messages'); if(el) el.scrollTop = el.scrollHeight; }, 50);"
        )

    @rx.event
    async def send_message(self, form_data: dict[str, str]):
        """Handle message submission from the chat input form."""
        user_text = form_data.get("message", "").strip()
        if not user_text:
            return
        self.messages.append({"role": "user", "content": user_text})
        self.current_message = ""
        self.is_typing = True
        yield
        yield rx.call_script(
            "setTimeout(() => { const el = document.getElementById('chat-messages'); if(el) el.scrollTop = el.scrollHeight; }, 50);"
        )
        response = await self._generate_response(user_text)
        self.messages.append({"role": "bot", "content": response})
        self.is_typing = False
        yield
        yield rx.call_script(
            "setTimeout(() => { const el = document.getElementById('chat-messages'); if(el) el.scrollTop = el.scrollHeight; }, 50);"
        )