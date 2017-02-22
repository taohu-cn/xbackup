# -*- coding: utf-8 -*-
# __author__: taohu

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
from flask import Blueprint

root = Blueprint('root', __name__)

from . import views
