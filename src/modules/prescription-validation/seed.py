from db import prescriptions_col, drugs_col, guidelines_col, violations_col, compliance_col, substitutions_col, audit_logs_col
from datetime import datetime, timedelta
import random

def seed():
    prescriptions_col.drop()
    drugs_col.drop()
    guidelines_col.drop()
    violations_col.drop()
    compliance_col.drop()
    substitutions_col.drop()
    audit_logs_col.drop()

    drugs = [
        {"drug_id":"D001","drug_name":"Amoxicillin","max_dose":500,"unit":"mg","allowed_routes":["oral"],"allowed_frequencies":["TDS","BD"],"max_duration_days":14},
        {"drug_id":"D002","drug_name":"Metformin","max_dose":1000,"unit":"mg","allowed_routes":["oral"],"allowed_frequencies":["BD","OD"],"max_duration_days":365},
        {"drug_id":"D003","drug_name":"Atorvastatin","max_dose":80,"unit":"mg","allowed_routes":["oral"],"allowed_frequencies":["OD"],"max_duration_days":365},
        {"drug_id":"D004","drug_name":"Paracetamol","max_dose":1000,"unit":"mg","allowed_routes":["oral","IV"],"allowed_frequencies":["QID","TDS","BD","OD"],"max_duration_days":7},
        {"drug_id":"D005","drug_name":"Ciprofloxacin","max_dose":500,"unit":"mg","allowed_routes":["oral","IV"],"allowed_frequencies":["BD"],"max_duration_days":14},
        {"drug_id":"D006","drug_name":"Aspirin","max_dose":300,"unit":"mg","allowed_routes":["oral"],"allowed_frequencies":["OD","BD"],"max_duration_days":365},
        {"drug_id":"D007","drug_name":"Omeprazole","max_dose":40,"unit":"mg","allowed_routes":["oral","IV"],"allowed_frequencies":["OD","BD"],"max_duration_days":30},
        {"drug_id":"D008","drug_name":"Amlodipine","max_dose":10,"unit":"mg","allowed_routes":["oral"],"allowed_frequencies":["OD"],"max_duration_days":365},
        {"drug_id":"D009","drug_name":"Azithromycin","max_dose":500,"unit":"mg","allowed_routes":["oral","IV"],"allowed_frequencies":["OD"],"max_duration_days":5},
        {"drug_id":"D010","drug_name":"Metoprolol","max_dose":100,"unit":"mg","allowed_routes":["oral"],"allowed_frequencies":["BD","OD"],"max_duration_days":365},
        {"drug_id":"D011","drug_name":"Lisinopril","max_dose":40,"unit":"mg","allowed_routes":["oral"],"allowed_frequencies":["OD"],"max_duration_days":365},
        {"drug_id":"D012","drug_name":"Warfarin","max_dose":10,"unit":"mg","allowed_routes":["oral"],"allowed_frequencies":["OD"],"max_duration_days":365},
        {"drug_id":"D013","drug_name":"Insulin Glargine","max_dose":50,"unit":"units","allowed_routes":["subcutaneous"],"allowed_frequencies":["OD"],"max_duration_days":365},
        {"drug_id":"D014","drug_name":"Salbutamol","max_dose":4,"unit":"mg","allowed_routes":["oral","inhaled"],"allowed_frequencies":["TDS","QID","BD"],"max_duration_days":30},
        {"drug_id":"D015","drug_name":"Prednisolone","max_dose":60,"unit":"mg","allowed_routes":["oral","IV"],"allowed_frequencies":["OD","BD"],"max_duration_days":14},
        {"drug_id":"D016","drug_name":"Ceftriaxone","max_dose":2000,"unit":"mg","allowed_routes":["IV","IM"],"allowed_frequencies":["OD","BD"],"max_duration_days":14},
        {"drug_id":"D017","drug_name":"Pantoprazole","max_dose":40,"unit":"mg","allowed_routes":["oral","IV"],"allowed_frequencies":["OD","BD"],"max_duration_days":30},
        {"drug_id":"D018","drug_name":"Furosemide","max_dose":80,"unit":"mg","allowed_routes":["oral","IV"],"allowed_frequencies":["OD","BD"],"max_duration_days":30},
        {"drug_id":"D019","drug_name":"Diazepam","max_dose":10,"unit":"mg","allowed_routes":["oral","IV"],"allowed_frequencies":["TDS","BD","OD"],"max_duration_days":7},
        {"drug_id":"D020","drug_name":"Morphine","max_dose":15,"unit":"mg","allowed_routes":["IV","IM","oral"],"allowed_frequencies":["QID","TDS"],"max_duration_days":7},
        {"drug_id":"D021","drug_name":"Doxycycline","max_dose":200,"unit":"mg","allowed_routes":["oral"],"allowed_frequencies":["OD","BD"],"max_duration_days":21},
        {"drug_id":"D022","drug_name":"Ramipril","max_dose":10,"unit":"mg","allowed_routes":["oral"],"allowed_frequencies":["OD"],"max_duration_days":365},
        {"drug_id":"D023","drug_name":"Glibenclamide","max_dose":15,"unit":"mg","allowed_routes":["oral"],"allowed_frequencies":["OD","BD"],"max_duration_days":365},
        {"drug_id":"D024","drug_name":"Ibuprofen","max_dose":800,"unit":"mg","allowed_routes":["oral"],"allowed_frequencies":["TDS","BD"],"max_duration_days":7},
        {"drug_id":"D025","drug_name":"Cetirizine","max_dose":10,"unit":"mg","allowed_routes":["oral"],"allowed_frequencies":["OD"],"max_duration_days":14},
    ]
    drugs_col.insert_many(drugs)

    guidelines_col.insert_many([
        {"guideline_id":"G001","source":"National","drug_id":"D001","rule":"Amoxicillin dose must not exceed 500mg per dose","version":"1.2"},
        {"guideline_id":"G002","source":"Institutional","drug_id":"D002","rule":"Metformin max dose 1000mg BD for T2DM","version":"2.0"},
        {"guideline_id":"G003","source":"Specialty-specific","drug_id":"D003","rule":"Atorvastatin once daily, dose adjusted per LDL","version":"1.0"},
        {"guideline_id":"G004","source":"National","drug_id":"D004","rule":"Paracetamol should not exceed 4g/day total","version":"3.1"},
        {"guideline_id":"G005","source":"National","drug_id":"D005","rule":"Ciprofloxacin only for confirmed bacterial infection","version":"1.5"},
        {"guideline_id":"G006","source":"Institutional","drug_id":"D012","rule":"Warfarin requires INR monitoring every 2 weeks","version":"2.1"},
        {"guideline_id":"G007","source":"National","drug_id":"D016","rule":"Ceftriaxone IV only in hospital setting","version":"1.0"},
        {"guideline_id":"G008","source":"Specialty-specific","drug_id":"D013","rule":"Insulin dose must be individualized per blood glucose","version":"3.0"},
        {"guideline_id":"G009","source":"National","drug_id":"D020","rule":"Morphine restricted to severe pain only with monitoring","version":"2.2"},
        {"guideline_id":"G010","source":"Institutional","drug_id":"D019","rule":"Diazepam max 7 days to avoid dependence","version":"1.1"},
        {"guideline_id":"G011","source":"National","drug_id":"D015","rule":"Prednisolone taper required for courses over 7 days","version":"1.3"},
        {"guideline_id":"G012","source":"Specialty-specific","drug_id":"D010","rule":"Metoprolol dose titrated based on heart rate response","version":"2.0"},
        {"guideline_id":"G013","source":"National","drug_id":"D018","rule":"Furosemide IV only in acute decompensated heart failure","version":"1.4"},
        {"guideline_id":"G014","source":"Institutional","drug_id":"D024","rule":"Ibuprofen avoided in renal impairment and elderly","version":"1.0"},
        {"guideline_id":"G015","source":"National","drug_id":"D009","rule":"Azithromycin 5 day course only, not to be extended","version":"1.2"},
    ])

    substitutions_col.insert_many([
        {"substitution_id":"S001","original_drug":"Amoxicillin","substitute_drug":"Azithromycin","reason":"Penicillin allergy"},
        {"substitution_id":"S002","original_drug":"Ciprofloxacin","substitute_drug":"Levofloxacin","reason":"Resistance pattern"},
        {"substitution_id":"S003","original_drug":"Atorvastatin","substitute_drug":"Rosuvastatin","reason":"Cost-effectiveness"},
        {"substitution_id":"S004","original_drug":"Amlodipine","substitute_drug":"Nifedipine","reason":"Side effect profile"},
        {"substitution_id":"S005","original_drug":"Metformin","substitute_drug":"Glibenclamide","reason":"Renal impairment"},
        {"substitution_id":"S006","original_drug":"Warfarin","substitute_drug":"Rivaroxaban","reason":"Better safety profile"},
        {"substitution_id":"S007","original_drug":"Ibuprofen","substitute_drug":"Paracetamol","reason":"Renal/GI risk"},
        {"substitution_id":"S008","original_drug":"Diazepam","substitute_drug":"Lorazepam","reason":"Shorter acting preferred"},
        {"substitution_id":"S009","original_drug":"Morphine","substitute_drug":"Tramadol","reason":"Lower dependence risk"},
        {"substitution_id":"S010","original_drug":"Prednisolone","substitute_drug":"Budesonide","reason":"Fewer systemic effects"},
    ])

    doctors = [
        "Dr. Sharma", "Dr. Patel", "Dr. Reddy", "Dr. Gupta", "Dr. Singh",
        "Dr. Mehta", "Dr. Joshi", "Dr. Rao", "Dr. Nair", "Dr. Kumar",
        "Dr. Verma", "Dr. Das", "Dr. Pillai", "Dr. Bose", "Dr. Iyer"
    ]

    patients = [
        "Rahul Verma","Priya Nair","Amit Kumar","Sunita Das","Rajesh Mehta",
        "Kavita Joshi","Suresh Rao","Anita Bose","Vikram Singh","Meena Pillai",
        "Arjun Sharma","Deepa Patel","Rohit Gupta","Sneha Reddy","Manoj Iyer",
        "Pooja Verma","Sanjay Kumar","Lakshmi Rao","Arun Nair","Divya Mehta",
        "Kiran Das","Ravi Pillai","Smita Joshi","Nikhil Bose","Anjali Singh",
        "Prakash Sharma","Rekha Patel","Vijay Gupta","Usha Reddy","Mohan Iyer",
        "Swati Verma","Dinesh Kumar","Padma Rao","Sunil Nair","Geeta Mehta",
        "Harish Das","Savita Pillai","Ramesh Joshi","Nisha Bose","Ajay Singh",
        "Bhavna Sharma","Suresh Patel","Asha Gupta","Kishore Reddy","Madhuri Iyer",
        "Tarun Verma","Sunita Kumar","Gopal Rao","Bindu Nair","Ashok Mehta",
    ]

    prescriptions = []
    for i, patient_name in enumerate(patients):
        num_items = random.randint(1, 4)
        selected_drugs = random.sample(drugs, num_items)
        items = []
        for drug in selected_drugs:
            overdose = random.choice([True, False, False, False])
            wrong_route = random.choice([True, False, False, False])
            wrong_freq = random.choice([True, False, False, False])
            long_duration = random.choice([True, False, False, False])
            dosage = drug["max_dose"] + 200 if overdose else drug["max_dose"] - int(drug["max_dose"]*0.2)
            route = "IM" if wrong_route else random.choice(drug["allowed_routes"])
            frequency = "TDS" if wrong_freq and "TDS" not in drug["allowed_frequencies"] else random.choice(drug["allowed_frequencies"])
            duration = drug["max_duration_days"] + 10 if long_duration else random.randint(3, drug["max_duration_days"])
            items.append({
                "item_id": f"ITEM{i+1}{drug['drug_id']}",
                "drug_id": drug["drug_id"],
                "drug_name": drug["drug_name"],
                "dosage_amount": dosage,
                "unit": drug["unit"],
                "frequency": frequency,
                "duration_days": duration,
                "route": route,
                "max_dose": drug["max_dose"],
                "allowed_routes": drug["allowed_routes"],
                "allowed_frequencies": drug["allowed_frequencies"],
                "max_duration_days": drug["max_duration_days"],
            })
        issued = (datetime.now() - timedelta(days=random.randint(0,60))).strftime("%Y-%m-%d")
        prescriptions.append({
            "prescription_id": f"RX{str(i+1).zfill(4)}",
            "patient_id": f"P{str(i+1).zfill(3)}",
            "patient_name": patient_name,
            "doctor_name": doctors[i % len(doctors)],
            "issued_at": issued,
            "status": "active",
            "items": items
        })

    prescriptions_col.insert_many(prescriptions)
    print(f"Seeded {len(drugs)} drugs")
    print(f"Seeded 15 guidelines")
    print(f"Seeded 10 substitutions")
    print(f"Seeded {len(prescriptions)} prescriptions")
    print("Done!")

if __name__ == "__main__":
    seed()
