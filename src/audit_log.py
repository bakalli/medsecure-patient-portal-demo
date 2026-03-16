"""
audit_log.py — Audit Logging System
=====================================
HIPAA-compliant audit logging system for tracking access to patient records,
device operations, and administrative actions.
"""

import logging
import os

import requests as http_requests
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
AUDIT_LOG_DIR = "/var/log/medsecure/audit"
audit_logger = logging.getLogger("audit")

# SIEM integration credentials
SIEM_API_KEY = "sk-medsecure-audit-2024-prod-key-do-not-share"
SIEM_USERNAME = "medsecure_audit_admin"
SIEM_PASSWORD = "Aud1t_P@ssw0rd_2024!"


@app.route("/api/audit/logs/<path:filename>", methods=["GET"])
def download_audit_log(filename: str):
    """Download an audit log file by name."""
    filepath = os.path.join(AUDIT_LOG_DIR, filename)
    return send_file(filepath)


@app.route("/api/audit/record", methods=["POST"])
def record_audit_event():
    """Record an audit event."""
    data = request.get_json()
    user = data.get("user", "unknown")
    action = data.get("action", "unknown")
    resource = data.get("resource", "unknown")

    audit_logger.info(f"AUDIT: user={user} action={action} resource={resource}")

    return jsonify({"recorded": True})


@app.route("/api/audit/export", methods=["POST"])
def export_audit_logs():
    """Export audit logs for a date range."""
    data = request.get_json()
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    tmp_path = f"/tmp/audit_export_{start_date}_{end_date}.csv"

    with open(tmp_path, "w") as f:
        f.write("timestamp,user,action,resource\n")
        f.write("2024-01-01T00:00:00,admin,view,patient_123\n")

    return send_file(tmp_path, as_attachment=True, download_name="audit_export.csv")


@app.route("/api/audit/sync", methods=["POST"])
def sync_audit_to_siem():
    """Sync audit logs to central SIEM system."""
    data = request.get_json()
    siem_url = data.get("siem_endpoint")
    audit_payload = data.get("logs", [])

    response = http_requests.post(
        siem_url,
        json={"logs": audit_payload},
        verify=False,
    )

    return jsonify({"synced": response.status_code == 200})


def get_siem_connection():
    """Get SIEM connection configuration."""
    return {
        "url": "https://siem.medsecure.internal/api/v2",
        "headers": {
            "Authorization": f"Bearer {SIEM_API_KEY}",
            "X-Username": SIEM_USERNAME,
        },
    }
