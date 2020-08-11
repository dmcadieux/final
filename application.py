from flask import Flask, redirect, render_template, request, session, jsonify
from tempfile import mkdtemp
from flask_session import Session
import os
from os.path import isfile, join
import sqlite3
from math import log
from functions import apology, checks_title, cleaner, runs_query, popnames, make_graph

# Dict class creator
class my_dict(dict):
    def __init__(self):
        self = dict()
    def add(self, key, value):
        self[key] = value

app = Flask(__name__)

# Adds log to filters
app.add_template_filter(log)

Session(app)

@app.route('/')
def index():

    return render_template("index.html")



@app.route("/RC_2006-02", methods = ["GET", "POST"])
def RC200602():

    name = "RC_2006-02"

    distinct = popnames(name)

    if request.method == "GET":

        graph = {}

        show = 0

        return render_template(name + ".html", distinct=distinct, name=name, graph=graph, show=show)

    else:

        show = 1

        # Gets input from form
        input = request.form.get("subreddit")

        # Checks if blank
        if input == '':
            return apology("Enter a Subreddit", 403)

        title = checks_title(name, input)

        if title is None:
            return apology("Not found", 404)

        title = "/r/" + title[0]

        result, tablehead = runs_query(name, input)

        graph = make_graph(result)

        return render_template(name + ".html", result=result, input=input, title=title, distinct=distinct, name=name, tablehead=tablehead, graph=graph, show=show)


@app.route("/RC_2010-08", methods = ["GET", "POST"])
def RC201008():

    name = "RC_2010-08"

    distinct = popnames(name)

    if request.method == "GET":

        graph = {}

        show = 0

        return render_template(name + ".html", distinct=distinct, name=name, graph=graph, show=show)

    else:

        show = 1

        # Gets input from form
        input = request.form.get("subreddit")

        # Checks if blank
        if input == '':
            return apology("Enter a Subreddit", 403)

        title = checks_title(name, input)

        if title is None:
            return apology("Not found", 404)

        title = "/r/" + title[0]

        result, tablehead = runs_query(name, input)

        graph = make_graph(result)

        return render_template(name + ".html", result=result, input=input, title=title, distinct=distinct, name=name, tablehead=tablehead, graph=graph, show=show)



@app.route("/RC_2011-01", methods = ["GET", "POST"])
def RC201101():

    name = "RC_2011-01"

    distinct = popnames(name)

    if request.method == "GET":

        graph = {}

        show = 0

        return render_template(name + ".html", distinct=distinct, name=name, graph=graph, show=show)

    else:

        show = 1

        # Gets input from form
        input = request.form.get("subreddit")

        # Checks if blank
        if input == '':
            return apology("Enter a Subreddit", 403)

        title = checks_title(name, input)

        if title is None:
            return apology("Not found", 404)

        title = "/r/" + title[0]

        result, tablehead = runs_query(name, input)

        graph = make_graph(result)

        return render_template(name + ".html", result=result, input=input, title=title, distinct=distinct, name=name, tablehead=tablehead, graph=graph, show=show)


@app.route("/RC_2016-11", methods = ["GET", "POST"])
def RC201611():

    name = "RC_2016-11"

    distinct = popnames(name)

    if request.method == "GET":

        graph = {}

        show = 0

        return render_template(name + ".html", distinct=distinct, name=name, graph=graph, show=show)

    else:

        show = 1

        # Gets input from form
        input = request.form.get("subreddit")

        # Checks if blank
        if input == '':
            return apology("Enter a Subreddit", 403)

        title = checks_title(name, input)

        if title is None:
            return apology("Not found", 404)

        title = "/r/" + title[0]

        result, tablehead = runs_query(name, input)

        graph = make_graph(result)

        return render_template(name + ".html", result=result, input=input, title=title, distinct=distinct, name=name, tablehead=tablehead, graph=graph, show=show)


@app.route("/RC_2017-06", methods = ["GET", "POST"])
def RC201706():

    name = "RC_2017-06"

    distinct = popnames(name)

    if request.method == "GET":

        graph = {}

        show = 0

        return render_template(name + ".html", distinct=distinct, name=name, graph=graph, show=show)

    else:

        show = 1

        # Gets input from form
        input = request.form.get("subreddit")

        # Checks if blank
        if input == '':
            return apology("Enter a Subreddit", 403)

        title = checks_title(name, input)

        if title is None:
            return apology("Not found", 404)

        title = "/r/" + title[0]

        result, tablehead = runs_query(name, input)

        graph = make_graph(result)

        return render_template(name + ".html", result=result, input=input, title=title, distinct=distinct, name=name, tablehead=tablehead, graph=graph, show=show)



@app.route("/RC_2018-02", methods = ["GET", "POST"])
def RC201802():

    name = "RC_2018-02"

    distinct = popnames(name)

    if request.method == "GET":

        graph = {}

        show = 0

        return render_template(name + ".html", distinct=distinct, name=name, graph=graph, show=show)

    else:

        show = 1

        # Gets input from form
        input = request.form.get("subreddit")

        # Checks if blank
        if input == '':
            return apology("Enter a Subreddit", 403)

        title = checks_title(name, input)

        if title is None:
            return apology("Not found", 404)

        title = "/r/" + title[0]

        result, tablehead = runs_query(name, input)

        graph = make_graph(result)

        return render_template(name + ".html", result=result, input=input, title=title, distinct=distinct, name=name, tablehead=tablehead, graph=graph, show=show)
