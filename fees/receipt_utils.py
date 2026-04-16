from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

def generate_fee_receipt(fee, student, club):
    buffer = BytesIO()
    
    # Create PDF canvas with A5 size (half of A4)
    p = canvas.Canvas(buffer, pagesize=A5)
    width, height = A5  # 148mm x 210mm
    
    y = height - 40  # Adjust top margin
    
    # Club Name (smaller font for A5)
    p.setFont("Helvetica-Bold", 12)
    club_name = club.name if club else "Taekwondo Club"
    p.drawString(30, y, club_name)
    
    # Receipt Title
    y -= 20
    p.setFont("Helvetica-Bold", 10)
    p.drawString(30, y, "OFFICIAL FEE RECEIPT")
    
    # Line separator
    y -= 10
    p.line(30, y, width - 30, y)
    
    # Receipt Number and Date (smaller font)
    y -= 15
    p.setFont("Helvetica", 8)
    receipt_no = fee.receipt_number if fee.receipt_number else f"REC-{fee.id}"
    p.drawString(30, y, f"Receipt No: {receipt_no}")
    p.drawString(180, y, f"Date: {datetime.now().strftime('%d/%m/%Y')}")
    
    # Student Information
    y -= 25
    p.setFont("Helvetica-Bold", 9)
    p.drawString(30, y, "STUDENT INFORMATION")
    
    y -= 15
    p.setFont("Helvetica", 8)
    p.drawString(30, y, f"Name: {student.name}")
    p.drawString(160, y, f"Student ID: {student.student_id}")
    
    y -= 12
    p.drawString(30, y, f"IC Number: {student.ic_number}")
    
    if hasattr(student, 'belt_rank') and student.belt_rank:
        y -= 12
        p.drawString(30, y, f"Belt Rank: {student.belt_rank}")
    
    # Payment Details
    y -= 25
    p.setFont("Helvetica-Bold", 9)
    p.drawString(30, y, "PAYMENT DETAILS")
    
    y -= 15
    p.setFont("Helvetica", 8)
    month_str = fee.month.strftime('%B %Y') if hasattr(fee, 'month') and fee.month else "Monthly Fee"
    p.drawString(30, y, f"Description: Monthly Fee - {month_str}")
    
    y -= 12
    p.drawString(30, y, f"Amount: RM {float(fee.amount):.2f}")
    
    if hasattr(fee, 'paid_date') and fee.paid_date:
        y -= 12
        p.drawString(30, y, f"Payment Date: {fee.paid_date.strftime('%d/%m/%Y')}")
    
    # Total
    y -= 25
    p.setFont("Helvetica-Bold", 10)
    p.drawString(30, y, f"TOTAL PAID: RM {float(fee.amount):.2f}")
    
    # Footer
    y -= 25
    p.setFont("Helvetica-Oblique", 6)
    p.drawString(30, y, "This is a computer-generated receipt. No signature required.")
    
    y -= 10
    p.drawString(30, y, f"Generated on: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    p.save()
    buffer.seek(0)
    return buffer