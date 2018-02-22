# Boli
# GAE application to assist in the process of writing
# Manage stories belonging to a user

import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users


from model.appinfo import AppInfo
from model.story import Story


class StoriesManager(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if user:
            user_name = user.nickname()
            stories = Story.query(Story.user == user.user_id()).order(-Story.added)
            access_link = users.create_logout_url("/")

            template_values = {
                "info": AppInfo,
                "user_name": user_name,
                "access_link": access_link,
                "stories": stories
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("stories.html", **template_values))
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([
    ('/manage_stories', StoriesManager),
], debug=True)
