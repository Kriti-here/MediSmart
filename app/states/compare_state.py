import reflex as rx
import asyncio
from app.states.medicine_state import MEDICINE_DATABASE


class CompareState(rx.State):
    medicine_query: str = ""
    is_analyzing: bool = False
    analysis_complete: bool = False
    error_message: str = ""
    copied_summary: bool = False
    med_brand_name: str = ""
    med_active_ingredients: str = ""
    med_dosage_form: str = ""
    med_therapeutic_category: str = ""
    med_mechanism: str = ""
    med_standard_use: str = ""
    med_cdsco_approved: bool = False
    med_nlem_listed: bool = False
    med_jan_aushadhi: str = ""
    med_manufacturing_tier: str = ""
    med_regulatory_warnings: str = ""
    med_safety_score: int = 0
    med_narrow_therapeutic_index: bool = False
    med_substitution_safety: str = ""
    med_substitution_note: str = ""
    med_alternatives: list[dict] = []
    med_price_original: float = 0.0
    med_price_cheapest_safe: float = 0.0
    med_annual_savings: float = 0.0
    med_affordability_tier: str = ""

    @rx.var
    def savings_amount(self) -> float:
        return round(self.med_price_original - self.med_price_cheapest_safe, 2)

    @rx.var
    def savings_percent(self) -> float:
        if self.med_price_original > 0:
            return round(self.savings_amount / self.med_price_original * 100, 1)
        return 0.0

    @rx.var
    def best_value_name(self) -> str:
        if not self.med_alternatives:
            return "N/A"
        cheapest = min(self.med_alternatives, key=lambda x: x["price"])
        return cheapest["name"]

    @rx.var
    def patient_summary_text(self) -> str:
        return f"MediCompare AI — Patient Summary\nMedicine: {self.med_brand_name}\nActive Ingredient: {self.med_active_ingredients}\nCheapest Safe Alternative: {self.best_value_name} at ₹{self.med_price_cheapest_safe}\nSavings: ₹{self.savings_amount} per strip ({self.savings_percent}%)\nSubstitution Safety: {self.med_substitution_safety}\nCaution: {self.med_regulatory_warnings}\nAlways confirm substitutions with your doctor or pharmacist."

    @rx.event
    def set_medicine_query(self, value: str):
        self.medicine_query = value

    @rx.event
    async def analyze_medicine(self, form_data: dict):
        query = form_data.get("medicine_query", self.medicine_query).strip()
        if not query:
            return
        self.medicine_query = query
        self.is_analyzing = True
        self.error_message = ""
        self.analysis_complete = False
        yield
        await asyncio.sleep(1.2)
        lower_q = query.lower()
        found_key = None
        for key, data in MEDICINE_DATABASE.items():
            if key in lower_q or data["brand_name"].lower() in lower_q:
                found_key = key
                break
        if found_key:
            med = MEDICINE_DATABASE[found_key]
            self.med_brand_name = med["brand_name"]
            self.med_active_ingredients = med["active_ingredients"]
            self.med_dosage_form = med["dosage_form"]
            self.med_therapeutic_category = med["therapeutic_category"]
            self.med_mechanism = med["mechanism"]
            self.med_standard_use = med["standard_use"]
            self.med_cdsco_approved = med["cdsco_approved"]
            self.med_nlem_listed = med["nlem_listed"]
            self.med_jan_aushadhi = med["jan_aushadhi_available"]
            self.med_manufacturing_tier = med["manufacturing_tier"]
            self.med_regulatory_warnings = med["regulatory_warnings"]
            self.med_safety_score = med["safety_score"]
            self.med_narrow_therapeutic_index = med["narrow_therapeutic_index"]
            self.med_substitution_safety = med["substitution_safety"]
            self.med_substitution_note = med["substitution_note"]
            self.med_alternatives = med["alternatives"]
            self.med_price_original = float(med["price_original"])
            self.med_price_cheapest_safe = float(med["price_cheapest_safe"])
            self.med_annual_savings = float(med["annual_savings_estimate"])
            self.med_affordability_tier = med["affordability_tier"]
            self.analysis_complete = True
        else:
            self.error_message = f"Could not find analysis data for '{query}'. Please try a different medicine."
        self.is_analyzing = False
        yield

    @rx.event
    def reset_analysis(self):
        self.analysis_complete = False
        self.medicine_query = ""
        self.error_message = ""
        self.copied_summary = False

    @rx.event
    async def copy_summary(self):
        self.copied_summary = True
        yield rx.set_clipboard(CompareState.patient_summary_text)
        yield rx.toast("Patient summary copied to clipboard!", duration=3000)
        await asyncio.sleep(2)
        self.copied_summary = False

    @rx.event
    def analyze_quick(self, medicine_name: str):
        self.medicine_query = medicine_name
        yield CompareState.analyze_medicine({"medicine_query": medicine_name})