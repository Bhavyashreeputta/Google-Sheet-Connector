from flask import jsonify
from utils.sheets_client import delete_row as delete_row_call

def handler(payload):
    try:
        sheet_id = payload["sheet_id"]
        sheet_title = payload["sheet_title"]
        row_index = int(payload["row_index"])

        resp = delete_row_call(sheet_id, sheet_title, row_index)
        return jsonify({"status": "success", "result": resp})
    except KeyError as e:
        return jsonify({"status":"error","message":f"Missing key: {e}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
