# fees/receipt_utils.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

def generate_fee_receipt(fee, student, club):
    """Generate PDF receipt for a paid fee"""
    
    buffer = BytesIO()
    
    # Create PDF canvas
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Starting Y position
    y = height - 50
    
    # Club Name
    p.setFont("Helvetica-Bold", 18)
    club_name = club.name if club else "Taekwondo Club"
    p.drawString(50, y, club_name)
    
    # Receipt Title
    y -= 35
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "OFFICIAL FEE RECEIPT")
    
    # Line separator
    y -= 15
    p.line(50, y, width - 50, y)
    
    # Receipt Number and Date
    y -= 25
    p.setFont("Helvetica", 10)
    receipt_no = f"REC-{fee.id}-{datetime.now().strftime('%Y%m')}"
    p.drawString(50, y, f"Receipt No: {receipt_no}")
    p.drawString(350, y, f"Date: {datetime.now().strftime('%d/%m/%Y')}")
    
    # Student Information Section
    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "STUDENT INFORMATION")
    
    y -= 20
    p.setFont("Helvetica", 10)
    p.drawString(50, y, f"Name: {student.name}")
    p.drawString(250, y, f"Student ID: {student.student_id}")
    
    y -= 18
    p.drawString(50, y, f"IC Number: {student.ic_number}")
    
    if hasattr(student, 'belt_rank') and student.belt_rank:
        y -= 18
        p.drawString(50, y, f"Belt Rank: {student.belt_rank}")
    
    # Payment Details Section
    y -= 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "PAYMENT DETAILS")
    
    y -= 20
    p.setFont("Helvetica", 10)
    
    # Format month
    if hasattr(fee, 'month') and fee.month:
        month_str = fee.month.strftime('%B %Y')
    else:
        month_str = "Monthly Fee"
    
    p.drawString(50, y, f"Description: Monthly Fee - {month_str}")
    
    y -= 18
    p.drawString(50, y, f"Amount: RM {float(fee.amount):.2f}")
    
    if hasattr(fee, 'paid_date') and fee.paid_date:
        y -= 18
        p.drawString(50, y, f"Payment Date: {fee.paid_date.strftime('%d/%m/%Y')}")
    
    # Total
    y -= 35
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"TOTAL PAID: RM {float(fee.amount):.2f}")
    
    # Footer
    y -= 50
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(50, y, "This is a computer-generated receipt. No signature required.")
    
    y -= 15
    p.drawString(50, y, f"Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Save PDF
    p.save()
    buffer.seek(0)
    
    return buffer