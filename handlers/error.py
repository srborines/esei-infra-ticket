#!/usr/bin/env python
# MIT License
# (c) baltasar 2015

import webapp2
from webapp2_extras import jinja2

from infra.appinfo import AppInfo
import model.user as usr_mgt


class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        try:
            msg = self.request.GET['msg']
        except KeyError:
            msg = None

        if not msg:
            msg = "CRITICAL - contact development team"

        template_variables = {
            "usr_info": usr_mgt.create_empty_user(),
            "error_msg": msg,
            "info": AppInfo
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("error.html", **template_variables));


app = webapp2.WSGIApplication([
    ("/error", ErrorHandler),
], debug=True)
