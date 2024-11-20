from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
import os
from reportlab.lib.units import inch


def generate_report_card(filename, summary):
    # Create the PDF document
    folder = 'assignments'
    if not os.path.exists(folder):
        os.makedirs(folder)
    pdf_content = os.path.join(folder, filename)
    pdf = SimpleDocTemplate(
        pdf_content, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30,
        bottomMargin=30)

    # Set up styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontSize = 18
    title_style.leading = 24

    # Header
    header = Paragraph(
        "Indian Institute of Technology Madras<br/>ASSIGNMENT REPORT",
        title_style
    )

    # Word wrapping style for table cells
    cell_style = styles['BodyText']
    cell_style.wordWrap = 'CJK'  # Ensures word wrapping for long text

    # Create the summary table
    summary_table_data = [["Student ID", "Event Order"]]
    for category in summary:
        summary_table_data.append([
            Paragraph(str(category["student_id"]), cell_style),
            Paragraph(str(category["event_order"]), cell_style)
        ])

    # Specify fixed column widths
    column_widths = [2 * inch, 4 * inch]  # Adjust as needed for your content

    # Create the table
    summary_table = Table(summary_table_data, colWidths=column_widths)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Add elements to the PDF
    elements = [header, Spacer(1, 12), summary_table]

    # If content is too long, additional pages will be created automatically
    pdf.build(elements)

    return pdf_content
