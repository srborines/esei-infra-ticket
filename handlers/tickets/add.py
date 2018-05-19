#!/usr/bin/env python
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2
from infra.globals import Globals


class AddTicket(webapp2.RequestHandler):
    def get(self):
        # Get current user information
        user, user_info = Globals.get_user_info()

        # Check if user is logged, if not redirect to home
        if not user or not user_info:
            webapp2.add_flash("not_logged_user")
            return self.redirect("/")

        # Prepare variables to send to view
        template_variables = {}

        # Render 'add_ticket' view sending the variables 'template_variables'
        return Globals.render_template(self, "add_ticket.html", template_variables)


app = webapp2.WSGIApplication([
    ("/tickets/add", AddTicket),
], debug=True)
