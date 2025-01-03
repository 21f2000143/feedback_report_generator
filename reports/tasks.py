from celery import shared_task
from .models import Report
from django.template.loader import render_to_string
from .utils import generate_report_card


def get_event_sorted_alis(events):
    # Sort units and assign aliases
    units = sorted(set(int(event["unit"]) for event in events))
    unit_to_alias = {str(unit): f"Q{i+1}" for i, unit in enumerate(units)}
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
    # Generate PDF report card using the summary with unique task ID
    pdf_file_link = generate_report_card(
        f'report_{generate_pdf_report.request.id}.pdf', summary)
    # Save the report
    report = Report.objects.create(
        task_id=generate_pdf_report.request.id, pdf_content=pdf_file_link)
    return report.id
