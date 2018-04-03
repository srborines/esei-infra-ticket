# infra-esei-tickets (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users


from model.appinfo import AppInfo
from model.user import User
import model.user as usr_mgt


class UsersManager(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        usr_info = usr_mgt.retrieve(user)

        if user and usr_info:
            user_admin_set = User.query(User.level == User.Level.Admin).order(-User.added)
            user_staff_set = User.query(User.level != User.Level.Admin).order(User.level).order(-User.added)
            user_set = list(user_admin_set) + list(user_staff_set)
            access_link = users.create_logout_url("/")

            if not(usr_info.is_admin()):
                self.redirect("/error?msg=User " + usr_info.nick + " not allowed to manage users")
                return

            template_values = {
                "info": AppInfo,
                "usr_info": usr_info,
                "access_link": access_link,
                "users": user_set,
                "Level": User.Level,
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("users.html", **template_values))
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([
    ('/manage_users', UsersManager),
], debug=True)
