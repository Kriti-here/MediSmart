import reflex as rx
import logging

SYMPTOM_MEDICINES = {
    "Headache": [
        {
            "brand": "Crocin 500mg",
            "generic": "Paracetamol 500mg",
            "brand_price": 40,
            "generic_price": 8,
            "interaction": "",
        },
        {
            "brand": "Combiflam",
            "generic": "Ibuprofen+Para",
            "brand_price": 45,
            "generic_price": 12,
            "interaction": "⚠ Avoid with blood thinners",
        },
    ],
    "Fever": [
        {
            "brand": "Dolo 650",
            "generic": "Paracetamol 650mg",
            "brand_price": 30,
            "generic_price": 10,
            "interaction": "",
        },
        {
            "brand": "Crocin 500mg",
            "generic": "Paracetamol 500mg",
            "brand_price": 40,
            "generic_price": 8,
            "interaction": "",
        },
    ],
    "Acidity": [
        {
            "brand": "Pan 40",
            "generic": "Pantoprazole 40mg",
            "brand_price": 150,
            "generic_price": 18,
            "interaction": "⚠ Take 30 min before food",
        },
        {
            "brand": "Rantac 150",
            "generic": "Ranitidine 150mg",
            "brand_price": 35,
            "generic_price": 6,
            "interaction": "⚠ Avoid with antifungals",
        },
    ],
    "Allergy": [
        {
            "brand": "Allegra 120mg",
            "generic": "Fexofenadine 120mg",
            "brand_price": 180,
            "generic_price": 30,
            "interaction": "⚠ Avoid fruit juices (reduces absorption)",
        },
        {
            "brand": "Cetrizine 10mg",
            "generic": "Cetirizine 10mg",
            "brand_price": 25,
            "generic_price": 5,
            "interaction": "⚠ May cause drowsiness",
        },
    ],
    "Joint Pain": [
        {
            "brand": "Voveran SR 100",
            "generic": "Diclofenac SR 100mg",
            "brand_price": 95,
            "generic_price": 14,
            "interaction": "⚠ Do NOT combine with other NSAIDs",
        },
        {
            "brand": "Combiflam",
            "generic": "Ibuprofen+Para",
            "brand_price": 45,
            "generic_price": 12,
            "interaction": "⚠ Avoid with blood thinners",
        },
    ],
    "Diabetes": [
        {
            "brand": "Glycomet 500",
            "generic": "Metformin 500mg",
            "brand_price": 60,
            "generic_price": 10,
            "interaction": "⚠ Monitor B12 levels long-term",
        },
        {
            "brand": "Januvia 100mg",
            "generic": "Sitagliptin 100mg",
            "brand_price": 650,
            "generic_price": 120,
            "interaction": "⚠ Risk of pancreatitis — report abdominal pain",
        },
    ],
}
EXPIRY_MEDICINES = [
    {"name": "Pantoprazole 40mg", "expiry": "2025-07-20"},
    {"name": "Metformin 500mg", "expiry": "2025-08-15"},
    {"name": "Paracetamol 500mg", "expiry": "2025-06-28"},
    {"name": "Fexofenadine 120mg", "expiry": "2026-03-10"},
    {"name": "Atorvastatin 10mg", "expiry": "2025-09-05"},
]
NEARBY_PHARMACIES = [
    {
        "name": "Jan Aushadhi Kendra",
        "distance": "0.8 km",
        "stock": "In Stock",
        "eta": "15 min",
        "price": "₹8",
    },
    {
        "name": "Apollo Pharmacy",
        "distance": "1.2 km",
        "stock": "In Stock",
        "eta": "20 min",
        "price": "₹35",
    },
    {
        "name": "MedPlus",
        "distance": "2.1 km",
        "stock": "Low Stock",
        "eta": "28 min",
        "price": "₹32",
    },
    {
        "name": "Netmeds Store",
        "distance": "3.5 km",
        "stock": "Out of Stock",
        "eta": "—",
        "price": "₹30",
    },
]
SAVINGS_CHART_DATA = [
    {"month": "Jan", "branded": 2400, "generic": 480},
    {"month": "Feb", "branded": 2400, "generic": 480},
    {"month": "Mar", "branded": 2600, "generic": 520},
    {"month": "Apr", "branded": 2400, "generic": 480},
    {"month": "May", "branded": 2800, "generic": 560},
    {"month": "Jun", "branded": 2400, "generic": 480},
    {"month": "Jul", "branded": 2600, "generic": 520},
    {"month": "Aug", "branded": 2400, "generic": 480},
    {"month": "Sep", "branded": 2800, "generic": 560},
    {"month": "Oct", "branded": 2400, "generic": 480},
    {"month": "Nov", "branded": 2600, "generic": 520},
    {"month": "Dec", "branded": 2400, "generic": 480},
]


