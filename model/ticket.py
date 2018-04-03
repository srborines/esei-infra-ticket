#!/usr/bin/env python
# coding: utf-8
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>


from google.appengine.api.mail import EmailMessage
from google.appengine.ext import ndb
import datetime as dt

from model.enums import Enum

from model.appinfo import AppInfo


class Comment(ndb.Model):
    author = ndb.TextProperty(indexed=True)
    text = ndb.TextProperty()


class Ticket(ndb.Model):
    Progress = Enum([
        "New", "Stalled", "Tracked",
        "Fixed", "Inappropriate", "Impossible"])

    Status = Enum(["Open", "Closed"], start=100)
    Priority = Enum(["Low", "Normal", "High"], start=200)
    Type = Enum(["Repair", "Printer", "Software", "Supplies"], start=300)

    serial = ndb.IntegerProperty(indexed=True, required=True)
    added = ndb.DateProperty(auto_now_add=True, indexed=True)
    title = ndb.TextProperty(indexed=True, required=True)
    owner_email = ndb.TextProperty(indexed=True, required=True)
    client_email = ndb.TextProperty(indexed=True)
    desc = ndb.TextProperty(required=True)
    progress = ndb.IntegerProperty(indexed=True)
    status = ndb.IntegerProperty(indexed=True)
    priority = ndb.IntegerProperty(indexed=True)
    type = ndb.IntegerProperty(indexed=True)
    classroom = ndb.TextProperty(indexed=True)
    comments = ndb.StructuredProperty(Comment, repeated=True)

    def __str__(self):
        return "#" + str(self.serial) + " " + self.title.encode("ascii", "replace")\
                + '\n' + str(self.added) + " (" + self.owner_email + ")\n"\
                + (" -> " + self.client_email if self.client_email else "")\
                + (" @ " + self.classroom if self.classroom else "")\
                + "\n|" + Ticket.Type.values[self.type] + " "\
                + Ticket.Priority.values[self.priority] + " "\
                + Ticket.Progress.values[self.progress] + " "\
                + Ticket.Status.values[self.status] + "| "\
                + "\n'" + self.desc.encode("ascii", "replace") + "'"


def create(user):
    """Creates a new ticket, given the author's user.

    :param user: The User (not GAE's user object) object.
    :return: A new Ticket object.
    """
    now = dt.datetime.today()
    num_tickets = Ticket.query(Ticket.added == now).count() + 1
    toret = Ticket()

    toret.serial = int(str.format(
                        "{0:04d}{1:02d}{2:02d}{3:02d}",
                        now.year, now.month, now.day, num_tickets))
    toret.title = "Big problem #" + str(num_tickets)
    toret.owner_email = user.email
    toret.client_email = ""
    toret.classroom = ""
    toret.desc = "Write a meaningful description of the problem, " \
                 "also the steps to reproduce it."
    toret.progress = Ticket.Progress.New
    toret.status = Ticket.Status.Open
    toret.type = Ticket.Type.Repair
    toret.priority = Ticket.Priority.Low

    return toret


def send_email_for(ticket, subject, body):
    str_time = dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    subject = subject.strip().lower()
    subject = subject[0].upper() + subject[1:]
    subject = subject + " ticket #" + str(ticket.serial)\
        + ' ' + ticket.title

    body = str_time + u'\n' + str(ticket) + u'\n'\
        + body + u"\n\n---\n\n" + AppInfo.AppWeb + u'\n'

    subject = subject.encode("ascii", "replace")
    body = body.encode("ascii", "replace")

    EmailMessage(
        sender=AppInfo.AppEmail,
        subject=subject,
        to=AppInfo.BroadcastEmail,
        body=body).send()

    if ticket.client_email:
        EmailMessage(
            sender=AppInfo.AppEmail,
            subject=subject,
            to=ticket.client_email,
            body=body).send()


@ndb.transactional
def update(ticket):
    """Updates a section.

        :param par: The ticket to update.
        :return: The key of the record.
    """
    return ticket.put()
