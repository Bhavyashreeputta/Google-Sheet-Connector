from flask import jsonify
from utils.sheets_client import get_metadata

def handler(payload):
    try:
        sheet_id = payload["sheet_id"]

        meta = get_metadata(sheet_id)
        props = meta.get("properties", {})
        sheets = []
        for s in meta.get("sheets", []):
            p = s.get("properties", {})
            gp = p.get("gridProperties", {})
            sheets.append({
                "title": p.get("title"),
                "sheetId": p.get("sheetId"),
                "rowCount": gp.get("rowCount"),
                "columnCount": gp.get("columnCount")
            })

        return jsonify({
            "status": "success",
            "spreadsheetId": meta.get("spreadsheetId"),
            "title": props.get("title"),
            "sheets": sheets
        })
    except KeyError as e:
        return jsonify({"status":"error","message":f"Missing key: {e}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
