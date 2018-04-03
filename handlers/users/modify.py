#!/usr/bin/env python
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>


import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

import model.user as usr_mgt
from model.user import User
from model.appinfo import AppInfo


class ModifyUser(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['user_id']
        except:
            self.redirect("/error?msg=user was not found")
            return

        user = users.get_current_user()
        user_info = usr_mgt.retrieve(user)

        if user and user_info:
            access_link = users.create_logout_url("/")

            if not(user_info.is_admin()):
                self.redirect("/error?msg=User " + user_info.email + " not allowed to modify users")
                return

            try:
                user_to_modify = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=key #" + id + " does not exist")
                return

            template_values = {
                "info": AppInfo,
                "access_link": access_link,
                "usr_info": user_info,
                "user_to_modify": user_to_modify,
                "Level": User.Level,
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("modify_user.html", **template_values));
        else:
            self.redirect("/")

    def post(self):
        try:
            id = self.request.GET['user_id']
        except:
            id = None

        if not id:
            self.redirect("/error?msg=missing id for modification")
            return

        user = users.get_current_user()

        if user:
            usr_info = usr_mgt.retrieve(user)

            if not(usr_info.is_admin()):
                self.redirect("/error?msg=user " + usr_info.email + " not allowed to modify other users")

            # Get user by key
            try:
                user_to_modify = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=key #" + id + " does not exist")
                return

            user_to_modify.email = self.request.get("email", "").strip()
            user_to_modify.nick = self.request.get("nick", "").strip()
            user_to_modify.level = User.Level.value_from_str(self.request.get("level", "Client").strip())

            # Chk
            if len(user_to_modify.email) < 1:
                self.redirect("/error?msg=Aborted modification: missing email")
                return

            if len(user_to_modify.nick) < 1:
                self.redirect("/error?msg=Aborted modification: missing nick")
                return

            # Save
            usr_mgt.update(user_to_modify)
            self.redirect("/info?url=/manage_users&msg=User modified: "
                          + user_to_modify.email.encode("ascii", "replace"))
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    ("/users/modify", ModifyUser),
], debug=True)
