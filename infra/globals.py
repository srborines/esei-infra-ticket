from webapp2_extras import jinja2

import model.user as usr_mgt
from google.appengine.api import users

from infra.appinfo import AppInfo


class Globals:
    def __init__(self):
        pass

    @staticmethod
    def get_user_info():
        # Get current user entity
        user = users.get_current_user()

        # Get current user information
        user_info = usr_mgt.retrieve(user)

        # Return both variables
        return user, user_info

    @staticmethod
    def render_template(entity, template, variables):
        # If variables is False or None convert to an empty dictionary
        variables = variables if variables else {}

        # Add app info to view variable
        variables["info"] = AppInfo

        # By default add view variable 'logged' to False
        variables["logged"] = False

        # Get user info
        user, user_info = Globals.get_user_info()

        # If user is logged in set 'logged' view variable to True and add user info
        if user and user_info:
            variables["logged"] = True
            variables["usr_info"] = user_info

        # Obtain Jinja instance
        jinja = jinja2.get_jinja2(app=entity.app)

        # Render view 'template' with the variables 'variables' using Jinja
        entity.response.write(jinja.render_template(template, **variables));
