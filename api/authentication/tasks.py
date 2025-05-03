import ssl

from celery import shared_task
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from saas_template_backend import settings


@shared_task
def send_password_reset_email(email, reset_code):
    try:
        if settings.DEBUG:
            context = ssl._create_default_https_context = ssl._create_unverified_context
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=email,
            subject='Password Reset Code',
            html_content=f'''
                <h2>Password Reset Code</h2>
                <p>Your password reset code is: <strong>{reset_code}</strong></p>
                <p>Please use this code to reset your password. The code will expire after you use it.</p>
                <p>If you did not request a password reset, please ignore this email.</p>
            '''
        )
        response = sg.send(message)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False