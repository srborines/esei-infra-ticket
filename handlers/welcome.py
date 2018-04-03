# infra-esei-tickets (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users


from model.appinfo import AppInfo
import model.user as usr_mgt


class WelcomePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        usr_info = usr_mgt.retrieve(user)
        
        if user and usr_info:
                self.redirect("/manage_tickets")
                return
        else:
                usr_info = usr_mgt.create_empty_user()
                usr_info.nick = "Login"
                access_link = users.create_login_url("/manage_tickets")

        template_values = {
            "info": AppInfo,
            "usr_info": usr_info,
            "access_link": access_link
        }
        
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("index.html", **template_values))


app = webapp2.WSGIApplication([
    ('/', WelcomePage),
], debug=True)
