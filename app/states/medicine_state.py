import reflex as rx
from typing import TypedDict, Optional
from datetime import datetime, date
import asyncio
import logging


class ExtractedMedicine(TypedDict):
    name: str
    confidence: int
    matched_id: str
    generic_name: str
    salt_composition: str
    brand_price: float
    generic_price: float
    expiry_date: str
    dosage: str
    frequency: str
    duration: str
    needs_review: bool
    review_reason: str


class Medicine(TypedDict):
    id: str
    brand_name: str
    generic_name: str
    salt_composition: str
    brand_price: float
    generic_price: float
    manufacturer: str
    dosage: str
    verified: bool
    category: str
    expiry_date: str


MEDICINE_DATABASE = {
    "crocin": {
        "brand_name": "Crocin",
        "active_ingredients": "Paracetamol 500mg",
        "dosage_form": "Tablet",
        "therapeutic_category": "Analgesic / Antipyretic",
        "mechanism": "Paracetamol works by blocking the production of prostaglandins in the brain, which reduces pain signals and lowers fever. It does not reduce inflammation significantly.",
        "standard_use": "Used for mild to moderate pain (headache, toothache, body ache) and fever. Typical course: 1-2 tablets every 4-6 hours, max 8 tablets/day. Short-term use (3-5 days) unless directed by doctor.",
        "cdsco_approved": True,
        "nlem_listed": True,
        "jan_aushadhi_available": "✅ Available",
        "manufacturing_tier": "WHO-GMP Certified",
        "regulatory_warnings": "Avoid exceeding 4g/day. Risk of liver damage with overdose or chronic alcohol use.",
        "safety_score": 98,
        "narrow_therapeutic_index": False,
        "substitution_safety": "🟢 GREEN",
        "substitution_note": "Direct substitution safe. All Paracetamol 500mg tablets are bioequivalent regardless of brand.",
        "alternatives": [
            {
                "name": "Paracetamol (Generic)",
                "type": "Jan Aushadhi",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 8.0,
                "regulatory_badge": "NLEM + Jan Aushadhi",
                "manufacturer": "PMBJP",
            },
            {
                "name": "Dolo 650",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "Paracetamol 650mg",
                "price": 30.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Micro Labs",
            },
            {
                "name": "Calpol 500",
                "type": "Original Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 35.0,
                "regulatory_badge": "CDSCO + WHO-GMP",
                "manufacturer": "GSK",
            },
            {
                "name": "P-500 (Generic)",
                "type": "OTC Generic",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 10.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Cipla",
            },
        ],
        "price_original": 40.0,
        "price_cheapest_safe": 8.0,
        "annual_savings_estimate": 384.0,
        "affordability_tier": "🟢 Very Affordable",
    },
    "augmentin": {
        "brand_name": "Augmentin 625",
        "active_ingredients": "Amoxicillin 500mg + Clavulanic Acid 125mg",
        "dosage_form": "Tablet",
        "therapeutic_category": "Antibiotic (Penicillin type)",
        "mechanism": "Amoxicillin kills bacteria, while Clavulanic Acid prevents the bacteria from destroying Amoxicillin.",
        "standard_use": "Used for bacterial infections of the ear, nose, throat, skin, and urinary tract.",
        "cdsco_approved": True,
        "nlem_listed": True,
        "jan_aushadhi_available": "⚠️ Partial",
        "manufacturing_tier": "WHO-GMP Certified",
        "regulatory_warnings": "Complete the full course even if feeling better. May cause diarrhea.",
        "safety_score": 92,
        "narrow_therapeutic_index": False,
        "substitution_safety": "🟡 YELLOW",
        "substitution_note": "Antibiotic - Verify sensitivity and complete the full course. Substitution is generally safe with reputed generics.",
        "alternatives": [
            {
                "name": "Amox+Clav (Gen)",
                "type": "Jan Aushadhi",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 50.0,
                "regulatory_badge": "NLEM",
                "manufacturer": "PMBJP",
            },
            {
                "name": "Moxikind-CV 625",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 110.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Mankind",
            },
            {
                "name": "Clavam 625",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 135.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Alkem",
            },
        ],
        "price_original": 200.0,
        "price_cheapest_safe": 50.0,
        "annual_savings_estimate": 1800.0,
        "affordability_tier": "🟡 Moderately Affordable",
    },
    "combiflam": {
        "brand_name": "Combiflam",
        "active_ingredients": "Ibuprofen 400mg + Paracetamol 325mg",
        "dosage_form": "Tablet",
        "therapeutic_category": "Analgesic / NSAID",
        "mechanism": "Combines an NSAID to reduce inflammation with a pain reliever/fever reducer for synergistic effect.",
        "standard_use": "Used for moderate pain relief, including headache, muscle ache, and joint pain.",
        "cdsco_approved": True,
        "nlem_listed": True,
        "jan_aushadhi_available": "✅ Available",
        "manufacturing_tier": "WHO-GMP Certified",
        "regulatory_warnings": "Take after meals to avoid stomach upset. Do not use for long-term without doctor advice.",
        "safety_score": 95,
        "narrow_therapeutic_index": False,
        "substitution_safety": "🟢 GREEN",
        "substitution_note": "Direct substitution safe. Excellent bioequivalence among leading generics.",
        "alternatives": [
            {
                "name": "Ibu+Para (Gen)",
                "type": "Jan Aushadhi",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 12.0,
                "regulatory_badge": "NLEM + Jan Aushadhi",
                "manufacturer": "PMBJP",
            },
            {
                "name": "Brufen Plus",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 20.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Abbott",
            },
            {
                "name": "Zerodol-P",
                "type": "Alternative NSAID",
                "salt_match": "Different",
                "dosage_match": "N/A",
                "price": 35.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Ipca",
            },
        ],
        "price_original": 45.0,
        "price_cheapest_safe": 12.0,
        "annual_savings_estimate": 396.0,
        "affordability_tier": "🟢 Very Affordable",
    },
    "allegra": {
        "brand_name": "Allegra 120mg",
        "active_ingredients": "Fexofenadine 120mg",
        "dosage_form": "Tablet",
        "therapeutic_category": "Antihistamine",
        "mechanism": "Blocks histamine, a chemical in the body that causes allergic symptoms.",
        "standard_use": "Used to relieve allergy symptoms such as watery eyes, runny nose, itching eyes/nose, sneezing.",
        "cdsco_approved": True,
        "nlem_listed": False,
        "jan_aushadhi_available": "⚠️ Partial",
        "manufacturing_tier": "WHO-GMP Certified",
        "regulatory_warnings": "Non-drowsy formulation, but avoid taking with fruit juices as they can decrease absorption.",
        "safety_score": 96,
        "narrow_therapeutic_index": False,
        "substitution_safety": "🟢 GREEN",
        "substitution_note": "Direct substitution safe. Most generic fexofenadine formulations offer similar relief.",
        "alternatives": [
            {
                "name": "Fexofenadine (Gen)",
                "type": "Jan Aushadhi",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 30.0,
                "regulatory_badge": "Jan Aushadhi",
                "manufacturer": "PMBJP",
            },
            {
                "name": "Fexova 120",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 65.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Sun Pharma",
            },
            {
                "name": "Allercet-F",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 80.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Micro Labs",
            },
        ],
        "price_original": 180.0,
        "price_cheapest_safe": 30.0,
        "annual_savings_estimate": 1800.0,
        "affordability_tier": "🟡 Moderately Affordable",
    },
    "pan 40": {
        "brand_name": "Pan 40",
        "active_ingredients": "Pantoprazole 40mg",
        "dosage_form": "Tablet",
        "therapeutic_category": "Antacid / PPI",
        "mechanism": "Proton pump inhibitor (PPI) that reduces the amount of acid produced in the stomach.",
        "standard_use": "Used to treat acid reflux, heartburn, and stomach ulcers.",
        "cdsco_approved": True,
        "nlem_listed": True,
        "jan_aushadhi_available": "✅ Available",
        "manufacturing_tier": "WHO-GMP Certified",
        "regulatory_warnings": "Take 30 minutes before food. Prolonged use may lead to B12 or magnesium deficiency.",
        "safety_score": 97,
        "narrow_therapeutic_index": False,
        "substitution_safety": "🟢 GREEN",
        "substitution_note": "Direct substitution safe. Pantoprazole generics are widely proven and bioequivalent.",
        "alternatives": [
            {
                "name": "Pantoprazole (Gen)",
                "type": "Jan Aushadhi",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 18.0,
                "regulatory_badge": "NLEM + Jan Aushadhi",
                "manufacturer": "PMBJP",
            },
            {
                "name": "Pantocid 40",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 120.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Sun Pharma",
            },
            {
                "name": "Pantodac 40",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 110.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Zydus",
            },
        ],
        "price_original": 150.0,
        "price_cheapest_safe": 18.0,
        "annual_savings_estimate": 1584.0,
        "affordability_tier": "🟢 Very Affordable",
    },
    "calpol": {
        "brand_name": "Calpol 500",
        "active_ingredients": "Paracetamol 500mg",
        "dosage_form": "Tablet",
        "therapeutic_category": "Analgesic / Antipyretic",
        "mechanism": "Reduces pain signals and lowers fever. Same active ingredient as Crocin.",
        "standard_use": "Used for mild to moderate pain and fever. 1-2 tablets every 4-6 hours, max 8/day.",
        "cdsco_approved": True,
        "nlem_listed": True,
        "jan_aushadhi_available": "✅ Available",
        "manufacturing_tier": "WHO-GMP Certified",
        "regulatory_warnings": "Avoid exceeding 4g/day. Risk of liver damage with overdose.",
        "safety_score": 98,
        "narrow_therapeutic_index": False,
        "substitution_safety": "🟢 GREEN",
        "substitution_note": "Direct substitution safe. Any Paracetamol 500mg generic is equally effective.",
        "alternatives": [
            {
                "name": "Paracetamol (Gen)",
                "type": "Jan Aushadhi",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 8.0,
                "regulatory_badge": "NLEM + Jan Aushadhi",
                "manufacturer": "PMBJP",
            },
            {
                "name": "Crocin 500",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 40.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "GSK",
            },
            {
                "name": "Dolo 650",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "650mg",
                "price": 30.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Micro Labs",
            },
        ],
        "price_original": 35.0,
        "price_cheapest_safe": 8.0,
        "annual_savings_estimate": 324.0,
        "affordability_tier": "🟢 Very Affordable",
    },
    "glycomet": {
        "brand_name": "Glycomet 500",
        "active_ingredients": "Metformin 500mg",
        "dosage_form": "Tablet",
        "therapeutic_category": "Anti-Diabetic",
        "mechanism": "Decreases hepatic glucose production and improves insulin sensitivity.",
        "standard_use": "First-line medication for Type 2 Diabetes mellitus.",
        "cdsco_approved": True,
        "nlem_listed": True,
        "jan_aushadhi_available": "✅ Available",
        "manufacturing_tier": "WHO-GMP Certified",
        "regulatory_warnings": "Take with meals. Risk of lactic acidosis in rare cases. Monitor B12 levels over long term.",
        "safety_score": 94,
        "narrow_therapeutic_index": False,
        "substitution_safety": "🟢 GREEN",
        "substitution_note": "Do not switch brands frequently for diabetes medication without doctor guidance.",
        "alternatives": [
            {
                "name": "Metformin (Gen)",
                "type": "Jan Aushadhi",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 10.0,
                "regulatory_badge": "NLEM + Jan Aushadhi",
                "manufacturer": "PMBJP",
            },
            {
                "name": "Glucophage 500",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 45.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Merck",
            },
            {
                "name": "Obimet 500",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 38.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Abbott",
            },
        ],
        "price_original": 60.0,
        "price_cheapest_safe": 10.0,
        "annual_savings_estimate": 600.0,
        "affordability_tier": "🟢 Very Affordable",
    },
    "telma": {
        "brand_name": "Telma 40",
        "active_ingredients": "Telmisartan 40mg",
        "dosage_form": "Tablet",
        "therapeutic_category": "Antihypertensive",
        "mechanism": "Blocks angiotensin II, allowing blood vessels to widen and lowering blood pressure.",
        "standard_use": "Treats high blood pressure and reduces risk of heart attack or stroke.",
        "cdsco_approved": True,
        "nlem_listed": True,
        "jan_aushadhi_available": "✅ Available",
        "manufacturing_tier": "WHO-GMP Certified",
        "regulatory_warnings": "Do not use during pregnancy. May increase potassium levels.",
        "safety_score": 93,
        "narrow_therapeutic_index": False,
        "substitution_safety": "🟡 YELLOW",
        "substitution_note": "BP medication - monitor blood pressure for a few days after switching brands.",
        "alternatives": [
            {
                "name": "Telmisartan (Gen)",
                "type": "Jan Aushadhi",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 15.0,
                "regulatory_badge": "NLEM + Jan Aushadhi",
                "manufacturer": "PMBJP",
            },
            {
                "name": "Telvas 40",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 85.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Aristo",
            },
            {
                "name": "Telsar 40",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 70.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Unichem",
            },
        ],
        "price_original": 110.0,
        "price_cheapest_safe": 15.0,
        "annual_savings_estimate": 1140.0,
        "affordability_tier": "🟢 Very Affordable",
    },
    "voveran": {
        "brand_name": "Voveran SR 100",
        "active_ingredients": "Diclofenac 100mg (Sustained Release)",
        "dosage_form": "Tablet SR",
        "therapeutic_category": "Pain Relief / NSAID",
        "mechanism": "Non-steroidal anti-inflammatory drug that reduces substances that cause inflammation.",
        "standard_use": "Used for severe joint pain, rheumatoid arthritis, osteoarthritis.",
        "cdsco_approved": True,
        "nlem_listed": True,
        "jan_aushadhi_available": "✅ Available",
        "manufacturing_tier": "WHO-GMP Certified",
        "regulatory_warnings": "Take with food. Do not crush SR tablets. Higher risk of stomach ulcers.",
        "safety_score": 90,
        "narrow_therapeutic_index": False,
        "substitution_safety": "🟡 YELLOW",
        "substitution_note": "SR formulation - ensure the generic is also a Sustained Release (SR) tablet.",
        "alternatives": [
            {
                "name": "Diclofenac SR",
                "type": "Jan Aushadhi",
                "salt_match": "100%",
                "dosage_match": "100% SR",
                "price": 14.0,
                "regulatory_badge": "NLEM",
                "manufacturer": "PMBJP",
            },
            {
                "name": "Dynapar SR",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100% SR",
                "price": 75.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Troikaa",
            },
            {
                "name": "Reactin SR",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100% SR",
                "price": 60.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Cipla",
            },
        ],
        "price_original": 95.0,
        "price_cheapest_safe": 14.0,
        "annual_savings_estimate": 972.0,
        "affordability_tier": "🟢 Very Affordable",
    },
    "taxim": {
        "brand_name": "Taxim-O 200",
        "active_ingredients": "Cefixime 200mg",
        "dosage_form": "Tablet",
        "therapeutic_category": "Antibiotic / Cephalosporin",
        "mechanism": "Kills bacteria by preventing them from forming their protective cell wall.",
        "standard_use": "Treats bacterial infections of the ear, lungs, throat, and urinary tract.",
        "cdsco_approved": True,
        "nlem_listed": False,
        "jan_aushadhi_available": "✅ Available",
        "manufacturing_tier": "WHO-GMP Certified",
        "regulatory_warnings": "Finish the prescribed course. Report any severe diarrhea.",
        "safety_score": 91,
        "narrow_therapeutic_index": False,
        "substitution_safety": "🟡 YELLOW",
        "substitution_note": "Antibiotic - substitution is fine, but verify the dose and complete the full course.",
        "alternatives": [
            {
                "name": "Cefixime (Gen)",
                "type": "Jan Aushadhi",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 35.0,
                "regulatory_badge": "Jan Aushadhi",
                "manufacturer": "PMBJP",
            },
            {
                "name": "Cefix 200",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 110.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Cipla",
            },
            {
                "name": "Zifi 200",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 125.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "FDC",
            },
        ],
        "price_original": 160.0,
        "price_cheapest_safe": 35.0,
        "annual_savings_estimate": 1500.0,
        "affordability_tier": "🟡 Moderately Affordable",
    },
    "dolo": {
        "brand_name": "Dolo 650",
        "active_ingredients": "Paracetamol 650mg",
        "dosage_form": "Tablet",
        "therapeutic_category": "Analgesic / Antipyretic",
        "mechanism": "Higher dose of paracetamol to reduce fever and pain.",
        "standard_use": "Used for moderate pain and high fever.",
        "cdsco_approved": True,
        "nlem_listed": True,
        "jan_aushadhi_available": "✅ Available",
        "manufacturing_tier": "WHO-GMP Certified",
        "regulatory_warnings": "Do not combine with other paracetamol products to avoid overdose.",
        "safety_score": 97,
        "narrow_therapeutic_index": False,
        "substitution_safety": "🟢 GREEN",
        "substitution_note": "Direct substitution safe. Equivalent to any Paracetamol 650mg.",
        "alternatives": [
            {
                "name": "Paracetamol 650",
                "type": "Jan Aushadhi",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 10.0,
                "regulatory_badge": "NLEM + Jan Aushadhi",
                "manufacturer": "PMBJP",
            },
            {
                "name": "Crocin 650",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 28.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "GSK",
            },
            {
                "name": "Pyrigesic 650",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 22.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "East India",
            },
        ],
        "price_original": 30.0,
        "price_cheapest_safe": 10.0,
        "annual_savings_estimate": 240.0,
        "affordability_tier": "🟢 Very Affordable",
    },
    "limcee": {
        "brand_name": "Limcee",
        "active_ingredients": "Vitamin C (Ascorbic Acid) 500mg",
        "dosage_form": "Chewable Tablet",
        "therapeutic_category": "Vitamin Supplement",
        "mechanism": "Provides essential Vitamin C for immune support and antioxidant effects.",
        "standard_use": "Vitamin C deficiency, immunity boosting. Chew completely before swallowing.",
        "cdsco_approved": True,
        "nlem_listed": False,
        "jan_aushadhi_available": "✅ Available",
        "manufacturing_tier": "WHO-GMP Certified",
        "regulatory_warnings": "Generally safe. High doses may cause stomach upset.",
        "safety_score": 99,
        "narrow_therapeutic_index": False,
        "substitution_safety": "🟢 GREEN",
        "substitution_note": "Direct substitution safe. Any Ascorbic acid 500mg generic is equivalent.",
        "alternatives": [
            {
                "name": "Vitamin C 500",
                "type": "Jan Aushadhi",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 8.0,
                "regulatory_badge": "Jan Aushadhi",
                "manufacturer": "PMBJP",
            },
            {
                "name": "Celin 500",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 20.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Koye",
            },
            {
                "name": "Sukcee 500",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 15.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Zydus",
            },
        ],
        "price_original": 25.0,
        "price_cheapest_safe": 8.0,
        "annual_savings_estimate": 204.0,
        "affordability_tier": "🟢 Very Affordable",
    },
    "azithral": {
        "brand_name": "Azithral 500",
        "active_ingredients": "Azithromycin 500mg",
        "dosage_form": "Tablet",
        "therapeutic_category": "Antibiotic / Macrolide",
        "mechanism": "Stops bacterial growth by interfering with their protein synthesis.",
        "standard_use": "Treats respiratory infections, skin infections, ear infections, and some STDs.",
        "cdsco_approved": True,
        "nlem_listed": True,
        "jan_aushadhi_available": "✅ Available",
        "manufacturing_tier": "WHO-GMP Certified",
        "regulatory_warnings": "Finish full 3 or 5 day course. May cause temporary stomach discomfort.",
        "safety_score": 91,
        "narrow_therapeutic_index": False,
        "substitution_safety": "🟡 YELLOW",
        "substitution_note": "Antibiotic - substitution is safe but must complete the full prescribed course.",
        "alternatives": [
            {
                "name": "Azithromycin 500",
                "type": "Jan Aushadhi",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 45.0,
                "regulatory_badge": "NLEM",
                "manufacturer": "PMBJP",
            },
            {
                "name": "Azee 500",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 105.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Cipla",
            },
            {
                "name": "Zithromax 500",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 115.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Pfizer",
            },
        ],
        "price_original": 120.0,
        "price_cheapest_safe": 45.0,
        "annual_savings_estimate": 900.0,
        "affordability_tier": "🟡 Moderately Affordable",
    },
    "thyronorm": {
        "brand_name": "Thyronorm 50",
        "active_ingredients": "Levothyroxine 50mcg",
        "dosage_form": "Tablet",
        "therapeutic_category": "Thyroid Hormone",
        "mechanism": "Replaces or provides more thyroid hormone, which is normally produced by the thyroid gland.",
        "standard_use": "Treats hypothyroidism. Taken empty stomach first thing in the morning.",
        "cdsco_approved": True,
        "nlem_listed": True,
        "jan_aushadhi_available": "✅ Available",
        "manufacturing_tier": "WHO-GMP Certified",
        "regulatory_warnings": "Requires regular TSH monitoring. DO NOT switch brands without consulting your doctor.",
        "safety_score": 85,
        "narrow_therapeutic_index": True,
        "substitution_safety": "🔴 RED",
        "substitution_note": "NARROW THERAPEUTIC INDEX: Even tiny dose variations between brands can affect TSH levels. Do NOT substitute without endocrinologist approval.",
        "alternatives": [
            {
                "name": "Levothyroxine 50",
                "type": "Jan Aushadhi",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 15.0,
                "regulatory_badge": "NLEM",
                "manufacturer": "PMBJP",
            },
            {
                "name": "Eltroxin 50",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 130.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "GSK",
            },
            {
                "name": "Thyrox 50",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 110.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Macleods",
            },
        ],
        "price_original": 140.0,
        "price_cheapest_safe": 15.0,
        "annual_savings_estimate": 1500.0,
        "affordability_tier": "🔴 High Caution",
    },
    "atorva": {
        "brand_name": "Atorva 10",
        "active_ingredients": "Atorvastatin 10mg",
        "dosage_form": "Tablet",
        "therapeutic_category": "Cholesterol / Statin",
        "mechanism": "Lowers bad cholesterol (LDL) and triglycerides by blocking a liver enzyme.",
        "standard_use": "Prevents cardiovascular disease and lowers cholesterol levels.",
        "cdsco_approved": True,
        "nlem_listed": True,
        "jan_aushadhi_available": "✅ Available",
        "manufacturing_tier": "WHO-GMP Certified",
        "regulatory_warnings": "Report any unexplained muscle pain. Avoid consuming large amounts of grapefruit juice.",
        "safety_score": 95,
        "narrow_therapeutic_index": False,
        "substitution_safety": "🟢 GREEN",
        "substitution_note": "Direct substitution safe. Generics provide equivalent cholesterol-lowering effects.",
        "alternatives": [
            {
                "name": "Atorvastatin 10",
                "type": "Jan Aushadhi",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 12.0,
                "regulatory_badge": "NLEM",
                "manufacturer": "PMBJP",
            },
            {
                "name": "Lipitor 10",
                "type": "Original Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 150.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Pfizer",
            },
            {
                "name": "Atorlip 10",
                "type": "Generic Brand",
                "salt_match": "100%",
                "dosage_match": "100%",
                "price": 60.0,
                "regulatory_badge": "CDSCO Approved",
                "manufacturer": "Cipla",
            },
        ],
        "price_original": 85.0,
        "price_cheapest_safe": 12.0,
        "annual_savings_estimate": 876.0,
        "affordability_tier": "🟢 Very Affordable",
    },
}


