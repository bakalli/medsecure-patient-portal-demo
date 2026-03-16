# MedSecure Patient Portal

Internal patient portal application for MedSecure — a medical storage equipment company.

## Overview

This application provides:
- **Patient Records Management**: CRUD operations for patient records, search, identity verification, and reporting
- **Medical Device API**: Device configuration, health reporting, diagnostics, and firmware management for temperature-controlled storage units and medication dispensers
- **Audit Logging**: HIPAA-compliant audit trail with SIEM integration for compliance reporting

## Architecture

```
src/
├── app.py                 # Application entry point and database initialization
├── patient_records.py     # Patient record management endpoints
├── device_api.py          # Medical device management API
└── audit_log.py           # Audit logging and SIEM integration
```

## Setup

```bash
pip install -r requirements.txt
python src/app.py
```

## API Endpoints

### Patient Records
- `GET /api/patients/search?name=<query>` — Search patients by name
- `GET /api/patients/report?id=<id>` — Generate patient report
- `POST /api/patients` — Create patient record
- `POST /api/patients/<id>/verify` — Verify patient identity

### Medical Devices
- `POST /api/devices/config` — Update device configuration
- `POST /api/devices/report` — Submit device health report (XML)
- `POST /api/devices/<id>/diagnostics` — Run device diagnostics
- `POST /api/devices/firmware/check` — Check firmware updates
- `POST /api/devices/import` — Import device config (YAML)

### Audit
- `GET /api/audit/logs/<filename>` — Download audit log
- `POST /api/audit/record` — Record audit event
- `POST /api/audit/export` — Export audit logs (CSV)
- `POST /api/audit/sync` — Sync to central SIEM

## Compliance

This application handles Protected Health Information (PHI) and must comply with:
- HIPAA Security Rule (45 CFR Part 164)
- FDA 21 CFR Part 11 (electronic records)
- SOC 2 Type II
