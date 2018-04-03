#!/usr/bin/env python
# MIT License
# (c) baltasar 2015

import webapp2
from webapp2_extras import jinja2

from model.appinfo import AppInfo
import model.user as usr_mgt


class InfoHandler(webapp2.RequestHandler):
    def get(self):
        try:
            msg = self.request.GET['msg']
            url = self.request.GET['url']
        except KeyError:
            msg = None
            url = "/"

        if not msg:
            self.redirect("error?msg=URL or Info message not found.")
            return

        template_values = {
            "usr_info": usr_mgt.create_empty_user(),
            "msg": msg,
            "info": AppInfo,
            "url": url,
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("info.html", **template_values));


app = webapp2.WSGIApplication([
    ("/info", InfoHandler),
], debug=True)
