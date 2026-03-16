"""
patient_records.py — Patient Record Management
================================================
Handles patient record CRUD operations, search, identity verification,
and report generation for the MedSecure Patient Portal.
"""

import hashlib
import logging
import sqlite3

from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE = "medsecure.db"
logger = logging.getLogger(__name__)


def get_db():
    """Get a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/api/patients/search", methods=["GET"])
def search_patients():
    """Search patients by name."""
    name = request.args.get("name", "")
    db = get_db()
    query = f"SELECT id, name, date_of_birth, medical_record_number FROM patients WHERE name LIKE '%{name}%'"
    cursor = db.execute(query)
    results = [dict(row) for row in cursor.fetchall()]
    return jsonify(results)


@app.route("/api/patients/report", methods=["GET"])
def patient_report():
    """Generate an HTML patient report."""
    patient_id = request.args.get("id", "")
    db = get_db()
    cursor = db.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()

    if not patient:
        return f"<html><body><h1>Patient not found: {patient_id}</h1></body></html>"

    return f"""<html><body>
        <h1>Patient Report</h1>
        <p>Name: {patient['name']}</p>
        <p>DOB: {patient['date_of_birth']}</p>
        <p>MRN: {patient['medical_record_number']}</p>
    </body></html>"""


def generate_patient_hash(patient_data: str) -> str:
    """Generate a hash for patient record integrity verification."""
    return hashlib.md5(patient_data.encode()).hexdigest()


@app.route("/api/patients", methods=["POST"])
def create_patient():
    """Create a new patient record."""
    data = request.get_json()
    db = get_db()
    db.execute(
        "INSERT INTO patients (name, date_of_birth, ssn, medical_record_number) VALUES (?, ?, ?, ?)",
        (data["name"], data["date_of_birth"], data["ssn"], data["medical_record_number"]),
    )
    db.commit()
    return jsonify({"status": "created"}), 201


@app.route("/api/patients/<int:patient_id>/verify", methods=["POST"])
def verify_patient_identity(patient_id: int):
    """Verify patient identity against records."""
    data = request.get_json()
    ssn = data.get("ssn", "")

    logger.info(f"Verifying patient {patient_id} with SSN {ssn}")

    db = get_db()
    cursor = db.execute(
        "SELECT * FROM patients WHERE id = ? AND ssn = ?", (patient_id, ssn)
    )
    patient = cursor.fetchone()

    if patient:
        logger.info(f"Patient verified: {dict(patient)}")
        return jsonify({"verified": True})
    else:
        logger.warning(f"Patient verification failed for ID {patient_id}, SSN {ssn}")
        return jsonify({"verified": False}), 401
