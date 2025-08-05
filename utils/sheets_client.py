from typing import List, Any, Dict
from googleapiclient.errors import HttpError
from auth import get_sheets_service

# Cache the spreadsheets client so we don't rebuild it every call
_spreadsheets = None

def _client():
    global _spreadsheets
    if _spreadsheets is None:
        _spreadsheets = get_sheets_service()
    return _spreadsheets

def get_metadata(spreadsheet_id: str) -> Dict[str, Any]:
    return _client().get(spreadsheetId=spreadsheet_id, includeGridData=False).execute()

def list_sheet_titles(spreadsheet_id: str) -> List[str]:
    meta = get_metadata(spreadsheet_id)
    return [s["properties"]["title"] for s in meta.get("sheets", [])]

def get_sheet_id_by_title(spreadsheet_id: str, title: str) -> int:
    meta = get_metadata(spreadsheet_id)
    for s in meta.get("sheets", []):
        props = s.get("properties", {})
        if props.get("title") == title:
            return int(props["sheetId"])
    raise ValueError(f"Sheet titled '{title}' not found in spreadsheet {spreadsheet_id}")

def get_values(spreadsheet_id: str, a1_range: str) -> List[List[Any]]:
    resp = _client().values().get(
        spreadsheetId=spreadsheet_id,
        range=a1_range
    ).execute()
    return resp.get("values", [])

def append_values(
    spreadsheet_id: str,
    a1_range: str,
    values_2d: List[List[Any]],
    value_input_option: str = "USER_ENTERED"
) -> Dict[str, Any]:
    body = {"values": values_2d}
    return _client().values().append(
        spreadsheetId=spreadsheet_id,
        range=a1_range,
        valueInputOption=value_input_option,
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()

def update_single_cell(
    spreadsheet_id: str,
    a1_cell: str,
    value: Any,
    value_input_option: str = "USER_ENTERED"
) -> Dict[str, Any]:
    body = {"values": [[value]]}
    return _client().values().update(
        spreadsheetId=spreadsheet_id,
        range=a1_cell,
        valueInputOption=value_input_option,
        body=body
    ).execute()

def clear_range(spreadsheet_id: str, a1_range: str) -> Dict[str, Any]:
    return _client().values().clear(
        spreadsheetId=spreadsheet_id,
        range=a1_range,
        body={}
    ).execute()

def create_sheet(spreadsheet_id: str, new_title: str) -> Dict[str, Any]:
    body = {
        "requests": [
            {"addSheet": {"properties": {"title": new_title}}}
        ]
    }
    return _client().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

def delete_row(spreadsheet_id: str, sheet_title: str, row_index: int) -> Dict[str, Any]:
    sheet_id = get_sheet_id_by_title(spreadsheet_id, sheet_title)
    body = {
        "requests": [
            {
                "deleteDimension": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "ROWS",
                        "startIndex": row_index,
                        "endIndex": row_index + 1
                    }
                }
            }
        ]
    }
    return _client().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()