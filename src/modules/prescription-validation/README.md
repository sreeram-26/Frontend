# Module 20 — Prescription Validation & Consistency System

**Category D: Drug & Prescription Safety Systems**
**Course:** Database Management Systems (DBMS) — IIT(ISM)
**Module:** 20

---

## Team Members
1. [Member 1 Name] — [GitHub ID]
2. [Member 2 Name] — [GitHub ID]
3. [Member 3 Name] — [GitHub ID]

---

## Overview
This module implements a Prescription Validation & Consistency System that:
- Validates prescriptions against drug master rules
- Detects violations (dosage, frequency, route, duration)
- Generates compliance reports and scores
- Simulates SQL Triggers and Stored Procedures
- Provides a full dashboard UI

---

## Tech Stack
- **Backend:** Flask (Python)
- **Database:** MongoDB
- **Frontend:** HTML/CSS/JS

---

## Setup & Run

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Install dependencies
pip install flask pymongo

# 3. Seed the database
python3 seed.py

# 4. Run the app
python3 app.py

# 5. Open browser
# http://localhost:5000
```

---

## Features
- Prescription error checking
- Dosage calculation validation
- Frequency and duration consistency checks
- Guideline compliance reports
- Therapeutic substitution suggestions
- Triggers and stored procedures simulation
- Doctor compliance scoring

---

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/prescriptions | All prescriptions |
| POST | /api/audit/run | Run full audit |
| GET | /api/violations | All violations |
| GET | /api/compliance | Compliance reports |
| GET | /api/drugs | Drug master |
| GET | /api/guidelines | Clinical guidelines |
| GET | /api/substitutions | Therapeutic substitutions |
| GET | /api/audit/logs | Audit trail |
