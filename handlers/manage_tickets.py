# infra-esei-tickets (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2
import logging
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb

from model.appinfo import AppInfo
from model.ticket import Ticket
import model.user as usr_mgt


class TicketsManager(webapp2.RequestHandler):
    @staticmethod
    def filter(tickets, list_search_terms):
        result_set_keys = []
        list_search_terms = [x.lower() for x in list_search_terms]

        if list_search_terms:
            for ticket in ndb.get_multi(tickets):
                found = False
                title = str(ticket.title).lower()
                desc = str(ticket.desc).lower()

                for search_term in list_search_terms:
                    logging.info("Looking for " + search_term + " in '" + title + "' and: " + desc)
                    if (search_term in title
                       or search_term in desc):
                        found = True
                        break

                if found:
                    result_set_keys.append(ticket.key)
        else:
            result_set_keys = tickets

        return ndb.get_multi(result_set_keys)

    def get(self):
        try:
            show_all = self.request.GET['show_all']
            search_terms = self.request.GET['search']
        except:
            show_all = "false"
            search_terms = ""

        show_all = True if show_all == "true" else False
        list_search_terms = search_terms.split()

        user = users.get_current_user()
        
        if user:
            usr_info = usr_mgt.retrieve(user)
            user_name = usr_info.nick
            access_link = users.create_logout_url("/")

            # Retrieve the relevant tickets
            tickets = Ticket.query().order(-Ticket.added)
            if not show_all:
                tickets = tickets.filter(Ticket.status == Ticket.Status.Open)

            if usr_info.is_client():
                tickets = tickets.filter(Ticket.owner_email == usr_info.email
                                         or Ticket.client_email == usr_info.email)

            tickets = TicketsManager.filter(tickets.fetch(keys_only=True), list_search_terms)

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "tickets": tickets,
                "Status": Ticket.Status,
                "Priority": Ticket.Priority,
                "Progress": Ticket.Progress,
                "usr_info": usr_info,
                "show_all": show_all,
                "search_terms": search_terms
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("tickets.html", **template_values))
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([
    ('/manage_tickets', TicketsManager),
], debug=True)
