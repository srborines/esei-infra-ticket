# infra-esei-tickets (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2

import model.user as usr_mgt
from infra.globals import Globals


class WelcomePage(webapp2.RequestHandler):
    def get(self):
        # Get current user information
        user, user_info = Globals.get_user_info()

        # Check if user is logged, if he is redirect to tickets list
        if user and user_info:
            return self.redirect("/tickets")

        # Create empty user with a random nick
        usr_info = usr_mgt.create_empty_user()
        usr_info.nick = "Login"

        # Prepare variables to send to view
        template_variables = {}

        # Render 'index' view sending the variables 'template_variables'
        return Globals.render_template(self, "index.html", template_variables)


app = webapp2.WSGIApplication([
    ('/', WelcomePage),
], debug=True)
