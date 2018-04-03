#!/usr/bin/env python
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

import model.user as usr_mgt
from model.ticket import Ticket
from model.appinfo import AppInfo


class DeleteTicket(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['ticket_id']
        except:
            self.redirect("/error?msg=ticket was not found")
            return

        user = users.get_current_user()
        usr_info = usr_mgt.retrieve(user)

        if user and usr_info:
            if not (usr_info.is_admin()):
                self.redirect("/error?msg=User " + user.email + " not allowed to delete tickets")
                return

            access_link = users.create_logout_url("/")

            try:
                ticket = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=key #" + id + " does not exist")
                return

            template_values = {
                "info": AppInfo,
                "usr_info": usr_info,
                "access_link": access_link,
                "ticket": ticket,
                "Status": Ticket.Status,
                "Type": Ticket.Type,
                "Progress": Ticket.Progress,
                "Priority": Ticket.Priority,
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("delete_ticket.html", **template_values));
        else:
            self.redirect("/")

        return

    def post(self):
        try:
            id = self.request.GET['ticket_id']
        except:
            id = None

        if not id:
            self.redirect("/error?msg=missing id for modification")
            return

        user = users.get_current_user()
        usr_info = usr_mgt.retrieve(user)

        if user and usr_info:
            if not (usr_info.is_admin()):
                self.redirect("/error?msg=user " + usr_info.email + "not allowed to delete users")
                return

            # Get ticket to delete by key
            try:
                ticket = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=key #" + id + " does not exist")
                return

            # Delete
            ticket.key.delete()
            self.redirect("/info?url=/manage_tickets&msg=Ticket deleted: "
                          + ticket.title.encode("ascii", "replace"))
        else:
            self.redirect("/")


app = webapp2.WSGIApplication([
    ("/tickets/delete", DeleteTicket),
], debug=True)
