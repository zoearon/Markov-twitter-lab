"""Generate Markov text from text files."""
import os
import sys
from random import choice
import twitter



def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    # your code goes here
    # file_name = (open(file_path)).read() + "."
    # return file_name
    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string, n_gram):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}
    words = text_string.split()
    for i in range(len(words)-n_gram):
        temp_list = []
        for z in range(n_gram):
            temp_list = temp_list + [words[i + z]]

        temp_tup = tuple(temp_list)

        # if temp_tup in chains:
        #     chains[temp_tup] = chains[temp_tup] + [words[i + 2]]
        # else:
        #     chains[temp_tup] = [words[i + 2]]
        chains.setdefault(temp_tup, [])
        chains[temp_tup].append(words[i + n_gram])
        #chains[temp_tup] = chains.get(temp_tup, []) + [words[i + 2]]

    return chains


def make_text(chains, n_gram):
    """Return text from chains."""
    words = []

    link_key = choice(chains.keys())


    while True:
        if link_key[0] != link_key[0].capitalize():
            link_key = choice(chains.keys())
        else:
            break
    #have random key from our dict
    counter = n_gram-1

    words = list(link_key)

    for item in words:
        counter += len(item)

    while link_key in chains:

        word = choice(chains[link_key])
        counter = counter + 1 + len(word)
        if counter > 140:
            break
        words.append(word)
        # link_key = (link_key[1], word)

        next_key = list(link_key[1:]) + [word]

        link_key = tuple(next_key)

    tweet_text = " ".join(words)

    count = 1
    for i in tweet_text[-1::-1]:
        count += 1
        if i == '.':
            tweet_text = tweet_text[:-count + 2]
            break

    return tweet_text


def tweet(chains):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.
    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    print api.VerifyCredentials()

    last_tweet = str(api.GetUserTimeline(count=1))

    for i in range(len(last_tweet)):
        if last_tweet[i] == "'":
            print "Your last tweet was: " + last_tweet[i+1:-3]
            print
            break

    status = api.PostUpdate(make_text(chains, 2))
    print status.text

    while True:
        tweet_again = raw_input("Enter to tweet again, q to quit: ")

        if tweet_again.lower() == 'q':
            break
        else:
            status = api.PostUpdate(make_text(chains))
            print status.text


# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text, 2)

# Your task is to write a new function tweet, that will take chains as input
tweet(chains)
