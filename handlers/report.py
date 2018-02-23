#!/usr/bin/env python
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2
from webapp2_extras import jinja2

from model.appinfo import AppInfo


class ReportHandler(webapp2.RequestHandler):
    EmailRcpt = "infraestructura@esei.uvigo.es"

    def get(self):
        message_body = "Daily report\n\nPending open tickets\n\n---\n\n"

        for ticket in []:
	    message_body += str(ticket)

        message_body += "\n\n---\n\n"
        message = mail.EmailMessage(
            sender="esei-infra-ticket@esei.uvigo.es",
            subject="Report"
            to=ReportHandler.EmailRcpt
            body=message_body)

        message.send()
        self.response.write("Report sent to: " + ReportHandler.EmailRcpt);

app = webapp2.WSGIApplication([
    ("/report", ReportHandler),
], debug=True)
