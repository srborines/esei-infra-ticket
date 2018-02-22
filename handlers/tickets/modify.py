#!/usr/bin/env python
# MIT License
# (c) baltasar 2017

import datetime
import time

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

from model.story import Story
from model.appinfo import AppInfo


class ModifyStory(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['story_id']
        except:
            self.redirect("/error?msg=story was not found")
            return

        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                story = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=key does not exist")
                return

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "story": story,
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("modify_story.html", **template_values));
        else:
            self.redirect("/")

    def post(self):
        try:
            id = self.request.GET['story_id']
        except:
            id = None

        if not id:
            self.redirect("/error?msg=missing id for modification")
            return

        user = users.get_current_user()
        story = None

        if user:
            # Get story by key
            try:
                story = ndb.Key(urlsafe = id).get()
            except:
                self.redirect("/error?msg=key does not exist")
                return

            story.title = self.request.get("title", "").strip()
            story.subtitle = self.request.get("subtitle", "").strip()
            story.summary = self.request.get("summary", "").strip()

            # Chk
            if len(story.title) < 1:
                self.redirect("/error?msg=Aborted modification: missing title")
                return

            # Chk title
            existing_stories = Story.query(Story.title == story.title)
            if  (existing_stories
             and existing_stories.count() > 0
             and existing_stories.get() != story):
                self.redirect("/error?msg=Story with title \""
                            + story.title.encode("ascii", "replace")
                            + "\" already exists.")
                return

            # Save
            story.put()
            self.redirect("/info?msg=Story modified: \""
                + story.title.encode("ascii", "replace")
                + "\"&url=/manage_stories")
        else:
            self.redirect("/")

app = webapp2.WSGIApplication([
    ("/stories/modify", ModifyStory),
], debug=True)
