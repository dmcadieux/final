import sqlite3
from math import sqrt, log
import re
from flask import request, render_template

def cleaner(s):
    cleaned = s

    # Cleans form input
    cleaned = re.sub('\.', '',  cleaned)

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

    return titleselect

def runs_query(s, i):

    route = "//" + s

    # Connects to appropriate db
    conn = sqlite3.connect("databases\\" + s + ".db")

    # Makes rows readable by header
    conn.row_factory = sqlite3.Row

    # Creates cursor object
    c = conn.cursor()

    searchreddit = cleaner(i).lower()
    minfreq = request.form.get("min")

    # Runs query
    c.execute("SELECT word, frequency, m_frequency, ((frequency / m_frequency) * frequency) AS 'Uniqueness' FROM lexicon INNER JOIN master ON lexicon.word = master.m_word WHERE subredditsearchkey=? AND frequency>? ORDER BY ((frequency / m_frequency) * frequency) DESC", (searchreddit, minfreq))

    result = c.fetchall()

    tablehead = ["Word", "Freq Sub", " Freq All", "Uniqueness"]

    return result, tablehead

def popnames(s):

    # Connects to appropriate db
    conn = sqlite3.connect("databases\\" + s + ".db")
    c = conn.cursor()

    # Gets subreddit names
    c.execute("SELECT DISTINCT subreddit FROM lexicon ORDER BY subreddit ASC")
    distinct = c.fetchall()

    return distinct

# Called in application.py for export to template. Used to pop graph.
def make_graph(input):
    storage = []

    for row in input:
        json = {'x': log(row['uniqueness']), 'y': row['frequency']}
        storage.append(json)

    return storage