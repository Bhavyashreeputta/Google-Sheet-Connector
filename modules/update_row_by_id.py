from auth import get_sheets_service

def update_row_by_id(spreadsheet_id: str, sheet_name: str, row_index: int, values: list, value_input_option: str = "USER_ENTERED"):
    service = get_sheets_service()
    row_number = int(row_index) + 1 
    body = {"values": [values]}
    resp = service.values().update(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!{row_number}:{row_number}",
        valueInputOption=value_input_option,
        body=body
    ).execute()
    return {"status": "success", "row_index": row_index, "updatedRange": resp.get("updatedRange")}
