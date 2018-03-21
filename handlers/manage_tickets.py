# infra-esei-tickets (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb

from model.appinfo import AppInfo
from model.ticket import Ticket
import model.user as usr_mgt


class TicketsManager(webapp2.RequestHandler):
    MAX_TICKETS_PER_PAGE = 12
    NUM_PAGES_SHOWN = 10

    @staticmethod
    def filter_by_search_terms(tickets, list_search_terms):
        toret = tickets

        if list_search_terms:
            toret = []

            for ticket in ndb.get_multi(tickets):
                found = False
                title = str(ticket.title).lower()
                desc = str(ticket.desc).lower()

                for search_term in list_search_terms:
                    if (search_term in title
                       or search_term in desc):
                        found = True
                        break

                if found:
                    toret.append(ticket.key)

        return toret

    @staticmethod
    def paginate(tickets, pages_info, current_page):
        """Paginates the results in self.tickets, and self.pages_info"""
        page_buttons_each_side = TicketsManager.MAX_TICKETS_PER_PAGE // 2
        num_tickets = len(tickets)
        num_pages = (num_tickets // TicketsManager.MAX_TICKETS_PER_PAGE) + 1
        current_page = min(num_pages - 1, max(0, current_page))
        pages_info["current"] = current_page
        pages_info["previous"] = max(0, current_page - 1)
        pages_info["last"] = num_pages - 1
        pages_info["next"] = min(num_pages - 1, current_page + 1)
        pages_info["relevant"] = range(max(0, current_page - page_buttons_each_side),
                                       min(num_pages - 1, current_page + page_buttons_each_side) + 1)

        first_ticket = current_page * TicketsManager.MAX_TICKETS_PER_PAGE
        last_ticket = first_ticket + TicketsManager.MAX_TICKETS_PER_PAGE
        tickets = tickets[first_ticket:last_ticket]
        tickets = ndb.get_multi(tickets)
        return tickets

    def get(self):
        try:
            arg_show_all = self.request.GET['kk']
        except KeyError:
            arg_show_all = "false"

        try:
            arg_page = int(self.request.GET['page'])
        except KeyError, ValueError:
            arg_page = 0

        try:
            arg_search_terms = self.request.GET['search']
        except KeyError:
            arg_search_terms = ""

        show_all = True if arg_show_all == "true" else False
        list_search_terms = [x.lower() for x in arg_search_terms.split()]
        pages_info = {}

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

            tickets = tickets.fetch(keys_only=True)
            tickets = TicketsManager.filter_by_search_terms(tickets, list_search_terms)
            tickets = TicketsManager.paginate(tickets, pages_info, arg_page)

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
                "search_terms": arg_search_terms,
                "pages_info": pages_info
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("tickets.html", **template_values))
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([
    ('/manage_tickets', TicketsManager),
], debug=True)
