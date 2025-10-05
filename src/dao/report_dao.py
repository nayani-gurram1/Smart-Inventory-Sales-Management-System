import json
import os

REPORT_FILE = "reports.json"

_reports = []

def _load_reports():
    global _reports
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r") as f:
            _reports = json.load(f)
    return _reports

def _save_reports():
    global _reports
    with open(REPORT_FILE, "w") as f:
        json.dump(_reports, f, indent=2)

def insert_report(report_data):
    global _reports
    _load_reports()
    _reports.append(report_data)
    _save_reports()

def list_reports():
    return _load_reports()
from src.config import get_supabase

supabase = get_supabase()

def insert_report(report_type, data):
    supabase.table("reports").insert({
        "report_type": report_type,
        "data": data
    }).execute()

def list_reports():
    response = supabase.table("reports").select("*").execute()
    return response.data
