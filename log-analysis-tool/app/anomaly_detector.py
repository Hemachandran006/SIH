"""
Anomaly Detection Module
Implements rule-based anomaly detection for log analysis
"""

from typing import List, Dict, Any
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import re


class AnomalyDetector:
    """Rule-based anomaly detection for log entries"""
    
    # Default blacklisted IPs (example list)
    DEFAULT_BLACKLIST = [
        '192.168.100.100',
        '10.0.0.666',
        '172.16.0.250',
    ]
    
    def __init__(self, blacklisted_ips: List[str] = None):
        """
        Initialize anomaly detector
        
        Args:
            blacklisted_ips: List of IP addresses to flag as suspicious
        """
        self.blacklisted_ips = blacklisted_ips or self.DEFAULT_BLACKLIST
        self.alerts = []
        
    def detect_anomalies(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze logs and detect anomalies
        
        Args:
            logs: List of parsed log entries
            
        Returns:
            List of detected anomalies/alerts
        """
        self.alerts = []
        
        # Run detection rules
        self._detect_failed_logins(logs)
        self._detect_blacklisted_ips(logs)
        self._detect_error_spikes(logs)
        self._detect_suspicious_patterns(logs)
        
        # Sort alerts by severity and timestamp
        severity_order = {'CRITICAL': 0, 'ERROR': 1, 'WARNING': 2, 'INFO': 3}
        self.alerts.sort(key=lambda x: (
            severity_order.get(x['severity'], 4),
            x['timestamp']
        ), reverse=True)
        
        return self.alerts
    
    def _detect_failed_logins(self, logs: List[Dict[str, Any]]) -> None:
        """Detect multiple failed login attempts"""
        # Track failed logins by source
        failed_attempts = defaultdict(list)
        
        for log in logs:
            event = log.get('event', '').lower()
            source = log.get('source', 'unknown')
            
            # Look for failed login indicators
            if any(indicator in event for indicator in [
                'failed', 'fail', 'authentication failed', 'invalid password',
                'login failed', 'access denied', 'unauthorized', '401', '403'
            ]):
                failed_attempts[source].append(log)
        
        # Flag sources with multiple failed attempts
        threshold = 3
        for source, attempts in failed_attempts.items():
            if len(attempts) >= threshold:
                self.alerts.append({
                    'timestamp': datetime.now().isoformat(),
                    'severity': 'CRITICAL' if len(attempts) >= 5 else 'WARNING',
                    'type': 'Multiple Failed Logins',
                    'source': source,
                    'description': f'{len(attempts)} failed login attempts detected from {source}',
                    'count': len(attempts),
                    'details': f"First attempt: {attempts[0].get('timestamp', 'unknown')}"
                })
    
    def _detect_blacklisted_ips(self, logs: List[Dict[str, Any]]) -> None:
        """Detect access from blacklisted IP addresses"""
        ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        
        for log in logs:
            # Check source field
            source = log.get('source', '')
            if source in self.blacklisted_ips:
                self.alerts.append({
                    'timestamp': log.get('timestamp', datetime.now().isoformat()),
                    'severity': 'CRITICAL',
                    'type': 'Blacklisted IP',
                    'source': source,
                    'description': f'Access detected from blacklisted IP: {source}',
                    'details': log.get('event', '')[:100]
                })
                continue
            
            # Check for IPs in event text
            event = log.get('event', '')
            ips_in_event = ip_pattern.findall(event)
            
            for ip in ips_in_event:
                if ip in self.blacklisted_ips:
                    self.alerts.append({
                        'timestamp': log.get('timestamp', datetime.now().isoformat()),
                        'severity': 'CRITICAL',
                        'type': 'Blacklisted IP',
                        'source': ip,
                        'description': f'Blacklisted IP {ip} found in log entry',
                        'details': event[:100]
                    })
    
    def _detect_error_spikes(self, logs: List[Dict[str, Any]]) -> None:
        """Detect unusual spikes in error rates"""
        # Count errors in time windows
        error_counts = Counter()
        
        for log in logs:
            severity = log.get('severity', 'INFO')
            if severity in ['ERROR', 'CRITICAL']:
                timestamp = log.get('timestamp', '')
                try:
                    # Group by hour
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    hour_key = dt.strftime('%Y-%m-%d %H:00')
                    error_counts[hour_key] += 1
                except:
                    pass
        
        # Flag if more than 10 errors in any hour
        threshold = 10
        for time_window, count in error_counts.items():
            if count >= threshold:
                self.alerts.append({
                    'timestamp': datetime.now().isoformat(),
                    'severity': 'WARNING',
                    'type': 'Error Spike',
                    'source': 'system',
                    'description': f'High error rate detected: {count} errors in time window {time_window}',
                    'count': count,
                    'details': f'Threshold: {threshold} errors per hour'
                })
    
    def _detect_suspicious_patterns(self, logs: List[Dict[str, Any]]) -> None:
        """Detect suspicious patterns in log events"""
        suspicious_keywords = [
            'exploit', 'attack', 'malware', 'virus', 'injection',
            'sql injection', 'xss', 'ddos', 'breach', 'intrusion',
            'vulnerability', 'backdoor', 'trojan', 'ransomware'
        ]
        
        for log in logs:
            event = log.get('event', '').lower()
            
            for keyword in suspicious_keywords:
                if keyword in event:
                    self.alerts.append({
                        'timestamp': log.get('timestamp', datetime.now().isoformat()),
                        'severity': 'CRITICAL',
                        'type': 'Suspicious Activity',
                        'source': log.get('source', 'unknown'),
                        'description': f'Suspicious keyword detected: "{keyword}"',
                        'details': log.get('event', '')[:200]
                    })
                    break  # Only flag once per log entry
    
    def add_blacklisted_ip(self, ip: str) -> None:
        """Add an IP to the blacklist"""
        if ip not in self.blacklisted_ips:
            self.blacklisted_ips.append(ip)
    
    def remove_blacklisted_ip(self, ip: str) -> None:
        """Remove an IP from the blacklist"""
        if ip in self.blacklisted_ips:
            self.blacklisted_ips.remove(ip)
    
    def get_blacklist(self) -> List[str]:
        """Get current blacklist"""
        return self.blacklisted_ips.copy()
