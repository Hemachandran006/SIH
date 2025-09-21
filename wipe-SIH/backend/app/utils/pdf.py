from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from io import BytesIO

def generate_certificate_pdf(certificate_id: str, user_email: str, device_uid: str, device_name: str, method: str, status: str, date: str) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Background
    c.setFillColorRGB(0.95, 0.97, 1)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    # Title
    c.setFillColor(colors.HexColor("#0f172a"))
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width/2, height - 60, "WipeChain Certificate of Data Sanitization")

    # Divider
    c.setStrokeColor(colors.HexColor("#94a3b8"))
    c.setLineWidth(1)
    c.line(40, height - 75, width - 40, height - 75)

    # Details
    c.setFont("Helvetica", 12)
    y = height - 120
    line_gap = 20
    fields = [
        ("Certificate ID", certificate_id),
        ("Issued To", user_email),
        ("Device UID", device_uid),
        ("Device Name", device_name),
        ("Wipe Method", method),
        ("Status", status.title()),
        ("Issued On", date),
        ("Authority", "WipeChain Automated Verifier"),
    ]
    for label, value in fields:
        c.setFillColor(colors.HexColor("#334155"))
        c.drawString(60, y, f"{label}:")
        c.setFillColor(colors.HexColor("#0f172a"))
        c.drawString(200, y, value)
        y -= line_gap

    # Footer
    c.setFillColor(colors.HexColor("#64748b"))
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width/2, 30, "This document certifies that the above device underwent data sanitization as per the specified method.")

    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf