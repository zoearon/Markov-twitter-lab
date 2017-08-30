import os
import sys
from random import choice
import twitter


def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    key = choice(chains.keys())
    while True:
        if key[0] != key[0].capitalize():
            key = choice(chains.keys())
        else:
            break
    #key = choice(chains.keys())
    words = [key[0], key[1]]
    counter = len(key[0] + key[1]) + 1
    # length of the first words and space

    while key in chains:
        # Keep looping until we have a key that isn't in the chains
        # (which would mean it was the end of our original text)
        #
        # Note that for long texts (like a full book), this might mean
        # it would run for a very long time.
        word = choice(chains[key])
        counter = counter + 1 + len(word)
        if counter > 140:
            break
        words.append(word)
        key = (key[1], word)

    tweet_text = " ".join(words)
    print tweet_text

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

    status = api.PostUpdate(make_text(chains))
    print status.text

    while True:
        tweet_again = raw_input("Enter to tweet again, q to quit: ")

        if tweet_again.lower() == 'q':
            break
        else:
            status = api.PostUpdate(make_text(chains))
            print status.text


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

# Your task is to write a new function tweet, that will take chains as input
tweet(chains)
#print make_text(chains)

# # Open the file and turn it into one long string
# input_text = open_and_read_file(filenames)

# # Get a Markov chain
# chains = make_chains(input_text)

# # Produce random text
# random_text = make_text(chains)