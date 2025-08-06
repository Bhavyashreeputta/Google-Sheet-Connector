from flask import Flask, jsonify, request
from auth import get_service_account_email
from utils.sheets_client import get_metadata
from modules import read_sheet, write_sheet, update_cell,  delete_row, create_sheet, get_sheet_metadata, clear_sheet, create_row, get_row_by_id, update_row_by_id

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/whoami", methods=["GET"])
def whoami():
    return jsonify({"service_account": get_service_account_email()})

@app.route("/ping_sheet", methods=["POST"])
def ping_sheet():
    try:
        payload = request.get_json(force=True) or {}
        sheet_id = payload.get("sheet_id")
        if not sheet_id:
            return jsonify({"status": "error", "message": "sheet_id is required"}), 400

        meta = get_metadata(sheet_id)
        titles = [s["properties"]["title"] for s in meta.get("sheets", [])]

        return jsonify({
            "status": "success",
            "title": meta.get("properties", {}).get("title"),
            "sheets": titles
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/read_sheet", methods=["POST"])
def read_sheet_handler():
    return read_sheet.handler(request.get_json(force=True))

@app.route("/write_sheet", methods=["POST"])
def write_sheet_handler():
    return write_sheet.handler(request.get_json(force=True))

@app.route("/update_cell", methods=["POST"])
def update_cell_handler():
    return update_cell.handler(request.get_json(force=True))

@app.route("/delete_row", methods=["POST"])
def delete_row_handler():
    return delete_row.handler(request.get_json(force=True))

@app.route("/create_sheet", methods=["POST"])
def create_sheet_handler():
    return create_sheet.handler(request.get_json(force=True))

@app.route("/get_sheet_metadata", methods=["POST"])  # POST for consistency
def get_sheet_metadata_handler():
    return get_sheet_metadata.handler(request.get_json(force=True))

@app.route("/clear_sheet", methods=["POST"])
def clear_sheet_handler():
    return clear_sheet.handler(request.get_json(force=True))

@app.route('/create_row', methods=['POST'])
def create_row_route():
    data = request.get_json()
    spreadsheet_id = data['sheet_id']
    sheet_name = data['sheet_name']
    values = data['values']
    return jsonify(create_row.create_row(spreadsheet_id, sheet_name, values))

@app.route('/get_row_by_id', methods=['POST'])
def get_row_by_id_route():
    data = request.get_json()
    spreadsheet_id = data['sheet_id']
    sheet_name = data['sheet_name']
    row_index = data['row_index']
    return jsonify(get_row_by_id.get_row_by_id(spreadsheet_id, sheet_name, row_index))

@app.route('/update_row_by_id', methods=['POST'])
def update_row_by_id_route():
    data = request.get_json(force=True)
    return jsonify(update_row_by_id.update_row_by_id(
        spreadsheet_id=data['sheet_id'],
        sheet_name=data['sheet_name'],
        row_index=data['row_index'],
        values=data['values']
    ))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
