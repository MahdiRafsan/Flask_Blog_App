from flask import render_template, Blueprint

error = Blueprint("error", __name__)

@error.app_errorhandler(404)
def page_not_found(e):
    """ 
    display a custom 404 error page
    """
    return render_template("404.html"), 404

@error.app_errorhandler(403)
def forbidden_route(e):
    """ 
    display a custom 403 error page
    """
    return render_template("403.html"), 403

@error.app_errorhandler(500)
def server_error(e):
    """ 
    display a custom 500 error page
    """
    return render_template("500.html"), 500





