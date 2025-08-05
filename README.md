# Google Sheets Connector

This project implements a **Google Sheets API connector** using **Flask**. It supports core spreadsheet operations through clearly defined modules and schemas and is deployed to **Google Cloud Run**.

---

## Features — Supported Modules

This connector implements **7 key operations**:

|  Module | Description |
|----------|----------------|
| `read_sheet` | Read rows from a specific range |
| `write_sheet` | Write or append rows to a sheet |
| `update_cell` | Update a single cell value |
| `delete_row` | Delete a row by index |
| `clear_sheet` | Clear all data from a sheet |
| `get_sheet_metadata` | Get sheet titles, IDs, row/column counts |
| `create_sheet` | Create a new named sheet inside a spreadsheet |

Each module is defined with a **schema file** in `module_schemas/`.

---
## Authentication

- The app uses a **hardcoded `service_account.json`** file for Google Sheets API auth.
- The target Google Sheet must be **shared with the `client_email`** from this service account and given **Editor access**.

## Deployment

The app is deployed on **Google Cloud Run**.

###  Live URL:
[Google-Sheet-connector](https://sheets-connector-319643445641.us-central1.run.app)

### Example Curl (Ping):
```bash
curl -X POST "https://sheets-connector-xxxxx.run.app/ping_sheet" \
  -H "Content-Type: application/json" \
  -d '{ "sheet_id": "your-google-sheet-id" }'
