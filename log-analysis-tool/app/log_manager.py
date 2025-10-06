"""
Log Manager Module
Manages log storage, filtering, and searching
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import re


class LogManager:
    """Manage log entries with search and filter capabilities"""
    
    def __init__(self):
        self.logs = []
        self.filtered_logs = []
        
    def add_logs(self, logs: List[Dict[str, Any]]) -> None:
        """Add logs to the manager"""
        self.logs.extend(logs)
        self.filtered_logs = self.logs.copy()
    
    def clear_logs(self) -> None:
        """Clear all logs"""
        self.logs = []
        self.filtered_logs = []
    
    def get_all_logs(self) -> List[Dict[str, Any]]:
        """Get all logs"""
        return self.logs
    
    def get_filtered_logs(self) -> List[Dict[str, Any]]:
        """Get currently filtered logs"""
        return self.filtered_logs
    
    def filter_logs(self, 
                   keyword: Optional[str] = None,
                   ip_address: Optional[str] = None,
                   severity: Optional[str] = None,
                   start_date: Optional[str] = None,
                   end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Filter logs based on various criteria
        
        Args:
            keyword: Search keyword in event text
            ip_address: Filter by IP address (in source or event)
            severity: Filter by severity level
            start_date: Start of date range (ISO format)
            end_date: End of date range (ISO format)
            
        Returns:
            Filtered list of log entries
        """
        filtered = self.logs.copy()
        
        # Filter by keyword
        if keyword:
            keyword_lower = keyword.lower()
            filtered = [
                log for log in filtered
                if keyword_lower in log.get('event', '').lower() or
                   keyword_lower in log.get('source', '').lower()
            ]
        
        # Filter by IP address
        if ip_address:
            ip_pattern = re.compile(re.escape(ip_address))
            filtered = [
                log for log in filtered
                if ip_pattern.search(log.get('source', '')) or
                   ip_pattern.search(log.get('event', ''))
            ]
        
        # Filter by severity
        if severity and severity != 'ALL':
            filtered = [
                log for log in filtered
                if log.get('severity', '').upper() == severity.upper()
            ]
        
        # Filter by date range
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                filtered = [
                    log for log in filtered
                    if self._parse_timestamp(log.get('timestamp', '')) >= start_dt
                ]
            except:
                pass
        
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                filtered = [
                    log for log in filtered
                    if self._parse_timestamp(log.get('timestamp', '')) <= end_dt
                ]
            except:
                pass
        
        self.filtered_logs = filtered
        return filtered
    
    def search_logs(self, query: str) -> List[Dict[str, Any]]:
        """
        Search logs for a query string
        
        Args:
            query: Search query
            
        Returns:
            List of matching log entries
        """
        query_lower = query.lower()
        results = [
            log for log in self.logs
            if query_lower in log.get('event', '').lower() or
               query_lower in log.get('source', '').lower()
        ]
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about logs"""
        if not self.logs:
            return {
                'total': 0,
                'by_severity': {},
                'by_source': {},
                'date_range': None
            }
        
        # Count by severity
        severity_counts = {}
        for log in self.logs:
            severity = log.get('severity', 'UNKNOWN')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Count by source
        source_counts = {}
        for log in self.logs:
            source = log.get('source', 'unknown')
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # Get date range
        timestamps = []
        for log in self.logs:
            try:
                ts = self._parse_timestamp(log.get('timestamp', ''))
                if ts:
                    timestamps.append(ts)
            except:
                pass
        
        date_range = None
        if timestamps:
            date_range = {
                'start': min(timestamps).isoformat(),
                'end': max(timestamps).isoformat()
            }
        
        return {
            'total': len(self.logs),
            'by_severity': severity_counts,
            'by_source': dict(sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
            'date_range': date_range
        }
    
    def _parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """Parse timestamp string to datetime object"""
        if not timestamp_str:
            return None
        
        try:
            return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except:
            return None
