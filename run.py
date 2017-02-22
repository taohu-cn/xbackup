# -*- coding: utf-8 -*-
# __author__: taohu

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

from flask import Flask
import generate


def create_app():
    app = Flask(__name__)
    app.config.from_object(generate)

    from apps.root import root
    app.register_blueprint(root, url_prefix='/')

    from apps.api_01_01 import api
    app.register_blueprint(api, url_prefix='/api')

    return app


if __name__ == '__main__':
    App = create_app()
    # with App.test_request_context():
    #     print(url_for('root.index'))
    #     print(url_for('api_01_01.data_post'))

    # App.run(debug=App.debug, host='0.0.0.0', port=5001)
    App.run(debug=App.debug, host='127.0.0.1', port=5001)
