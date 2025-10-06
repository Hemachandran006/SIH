"""
Log Parser Module
Parses and normalizes various log file formats into a structured table
"""

import re
import csv
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd


class LogParser:
    """Parse and normalize log files into structured format"""
    
    # Common log patterns
    PATTERNS = {
        'apache_combined': r'(?P<source>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] "(?P<event>[^"]+)" (?P<severity>\d+)',
        'syslog': r'(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+) (?P<source>\S+) (?P<event>.*)',
        'windows_event': r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(?P<severity>\w+)\s+(?P<source>\S+)\s+(?P<event>.*)',
        'generic': r'(?P<timestamp>\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)\s*(?P<severity>\w+)?\s*(?P<source>\S+)?\s*(?P<event>.*)',
    }
    
    def __init__(self):
        self.logs = []
        
    def parse_file(self, filepath: str, file_type: str = None) -> List[Dict[str, Any]]:
        """
        Parse log file and return structured data
        
        Args:
            filepath: Path to log file
            file_type: Type of file (.log, .txt, .csv)
            
        Returns:
            List of dictionaries containing parsed log entries
        """
        if file_type == '.csv':
            return self._parse_csv(filepath)
        else:
            return self._parse_text_log(filepath)
    
    def _parse_csv(self, filepath: str) -> List[Dict[str, Any]]:
        """Parse CSV log file"""
        logs = []
        try:
            df = pd.read_csv(filepath)
            
            # Try to map common column names to our schema
            column_mapping = {
                'timestamp': ['timestamp', 'time', 'date', 'datetime', 'log_time'],
                'source': ['source', 'host', 'ip', 'hostname', 'server', 'origin'],
                'event': ['event', 'message', 'msg', 'description', 'log', 'details'],
                'severity': ['severity', 'level', 'priority', 'type', 'status']
            }
            
            for index, row in df.iterrows():
                log_entry = {
                    'timestamp': None,
                    'source': None,
                    'event': None,
                    'severity': 'INFO'
                }
                
                # Map columns
                for target_col, possible_names in column_mapping.items():
                    for col_name in possible_names:
                        if col_name.lower() in [c.lower() for c in df.columns]:
                            actual_col = [c for c in df.columns if c.lower() == col_name.lower()][0]
                            log_entry[target_col] = str(row[actual_col]) if pd.notna(row[actual_col]) else None
                            break
                
                # Use first column as event if not found
                if not log_entry['event'] and len(df.columns) > 0:
                    log_entry['event'] = str(row[df.columns[0]])
                
                # Normalize timestamp
                if log_entry['timestamp']:
                    log_entry['timestamp'] = self._normalize_timestamp(log_entry['timestamp'])
                else:
                    log_entry['timestamp'] = datetime.now().isoformat()
                
                logs.append(log_entry)
                
        except Exception as e:
            print(f"Error parsing CSV: {e}")
            
        return logs
    
    def _parse_text_log(self, filepath: str) -> List[Dict[str, Any]]:
        """Parse text-based log file (.log, .txt)"""
        logs = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    log_entry = self._parse_line(line)
                    if log_entry:
                        logs.append(log_entry)
                    else:
                        # If no pattern matches, create a basic entry
                        logs.append({
                            'timestamp': datetime.now().isoformat(),
                            'source': 'unknown',
                            'event': line,
                            'severity': 'INFO'
                        })
                        
        except Exception as e:
            print(f"Error parsing text log: {e}")
            
        return logs
    
    def _parse_line(self, line: str) -> Dict[str, Any]:
        """Try to parse a single log line using various patterns"""
        
        # Try each pattern
        for pattern_name, pattern in self.PATTERNS.items():
            match = re.match(pattern, line)
            if match:
                data = match.groupdict()
                
                # Normalize timestamp
                timestamp = data.get('timestamp')
                if timestamp:
                    data['timestamp'] = self._normalize_timestamp(timestamp)
                else:
                    data['timestamp'] = datetime.now().isoformat()
                
                # Normalize severity
                severity = data.get('severity', 'INFO')
                data['severity'] = self._normalize_severity(severity)
                
                # Ensure all required fields exist
                data.setdefault('source', 'unknown')
                data.setdefault('event', line)
                
                return data
        
        return None
    
    def _normalize_timestamp(self, timestamp_str: str) -> str:
        """Normalize various timestamp formats to ISO format"""
        timestamp_formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f',
            '%d/%b/%Y:%H:%M:%S',
            '%b %d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%Y-%m-%dT%H:%M:%S%z',
        ]
        
        for fmt in timestamp_formats:
            try:
                dt = datetime.strptime(timestamp_str, fmt)
                # If year is not in string, use current year
                if '%Y' not in fmt:
                    dt = dt.replace(year=datetime.now().year)
                return dt.isoformat()
            except ValueError:
                continue
        
        # If no format matches, return as-is
        return timestamp_str
    
    def _normalize_severity(self, severity: str) -> str:
        """Normalize severity levels"""
        severity_upper = str(severity).upper()
        
        # Map common severity indicators
        severity_map = {
            '200': 'INFO', '201': 'INFO', '204': 'INFO',
            '400': 'WARNING', '401': 'WARNING', '403': 'WARNING', '404': 'WARNING',
            '500': 'ERROR', '502': 'ERROR', '503': 'ERROR',
            'DEBUG': 'DEBUG', 'INFO': 'INFO', 'INFORMATION': 'INFO',
            'WARN': 'WARNING', 'WARNING': 'WARNING',
            'ERROR': 'ERROR', 'ERR': 'ERROR',
            'CRITICAL': 'CRITICAL', 'CRIT': 'CRITICAL', 'FATAL': 'CRITICAL',
        }
        
        for key, value in severity_map.items():
            if key in severity_upper:
                return value
        
        # Default to INFO if unknown
        return 'INFO'
