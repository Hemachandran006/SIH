"""
Export Module
Export log analysis results to CSV and PDF formats
"""

import csv
from datetime import datetime
from typing import List, Dict, Any
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT


class Exporter:
    """Export logs and alerts to various formats"""
    
    @staticmethod
    def export_to_csv(logs: List[Dict[str, Any]], 
                      alerts: List[Dict[str, Any]], 
                      filepath: str) -> str:
        """
        Export logs and alerts to CSV file
        
        Args:
            logs: List of log entries
            alerts: List of alerts
            filepath: Output file path
            
        Returns:
            Path to created file
        """
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            # Write logs section
            f.write("=== LOG ENTRIES ===\n")
            if logs:
                writer = csv.DictWriter(f, fieldnames=['timestamp', 'source', 'event', 'severity'])
                writer.writeheader()
                for log in logs:
                    writer.writerow({
                        'timestamp': log.get('timestamp', ''),
                        'source': log.get('source', ''),
                        'event': log.get('event', ''),
                        'severity': log.get('severity', '')
                    })
            else:
                f.write("No logs available\n")
            
            # Write alerts section
            f.write("\n\n=== ALERTS ===\n")
            if alerts:
                writer = csv.DictWriter(f, fieldnames=['timestamp', 'severity', 'type', 'source', 'description'])
                writer.writeheader()
                for alert in alerts:
                    writer.writerow({
                        'timestamp': alert.get('timestamp', ''),
                        'severity': alert.get('severity', ''),
                        'type': alert.get('type', ''),
                        'source': alert.get('source', ''),
                        'description': alert.get('description', '')
                    })
            else:
                f.write("No alerts detected\n")
        
        return filepath
    
    @staticmethod
    def export_to_pdf(logs: List[Dict[str, Any]], 
                      alerts: List[Dict[str, Any]], 
                      stats: Dict[str, Any],
                      filepath: str) -> str:
        """
        Export logs and alerts to PDF report
        
        Args:
            logs: List of log entries
            alerts: List of alerts
            stats: Statistics dictionary
            filepath: Output file path
            
        Returns:
            Path to created PDF file
        """
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph("Log Analysis Report", title_style))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                              styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Statistics Summary
        story.append(Paragraph("Summary Statistics", heading_style))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Logs', str(stats.get('total', 0))],
            ['Total Alerts', str(len(alerts))],
        ]
        
        # Add severity breakdown
        by_severity = stats.get('by_severity', {})
        for severity, count in by_severity.items():
            summary_data.append([f'{severity} Logs', str(count)])
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Alerts Section
        if alerts:
            story.append(Paragraph("Security Alerts", heading_style))
            
            # Limit to first 50 alerts for PDF
            alerts_to_show = alerts[:50]
            alert_data = [['Time', 'Severity', 'Type', 'Description']]
            
            for alert in alerts_to_show:
                timestamp = alert.get('timestamp', '')[:19]  # Truncate timestamp
                severity = alert.get('severity', '')
                alert_type = alert.get('type', '')
                description = alert.get('description', '')[:60]  # Truncate description
                
                alert_data.append([
                    timestamp,
                    severity,
                    alert_type,
                    description
                ])
            
            alert_table = Table(alert_data, colWidths=[1.5*inch, 1*inch, 1.5*inch, 2.5*inch])
            alert_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d32f2f')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ffebee')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            
            story.append(alert_table)
            
            if len(alerts) > 50:
                story.append(Spacer(1, 10))
                story.append(Paragraph(f"Note: Showing 50 of {len(alerts)} alerts. "
                                     f"Export to CSV for complete data.", 
                                     styles['Italic']))
        else:
            story.append(Paragraph("Security Alerts", heading_style))
            story.append(Paragraph("No security alerts detected.", styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Log Entries Section (sample)
        if logs:
            story.append(Paragraph("Sample Log Entries", heading_style))
            story.append(Paragraph(f"Showing 30 of {len(logs)} total entries", 
                                 styles['Italic']))
            story.append(Spacer(1, 10))
            
            # Limit to first 30 logs
            logs_to_show = logs[:30]
            log_data = [['Time', 'Severity', 'Source', 'Event']]
            
            for log in logs_to_show:
                timestamp = log.get('timestamp', '')[:19]
                severity = log.get('severity', '')
                source = log.get('source', '')[:20]
                event = log.get('event', '')[:50]
                
                log_data.append([timestamp, severity, source, event])
            
            log_table = Table(log_data, colWidths=[1.5*inch, 0.8*inch, 1.2*inch, 3*inch])
            log_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            
            story.append(log_table)
        
        # Build PDF
        doc.build(story)
        
        return filepath
