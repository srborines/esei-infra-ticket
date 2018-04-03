#!/usr/bin/env python
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2
from google.appengine.api import users


import model.ticket as tickets
import model.user as usr_mgt


class AddTicket(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        usr_info = usr_mgt.retrieve(user)

        if user and usr_info:
            key = tickets.update(tickets.create(usr_info))
            self.redirect("/tickets/modify?ticket_id=" + key.urlsafe())
        else:
            self.redirect("/")

        return


app = webapp2.WSGIApplication([
    ("/tickets/add", AddTicket),
], debug=True)
