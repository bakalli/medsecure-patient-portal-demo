"""
app.py — MedSecure Patient Portal
===================================
MedSecure Patient Portal application for managing patient records,
medical device inventory, and HIPAA-compliant audit logging.

Modules:
  - patient_records: Patient record CRUD and search
  - device_api: Medical device management and diagnostics
  - audit_log: HIPAA audit trail and SIEM integration
"""

import sqlite3
import os

from flask import Flask

app = Flask(__name__)
DATABASE = "medsecure.db"


def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DATABASE)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_of_birth TEXT,
            ssn TEXT,
            medical_record_number TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT UNIQUE NOT NULL,
            device_type TEXT,
            location TEXT,
            firmware_version TEXT,
            last_calibration TEXT
        );

        CREATE TABLE IF NOT EXISTS audit_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            user TEXT,
            action TEXT,
            resource TEXT,
            details TEXT
        );
    """)
    conn.close()


from patient_records import app as patient_app
from device_api import app as device_app
from audit_log import app as audit_app


@app.route("/health")
def health():
    return {"status": "ok", "service": "medsecure-patient-portal"}


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
