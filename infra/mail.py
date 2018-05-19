from google.appengine.api.mail import EmailMessage

from infra.appinfo import AppInfo


class Mail:
    def __init__(self):
        pass

    @staticmethod
    def send_email(recipient, subject, body):
        subject = subject.encode("ascii", "replace")
        body = body.encode("ascii", "replace")

        EmailMessage(
            sender=AppInfo.AppEmail,
            subject=subject,
            to=recipient,
            body=body).send()