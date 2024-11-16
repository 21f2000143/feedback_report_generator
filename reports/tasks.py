from celery import shared_task
from .models import Report


@shared_task
def generate_html_report(data):
    # Process the data and generate HTML content
    print(type(data))
    html_content = "<h2>Student ID: {}</h2><p>Event Order: ...</p>".format(
        data[0])
    report = Report.objects.create(
        task_id=generate_html_report.request.id, html_content=html_content)
    return html_content


@shared_task
def generate_pdf_report(data):
    from reportlab.pdfgen import canvas
    import io
    print(type(data))
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, "Student ID: {}".format(data[0]))
    p.showPage()
    p.save()

    pdf_content = buffer.getvalue()
    buffer.close()

    report = Report.objects.create(
        task_id=generate_pdf_report.request.id, pdf_content=pdf_content)
    return pdf_content
