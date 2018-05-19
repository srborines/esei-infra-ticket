#!/usr/bin/env python
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2
from google.appengine.ext import ndb

from infra.globals import Globals
from model.ticket import Ticket


class DeleteTicket(webapp2.RequestHandler):
    def get(self, ticket_id):
        # Get current user information
        user, user_info = Globals.get_user_info()

        # Check if user is logged, if not redirect to home
        if not user or not user_info:
            webapp2.add_flash("not_logged_user")
            return self.redirect("/")

        # If user is not admin go to tickets list showing that he has not permissions
        if not (user_info.is_admin()):
            webapp2.add_flash("not_allowed_delete_tickets")
            return self.redirect("/tickets")

        # Get ticket by id
        ticket = ndb.Key(urlsafe=ticket_id).get()

        # If ticket doesn't exist go to tickets list showing the error
        if not ticket:
            webapp2.add_flash("missing_ticket_to_delete")
            return self.redirect("/tickets")

        # Prepare variables to send to view
        template_variables = {
            "ticket": ticket,
            "ticket_model": Ticket
        }

        # Render 'delete_ticket' view sending the variables 'template_variables'
        return Globals.render_template(self, "delete_ticket.html", template_variables)

    def post(self, ticket_id):
        # Get current user information
        user, user_info = Globals.get_user_info()

        # Check if user is logged, if not redirect to home
        if not user or not user_info:
            webapp2.add_flash("not_logged_user")
            return self.redirect("/")

        # If user is not admin go to tickets list showing that he has not permissions
        if not (user_info.is_admin()):
            webapp2.add_flash("not_allowed_delete_tickets")
            return self.redirect("/tickets")

        # Get ticket by id
        ticket = ndb.Key(urlsafe=ticket_id).get()

        # If ticket doesn't exist go to tickets list showing the error
        if not ticket:
            webapp2.add_flash("missing_ticket_title")
            return self.redirect("/tickets")

        # Delete ticket
        ticket.key.delete()

        # Set successful message and redirect to tickets list
        webapp2.add_flash("ticket_deleted_successfully")
        return self.redirect("/tickets")


app = webapp2.WSGIApplication([
    ("/tickets/delete/(.+)", DeleteTicket),
], debug=True)
