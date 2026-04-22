from flask import Flask, render_template, jsonify, request
from db import prescriptions_col, drugs_col, guidelines_col, violations_col, compliance_col, substitutions_col, audit_logs_col
from audit_engine import run_audit
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/prescriptions", methods=["GET"])
def get_prescriptions():
    return jsonify(list(prescriptions_col.find({}, {"_id": 0})))

@app.route("/api/prescriptions", methods=["POST"])
def add_prescription():
    data = request.json
    data["issued_at"] = datetime.now().strftime("%Y-%m-%d")
    data["status"] = "active"
    prescriptions_col.insert_one(data)
    run_audit(data["prescription_id"])
    return jsonify({"message": "Added and audited", "prescription_id": data["prescription_id"]}), 201

@app.route("/api/audit/run", methods=["POST"])
def trigger_audit():
    rx_id = request.json.get("prescription_id") if request.json else None
    results = run_audit(rx_id)
    return jsonify({"message": "Audit complete", "results": results})

@app.route("/api/audit/logs", methods=["GET"])
def get_audit_logs():
    return jsonify(list(audit_logs_col.find({}, {"_id": 0}).sort("timestamp", -1).limit(50)))

@app.route("/api/violations", methods=["GET"])
def get_violations():
    return jsonify(list(violations_col.find({}, {"_id": 0})))

@app.route("/api/violations/summary", methods=["GET"])
def violations_summary():
    return jsonify(list(violations_col.aggregate([{"$group": {"_id": "$type", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])))

@app.route("/api/violations/by-severity", methods=["GET"])
def violations_by_severity():
    return jsonify(list(violations_col.aggregate([{"$group": {"_id": "$severity", "count": {"$sum": 1}}}])))

@app.route("/api/compliance", methods=["GET"])
def get_compliance():
    return jsonify(list(compliance_col.find({}, {"_id": 0}).sort("compliance_score", 1)))

@app.route("/api/compliance/stats", methods=["GET"])
def compliance_stats():
    all_reports = list(compliance_col.find({}, {"_id": 0}))
    if not all_reports:
        return jsonify({"avg_score": 0, "pass_count": 0, "fail_count": 0, "total": 0})
    scores = [r["compliance_score"] for r in all_reports]
    avg = round(sum(scores) / len(scores), 2)
    pass_count = sum(1 for r in all_reports if r["status"] == "PASS")
    return jsonify({"avg_score": avg, "pass_count": pass_count, "fail_count": len(all_reports) - pass_count, "total": len(all_reports)})

@app.route("/api/drugs", methods=["GET"])
def get_drugs():
    return jsonify(list(drugs_col.find({}, {"_id": 0})))

@app.route("/api/guidelines", methods=["GET"])
def get_guidelines():
    return jsonify(list(guidelines_col.find({}, {"_id": 0})))

@app.route("/api/substitutions", methods=["GET"])
def get_substitutions():
    return jsonify(list(substitutions_col.find({}, {"_id": 0})))

@app.route("/api/queries/showcase", methods=["GET"])
def queries_showcase():
    return jsonify([
        {"name": "Find all flagged prescriptions", "query": "db.prescriptions.find({ \"status\": \"flagged\" })", "type": "SELECT", "result_count": prescriptions_col.count_documents({"status": "flagged"})},
        {"name": "Prescriptions with dosage violations", "query": "db.violations.find({ \"type\": \"DOSAGE_EXCEEDED\" })", "type": "SELECT", "result_count": violations_col.count_documents({"type": "DOSAGE_EXCEEDED"})},
        {"name": "Average compliance score per doctor", "query": "db.compliance_reports.aggregate([{ $group: { _id: \"$doctor_name\", avg_score: { $avg: \"$compliance_score\" } } }])", "type": "AGGREGATE", "result_count": len(compliance_col.distinct("doctor_name"))},
        {"name": "High severity violations", "query": "db.violations.find({ \"severity\": \"HIGH\" }).sort({ \"detected_at\": -1 })", "type": "SELECT", "result_count": violations_col.count_documents({"severity": "HIGH"})},
        {"name": "Compliance PASS/FAIL count", "query": "db.compliance_reports.aggregate([{ $group: { _id: \"$status\", count: { $sum: 1 } } }])", "type": "AGGREGATE", "result_count": compliance_col.count_documents({})},
        {"name": "Violations grouped by type", "query": "db.violations.aggregate([{ $group: { _id: \"$type\", count: { $sum: 1 } } }, { $sort: { count: -1 } }])", "type": "AGGREGATE", "result_count": len(violations_col.distinct("type"))},
    ])

@app.route("/api/doctor-scores", methods=["GET"])
def doctor_scores():
    pipeline = [{"$group": {"_id": "$doctor_name", "avg_score": {"$avg": "$compliance_score"}, "total": {"$sum": 1}, "violations": {"$sum": "$total_violations"}}}, {"$sort": {"avg_score": -1}}]
    result = list(compliance_col.aggregate(pipeline))
    for r in result:
        r["avg_score"] = round(r["avg_score"], 1)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
