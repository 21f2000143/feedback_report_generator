from celery import shared_task
from .models import Report
from django.template.loader import render_to_string
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from datetime import datetime
from reportlab.lib.styles import getSampleStyleSheet
import os
from reportlab.lib.units import inch


def generate_report_card(filename, summary):
    # Create the PDF document
    folder = 'assignments'
    if not os.path.exists(folder):
        os.makedirs(folder)
    pdf_path = os.path.join(folder, filename)
    pdf = SimpleDocTemplate(
        pdf_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30,
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

    return pdf_path


def get_event_sorted_alis(events):
    # Sort units and assign aliases
    units = sorted(set(event["unit"] for event in events))
    unit_to_alias = {unit: f"Q{i+1}" for i, unit in enumerate(units)}

    # Generate event order
    event_order = " -> ".join(unit_to_alias[
        event["unit"]] for event in events)
    return event_order


@shared_task
def generate_html_report(data):
    # Parse events
    context = []
    for each in data:
        dic_obj = {}
        dic_obj['student_id'] = each['student_id']
        event_order = get_event_sorted_alis(each['events'])
        dic_obj['event_order'] = event_order
        context.append(dic_obj)
    # Wrap the list in a dictionary for the template
    full_context = {'full_context': context}
    html_report = render_to_string('feedback_report_generator/report.html',
                                   context=full_context)
    report = Report.objects.create(
        task_id=generate_html_report.request.id, html_content=html_report)
    return report.id


@shared_task
def generate_pdf_report(data):
    # Parse events and prepare data
    summary = []
    for each in data:
        dic_obj = {}
        dic_obj['student_id'] = each['student_id']
        event_order = get_event_sorted_alis(each['events'])
        dic_obj['event_order'] = event_order
        summary.append(dic_obj)
    now = datetime.now()
    filename = f"assignment_report_{now.strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    pdf_file_link = generate_report_card(filename, summary)
    report = Report.objects.create(
        task_id=generate_pdf_report.request.id, pdf_content=pdf_file_link)
    return report.id
