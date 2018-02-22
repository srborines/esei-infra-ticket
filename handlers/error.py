#!/usr/bin/env python
# MIT License
# (c) baltasar 2015

import webapp2
from webapp2_extras import jinja2

from model.appinfo import AppInfo


class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        try:
            msg = self.request.GET['msg']
        except:
            msg = None

        if not msg:
            msg = "CRITICAL - contact development team"

        template_values = {
            "error_msg": msg,
            "info": AppInfo
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("error.html", **template_values));

app = webapp2.WSGIApplication([
    ("/error", ErrorHandler),
], debug=True)
