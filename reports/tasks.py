from celery import shared_task
from .models import Report
from .utils import generate_report_card
from celery.signals import task_success, task_failure
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
import time


def get_event_sorted_alis(events):
    # Sort units and assign aliases
    units = sorted(set(int(event["unit"]) for event in events))
    unit_to_alias = {str(unit): f"Q{i+1}" for i, unit in enumerate(units)}
    # Generate event order
    event_order = " -> ".join(unit_to_alias[
        event["unit"]] for event in events)
    return event_order


@task_success.connect
def task_success_handler(sender=None, result=None, **kwargs):
    task_id = sender.request.id
    if result['type'] == 'pdf':
        # Save the PDF report
        Report.objects.create(
            task_id=task_id,
            status="SUCCESS",
            pdf_content=result['pdf_file_link'])
    elif result['type'] == 'html':
        Report.objects.create(
            task_id=task_id,
            status="SUCCESS",
            html_content=result['html_content'])


@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None,
                         args=None, kwargs=None, traceback=None, einfo=None, **kwds):
    Report.objects.create(
        task_id=task_id,
        status="FAILURE",
        error=str(exception)
    )


@shared_task(autoretry_for=(Exception,), max_retries=3, retry_backoff=True)
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
    # Generate HTML directly without template file
    html_report = mark_safe(render_to_string('report.html', full_context))
    return {"html_report": html_report, "type": "html"}


@shared_task(autoretry_for=(Exception,), max_retries=3, retry_backoff=True)
def generate_pdf_report(data):
    time.sleep(60)  # Simulate a long-running task
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
    return {"pdf_file_link": pdf_file_link, "type": "pdf"}
