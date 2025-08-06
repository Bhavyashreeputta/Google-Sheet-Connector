from auth import get_sheets_service

def create_row(spreadsheet_id: str, sheet_name: str, values: list):
    service = get_sheets_service()
    body = {
        "values": [values]
    }
    result = service.values().append(
        spreadsheetId=spreadsheet_id,
        range=sheet_name,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
    return {"status": "success", "updates": result.get("updates", {})}
