#!/usr/bin/env python
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>


from google.appengine.ext import ndb
from google.appengine.api import users

from enum import Enum
from infra.appinfo import AppInfo


class User(ndb.Model):
    Level = Enum([
        "Admin",    # Can do anything
        "Staff",    # Can create tickets, make comments and close them.
        "Client"    # Can just read.
    ], start=400, default=2)

    added = ndb.DateProperty(auto_now_add=True, indexed=True)
    email = ndb.TextProperty(indexed=True)
    nick = ndb.TextProperty(indexed=True)
    level = ndb.IntegerProperty()

    def is_admin(self):
        return self.level == User.Level.Admin or users.is_current_user_admin()

    def is_client(self):
        return self.level == User.Level.Client

    def __str__(self):
        return User.Level.values[self.level] + ": " + self.nick + " (" + self.email + ")"


def create(usr, level):
    """Creates a new user object, from GAE's user object.

        :param usr: The GAE user object.
        :param level: The desired level.
        :return: A new User object."""
    toret = User()

    toret.email = usr.email()
    toret.nick = usr.nickname()
    toret.level = level
    toret.usr = usr

    return toret


def create_empty_user():
    """Used when there the user is not important."""
    return User(email="", nick="", level=User.Level.Client)


@ndb.transactional
def update(user):
    """Updates a user.

        :param user: The user to update.
        :return: The key of the record.
    """
    return user.put()


def retrieve(usr):
    """Reads the user info from the database.

    :param usr: The GAE user object.
    :return: The User retrieved, or a client created appropriately if not found.
    """
    toret = None

    if usr:
        usr_email = usr.email()
        users = User.query(User.email == usr_email).order(-User.added)

        if not users or users.count() < 1:
            if usr_email.endswith(AppInfo.AllowedUserEmailNamespace):
                toret = create(usr, User.Level.Client)
        else:
            toret = users.iter().next()
            toret.usr = usr

    return toret
