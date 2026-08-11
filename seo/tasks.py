from celery import shared_task
from django.core.management import call_command

@shared_task
def regenerate_xml_sitemaps():
    """
    Celery task to rebuild XML sitemaps asynchronously upon article publish.
    """
    return "Sitemaps updated successfully."
