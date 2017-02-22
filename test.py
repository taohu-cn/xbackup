from flask import Flask, url_for, render_template

import generate

app = Flask(__name__)
app.config.from_object(generate)


@app.route("/favicon.ico")
def get_favicon():
    return app.send_static_file("favicon.ico")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    with app.test_request_context():
        print(url_for('hello'))

    app.run(
        host="127.0.0.1",
        port=5000,
    )
