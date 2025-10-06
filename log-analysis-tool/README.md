# Log Analysis Tool for Isolated Networks

A portable, Python-based log analysis tool designed for isolated/air-gapped networks. Features manual log file import, parsing, anomaly detection, and a clean web dashboard for visualization and analysis.

## 🎯 Features

### Core Functionality
- **Manual Log Import**: Support for .log, .txt, and .csv files
- **Log Parsing & Normalization**: Automatically parse and structure logs into standardized format
  - Timestamp
  - Source (IP/hostname)
  - Event description
  - Severity level
- **Search & Filter**: 
  - Keyword search across all fields
  - IP address filtering
  - Severity level filtering
  - Time range filtering
- **Anomaly Detection**: Rule-based detection for:
  - Multiple failed login attempts
  - Blacklisted IP addresses
  - Error rate spikes
  - Suspicious activity patterns
- **Web Dashboard**: Clean, intuitive interface built with Flask
  - Log table with pagination
  - Alerts section highlighting detected anomalies
  - Statistics overview
  - Real-time filtering
- **Export Reports**: Generate analysis reports in CSV and PDF formats

### Design Principles
- **Modular Architecture**: Easy to extend with new features
- **Well-Commented Code**: Clear documentation throughout
- **Portable**: No external dependencies beyond Python packages
- **User-Friendly**: Prioritizes clarity and ease of use

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Quick Start

### 1. Installation

```bash
# Navigate to the tool directory
cd log-analysis-tool

# Install required packages
pip install -r requirements.txt
```

### 2. Run the Application

```bash
# Start the Flask web server
python app.py
```

The dashboard will be available at: **http://127.0.0.1:5000**

### 3. Usage Workflow

1. **Upload Log Files**: Click or drag-and-drop log files (.log, .txt, .csv)
2. **View Analysis**: Automatically parsed logs appear in the table
3. **Check Alerts**: Security alerts are displayed in the alerts section
4. **Filter & Search**: Use filters to narrow down specific logs
5. **Export Reports**: Download CSV or PDF reports for documentation

## 📁 Project Structure

```
log-analysis-tool/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                  # This file
├── app/
│   ├── __init__.py
│   ├── log_parser.py          # Log parsing and normalization
│   ├── log_manager.py         # Log storage and filtering
│   ├── anomaly_detector.py    # Rule-based anomaly detection
│   └── exporter.py            # CSV and PDF export functionality
├── templates/
│   └── index.html             # Web dashboard template
├── uploads/                   # Uploaded log files (auto-created)
├── exports/                   # Generated reports (auto-created)
└── data/                      # Sample log files (auto-created)
```

## 🔍 Supported Log Formats

### 1. Apache/Nginx Access Logs
```
192.168.1.100 - - [01/Jan/2024:10:30:45 +0000] "GET /index.html HTTP/1.1" 200
```

### 2. Syslog Format
```
Jan 15 10:30:45 server1 sshd[1234]: Failed password for admin from 192.168.1.100
```

### 3. Windows Event Logs
```
2024-01-15 10:30:45 ERROR Server Application error occurred
```

### 4. Generic Structured Logs
```
2024-01-15T10:30:45Z INFO webserver User login successful
```

### 5. CSV Files
CSV files with columns like: timestamp, severity, source, event, etc.

## 🛡️ Anomaly Detection Rules

The tool implements the following detection rules:

1. **Multiple Failed Logins**
   - Threshold: 3+ failed attempts from same source
   - Severity: WARNING (3-4 attempts), CRITICAL (5+ attempts)

2. **Blacklisted IPs**
   - Checks against configurable IP blacklist
   - Severity: CRITICAL

3. **Error Rate Spikes**
   - Detects unusual concentration of errors
   - Threshold: 10+ errors per hour
   - Severity: WARNING

4. **Suspicious Patterns**
   - Keywords: exploit, attack, malware, injection, etc.
   - Severity: CRITICAL

## 📊 Dashboard Features

### Statistics Overview
- Total log entries
- Total alerts detected
- Error count
- Unique sources