class MedicineState(rx.State):
    all_medicines: list[Medicine] = [
        {
            "id": "1",
            "brand_name": "Crocin",
            "generic_name": "Paracetamol",
            "salt_composition": "Paracetamol 500mg",
            "brand_price": 40.0,
            "generic_price": 12.0,
            "manufacturer": "GSK",
            "dosage": "Tablet",
            "verified": True,
            "category": "Analgesic",
            "expiry_date": "2025-08-15",
        },
        {
            "id": "2",
            "brand_name": "Augmentin 625",
            "generic_name": "Amoxycillin + Clavulanic Acid",
            "salt_composition": "Amoxycillin (500mg) + Clavulanic Acid (125mg)",
            "brand_price": 200.0,
            "generic_price": 85.0,
            "manufacturer": "GSK",
            "dosage": "Tablet",
            "verified": True,
            "category": "Antibiotic",
            "expiry_date": "2025-10-15",
        },
        {
            "id": "3",
            "brand_name": "Combiflam",
            "generic_name": "Ibuprofen + Paracetamol",
            "salt_composition": "Ibuprofen (400mg) + Paracetamol (325mg)",
            "brand_price": 45.0,
            "generic_price": 15.0,
            "manufacturer": "Sanofi",
            "dosage": "Tablet",
            "verified": True,
            "category": "Analgesic",
            "expiry_date": "2025-06-01",
        },
        {
            "id": "4",
            "brand_name": "Allegra 120mg",
            "generic_name": "Fexofenadine",
            "salt_composition": "Fexofenadine (120mg)",
            "brand_price": 180.0,
            "generic_price": 60.0,
            "manufacturer": "Sanofi",
            "dosage": "Tablet",
            "verified": True,
            "category": "Antihistamine",
            "expiry_date": "2025-12-01",
        },
        {
            "id": "5",
            "brand_name": "Pan 40",
            "generic_name": "Pantoprazole",
            "salt_composition": "Pantoprazole (40mg)",
            "brand_price": 150.0,
            "generic_price": 40.0,
            "manufacturer": "Alkem",
            "dosage": "Tablet",
            "verified": True,
            "category": "Antacid",
            "expiry_date": "2025-08-01",
        },
        {
            "id": "6",
            "brand_name": "Calpol 500",
            "generic_name": "Paracetamol",
            "salt_composition": "Paracetamol 500mg",
            "brand_price": 35.0,
            "generic_price": 12.0,
            "manufacturer": "GSK",
            "dosage": "Tablet",
            "verified": True,
            "category": "Analgesic",
            "expiry_date": "2026-03-20",
        },
        {
            "id": "7",
            "brand_name": "Glycomet 500",
            "generic_name": "Metformin",
            "salt_composition": "Metformin (500mg)",
            "brand_price": 60.0,
            "generic_price": 18.0,
            "manufacturer": "USV",
            "dosage": "Tablet",
            "verified": True,
            "category": "Anti-Diabetic",
            "expiry_date": "2025-08-20",
        },
        {
            "id": "8",
            "brand_name": "Telma 40",
            "generic_name": "Telmisartan",
            "salt_composition": "Telmisartan (40mg)",
            "brand_price": 110.0,
            "generic_price": 35.0,
            "manufacturer": "Glenmark",
            "dosage": "Tablet",
            "verified": True,
            "category": "Hypertension",
            "expiry_date": "2026-06-15",
        },
        {
            "id": "9",
            "brand_name": "Voveran SR 100",
            "generic_name": "Diclofenac",
            "salt_composition": "Diclofenac (100mg)",
            "brand_price": 95.0,
            "generic_price": 30.0,
            "manufacturer": "Novartis",
            "dosage": "Tablet",
            "verified": True,
            "category": "Pain Relief",
            "expiry_date": "2025-09-15",
        },
        {
            "id": "10",
            "brand_name": "Taxim-O 200",
            "generic_name": "Cefixime",
            "salt_composition": "Cefixime (200mg)",
            "brand_price": 160.0,
            "generic_price": 70.0,
            "manufacturer": "Alkem",
            "dosage": "Tablet",
            "verified": True,
            "category": "Antibiotic",
            "expiry_date": "2025-11-20",
        },
        {
            "id": "11",
            "brand_name": "Dolo 650",
            "generic_name": "Paracetamol",
            "salt_composition": "Paracetamol 650mg",
            "brand_price": 30.0,
            "generic_price": 15.0,
            "manufacturer": "Micro Labs",
            "dosage": "Tablet",
            "verified": True,
            "category": "Analgesic",
            "expiry_date": "2025-07-25",
        },
        {
            "id": "12",
            "brand_name": "Limcee",
            "generic_name": "Vitamin C",
            "salt_composition": "Vitamin C (500mg)",
            "brand_price": 25.0,
            "generic_price": 10.0,
            "manufacturer": "Abbott",
            "dosage": "Chewable Tablet",
            "verified": True,
            "category": "Vitamin",
            "expiry_date": "2026-12-31",
        },
        {
            "id": "13",
            "brand_name": "Azithral 500",
            "generic_name": "Azithromycin",
            "salt_composition": "Azithromycin (500mg)",
            "brand_price": 120.0,
            "generic_price": 55.0,
            "manufacturer": "Alembic",
            "dosage": "Tablet",
            "verified": True,
            "category": "Antibiotic",
            "expiry_date": "2025-10-10",
        },
        {
            "id": "14",
            "brand_name": "Thyronorm 50",
            "generic_name": "Levothyroxine",
            "salt_composition": "Levothyroxine (50mcg)",
            "brand_price": 140.0,
            "generic_price": 50.0,
            "manufacturer": "Abbott",
            "dosage": "Tablet",
            "verified": True,
            "category": "Thyroid",
            "expiry_date": "2026-01-15",
        },
        {
            "id": "15",
            "brand_name": "Atorva 10",
            "generic_name": "Atorvastatin",
            "salt_composition": "Atorvastatin (10mg)",
            "brand_price": 85.0,
            "generic_price": 25.0,
            "manufacturer": "Zydus",
            "dosage": "Tablet",
            "verified": True,
            "category": "Cholesterol",
            "expiry_date": "2026-05-10",
        },
    ]
    search_query: str = ""
    selected_medicine_id: str = ""
    is_menu_open: bool = False
    is_processing: bool = False
    ocr_progress: int = 0
    ocr_complete: bool = False
    processing_step: str = ""
    extracted_medicines: list[ExtractedMedicine] = []

    @rx.var
    def total_savings(self) -> float:
        total = 0.0
        for med in self.extracted_medicines:
            total += med["brand_price"] - med["generic_price"]
        return round(total, 2)

    @rx.var
    def items_needing_review(self) -> int:
        return sum(
            (1 for med in self.extracted_medicines if med.get("needs_review", False))
        )

    def _get_expiry_status(self, expiry_date_str: str) -> dict[str, str | int]:
        try:
            expiry = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
            today = date.today()
            delta = (expiry - today).days
            if delta <= 0:
                return {"days_left": delta, "status": "expired", "label": "Expired"}
            elif delta <= 30:
                return {
                    "days_left": delta,
                    "status": "critical",
                    "label": f"{delta} days left",
                }
            elif delta <= 90:
                return {
                    "days_left": delta,
                    "status": "warning",
                    "label": f"{delta} days left",
                }
            else:
                return {"days_left": delta, "status": "good", "label": "Safe to use"}
        except Exception:
            logging.exception("Unexpected error")
            return {"days_left": 0, "status": "unknown", "label": "Unknown"}

    @rx.var
    def expiring_soon_medicines(self) -> list[Medicine]:
        today = date.today()
        results = []
        for m in self.all_medicines:
            try:
                expiry = datetime.strptime(m["expiry_date"], "%Y-%m-%d").date()
                delta = (expiry - today).days
                if 0 < delta <= 90:
                    results.append(m)
            except Exception:
                logging.exception("Unexpected error")
                continue
        return results[:6]

    @rx.var
    def search_results(self) -> list[Medicine]:
        if not self.search_query:
            return []
        q = self.search_query.lower()
        return [
            m
            for m in self.all_medicines
            if q in m["brand_name"].lower()
            or q in m["generic_name"].lower()
            or q in m["salt_composition"].lower()
        ][:5]

    @rx.var
    def filtered_alternatives(self) -> list[Medicine]:
        if not self.selected_medicine_id:
            return []
        selected = next(
            (m for m in self.all_medicines if m["id"] == self.selected_medicine_id),
            None,
        )
        if not selected:
            return []
        return [
            m
            for m in self.all_medicines
            if (
                m["generic_name"] == selected["generic_name"]
                or m["salt_composition"] == selected["salt_composition"]
            )
            and m["id"] != self.selected_medicine_id
        ]

    @rx.var
    def selected_medicine(self) -> Optional[Medicine]:
        if not self.selected_medicine_id:
            return None
        return next(
            (m for m in self.all_medicines if m["id"] == self.selected_medicine_id),
            None,
        )

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def select_medicine(self, med_id: str):
        self.selected_medicine_id = med_id
        self.search_query = ""
        return rx.redirect("/results")

    @rx.event
    def toggle_menu(self):
        self.is_menu_open = not self.is_menu_open

    @rx.event
    def go_home(self):
        self.selected_medicine_id = ""
        self.search_query = ""
        return rx.redirect("/")

    @rx.event
    async def analyze_prescription(self):
        self.is_processing = True
        self.ocr_complete = False
        self.extracted_medicines = []
        self.processing_step = "Uploading image..."
        for i in range(0, 21, 10):
            self.ocr_progress = i
            yield
            await asyncio.sleep(0.2)
        self.processing_step = "Running OCR text recognition..."
        for i in range(20, 41, 10):
            self.ocr_progress = i
            yield
            await asyncio.sleep(0.2)
        self.processing_step = "Identifying medicine names and dosages..."
        for i in range(40, 61, 10):
            self.ocr_progress = i
            yield
            await asyncio.sleep(0.2)
        self.processing_step = "Scoring extraction confidence..."
        for i in range(60, 76, 5):
            self.ocr_progress = i
            yield
            await asyncio.sleep(0.15)
        self.processing_step = "Matching verified generic alternatives..."
        for i in range(75, 91, 5):
            self.ocr_progress = i
            yield
            await asyncio.sleep(0.15)
        self.processing_step = "Computing price comparisons..."
        for i in range(90, 101, 5):
            self.ocr_progress = i
            yield
            await asyncio.sleep(0.15)
        self.extracted_medicines = [
            {
                "name": "Augmentin 625 Duo",
                "confidence": 96,
                "matched_id": "2",
                "generic_name": "Amoxycillin + Clavulanic Acid",
                "salt_composition": "Amoxycillin (500mg) + Clavulanic Acid (125mg)",
                "brand_price": 200.0,
                "generic_price": 85.0,
                "expiry_date": "2025-10-15",
                "dosage": "625mg",
                "frequency": "Twice daily (BD)",
                "duration": "7 days",
                "needs_review": False,
                "review_reason": "",
            },
            {
                "name": "Pan 40",
                "confidence": 93,
                "matched_id": "5",
                "generic_name": "Pantoprazole",
                "salt_composition": "Pantoprazole (40mg)",
                "brand_price": 150.0,
                "generic_price": 40.0,
                "expiry_date": "2025-08-01",
                "dosage": "40mg",
                "frequency": "Once daily before breakfast (OD AC)",
                "duration": "14 days",
                "needs_review": False,
                "review_reason": "",
            },
            {
                "name": "Crocin 500",
                "confidence": 91,
                "matched_id": "1",
                "generic_name": "Paracetamol",
                "salt_composition": "Paracetamol 500mg",
                "brand_price": 40.0,
                "generic_price": 12.0,
                "expiry_date": "2025-08-15",
                "dosage": "500mg",
                "frequency": "Three times daily (TDS) SOS",
                "duration": "As needed",
                "needs_review": False,
                "review_reason": "",
            },
            {
                "name": "Allegra 120",
                "confidence": 89,
                "matched_id": "4",
                "generic_name": "Fexofenadine",
                "salt_composition": "Fexofenadine (120mg)",
                "brand_price": 180.0,
                "generic_price": 60.0,
                "expiry_date": "2025-12-01",
                "dosage": "120mg",
                "frequency": "Once daily (OD)",
                "duration": "10 days",
                "needs_review": False,
                "review_reason": "",
            },
            {
                "name": "Glycomet GP 0.5",
                "confidence": 78,
                "matched_id": "7",
                "generic_name": "Metformin",
                "salt_composition": "Metformin (500mg)",
                "brand_price": 60.0,
                "generic_price": 18.0,
                "expiry_date": "2025-08-20",
                "dosage": "500mg",
                "frequency": "Twice daily with meals (BD PC)",
                "duration": "Ongoing",
                "needs_review": True,
                "review_reason": "Low OCR confidence — handwriting partially unclear. Verify: is this Glycomet GP 0.5 or Glycomet SR 500?",
            },
            {
                "name": "Wnlok-D3 60K",
                "confidence": 62,
                "matched_id": "",
                "generic_name": "Cholecalciferol (Vitamin D3)",
                "salt_composition": "Cholecalciferol 60,000 IU",
                "brand_price": 120.0,
                "generic_price": 45.0,
                "expiry_date": "2026-06-01",
                "dosage": "60,000 IU",
                "frequency": "Once weekly",
                "duration": "8 weeks",
                "needs_review": True,
                "review_reason": "Unclear handwriting — brand name uncertain. Could be 'Uprise-D3 60K' or 'Wnlok-D3 60K'. Please verify with pharmacist.",
            },
        ]
        self.is_processing = False
        self.ocr_complete = True

    @rx.event
    def reset_upload(self):
        self.ocr_complete = False
        self.ocr_progress = 0
        self.extracted_medicines = []
        self.is_processing = False
        return rx.clear_selected_files("prescription_upload")

    @rx.event
    def get_savings_amt(self, med: Medicine) -> float:
        return med["brand_price"] - med["generic_price"]

    @rx.event
    def get_savings_pct(self, med: Medicine) -> float:
        if med["brand_price"] == 0:
            return 0
        return round(
            (med["brand_price"] - med["generic_price"]) / med["brand_price"] * 100, 1
        )