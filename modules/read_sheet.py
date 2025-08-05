from flask import jsonify
from utils.sheets_client import get_values

def handler(payload):
    try:
        sheet_id = payload["sheet_id"]
        range_name = payload["range"]

        values = get_values(sheet_id, range_name)

        return jsonify({
            "status": "success",
            "data": values
        })

    except KeyError as e:
        return jsonify({
            "status": "error",
            "message": f"Missing key in request: {str(e)}"
        }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
