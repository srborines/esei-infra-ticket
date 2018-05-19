# infra-esei-tickets (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2

from infra.globals import Globals
from model.user import User


class UsersManager(webapp2.RequestHandler):
    def get(self):
        # Get current user information
        user, user_info = Globals.get_user_info()

        # Check if user is logged, if not redirect to home
        if not user or not user_info:
            webapp2.add_flash("not_logged_user")
            return self.redirect("/")

        # If user is not admin go to home showing that he has not permissions
        if not (user_info.is_admin()):
            webapp2.add_flash("not_allowed_show_users")
            return self.redirect("/")

        # Get all users ordered by X way
        user_admin_set = User.query(User.level == User.Level.Admin).order(-User.added)
        user_staff_set = User.query(User.level != User.Level.Admin).order(User.level).order(-User.added)
        user_set = list(user_admin_set) + list(user_staff_set)

        # Prepare variables to send to view
        template_variables = {
            "users": user_set,
            "Level": User.Level,
        }

        # Render 'users' view sending the variables 'template_variables'
        return Globals.render_template(self, "users.html", template_variables)


app = webapp2.WSGIApplication([
    ('/manage_users', UsersManager),
], debug=True)
