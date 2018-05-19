#!/usr/bin/env python
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2
from google.appengine.ext import ndb
from infra.globals import Globals
from model.ticket import Ticket


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

    def get(self, page):
        # Get current user information
        user, user_info = Globals.get_user_info()

        # Check if user is logged, if not redirect to home
        if not user or not user_info:
            webapp2.add_flash("not_logged_user")
            return self.redirect("/")

        # Describe query to get all tickets ordered by added date
        tickets = Ticket.query().order(-Ticket.added)

        # Obtain url parameter show_all
        show_all = self.request.get('show_all')

        # If show_all is not a GET parameter initialize to 'opened'
        if not show_all:
            show_all = 'opened'

        # If parameter show_all is not 'all' filter tickets by opened status
        if show_all != "all":
            tickets = tickets.filter(Ticket.status == Ticket.Status.Open)

        # If user role is client filter tickets matching his email with owner_email or user_info.email
        if user_info.is_client():
            tickets = tickets.filter(Ticket.owner_email == user_info.email
                                     or Ticket.client_email == user_info.email)

        # Fetch all tickets
        tickets = tickets.fetch(keys_only=True)

        # Get search parameter and filter tickets by search field
        search_arg = self.request.get('search')
        if search_arg:
            list_search_terms = [x.lower() for x in search_arg.split()]
            tickets = TicketsManager.filter_by_search_terms(tickets, list_search_terms)

        # If page is not in the url set page to 0
        if not page:
            page = 0

        # Paginate tickets and generate pages information
        pages_info = {}
        tickets = TicketsManager.paginate(tickets, pages_info, page)

        # Prepare variables to send to view
        template_variables = {
            "ticket_model": Ticket,
            "show_all": show_all,
            "search_terms": search_arg,
            "pages_info": pages_info,
            "tickets": tickets,
        }

        # Render 'tickets' view sending the variables 'template_variables'
        return Globals.render_template(self, "tickets.html", template_variables)


app = webapp2.WSGIApplication([
    ('/tickets/(\d*)', TicketsManager),
], debug=True)
