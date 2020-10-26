#!/usr/bin/env python3

from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

threads = {}
users = {}

def create_user(username, email, password):
    if email in users.keys():
        print(email + " has already been registered")
        return
    user = {}
    user["username"] = username
    user["email"] = email
    user["password"] = password
    users[email] = user

def create_post(poster, contents):
    post = {}
    post["poster"] = poster
    # todo: post["date"] = getDate()
    post["content"] = contents
    return post

def create_thread(threadname, firstpost):
    posts = []
    posts.append(firstpost)
    threads[threadname] = posts

def add_reply(threadname, post):
    thread = threads[threadname]
    thread.append(post)

def validate(email, password):
    if email not in users.keys():
        print("No such email registered")
        return False
    return users[email]["password"] == password

@app.route("/")
def index():
    return render_template("index.html", threads=threads.keys())

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
def makeThread():
    if request.method == "GET":
        return render_template("makethread.html")
    else:
        email = request.form['email']
        password = request.form['pwd']
        if not validate(email, password):
            return "Invalid user!"
        threadname = request.form['threadname']
        post_contents = request.form['firstpost']
        post = create_post(users[email]['username'], post_contents)
        create_thread(threadname, post)
        return render_template("thread.html", title=threadname, posts=threads[threadname])

@app.route("/thread/<threadname>", methods=["GET","POST"])
def getThread(threadname):
    if request.method == "GET":
        if threadname in threads:
            return render_template("thread.html", title=threadname, posts=threads[threadname])
        return "<h1>Invalid thread!</h1>"
    else:
        email = request.form['email']
        password = request.form['pwd']
        if not validate(email, password):
            return "Invalid user!"
        post_contents = request.form['post']
        post = create_post(email, post_contents)
        add_reply(threadname, post)
        return render_template("thread.html", title=threadname, posts=threads[threadname])
