from flask import Flask, redirect, render_template, request, session, jsonify
from tempfile import mkdtemp
from flask_session import Session
from os import listdir
from os.path import isfile, join
import re
import sqlite3
from math import sqrt

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Navbar on top with main page and link to description
# On main page, sidebar where user can select month
# Populated with the names of whatever files are in \databases dir
# Selecting link will launch a page and load appropriate db
    # Make some kind of dict that contains strings of all db paths
    # Populate sidebar with keys of this dict as names, values as db name string
    # When clicked, runs GET request and renders template of input form & assigns appropriate db object
    # Input form contains a field to ender desired subreddit
    # Submitting POST request runs query and prints results
    # Make sure to validate entry with 'valid' table
    # Maybe can get fancy and add some visualization

# I also want to set this up so when a subreddit is selected, it shows the top 20 words at each cutoff for desired time period
# Also want to show a time series of top 20 words over each db entry

def cleaner(s):
    cleaned = s

    # Cleans form input
    cleaned = re.sub('\.', '',  cleaned)

    # Regex for subs with leading numbers. Replace this with leading letter
    # p = re.compile("(^[0-9]{1,21})")

    # if p.search(cleaned):
        # cleaned = "[" + cleaned

    return cleaned

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]: #  (" ", "-")
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def checks_title(s, i):

    conn = sqlite3.connect("databases\\" + s + ".db")
    c = conn.cursor()

    searchreddit = cleaner(i).lower()

    c.execute("SELECT DISTINCT subreddit FROM lexicon WHERE subredditsearchkey=? LIMIT 1", (searchreddit,))

    titleselect = c.fetchone()

    #if titleselect is None:
        #return apology("Not found", 404)

    #if titleselect == None:
        #return apology("Not found", 404)

    #title = titleselect

    return titleselect

def runs_query(s, i):

    route = "//" + s

    # Connects to appropriate db
    conn = sqlite3.connect("databases\\" + s + ".db")
    c = conn.cursor()

    searchreddit = cleaner(i).lower()
    minfreq = request.form.get("min")

    # Runs query
    c.execute("SELECT word, frequency, m_frequency, (frequency / m_frequency) AS 'Uniqueness' FROM lexicon INNER JOIN master ON lexicon.word = master.m_word WHERE subredditsearchkey=? AND frequency>? AND (frequency / m_frequency) > 1 ORDER BY (frequency / m_frequency) DESC", (searchreddit, minfreq))

    result = c.fetchall()



    tablehead = ["A", "B", "C", "D"]

    return result, tablehead

def popnames(s):

    # Connects to appropriate db
    conn = sqlite3.connect("databases\\" + s + ".db")
    c = conn.cursor()

    # Gets subreddit names
    c.execute("SELECT DISTINCT subreddit FROM lexicon ORDER BY subreddit ASC")
    distinct = c.fetchall()

    return distinct

@app.route('/')
def index():

    return render_template("index.html")



@app.route("/RC_2006-02", methods = ["GET", "POST"])
def RC200602():

    name = "RC_2006-02"

    distinct = popnames(name)

    if request.method == "GET":

        return render_template(name + ".html", distinct=distinct, name=name)

    else:

        # Gets input from form
        input = request.form.get("subreddit")

        if input == '':
            return apology("Enter a Subreddit", 403)

        title = checks_title(name, input)

        if title is None:
            return apology("Not found", 404)

        title = title[0]

        result, tablehead = runs_query(name, input)

        return render_template(name + ".html", result=result, input=input, title=title, distinct=distinct, name=name, tablehead=tablehead)


@app.route("/RC_2010-08", methods = ["GET", "POST"])
def RC201008():

    name = "RC_2010-08"

    distinct = popnames(name)

    if request.method == "GET":

        return render_template(name + ".html", distinct=distinct, name=name)

    else:

        # Gets input from form
        input = request.form.get("subreddit")

        if input == '':
            return apology("Enter a Subreddit", 403)

        title = checks_title(name, input)

        if title is None:
            return apology("Not found", 404)

        title = title[0]

        result, tablehead = runs_query(name, input)

        return render_template(name + ".html", result=result, input=input, title=title, distinct=distinct, name=name, tablehead=tablehead)


@app.route("/RC_2016-11", methods = ["GET", "POST"])
def RC201611():

    name = "RC_2016-11"

    distinct = popnames(name)

    if request.method == "GET":

        return render_template(name + ".html", distinct=distinct, name=name)

    else:

        # Gets input from form
        input = request.form.get("subreddit")

        if input == '':
            return apology("Enter a Subreddit", 403)

        title = checks_title(name, input)

        if title is None:
            return apology("Not found", 404)

        title = title[0]

        result, tablehead = runs_query(name, input)

        return render_template(name + ".html", result=result, input=input, title=title, distinct=distinct, name=name, tablehead=tablehead)


##############TODO##############
# Redo the data display to make a column of words for each range of freqs instead of number spam (apply this, solution found in test.py)
# finish regex list in tofile.py and re-run
# Add a few more data points
# Re-do 2006-02
# Look into wordcloud visualization librarires
# Pretty it up
# Make the video and submit
# Future considerations: Time series wordcloud