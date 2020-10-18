from flask_nav.elements import View, Navbar
from flask_bootstrap.nav import BootstrapRenderer
from flask_nav import register_renderer
from flask_nav import Nav
from flask_nav.elements import *
from dominate.tags import img
from flask import current_app as app

# To keep things clean, we keep our Flask-Nav instance in here. We will define
# frontend-specific navbars in the respective frontend, but it is also possible
# to put share navigational items in here.

branding = img(src='static/logotype_dark.png')
topbar = Navbar(
    branding,
    View('Home', 'home_bp.home'),
    View('Trends', 'trends_bp.trends'),
    View('Control', 'control_bp.control'),
    View('Admin', 'admin_bp.admin'),
    View('Help', 'home_bp.help')
)

nav = Nav()
nav.init_app(app)
nav.register_element('top', topbar)


# Custom Navbar Renderer to render after certain bootstrap navbars templates
class CustomRenderer(BootstrapRenderer):
    def visit_Navbar(self, node):
        nav_tag = super(CustomRenderer, self).visit_Navbar(node)
        nav_tag['class'] += 'navbar navbar-inverse navbar-fixed-top'
        return nav_tag

     
register_renderer(app, 'custom', CustomRenderer)
