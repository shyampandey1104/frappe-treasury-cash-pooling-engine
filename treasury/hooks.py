# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "treasury"
app_title = "Frappe Treasury Cash Pooling Engine"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Treasury Cash Pooling Engine - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/treasury/css/treasury.bundle.css"
app_include_js = "/assets/treasury/js/treasury.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Treasury Cash Pooling Engine Entry": {
        "validate": "treasury.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "treasury.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "treasury.tasks.hourly_sync"
    ],
    "daily": [
        "treasury.tasks.daily_reconciliation"
    ],
    "weekly": [
        "treasury.tasks.weekly_digest"
    ]
}
