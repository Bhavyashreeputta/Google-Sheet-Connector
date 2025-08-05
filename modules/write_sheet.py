# modules/write_sheet.py
from flask import jsonify
from utils.sheets_client import append_values

def handler(payload):
    try:
        sheet_id = payload["sheet_id"]
        a1_range = payload["range"]         
        values = payload["values"]

        if not isinstance(values, list) or (values and not isinstance(values[0], list)):
            return jsonify({"status":"error","message":"`values` must be a 2D list"}), 400

        resp = append_values(sheet_id, a1_range, values)
        return jsonify({"status": "success", "result": resp})
    except KeyError as e:
        return jsonify({"status":"error","message":f"Missing key: {e}"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
