#!/usr/bin/env python
# (c) Baltasar 2018 MIT License <baltasarq@gmail.com>


from google.appengine.ext import ndb


class Ticket(ndb.Model):
    added = ndb.DateProperty(auto_now_add=True)
    title = ndb.TextProperty()
    desc = ndb.TextProperty()
    status = ndb.IntegerProperty()


@ndb.transactional
def update(section):
    """Updates a section.

        :param par: The section to update.
        :return: The key of the section.
    """
    return section.put()