### Alerts Section
- Real-time anomaly alerts
- Color-coded by severity
- Detailed descriptions
- Source tracking

### Log Table
- Paginated view (50 entries per page)
- Sortable columns
- Search and filter capabilities
- Responsive design

### Export Options
- **CSV**: Complete data export for further analysis
- **PDF**: Professional report with statistics and alerts

## 🔧 Configuration

### Blacklist Management

The tool comes with default blacklisted IPs. You can manage them via the API:

```bash
# Get current blacklist
curl http://127.0.0.1:5000/api/blacklist

# Add IP to blacklist
curl -X POST http://127.0.0.1:5000/api/blacklist \
  -H "Content-Type: application/json" \
  -d '{"ip": "192.168.1.100"}'

# Remove IP from blacklist
curl -X DELETE http://127.0.0.1:5000/api/blacklist \
  -H "Content-Type: application/json" \
  -d '{"ip": "192.168.1.100"}'
```

## 🔌 API Endpoints

The tool provides a RESTful API for integration:

- `POST /api/upload` - Upload log file
- `GET /api/logs` - Get logs with optional filters
- `GET /api/alerts` - Get detected alerts
- `GET /api/stats` - Get statistics
- `GET /api/export/csv` - Export to CSV
- `GET /api/export/pdf` - Export to PDF
- `POST /api/clear` - Clear all logs
- `GET/POST/DELETE /api/blacklist` - Manage IP blacklist

## 🎨 Customization

### Adding New Detection Rules

Edit `app/anomaly_detector.py` and add new methods:

```python
def _detect_custom_rule(self, logs: List[Dict[str, Any]]) -> None:
    """Your custom detection logic"""
    for log in logs:
        # Your logic here
        if condition:
            self.alerts.append({
                'timestamp': log.get('timestamp'),
                'severity': 'WARNING',
                'type': 'Custom Rule',
                'source': log.get('source'),
                'description': 'Description of the alert'
            })
```

Then call it in the `detect_anomalies` method.

### Adding New Log Patterns

Edit `app/log_parser.py` and add patterns to the `PATTERNS` dictionary:

```python
PATTERNS = {
    'custom_format': r'(?P<timestamp>...) (?P<source>...) (?P<event>...)',
    # ... existing patterns
}
```

## 🧪 Testing

### Sample Log Files

Create sample log files in the `data/` directory for testing:

```bash
# Apache-style log
echo '192.168.1.100 - - [15/Jan/2024:10:30:45 +0000] "GET /admin HTTP/1.1" 401' > data/sample.log

# Failed login attempts
echo '2024-01-15 10:30:45 WARNING 192.168.1.100 Failed login attempt' >> data/sample.log
echo '2024-01-15 10:30:46 WARNING 192.168.1.100 Failed login attempt' >> data/sample.log
echo '2024-01-15 10:30:47 WARNING 192.168.1.100 Failed login attempt' >> data/sample.log
```

## 🔒 Security Considerations

- This tool is designed for **isolated networks** without internet access
- No authentication is built-in; deploy behind a firewall or add authentication as needed
- Uploaded files are stored locally in the `uploads/` directory
- Consider implementing HTTPS for production deployment

## 🚧 Future Enhancements

The modular architecture supports easy addition of:

- **Visualization**: Time-series graphs, heat maps, network diagrams
- **Authentication**: User login and role-based access control
- **Database Backend**: PostgreSQL/SQLite for persistent storage
- **Real-time Monitoring**: WebSocket support for live log streaming
- **Machine Learning**: Advanced anomaly detection using ML models
- **Multi-user Support**: Collaborative analysis features
- **API Authentication**: JWT tokens for API access

## 📝 License

This tool is provided as-is for educational and professional use.

## 🤝 Contributing

To extend functionality:

1. Follow the existing code structure
2. Add comprehensive comments
3. Update this README with new features
4. Test thoroughly before deployment

## 📧 Support

For issues or questions, refer to the inline code documentation or extend the codebase as needed.

---

**Built for isolated networks. Secure. Portable. Extensible.**
