# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "treasury"
app_title = "Frappe Treasury Cash Pooling Engine"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Treasury Cash Pooling Engine for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/treasury/css/treasury.bundle.css"
app_include_js = "/assets/treasury/js/treasury.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "treasury.engine.on_document_submit",
        "on_cancel": "treasury.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "treasury.engine.daily_scheduled_sync"
    ]
}
