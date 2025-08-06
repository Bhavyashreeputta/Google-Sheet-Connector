from auth import get_sheets_service

def get_row_by_id(spreadsheet_id: str, sheet_name: str, row_index: int):
    service = get_sheets_service()
    range_ = f"{sheet_name}!{row_index + 1}:{row_index + 1}"
    result = service.values().get(
        spreadsheetId=spreadsheet_id,
        range=range_
    ).execute()
    values = result.get("values", [])
    return {
        "status": "success",
        "row": values[0] if values else [],
        "index": row_index
    }
