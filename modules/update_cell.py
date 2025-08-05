from flask import jsonify
from utils.sheets_client import update_single_cell

def handler(payload):
    try:
        sheet_id = payload["sheet_id"]
        cell = payload["cell"]          
        value = payload["value"] 

        resp = update_single_cell(sheet_id, cell, value)
        return jsonify({"status": "success", "result": resp})
    except KeyError as e:
        return jsonify({"status":"error","message":f"Missing key: {e}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
