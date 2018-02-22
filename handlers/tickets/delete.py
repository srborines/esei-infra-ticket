#!/usr/bin/env python
# MIT License
# (c) baltasar 2015

import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import jinja2

import model.remove_data
from model.appinfo import AppInfo
from model.story import Story


class DeleteStory(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET['story_id']
        except:
            id = None

        if not id:
            self.redirect("/error?msg=Key missing for deletion.")
            return

        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                story = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=Key was not found.")
                return

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "story": story,
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("delete_story.html", **template_values));
        else:
            self.redirect("/")

    def post(self):
        try:
            id = self.request.GET['story_id']
        except:
            self.redirect("/error?msg=Key missing for deletion.")
            return

        user = users.get_current_user()

        if user and id:
            try:
                story = ndb.Key(urlsafe=id).get()
            except:
                self.redirect("/error?msg=Key was not found.")
                return

            self.redirect("/info?msg=Story deleted: "
                + story.title.encode("ascii", "replace")
                + "&url=/manage_stories")

            # Remove story
            model.remove_data.remove_story(story.key)
        else:
            self.redirect("/")

app = webapp2.WSGIApplication([
    ("/stories/delete", DeleteStory),
], debug=True)
