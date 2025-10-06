"""
Log Analysis Tool - Flask Web Application
A portable log analysis tool for isolated networks with web dashboard
"""

import os
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime

from app.log_parser import LogParser
from app.log_manager import LogManager
from app.anomaly_detector import AnomalyDetector
from app.exporter import Exporter


# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
app.config['EXPORT_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'exports')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'.log', '.txt', '.csv'}

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)

# Initialize components
log_parser = LogParser()
log_manager = LogManager()
anomaly_detector = AnomalyDetector()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return os.path.splitext(filename)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle log file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: .log, .txt, .csv'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse file
        file_ext = os.path.splitext(filename)[1].lower()
        parsed_logs = log_parser.parse_file(filepath, file_ext)
        
        # Add to log manager
        log_manager.add_logs(parsed_logs)
        
        # Detect anomalies
        alerts = anomaly_detector.detect_anomalies(log_manager.get_all_logs())
        
        # Get statistics
        stats = log_manager.get_statistics()
        
        return jsonify({
            'success': True,
            'message': f'Successfully parsed {len(parsed_logs)} log entries',
            'logs_count': len(parsed_logs),
            'alerts_count': len(alerts),
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get logs with optional filtering"""
    try:
        # Get filter parameters
        keyword = request.args.get('keyword', '').strip()
        ip_address = request.args.get('ip', '').strip()
        severity = request.args.get('severity', '').strip()
        start_date = request.args.get('start_date', '').strip()
        end_date = request.args.get('end_date', '').strip()
        
        # Apply filters
        if any([keyword, ip_address, severity, start_date, end_date]):
            filtered_logs = log_manager.filter_logs(
                keyword=keyword or None,
                ip_address=ip_address or None,
                severity=severity or None,
                start_date=start_date or None,
                end_date=end_date or None
            )
        else:
            filtered_logs = log_manager.get_all_logs()
        
        # Pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated_logs = filtered_logs[start_idx:end_idx]
        
        return jsonify({
            'logs': paginated_logs,
            'total': len(filtered_logs),
            'page': page,
            'per_page': per_page,
            'total_pages': (len(filtered_logs) + per_page - 1) // per_page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get detected alerts"""
    try:
        alerts = anomaly_detector.detect_anomalies(log_manager.get_all_logs())
        
        # Optional severity filter
        severity_filter = request.args.get('severity', '').strip()
        if severity_filter:
            alerts = [a for a in alerts if a.get('severity') == severity_filter.upper()]
        
        return jsonify({
            'alerts': alerts,
            'total': len(alerts)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get log statistics"""
    try:
        stats = log_manager.get_statistics()
        alerts = anomaly_detector.detect_anomalies(log_manager.get_all_logs())
        
        # Add alert statistics
        alert_by_severity = {}
        for alert in alerts:
            severity = alert.get('severity', 'UNKNOWN')
            alert_by_severity[severity] = alert_by_severity.get(severity, 0) + 1
        
        stats['alerts'] = {
            'total': len(alerts),
            'by_severity': alert_by_severity
        }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Export logs and alerts to CSV"""
    try:
        logs = log_manager.get_all_logs()
        alerts = anomaly_detector.detect_anomalies(logs)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'log_analysis_{timestamp}.csv'
        filepath = os.path.join(app.config['EXPORT_FOLDER'], filename)
        
        Exporter.export_to_csv(logs, alerts, filepath)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/pdf', methods=['GET'])
def export_pdf():
    """Export logs and alerts to PDF"""
    try:
        logs = log_manager.get_all_logs()
        alerts = anomaly_detector.detect_anomalies(logs)
        stats = log_manager.get_statistics()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'log_analysis_{timestamp}.pdf'
        filepath = os.path.join(app.config['EXPORT_FOLDER'], filename)
        
        Exporter.export_to_pdf(logs, alerts, stats, filepath)
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clear', methods=['POST'])
def clear_logs():
    """Clear all logs"""
    try:
        log_manager.clear_logs()
        return jsonify({'success': True, 'message': 'All logs cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/blacklist', methods=['GET', 'POST', 'DELETE'])
def manage_blacklist():
    """Manage blacklisted IPs"""
    try:
        if request.method == 'GET':
            return jsonify({'blacklist': anomaly_detector.get_blacklist()})
        
        elif request.method == 'POST':
            data = request.get_json()
            ip = data.get('ip', '').strip()
            if ip:
                anomaly_detector.add_blacklisted_ip(ip)
                return jsonify({'success': True, 'message': f'IP {ip} added to blacklist'})
            return jsonify({'error': 'No IP provided'}), 400
        
        elif request.method == 'DELETE':
            data = request.get_json()
            ip = data.get('ip', '').strip()
            if ip:
                anomaly_detector.remove_blacklisted_ip(ip)
                return jsonify({'success': True, 'message': f'IP {ip} removed from blacklist'})
            return jsonify({'error': 'No IP provided'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Log Analysis Tool for Isolated Networks")
    print("=" * 60)
    print("\nStarting web server...")
    print("Dashboard: http://127.0.0.1:5000")
    print("\nPress CTRL+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
