import json
import nltk
import matplotlib
import os
import re
import sqlite3
import cs50
from collections import OrderedDict
from sys import argv, exit

# *********************************************** EXPLANATION *********************************************** #
# This program takes the comment source file from https://files.pushshift.io/reddit/comments/ and creates a series of dicts to organize lexical data
# This source data is only parsable 'line by line'
# Subreddits are first organized into top 5k most commented subreddits (if doing this for multiple months will need to change this since top 5k isn't always the same)
# Word freq is organized by a nested dict with the first level the subreddit name, and the 2nd level kv pairs where the word is the key and the v is the freq
# If the parsed line is a comment from a sub in the top 5k, adds the instance of the word to the count of words in that subreddit's dictionary
# E.g. subreddit['politics']['the'] = 2, next time loop encounters 'the', subreddit['politics']['the'] = 3
# Then sorts the words by freq and eliminates the bottom 5% and adds to final dict
# Then a master freq list is created of all words across all subs with word freqs given in freq per 100k
# Add the data to a SQL database

# *********************************************** FURTHER WORK *********************************************** #
# Further work would entail making it possible to add data month by month to a cumulative total, and showing trends
# Would need to remove the filtering and write each month's full output to different files. 
# Then fur cum total, re-pop SQL for each addition and filter the data as it's written to the SQL database


f = open("wordcount.json", "w")
f.close()

count_all_comments = 0
comments_per_sub = 0
words_per_sub = 0

# Dictionary creation class
class my_dict(dict):
    def __init__(self):
        self = dict()
    def add(self, key, value):
        self[key] = value

# Counts the number of comments per subreddit
def comment_counter(f):
    comment_count = {}

    for line in f:
        loaded = json.loads(line)

        subreddit = loaded['subreddit'].casefold()

        if subreddit in comment_count:
            comment_count[subreddit] += 1
        else:
            comment_count[subreddit] = 1
    
    return comment_count

# Selects top 5000 subs
def select_subs(sorted_x):
    sorted_subs = my_dict()

    # Could probably do this as while i in range(len(sorted_x)) < 5000:
    for i in range(len(sorted_x)):
        sorted_subs.key = sorted_x[i][0]
        sorted_subs.value = sorted_x[i][1]
        if i < 5000:
            sorted_subs.add(sorted_subs.key, sorted_subs.value)
        else:
            break
    return sorted_subs

# Adds words to dictionary of subs
def make_sub_dict():
    dict_of_subs = {}
    subreddit_lex = []
    wordcount = my_dict()
    total_comments = 0
    total_words = 0

    with open(filename, 'r') as f:
        for line in f:
            total_comments += 1

            # Loads each line as a json object
            loaded = json.loads(line)

            subreddit = loaded['subreddit'].casefold()

            if subreddit in top_subs and subreddit not in dict_of_subs:
                dict_of_subs.update( {subreddit : {}} )
            
            # Tokenizes comment body
            subreddit_lex = nltk.tokenize.word_tokenize(loaded['body'])

            # Adds words to dict and counts words
            if subreddit in dict_of_subs:

                # Adds subreddit key to wordcount dict
                if subreddit not in wordcount:
                    wordcount.key = subreddit
                    wordcount.value = 0
                    wordcount.add(wordcount.key, wordcount.value)
                
                # Iterates through words in comment body
                for word in subreddit_lex:

                    # Adds words to subreddit frequency dict
                    word = word.lower()

                    # Old version. I like this better because it ignores all kinds of string junk, even if it misses emojis.
                    if not word.isalnum():
                        continue

                    # Counts up words in subreddit
                    wordcount[subreddit] += 1
                    total_words += 1

                    if word in dict_of_subs[subreddit]:
                        dict_of_subs[subreddit][word] += 1
                    else:
                        dict_of_subs[subreddit].update( {word : 1} )
        
        # Wordcount is the dict for number of words per subreddit, total words is a count of all words
        return dict_of_subs, wordcount, total_comments, total_words


# Adds k: v's to new dict until 95% of words in subreddit added
def select_words(s, c):
    
    add_to_dict = my_dict()
    word_sum = 0

    for i in range(len(s)):

        if word_sum/c < 0.95:
            add_to_dict.key = s[i][0]

            # Word freq out of 10,000
            add_to_dict.value = s[i][1]
            word_sum += s[i][1]
            add_to_dict.add(add_to_dict.key, add_to_dict.value)
        else:
            break

    return add_to_dict

# Sorts subreddit word freq
def result(dict, f, wc_dict):

    final_dict = {}

    for entry in lexicon:

        # Selects subreddits with over 10,000 words only
        if wc_dict[entry] >= 10000:
            dict[entry] = sorted(dict[entry].items(), key=lambda x: x[1], reverse=True)
            final_dict[entry] = f(dict[entry],wc_dict[entry])

    return final_dict

# Creates master reference for word frequencies out of 10k
def master_dict():

    word_totals = my_dict()

    for entry in r:
        for word in r[entry]:
            if word in word_totals:
                word_totals[word] += r[entry][word]
            else:
                word_totals.key = word
                word_totals.value = r[entry][word]
                word_totals.add(word_totals.key, word_totals.value)
    
    # Freqs of words out of 10k
    for word in word_totals:
        word_totals[word] = word_totals[word] / total_words * 10000

    return word_totals

# Execution
if len(argv) != 2:
    print("Usage: tofile.py <input path>")
    exit()
else:
    filename = argv[1]


with open(filename, 'r') as f:
    
    #### PRE PROCESSING ####
    # Counts number of comments in sub
    comments_per_sub = comment_counter(f)

    # Sorts subs by number of comments
    sorted_x = sorted(comments_per_sub.items(), key=lambda x: x[1], reverse=True)

    # Selects top 5000 subreddits and adds to dict
    top_subs = select_subs(sorted_x)

# Lexicon contains dict of word freqs for top 5k subs, total comments sum number of comments for top 5k subs, subreddit_wordcount counts total words per top 5k subs
lexicon, subreddit_wordcount, total_comments, total_words = make_sub_dict()

# Creates final dictionary of subreddits and word freqs
r = result(lexicon, select_words, subreddit_wordcount)

# Creates master word list of kept words. Unit is freq out of 10k. Total word count is for all alphanum words before 5% prune.
master = master_dict()

# Extracts date from input and returns database filename string
def db_titler(f):
    p = re.compile("([A-Z]{2,}_[0-9]{4,}-[0-9]{2,})")
    extract = p.search(f)
    result = "databases\\" + extract.group(1) + ".db"
    return result

conn = sqlite3.connect(db_titler(filename))

c = conn.cursor()

# Creates master word list table
c.execute("CREATE TABLE master (m_word TEXT, m_frequency REAL, id INTEGER PRIMARY KEY)")

for word in master:
    c.execute("INSERT INTO master (m_word, m_frequency) VALUES(?, ?)", (word, master[word]))

# Creates lexicon by subreddit
c.execute("CREATE TABLE lexicon (subreddit VARCHAR(22), subredditsearchkey VARCHAR(22), word TEXT, frequency REAL, id INTEGER PRIMARY KEY)")



# Not finding database for some reason
for entry in r:

    # Cleans the subreddit titles of periods
    cleaned = re.sub('\.', '',  entry)
    title = cleaned
    searchkey = cleaned.lower()

    # Loads the words
    for word in r[entry]:
        c.execute("INSERT INTO lexicon (subreddit, subredditsearchkey, word, frequency) VALUES(?, ?, ?, ?)", (title, searchkey, word, (r[entry][word] / subreddit_wordcount[entry] * 10000)))

conn.commit()
conn.close()


