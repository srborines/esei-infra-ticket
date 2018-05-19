#!/usr/bin/env python
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2

from handlers import tickets
from infra.globals import Globals
from model.ticket import Ticket


class AddTicket(webapp2.RequestHandler):
    def get(self):
        # Get current user information
        user, user_info = Globals.get_user_info()

        # Check if user is logged, if not redirect to home
        if not user or not user_info:
            webapp2.add_flash("not_logged_user")
            return self.redirect("/")

        # Prepare variables to send to view
        template_variables = {
            "ticket_model": Ticket
        }

        # Render 'add_ticket' view sending the variables 'template_variables'
        return Globals.render_template(self, "add_ticket.html", template_variables)

    def post(self):
        # Get current user information
        user, user_info = Globals.get_user_info()

        # Check if user is logged, if not redirect to home
        if not user or not user_info:
            webapp2.add_flash("not_logged_user")
            return self.redirect("/")

        # Create empty ticket
        ticket = Ticket()

        # Set all parameters from the request to ticket
        ticket.title = self.request.get("title", "").strip()
        ticket.desc = self.request.get("desc", "").strip()
        ticket.client_email = self.request.get("client_email", "").strip()
        ticket.classroom = self.request.get("classroom", "").strip()
        ticket.progress = Ticket.Progress.value_from_str(self.request.get("progress"))
        ticket.status = Ticket.Status.value_from_str(self.request.get("status"))
        ticket.priority = Ticket.Priority.value_from_str(self.request.get("priority"))
        ticket.type = Ticket.Type.value_from_str(self.request.get("type"))

        # If ticket title is missing return to modify view showing the error
        if len(ticket.title) < 1:
            webapp2.add_flash("missing_ticket_title")
            return self.redirect("/tickets/add/")

        # If ticket description is missing return to modify view showing the error
        if len(ticket.desc) < 1:
            webapp2.add_flash("missing_ticket_description")
            return self.redirect("/tickets/add/")

        # Save ticket
        tickets.update(ticket)

        # Set successful message and redirect to tickets list
        webapp2.add_flash("ticket_modified_successfully")
        return self.redirect("/tickets")


app = webapp2.WSGIApplication([
    ("/tickets/add", AddTicket),
], debug=True)
