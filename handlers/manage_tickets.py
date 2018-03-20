# infra-esei-tickets (c) Baltasar 2018 MIT License <baltasarq@gmail.com>

import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users


from model.appinfo import AppInfo
from model.ticket import Ticket
import model.user as usr_mgt


class TicketsManager(webapp2.RequestHandler):
    def get(self):
        try:
            show_all = self.request.GET['show_all']
        except:
            show_all = "false"

        show_all = True if show_all == "true" else False

        user = users.get_current_user()
        
        if user:
            usr_info = usr_mgt.retrieve(user)
            user_name = usr_info.nick
            access_link = users.create_logout_url("/")

            # Retrieve the relevant tickets
            tickets = Ticket.query().order(Ticket.added)

            if not show_all:
                tickets = tickets.filter(Ticket.status == Ticket.Status.Open)

            if usr_info.is_client():
                tickets = tickets.filter(Ticket.owner_email == usr_info.email
                                         or Ticket.client_email == usr_info.email)

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "tickets": tickets,
                "Status": Ticket.Status,
                "Priority": Ticket.Priority,
                "Progress": Ticket.Progress,
                "usr_info": usr_info,
                "show_all": show_all
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("tickets.html", **template_values))
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([
    ('/manage_tickets', TicketsManager),
], debug=True)
