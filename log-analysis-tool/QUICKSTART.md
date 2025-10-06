# Quick Start Guide - Log Analysis Tool

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Install Dependencies
```bash
cd log-analysis-tool
pip install -r requirements.txt
```

### Step 2: Start the Application
```bash
python app.py
```

The dashboard will be available at: **http://127.0.0.1:5000**

## Using the Dashboard

### 1. Upload Log Files

**Method 1: Click to Browse**
- Click on "Select File" button
- Choose a log file (.log, .txt, or .csv)
- File will be automatically parsed and analyzed

**Method 2: Drag and Drop**
- Drag a log file from your file explorer
- Drop it onto the upload area
- File will be processed immediately

### 2. View Statistics

The dashboard shows:
- **Total Logs**: Number of log entries imported
- **Alerts**: Number of security alerts detected
- **Errors**: Count of ERROR and CRITICAL logs
- **Sources**: Number of unique log sources

### 3. Review Security Alerts

The alerts section displays detected anomalies:
- **CRITICAL**: Urgent security threats (red background)
- **WARNING**: Potential issues (yellow background)
- **ERROR**: Error conditions (orange background)

Each alert shows:
- Severity level
- Alert type (e.g., "Multiple Failed Logins", "Blacklisted IP")
- Source of the alert
- Detailed description
- Timestamp

### 4. Search and Filter Logs

Use the filter bar to narrow down logs:

**Search by Keyword**
- Enter any text to search across all log fields
- Example: "login", "error", "database"

**Filter by IP Address**
- Enter an IP address to find related logs
- Example: "192.168.1.100"

**Filter by Severity**
- Select from dropdown: CRITICAL, ERROR, WARNING, INFO, DEBUG
- Shows only logs of that severity level

**Apply Filters**
- Click "Apply Filters" button to execute the search

### 5. Navigate Log Table

The log table shows:
- **Timestamp**: When the event occurred
- **Severity**: Log level with color coding
- **Source**: Origin of the log (hostname, IP, service)
- **Event**: Log message details

Features:
- Scrollable table with up to 50 entries per page
- Pagination controls at bottom (if more than 50 logs)
- Color-coded severity badges

### 6. Export Reports

**CSV Export**
- Click "📄 Export CSV"
- Downloads a CSV file with all logs and alerts
- Suitable for spreadsheet analysis

**PDF Export**
- Click "📑 Export PDF Report"
- Generates a professional report with:
  - Summary statistics
  - All alerts with details
  - Sample log entries
  - Formatted for printing/sharing

### 7. Clear Logs

To start fresh:
- Click "Clear All Logs" button
- Confirm the action
- All logs and alerts will be removed

## Sample Log Files

Three sample files are included in the `data/` directory:

### 1. sample_generic.log
Generic structured logs with timestamps, severity, and events.
Perfect for testing all features.

### 2. sample_apache.log
Apache/Nginx access log format.
Tests HTTP request parsing.

### 3. sample_csv.csv
CSV format with columns for timestamp, severity, source, event.
Tests CSV import functionality.

## Anomaly Detection Rules

The tool automatically detects:

### 1. Multiple Failed Logins
- **Trigger**: 3+ failed login attempts from same source
- **Severity**: WARNING (3-4), CRITICAL (5+)
- **Keywords**: "failed", "authentication failed", "invalid password"

### 2. Blacklisted IPs
- **Trigger**: Log from known malicious IP
- **Severity**: CRITICAL
- **Default blacklist**: 192.168.100.100, 10.0.0.666, 172.16.0.250

### 3. Error Spikes
- **Trigger**: 10+ errors in one hour
- **Severity**: WARNING
- **Detects**: Unusual concentration of ERROR/CRITICAL logs

### 4. Suspicious Activity
- **Trigger**: Keywords indicating attacks
- **Severity**: CRITICAL
- **Keywords**: exploit, attack, malware, injection, ddos, breach, etc.

## Tips for Best Results

### Log File Preparation
- Ensure timestamps are included in logs
- Use consistent severity levels (INFO, WARNING, ERROR, CRITICAL)
- Include source information (IP, hostname, service name)

### Filtering Strategy
1. Start with severity filters (CRITICAL, ERROR) to find urgent issues
2. Use keyword search to investigate specific problems
3. Filter by IP to track activity from specific sources

### Export Workflow
1. Apply filters to focus on relevant logs
2. Export CSV for detailed analysis in Excel/Google Sheets
3. Export PDF for formal reports and documentation

## Troubleshooting

### File Upload Issues
- **Error: "Invalid file type"**
  - Only .log, .txt, .csv files are supported
  - Check file extension

- **Error: "File too large"**
  - Maximum file size is 16MB
  - Split large log files before uploading

### No Logs Displayed
- Check if file was successfully uploaded (look for success message)
- Try clearing filters (remove keyword/IP filters)
- Refresh the page and try again

### No Alerts Detected
- This is normal if logs don't contain suspicious activity
- Upload sample files from `data/` directory to see alerts

## Advanced Usage

### API Access

The tool provides a REST API for programmatic access:

```bash
# Get logs
curl http://127.0.0.1:5000/api/logs

# Get alerts
curl http://127.0.0.1:5000/api/alerts

# Get statistics
curl http://127.0.0.1:5000/api/stats
```

### Custom Blacklist

Manage IP blacklist via API:

```bash
# Add IP to blacklist
curl -X POST http://127.0.0.1:5000/api/blacklist \
  -H "Content-Type: application/json" \
  -d '{"ip": "192.168.1.200"}'

# Remove IP from blacklist
curl -X DELETE http://127.0.0.1:5000/api/blacklist \
  -H "Content-Type: application/json" \
  -d '{"ip": "192.168.1.200"}'
```

## Security Notes

- This tool is designed for **isolated networks**
- No built-in authentication (add as needed)
- Uploaded files are stored in `uploads/` directory
- Generated reports are in `exports/` directory
- Consider implementing HTTPS for production

## Support

For more information:
- Read the full README.md
- Check inline code comments
- Examine sample log files in `data/` directory

---

**Happy Log Analyzing! 🔍**
