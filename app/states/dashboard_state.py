import reflex as rx
from datetime import datetime, date, timedelta
import random
import logging


class DashboardState(rx.State):
    active_member_index: int = 0
    family_members: list[dict] = [
        {
            "name": "Rajesh Kumar",
            "age": 58,
            "relationship": "Father",
            "avatar_seed": "RK",
            "medicines": [
                {
                    "name": "Telmisartan 40mg",
                    "dosage": "1 tablet morning",
                    "time": "8:00 AM",
                    "category": "BP",
                },
                {
                    "name": "Metformin 500mg",
                    "dosage": "1 tablet with meals, twice daily",
                    "time": "8:00 AM, 8:00 PM",
                    "category": "Diabetes",
                },
                {
                    "name": "Atorvastatin 10mg",
                    "dosage": "1 tablet at bedtime",
                    "time": "10:00 PM",
                    "category": "Cholesterol",
                },
            ],
            "vitals": [
                {
                    "date": "2025-01-20",
                    "bp_systolic": 138,
                    "bp_diastolic": 88,
                    "sugar_fasting": 142,
                    "weight": 78.5,
                    "temp": 98.4,
                },
                {
                    "date": "2025-01-21",
                    "bp_systolic": 135,
                    "bp_diastolic": 86,
                    "sugar_fasting": 138,
                    "weight": 78.3,
                    "temp": 98.6,
                },
                {
                    "date": "2025-01-22",
                    "bp_systolic": 132,
                    "bp_diastolic": 84,
                    "sugar_fasting": 135,
                    "weight": 78.4,
                    "temp": 98.2,
                },
                {
                    "date": "2025-01-23",
                    "bp_systolic": 130,
                    "bp_diastolic": 82,
                    "sugar_fasting": 130,
                    "weight": 78.2,
                    "temp": 98.5,
                },
                {
                    "date": "2025-01-24",
                    "bp_systolic": 128,
                    "bp_diastolic": 80,
                    "sugar_fasting": 126,
                    "weight": 78.0,
                    "temp": 98.4,
                },
                {
                    "date": "2025-01-25",
                    "bp_systolic": 126,
                    "bp_diastolic": 78,
                    "sugar_fasting": 122,
                    "weight": 77.8,
                    "temp": 98.3,
                },
                {
                    "date": "2025-01-26",
                    "bp_systolic": 124,
                    "bp_diastolic": 76,
                    "sugar_fasting": 118,
                    "weight": 77.5,
                    "temp": 98.6,
                },
            ],
        },
        {
            "name": "Sunita Kumar",
            "age": 54,
            "relationship": "Mother",
            "avatar_seed": "SK",
            "medicines": [
                {
                    "name": "Levothyroxine 50mcg",
                    "dosage": "1 tablet empty stomach",
                    "time": "6:30 AM",
                    "category": "Thyroid",
                },
                {
                    "name": "Calcium + Vitamin D",
                    "dosage": "1 tablet after lunch",
                    "time": "1:00 PM",
                    "category": "Supplement",
                },
            ],
            "vitals": [
                {
                    "date": "2025-01-20",
                    "bp_systolic": 118,
                    "bp_diastolic": 76,
                    "sugar_fasting": 98,
                    "weight": 65.0,
                    "temp": 98.4,
                },
                {
                    "date": "2025-01-21",
                    "bp_systolic": 120,
                    "bp_diastolic": 78,
                    "sugar_fasting": 100,
                    "weight": 64.8,
                    "temp": 98.6,
                },
                {
                    "date": "2025-01-22",
                    "bp_systolic": 116,
                    "bp_diastolic": 74,
                    "sugar_fasting": 96,
                    "weight": 64.9,
                    "temp": 98.2,
                },
                {
                    "date": "2025-01-23",
                    "bp_systolic": 118,
                    "bp_diastolic": 76,
                    "sugar_fasting": 99,
                    "weight": 64.7,
                    "temp": 98.5,
                },
                {
                    "date": "2025-01-24",
                    "bp_systolic": 115,
                    "bp_diastolic": 72,
                    "sugar_fasting": 94,
                    "weight": 64.5,
                    "temp": 98.4,
                },
                {
                    "date": "2025-01-25",
                    "bp_systolic": 117,
                    "bp_diastolic": 75,
                    "sugar_fasting": 97,
                    "weight": 64.6,
                    "temp": 98.3,
                },
                {
                    "date": "2025-01-26",
                    "bp_systolic": 114,
                    "bp_diastolic": 73,
                    "sugar_fasting": 92,
                    "weight": 64.4,
                    "temp": 98.6,
                },
            ],
        },
        {
            "name": "Ankit Kumar",
            "age": 28,
            "relationship": "Self",
            "avatar_seed": "AK",
            "medicines": [
                {
                    "name": "Pantoprazole 40mg",
                    "dosage": "1 tablet before breakfast",
                    "time": "7:30 AM",
                    "category": "Acidity",
                }
            ],
            "vitals": [
                {
                    "date": "2025-01-20",
                    "bp_systolic": 120,
                    "bp_diastolic": 80,
                    "sugar_fasting": 90,
                    "weight": 72.0,
                    "temp": 98.6,
                },
                {
                    "date": "2025-01-21",
                    "bp_systolic": 118,
                    "bp_diastolic": 78,
                    "sugar_fasting": 88,
                    "weight": 71.8,
                    "temp": 98.4,
                },
                {
                    "date": "2025-01-22",
                    "bp_systolic": 122,
                    "bp_diastolic": 82,
                    "sugar_fasting": 92,
                    "weight": 72.1,
                    "temp": 98.5,
                },
                {
                    "date": "2025-01-23",
                    "bp_systolic": 119,
                    "bp_diastolic": 79,
                    "sugar_fasting": 89,
                    "weight": 71.9,
                    "temp": 98.6,
                },
                {
                    "date": "2025-01-24",
                    "bp_systolic": 120,
                    "bp_diastolic": 80,
                    "sugar_fasting": 91,
                    "weight": 72.0,
                    "temp": 98.4,
                },
                {
                    "date": "2025-01-25",
                    "bp_systolic": 118,
                    "bp_diastolic": 78,
                    "sugar_fasting": 87,
                    "weight": 71.7,
                    "temp": 98.3,
                },
                {
                    "date": "2025-01-26",
                    "bp_systolic": 116,
                    "bp_diastolic": 76,
                    "sugar_fasting": 85,
                    "weight": 71.5,
                    "temp": 98.5,
                },
            ],
        },
    ]
    adherence_grid: list[list[str]] = [
        ["taken", "taken", "taken"],
        ["taken", "missed", "taken"],
        ["taken", "taken", "taken"],
        ["taken", "taken", "missed"],
        ["taken", "taken", "taken"],
        ["pending", "pending", "pending"],
        ["pending", "pending", "pending"],
    ]
    streak_days: int = 5
    total_saved_amount: float = 1250.0
    wearable_connected: bool = False
    heart_rate: int = 72
    steps_today: int = 6842
    sleep_hours: float = 7.2
    last_sync: str = "2 min ago"
    show_add_member: bool = False
    new_member_name: str = ""
    new_member_age: str = ""
    new_member_relationship: str = "Other"
    show_add_vital: bool = False

    @rx.var
    def active_member(self) -> dict:
        if 0 <= self.active_member_index < len(self.family_members):
            return self.family_members[self.active_member_index]
        return self.family_members[0] if self.family_members else {}

    @rx.var
    def active_member_medicines(self) -> list[dict]:
        return self.active_member.get("medicines", [])

    @rx.var
    def active_member_vitals(self) -> list[dict]:
        return self.active_member.get("vitals", [])

    @rx.var
    def vitals_chart_data(self) -> list[dict]:
        vitals = self.active_member_vitals
        return [
            {
                "date": v["date"][-5:],
                "BP Systolic": v["bp_systolic"],
                "BP Diastolic": v["bp_diastolic"],
                "Sugar": v["sugar_fasting"],
            }
            for v in vitals
        ]

    @rx.var
    def weight_chart_data(self) -> list[dict]:
        vitals = self.active_member_vitals
        return [{"date": v["date"][-5:], "Weight": v["weight"]} for v in vitals]

    @rx.var
    def adherence_percent(self) -> int:
        taken = sum(
            (1 for day in self.adherence_grid for dose in day if dose == "taken")
        )
        total = sum(
            (1 for day in self.adherence_grid for dose in day if dose != "pending")
        )
        return int(taken / total * 100) if total > 0 else 0

    @rx.var
    def total_taken(self) -> int:
        return sum(
            (1 for day in self.adherence_grid for dose in day if dose == "taken")
        )

    @rx.var
    def total_missed(self) -> int:
        return sum(
            (1 for day in self.adherence_grid for dose in day if dose == "missed")
        )

    @rx.var
    def achievements(self) -> list[dict]:
        badges = []
        if self.streak_days >= 1:
            badges.append(
                {
                    "icon": "💊",
                    "name": "First Dose",
                    "desc": "Took your first medicine",
                    "earned": True,
                }
            )
        if self.streak_days >= 7:
            badges.append(
                {
                    "icon": "🔥",
                    "name": "Week Warrior",
                    "desc": "7-day streak!",
                    "earned": True,
                }
            )
        else:
            badges.append(
                {
                    "icon": "🔥",
                    "name": "Week Warrior",
                    "desc": f"{self.streak_days}/7 days",
                    "earned": False,
                }
            )
        if self.streak_days >= 30:
            badges.append(
                {
                    "icon": "🏆",
                    "name": "Month Master",
                    "desc": "30-day streak!",
                    "earned": True,
                }
            )
        else:
            badges.append(
                {
                    "icon": "🏆",
                    "name": "Month Master",
                    "desc": f"{min(self.streak_days, 30)}/30 days",
                    "earned": False,
                }
            )
        if self.total_saved_amount >= 100:
            badges.append(
                {
                    "icon": "💰",
                    "name": "₹100 Saved",
                    "desc": "First savings milestone",
                    "earned": True,
                }
            )
        if self.total_saved_amount >= 1000:
            badges.append(
                {
                    "icon": "💎",
                    "name": "₹1000 Saved",
                    "desc": "Smart saver!",
                    "earned": True,
                }
            )
        else:
            badges.append(
                {
                    "icon": "💎",
                    "name": "₹1000 Saved",
                    "desc": f"₹{self.total_saved_amount}/₹1000",
                    "earned": False,
                }
            )
        if self.total_saved_amount >= 5000:
            badges.append(
                {
                    "icon": "👑",
                    "name": "₹5000 Saved",
                    "desc": "Legendary saver!",
                    "earned": True,
                }
            )
        else:
            badges.append(
                {
                    "icon": "👑",
                    "name": "₹5000 Saved",
                    "desc": f"₹{self.total_saved_amount}/₹5000",
                    "earned": False,
                }
            )
        return badges

    @rx.var
    def refill_alerts(self) -> list[dict]:
        from app.states.checkout_state import SHOP_MEDICINES
        from datetime import datetime, date

        today = date.today()
        alerts = []
        for m in SHOP_MEDICINES:
            try:
                exp = datetime.strptime(m["expiry_date"], "%Y-%m-%d").date()
                days_left = (exp - today).days
                if 0 < days_left <= 60:
                    alerts.append(
                        {
                            "name": m["generic_name"],
                            "days_left": days_left,
                            "price": m["generic_price"],
                        }
                    )
            except:
                logging.exception("Unexpected error")
        return sorted(alerts, key=lambda x: x["days_left"])[:5]

    @rx.var
    def wearable_suggestions(self) -> list[dict]:
        suggestions = []
        if self.heart_rate > 80:
            suggestions.append(
                {
                    "icon": "heart-pulse",
                    "text": "Heart rate slightly elevated — take BP medicine on time",
                    "urgency": "warning",
                }
            )
        if self.steps_today < 5000:
            suggestions.append(
                {
                    "icon": "footprints",
                    "text": "Low activity today — a 20min walk can improve blood sugar control",
                    "urgency": "info",
                }
            )
        if self.sleep_hours < 7:
            suggestions.append(
                {
                    "icon": "moon",
                    "text": "Sleep was below 7h — poor sleep affects BP. Consider earlier bedtime.",
                    "urgency": "warning",
                }
            )
        if (
            self.heart_rate <= 80
            and self.steps_today >= 5000
            and (self.sleep_hours >= 7)
        ):
            suggestions.append(
                {
                    "icon": "check-circle",
                    "text": "All vitals look good! Keep it up 💪",
                    "urgency": "success",
                }
            )
        return suggestions

    @rx.event
    def set_active_member(self, index: int):
        self.active_member_index = index

    @rx.event
    def toggle_adherence(self, day_idx: int, dose_idx: int):
        current = self.adherence_grid[day_idx][dose_idx]
        if current == "pending":
            self.adherence_grid[day_idx][dose_idx] = "taken"
        elif current == "taken":
            self.adherence_grid[day_idx][dose_idx] = "missed"
        else:
            self.adherence_grid[day_idx][dose_idx] = "pending"

    @rx.event
    def toggle_add_member(self):
        self.show_add_member = not self.show_add_member

    @rx.event
    def add_family_member(self, form_data: dict):
        name = form_data.get("name", "").strip()
        age = form_data.get("age", "0").strip()
        relationship = form_data.get("relationship", "Other").strip()
        if not name:
            yield rx.toast("Please enter a name", level="error")
            return
        new_member = {
            "name": name,
            "age": int(age) if age.isdigit() else 0,
            "relationship": relationship,
            "avatar_seed": name[:2].upper(),
            "medicines": [],
            "vitals": [],
        }
        self.family_members.append(new_member)
        self.show_add_member = False
        yield rx.toast(
            f"Added {name} to your family! 👨\u200d👩\u200d👧\u200d👦", duration=3000
        )

    @rx.event
    def remove_family_member(self, index: int):
        if 0 <= index < len(self.family_members) and len(self.family_members) > 1:
            removed = self.family_members.pop(index)
            if self.active_member_index >= len(self.family_members):
                self.active_member_index = 0
            yield rx.toast(f"Removed {removed['name']}", duration=2000)

    @rx.event
    def toggle_wearable(self):
        self.wearable_connected = not self.wearable_connected
        if self.wearable_connected:
            yield rx.toast(
                "🔗 Wearable connected! Syncing health data...", duration=3000
            )
        else:
            yield rx.toast("Wearable disconnected", duration=2000)

    @rx.event
    def sync_wearable(self):
        import random

        self.heart_rate = random.randint(65, 85)
        self.steps_today = random.randint(3000, 12000)
        self.sleep_hours = round(random.uniform(5.5, 8.5), 1)
        self.last_sync = "Just now"
        yield rx.toast("✅ Wearable data synced!", duration=2000)