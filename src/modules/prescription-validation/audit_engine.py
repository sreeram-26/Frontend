from db import prescriptions_col, violations_col, compliance_col, audit_logs_col
from datetime import datetime

def validate_prescription(prescription):
    violations = []
    items = prescription.get("items", [])
    total_checks = 0
    passed_checks = 0
    for item in items:
        drug_name = item.get("drug_name", "Unknown")
        dosage = item.get("dosage_amount", 0)
        max_dose = item.get("max_dose", 9999)
        frequency = item.get("frequency", "")
        allowed_freqs = item.get("allowed_frequencies", [])
        route = item.get("route", "")
        allowed_routes = item.get("allowed_routes", [])
        duration = item.get("duration_days", 0)
        max_duration = item.get("max_duration_days", 365)
        total_checks += 1
        if dosage > max_dose:
            violations.append({"type": "DOSAGE_EXCEEDED", "drug": drug_name, "detail": f"Prescribed {dosage}{item.get('unit','mg')} exceeds max {max_dose}{item.get('unit','mg')}", "severity": "HIGH"})
        else:
            passed_checks += 1
        total_checks += 1
        if frequency not in allowed_freqs:
            violations.append({"type": "INVALID_FREQUENCY", "drug": drug_name, "detail": f"Frequency '{frequency}' not allowed. Allowed: {', '.join(allowed_freqs)}", "severity": "MEDIUM"})
        else:
            passed_checks += 1
        total_checks += 1
        if route not in allowed_routes:
            violations.append({"type": "INVALID_ROUTE", "drug": drug_name, "detail": f"Route '{route}' not allowed. Allowed: {', '.join(allowed_routes)}", "severity": "MEDIUM"})
        else:
            passed_checks += 1
        total_checks += 1
        if duration > max_duration:
            violations.append({"type": "EXCESSIVE_DURATION", "drug": drug_name, "detail": f"Duration {duration} days exceeds max {max_duration} days", "severity": "LOW"})
        else:
            passed_checks += 1
    compliance_score = round((passed_checks / total_checks) * 100, 2) if total_checks > 0 else 100.0
    return violations, compliance_score

def run_audit(prescription_id=None):
    rxs = list(prescriptions_col.find({"prescription_id": prescription_id})) if prescription_id else list(prescriptions_col.find())
    results = []
    for rx in rxs:
        violations, score = validate_prescription(rx)
        if violations:
            for v in violations:
                v["prescription_id"] = rx["prescription_id"]
                v["patient_name"] = rx.get("patient_name", "")
                v["doctor_name"] = rx.get("doctor_name", "")
                v["detected_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            violations_col.delete_many({"prescription_id": rx["prescription_id"]})
            violations_col.insert_many(violations)
        report = {"prescription_id": rx["prescription_id"], "patient_name": rx.get("patient_name",""), "doctor_name": rx.get("doctor_name",""), "compliance_score": score, "total_violations": len(violations), "audited_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "status": "PASS" if score >= 75 else "FAIL"}
        compliance_col.delete_many({"prescription_id": rx["prescription_id"]})
        compliance_col.insert_one(report)
        audit_logs_col.insert_one({"action": "AUDIT_RUN", "prescription_id": rx["prescription_id"], "compliance_score": score, "violations_found": len(violations), "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        prescriptions_col.update_one({"prescription_id": rx["prescription_id"]}, {"$set": {"status": "flagged" if score < 75 else rx.get("status","active"), "last_audited": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}})
        results.append({"prescription_id": rx["prescription_id"], "patient": rx.get("patient_name"), "score": score, "violations": len(violations), "status": report["status"]})
    return results