class MedOSState(rx.State):
    active_tab: str = "features"
    selected_symptoms: list[str] = []
    dosage_grid: list[list[str]] = [["pending", "pending", "pending"] for _ in range(7)]
    dosage_days: list[str] = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    @rx.event
    def set_active_tab(self, tab: str):
        self.active_tab = tab

    @rx.event
    def toggle_symptom(self, symptom: str):
        if symptom in self.selected_symptoms:
            self.selected_symptoms.remove(symptom)
        else:
            self.selected_symptoms.append(symptom)

    @rx.event
    def toggle_pill(self, day_index: int, dose_index: int):
        current = self.dosage_grid[day_index][dose_index]
        if current == "pending":
            self.dosage_grid[day_index][dose_index] = "taken"
        elif current == "taken":
            self.dosage_grid[day_index][dose_index] = "missed"
        else:
            self.dosage_grid[day_index][dose_index] = "pending"

    @rx.var
    def total_taken(self) -> int:
        return sum((1 for day in self.dosage_grid for pill in day if pill == "taken"))

    @rx.var
    def total_missed(self) -> int:
        return sum((1 for day in self.dosage_grid for pill in day if pill == "missed"))

    @rx.var
    def adherence_percent(self) -> int:
        taken = self.total_taken
        missed = self.total_missed
        total = taken + missed
        if total == 0:
            return 0
        return int(taken / total * 100)

    @rx.var
    def recommended_medicines(self) -> list[dict[str, str | int]]:
        meds = []
        seen = set()
        for symptom in self.selected_symptoms:
            for med in SYMPTOM_MEDICINES.get(symptom, []):
                if med["brand"] not in seen:
                    meds.append(med)
                    seen.add(med["brand"])
        return meds

    @rx.var
    def interaction_warnings(self) -> list[str]:
        warnings = set()
        meds = self.recommended_medicines
        for med in meds:
            if med["interaction"]:
                warnings.add(med["interaction"])
        if (
            "Headache" in self.selected_symptoms
            and "Joint Pain" in self.selected_symptoms
        ):
            warnings.add(
                "⚠ CRITICAL: Multiple NSAIDs selected (Combiflam + Voveran). Risk of stomach bleeding. Consult doctor."
            )
        if "Fever" in self.selected_symptoms and "Headache" in self.selected_symptoms:
            warnings.add(
                "ℹ Paracetamol covers both — no need for separate medications."
            )
        return list(warnings)

    @rx.var
    def expiry_medicines(self) -> list[dict[str, str | int]]:
        from datetime import datetime, date

        today = date.today()
        res = []
        for em in EXPIRY_MEDICINES:
            try:
                exp = datetime.strptime(em["expiry"], "%Y-%m-%d").date()
                days_left = (exp - today).days
                if days_left <= 7:
                    status = "critical"
                elif days_left <= 30:
                    status = "warning"
                else:
                    status = "good"
                res.append(
                    {
                        "name": em["name"],
                        "expiry": em["expiry"],
                        "days_left": days_left,
                        "status": status,
                    }
                )
            except Exception:
                logging.exception("Unexpected error")
        return sorted(res, key=lambda x: x["days_left"])

    @rx.var
    def morning_pills(self) -> list[dict[str, str | int]]:
        return [
            {
                "day_idx": i,
                "dose_idx": 0,
                "day_name": self.dosage_days[i],
                "status": self.dosage_grid[i][0],
            }
            for i in range(7)
        ]

    @rx.var
    def afternoon_pills(self) -> list[dict[str, str | int]]:
        return [
            {
                "day_idx": i,
                "dose_idx": 1,
                "day_name": self.dosage_days[i],
                "status": self.dosage_grid[i][1],
            }
            for i in range(7)
        ]

    @rx.var
    def night_pills(self) -> list[dict[str, str | int]]:
        return [
            {
                "day_idx": i,
                "dose_idx": 2,
                "day_name": self.dosage_days[i],
                "status": self.dosage_grid[i][2],
            }
            for i in range(7)
        ]

    @rx.var
    def nearby_pharmacies(self) -> list[dict[str, str]]:
        return NEARBY_PHARMACIES