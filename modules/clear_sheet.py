from flask import jsonify
from utils.sheets_client import clear_range

def handler(payload):
    try:
        sheet_id = payload["sheet_id"]
        # A1 range or just a sheet title to clear entire sheet, e.g., "Sheet1"
        a1_range = payload["range"]

        resp = clear_range(sheet_id, a1_range)
        return jsonify({"status": "success", "result": resp})
    except KeyError as e:
        return jsonify({"status":"error","message":f"Missing key: {e}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
