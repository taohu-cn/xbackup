# -*- coding: utf-8 -*-
# __author__: taohu

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
from flask import render_template
from . import root


@root.route("/favicon.ico")
def get_favicon():
    return root.send_static_file("favicon.ico")


@root.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@root.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


@root.route('/')
def index():
    return render_template("index.html")
