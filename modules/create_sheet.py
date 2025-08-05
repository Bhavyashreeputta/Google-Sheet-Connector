from flask import jsonify
from utils.sheets_client import create_sheet as create_sheet_call

def handler(payload):
    try:
        sheet_id = payload["sheet_id"]
        new_title = payload["new_title"] 

        resp = create_sheet_call(sheet_id, new_title)
        return jsonify({"status": "success", "result": resp})
    except KeyError as e:
        return jsonify({"status":"error","message":f"Missing key: {e}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
