#!/usr/bin/env python3

from flask import Flask
from flask import render_template
from flask import request

from forum.models import create_user, create_post, create_thread, add_reply, validate, get_threads, get_thread, \
    get_user, has_thread

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", threads=get_threads().keys())


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        if request.form['pwd'] != request.form['pwd2']:
            return "<p>Passwords don't match!</p>"
        if not request.form['jockesboll']:
            return "<p>We don't serve your kind here!</p>"
        create_user(request.form['name'], request.form['email'], request.form['pwd'])
        return render_template("welcome.html", username=request.form['name'])


@app.route("/makethread", methods=["GET", "POST"])
def make_thread():
    if request.method == "GET":
        return render_template("makethread.html")
    else:
        email = request.form['email']
        password = request.form['pwd']
        if not validate(email, password):
            return "Invalid user!"
        thread_name = request.form['threadname']
        post_contents = request.form['firstpost']
        post = create_post(get_user(email)['username'], post_contents)
        create_thread(thread_name, post)
        return render_template("thread.html", title=thread_name, posts=get_thread(thread_name))


@app.route("/thread/<thread_name>", methods=["GET", "POST"])
def view_thread(thread_name):
    if request.method == "GET":
        if has_thread(thread_name):
            return render_template("thread.html", title=thread_name, posts=get_thread(thread_name))
        return "<h1>Invalid thread!</h1>"
    else:
        email = request.form['email']
        password = request.form['pwd']
        if not validate(email, password):
            return "Invalid user!"
        post_contents = request.form['post']
        post = create_post(email, post_contents)
        add_reply(thread_name, post)
        return render_template("thread.html", title=thread_name, posts=get_thread(thread_name))


if __name__ == "__main__":
    app.run(ssl_context='adhoc')
