#!/usr/bin/env python
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

import model.user as usr_mgt
from model.user import User
from model.appinfo import AppInfo


class DeleteUser(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['user_id']
        except:
            self.redirect("/error?msg=user was not found")
            return

        user = users.get_current_user()
        usr_info = usr_mgt.retrieve(user)

        if user and usr_info:
            if not (usr_info.is_admin()):
                self.redirect("/error?msg=User " + user.email + " not allowed to delete users")
                return

            access_link = users.create_logout_url("/")

            try:
                user_to_delete = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=key #" + id + " does not exist")
                return

            template_values = {
                "info": AppInfo,
                "access_link": access_link,
                "usr_info": usr_info,
                "user_to_delete": user_to_delete,
                "user_desc": user_to_delete,
                "Level": User.Level,
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("delete_user.html", **template_values));
        else:
            self.redirect("/")

        return

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

            if not (usr_info.is_admin()):
                self.redirect("/error?msg=user " + usr_info.email + "not allowed to delete users")
                return

            # Get user to delete by key
            try:
                user_to_delete = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=key #" + id + " does not exist")
                return

            # Delete
            user_to_delete.key.delete()
            self.redirect("/info?url=/manage_users&msg=User deleted: "
                            + user_to_delete.email.encode("ascii", "replace"))
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    ("/users/delete", DeleteUser),
], debug=True)
