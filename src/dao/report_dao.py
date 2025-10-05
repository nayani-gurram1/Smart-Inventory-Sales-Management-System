from src.config import get_supabase

supabase = get_supabase()

def insert_report(report_type: str, data: dict):
    """
    Insert a new report into the 'reports' table.
    Works with the latest supabase-py client.
    """
    response = supabase.table("reports").insert({
        "report_type": report_type,
        "data": data
    }).execute()

    res_dict = response.model_dump()

    # ✅ Check if 'data' exists and is non-empty to confirm success
    if not res_dict.get("data"):
        raise Exception(f"Failed to insert report: {res_dict}")

    return res_dict.get("data")

def list_reports():
    """
    Retrieve all reports from the 'reports' table.
    """
    response = supabase.table("reports").select("*").order("report_id", desc=True).execute()
    res_dict = response.model_dump()

    return res_dict.get("data", [])
