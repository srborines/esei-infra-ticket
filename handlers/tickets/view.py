#!/usr/bin/env python
# coding: utf-8
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>


import webapp2
from google.appengine.ext import ndb

import model.ticket as tickets
from infra.globals import Globals
from model.ticket import Ticket


class ViewTicket(webapp2.RequestHandler):
    MinCommentLength = 10

    def get(self, ticket_id):
        # Get current user information
        user, user_info = Globals.get_user_info()

        # Check if user is logged, if not redirect to home
        if not user or not user_info:
            webapp2.add_flash("not_logged_user")
            return self.redirect("/")

        # Get ticket by id
        ticket = ndb.Key(urlsafe=ticket_id).get()

        # If ticket doesn't exist go to tickets index showing the error
        if not ticket:
            webapp2.add_flash("ticket_not_exist")
            return self.redirect("/tickets")

        # If user is client and this is not his ticket set error and redirect to tickets list
        if user_info.email != ticket.owner_email and user_info.is_client():
            webapp2.add_flash("not_allowed_see_ticket")
            return self.redirect("/tickets")

        # Prepare variables to send to view
        template_variables = {
            "ticket": ticket,
            "ticket_model": Ticket,
            "MinCommentLength": ViewTicket.MinCommentLength
        }

        # Render 'view_ticket' view sending the variables 'template_variables'
        return Globals.render_template(self, "view_ticket.html", template_variables)

    def post(self, ticket_id):
        # Get current user information
        user, user_info = Globals.get_user_info()

        # Check if user is logged, if not redirect to home
        if not user or not user_info:
            webapp2.add_flash("not_logged_user")
            return self.redirect("/")

        # Get ticket by id
        ticket = ndb.Key(urlsafe=ticket_id).get()

        # If ticket doesn't exist go to tickets index showing the error
        if not ticket:
            webapp2.add_flash("ticket_not_exist")
            return self.redirect("/tickets")

        # If user is client and this is not his ticket set error and redirect to tickets list
        if user_info.email != ticket.owner_email and user_info.is_client():
            webapp2.add_flash("not_allowed_see_ticket")
            return self.redirect("/tickets")

        # Get new comment from request
        new_comment = self.request.get("comment", "").strip()

        # If the length of comment is lees than  'MinCommentLength' set error and redirect to ticket view
        if new_comment and len(new_comment) < ViewTicket.MinCommentLength:
            webapp2.add_flash("comment_too_short")
            return self.redirect("/tickets/view/" + ticket_id)

        # Set new comment to ticket
        ticket.comments.append(tickets.Comment(author=user_info.email, text=new_comment))

        # Report
        # tickets.send_email_chk_for(ticket, "checked", user_info.email + " says:\n" + new_comment)

        # Save ticket
        tickets.update(ticket)

        # Set successful comment and redirect to tickets view
        webapp2.add_flash("comment_added_successfully")
        return self.redirect("/tickets/view/" + ticket_id)


app = webapp2.WSGIApplication([
    ("/tickets/view/(.+)", ViewTicket),
], debug=True)
