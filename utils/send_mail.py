import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template

logger = logging.getLogger(__name__)


def send_mail_reset_password(to, url_id):
    subject = "Wordyforest Reset Password"
    context = {"reset_password_url": settings.BASE_URL, "id": url_id}
    message = get_template("email/reset_password.html").render(context)

    msg = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to],
    )

    msg.content_subtype = "html"
    msg.send()

    logger.info(f"Sent email to {to}")
