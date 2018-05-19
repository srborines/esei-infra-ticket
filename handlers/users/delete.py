#!/usr/bin/env python
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

import model.user as usr_mgt
from infra.globals import Globals
from model.user import User
from infra.appinfo import AppInfo


class DeleteUser(webapp2.RequestHandler):
    def get(self, user_id):
        # Get current user information
        user, user_info = Globals.get_user_info()

        # Check if user is logged, if not redirect to home
        if not user or not user_info:
            webapp2.add_flash("not_logged_user")
            return self.redirect("/")

        # If user is not admin go to users list showing that he has not permissions
        if not (user_info.is_admin()):
            webapp2.add_flash("not_allowed_delete_users")
            return self.redirect("/users")

        # Get user by id
        user_to_delete = ndb.Key(urlsafe=user_id).get()

        # If user doesn't exist go to users list showing the error
        if not user_to_delete:
            webapp2.add_flash("missing_user_to_delete")
            return self.redirect("/users")

        # Prepare variables to send to view
        template_variables = {
            "user_to_delete": user_to_delete,
            "user_model": User
        }

        # Render 'delete_user' view sending the variables 'template_variables'
        return Globals.render_template(self, "delete_user.html", template_variables)

    def post(self, user_id):
        # Get current user information
        user, user_info = Globals.get_user_info()

        # Check if user is logged, if not redirect to home
        if not user or not user_info:
            webapp2.add_flash("not_logged_user")
            return self.redirect("/")

        # If user is not admin go to users list showing that he has not permissions
        if not (user_info.is_admin()):
            webapp2.add_flash("not_allowed_delete_users")
            return self.redirect("/users")

        # Get user by id
        user_to_delete = ndb.Key(urlsafe=user_id).get()

        # If user doesn't exist go to users list showing the error
        if not user_to_delete:
            webapp2.add_flash("missing_user_to_delete")
            return self.redirect("/users")

        # Delete user
            user_to_delete.key.delete()

        # Set successful message and redirect to users list
        webapp2.add_flash("user_deleted_successfully")
        return self.redirect("/users")


app = webapp2.WSGIApplication([
    ("/users/delete/(.+)", DeleteUser),
], debug=True)
