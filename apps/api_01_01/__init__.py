# -*- coding: utf-8 -*-
# __author__: taohu

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

from flask import Blueprint

api = Blueprint('api_01_01', __name__)

from . import views
