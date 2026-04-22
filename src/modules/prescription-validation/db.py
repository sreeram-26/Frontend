from pymongo import MongoClient
import certifi

client = MongoClient(
    "mongodb+srv://admin:1234@cluster0.fxqzayh.mongodb.net/?appName=Cluster0",
    tlsCAFile=certifi.where()
)
db = client["prescription_validation_db"]

prescriptions_col = db["prescriptions"]
drugs_col = db["drugs"]
guidelines_col = db["guidelines"]
violations_col = db["violations"]
compliance_col = db["compliance_reports"]
substitutions_col = db["therapeutic_substitutions"]
audit_logs_col = db["audit_logs"]
