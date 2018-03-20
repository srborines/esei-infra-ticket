#!/usr/bin/env python
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2
from google.appengine.api import users

from model.user import User
import model.user as usr_mgt


class AddUser(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            usr_info = usr_mgt.retrieve(user)

            if not (usr_info.is_admin()):
                self.redirect("/error?msg=user " + usr_info.email + "not allowed to add new users")
                return

            key = usr_mgt.update(usr_mgt.create(user, User.Level.Staff))
            self.redirect("/users/modify?user_id=" + key.urlsafe())
        else:
            self.redirect("/")

        return


app = webapp2.WSGIApplication([
    ("/users/add", AddUser),
], debug=True)
