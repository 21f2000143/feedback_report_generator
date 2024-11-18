from celery import shared_task
from .models import Report
from reportlab.pdfgen import canvas
import io
from django.template.loader import render_to_string


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
    content = render_to_string('feedback_report_generator/report.html',
                               full_context)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, content)
    p.showPage()
    p.save()

    pdf_content = buffer.getvalue()
    buffer.close()

    report = Report.objects.create(
        task_id=generate_pdf_report.request.id, pdf_content=pdf_content)
    return report.id
