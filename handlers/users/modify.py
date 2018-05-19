#!/usr/bin/env python
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>


import webapp2
from google.appengine.ext import ndb

from infra.globals import Globals
from model.user import User


class ModifyUser(webapp2.RequestHandler):
    def get(self, user_id):
        # Get current user information
        user, user_info = Globals.get_user_info()

        # Check if user is logged, if not redirect to home
        if not user or not user_info:
            webapp2.add_flash("not_logged_user")
            return self.redirect("/")

        # If user is not admin go to users list showing that he has not permissions
        if not (user_info.is_admin()):
            webapp2.add_flash("not_allowed_edit_users")
            return self.redirect("/")

        # Get user by id
        user_to_modify = ndb.Key(urlsafe=user_id).get()

        # If user doesn't exist go to users index showing the error
        if not user_to_modify:
            webapp2.add_flash("user_not_exist")
            return self.redirect("/users")

        # Prepare variables to send to view
        template_variables = {
            "user_to_modify": user_to_modify,
            "user_model": User
        }

        # Render 'modify_user' view sending the variables 'template_variables'
        return Globals.render_template(self, "modify_user.html", template_variables)

    def post(self, user_id):
        # Get current user information
        user, user_info = Globals.get_user_info()

        # Check if user is logged, if not redirect to home
        if not user or not user_info:
            webapp2.add_flash("not_logged_user")
            return self.redirect("/")

        # If user is not admin go to users list showing that he has not permissions
        if not (user_info.is_admin()):
            webapp2.add_flash("not_allowed_edit_users")
            return self.redirect("/")

        # Get user by id
            user_to_modify = ndb.Key(urlsafe=user_id).get()

        # If user doesn't exist go to users index showing the error
        if not user_to_modify:
            webapp2.add_flash("user_not_exist")
            return self.redirect("/users")

        # Set all parameters from the request to user
        user_to_modify.email = self.request.get("email", "").strip()
        user_to_modify.nick = self.request.get("nick", "").strip()
        user_to_modify.level = User.Level.value_from_str(self.request.get("level", "Client").strip())

        # If user email is missing return to modify view showing the error
        if len(user_to_modify.email) < 1:
            webapp2.add_flash("missing_user_email")
            return self.redirect("/users/modify/" + user_id)

        # If user nick is missing return to modify view showing the error
        if len(user_to_modify.nick) < 1:
            webapp2.add_flash("missing_user_nick")
            return self.redirect("/users/modify/" + user_id)

        # Save user
        User.update(user_to_modify)

        # Set successful message and redirect to users list
        webapp2.add_flash("user_modified_successfully")
        return self.redirect("/users")


app = webapp2.WSGIApplication([
    ("/users/modify", ModifyUser),
], debug=True)
