#!/usr/bin/env python
# MIT License
# (c) baltasar 2015

import webapp2
from webapp2_extras import jinja2

from model.appinfo import AppInfo


class InfoHandler(webapp2.RequestHandler):
    def get(self):
        try:
            msg = self.request.GET['msg']
            url = self.request.GET['url']
        except:
            msg = None
            url = "/"

        if not msg:
            self.redirect("error?msg=Info message not found.")
            return

        template_values = {
            "msg": msg,
            "info": AppInfo,
            "url": url,
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("info.html", **template_values));

app = webapp2.WSGIApplication([
    ("/info", InfoHandler),
], debug=True)
