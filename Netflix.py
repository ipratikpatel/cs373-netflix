#!/usr/bin/env python3

# ------------------------------
# projects/netflix/TestNetflix.py
# Copyright (C) 2013
# Josh Kelle
# Pratik Patel
# -------------------------------

# -------------
# netflix_read
# -------------

import math

#########################
#  Reading cache files  #
#########################

correct_answers = {}
def read_correct_answers () :
    """
    Return a dictionary of (movieid, custid): (actual rating) pairs.
    """
    ratings_path = "/u/thunt/cs373-netflix-tests/irvin-probe_ratings.txt"
    custid_path = "/u/downing/cs/netflix/probe.txt"
    with open(ratings_path) as ratings_f, open(custid_path) as custid_f:
        for ratings_line in ratings_f.readlines():
            if is_movieid(ratings_line):
                movieid = int(ratings_line[:-2])
                assert custid_f.readline() == ratings_line
            else:
                custid = int(custid_f.readline())
                rating = int(ratings_line)
                correct_answers[(movieid, custid)] = rating
    return correct_answers

movie_avg_rating = {}
def read_avg_movie_ratings () :
    """
    Populate a dictionary of movieid: average_rating pairs.
    """
    path = "/u/thunt/cs373-netflix-tests/ericweb2-movieAveragesOneLine.txt"
    with open(path) as f :
        for line in f.readlines():
            movieid, rating = line.split(": ")
            movie_avg_rating[int(movieid)] = float(rating) 
    return movie_avg_rating

cust_avg_rating = {}
def read_avg_cust_ratings () :
    """
    Populate a dictionary of customer_id: average_rating pairs.
    """
    path = "/u/thunt/cs373-netflix-tests/ericweb2-custAveragesOneLine.txt"
    with open(path) as f :
        for line in f.readlines():
            custid, rating = line.split(": ")
            cust_avg_rating[int(custid)] = float(rating)
    return cust_avg_rating

movie_dec_avg_rating = {}
def read_dec_avg_movie_ratings () :
    """
    Populate a dictionary of movieid: decade average rating pairs.
    """
    path = "/u/thunt/cs373-netflix-tests/ericweb2-movieDecadeAvgRatingOneLine.txt"
    with open(path) as f :
        for line in f.readlines():
            movieid, rating = line.split(": ")
            movie_dec_avg_rating[int(movieid)] = float(rating)
    return movie_dec_avg_rating

cust_rating_by_decade = {}
def read_cust_rating_by_decade () :
    """
    Populate a dictionary of (custid, decade): avg_rating pairs.
    """
    path = "/u/thunt/cs373-netflix-tests/jkelle-avgByCustomeridByDecadeOneLine.txt"
    with open(path) as f :
        for line in f.readlines():
            custid, decade, avg_rating = line.split()
            cust_rating_by_decade[(int(custid), int(decade))] = float(avg_rating)
    return cust_rating_by_decade

movieid_to_decade = {}
def read_movie_to_decade():
    """
    Populate a dictionary of movieid : decade pairs.
    """
    path = "/u/thunt/cs373-netflix-tests/verstarr-movie_year.txt"
    with open(path) as f:
        for line in f.readlines():
            movieid, year = line.split(": ")
            if "NULL" in line or year[0] == "0":
                continue
            decade = int(year[:3] + "0")
            assert 1000 < decade < 3000
            movieid_to_decade[int(movieid)] = decade
    return movieid_to_decade

########################
#  Reading from input  #
########################

def netflix_read (r) :
    """
    read one line of the input file,
    r is a reader
    returns a tuple of number and boolean, 
        where boolean is True if number is Movie id, false otherwise
    """
    for line in r.readlines():
        line = line.rstrip()
        if line[-1] == ':' :
            yield int(line[ : -1]), True
        else :
            yield int(line), False

# -------------
# netflix_solve
# -------------

def netflix_predict (movieid, custid) :
    """
    Predict what customer custid will rate the movie movieid.
    movieid is the movie id.
    custid is the customer id.
    Return a float between 0 and 5 inclusive
    """
    if movieid in movieid_to_decade:
        decade = movieid_to_decade[movieid]
        assert( (custid, decade) in cust_rating_by_decade )
        ans = (cust_rating_by_decade[(custid, decade)] + movie_avg_rating[movieid])/2
    else:
        ans = (cust_avg_rating[custid] + movie_avg_rating[movieid])/2
    assert(0 <= ans <= 5)
    return ans

# -------------
# netflix_solve
# -------------

def netflix_solve (r, w) :
    """
    read, eval, print ratings
    r is a reader
    w is a writer
    """
    # reading from cache files
    read_correct_answers()
    read_avg_movie_ratings ()
    read_avg_cust_ratings ()
    read_dec_avg_movie_ratings ()
    #read_num_ratings_movie ()
    read_cust_rating_by_decade ()
    read_movie_to_decade ()

    our_answers = {}

    for t in netflix_read(r) :
        if t[1] :
            movieid = t[0]
            w.write(str(movieid) + ":" + "\n")
        else :
            rating = netflix_predict(movieid, t[0])
            our_answers[(movieid, t[0])] = rating
            w.write("%.4f\n" % rating)

    w.write("RMSE: %.4f\n" % rmse(our_answers, correct_answers))

def is_movieid(line):
    """
    Return True if the line represents a movieid, False otherwise.
    line is a string
    """
    return ":" in line

def rmse(our_answers, correct_answers):
    """
    Compute the root mean squared error of two iterables.
    our_answers     is a dictionary of (movieid, customerid) : (predicted rating) pairs.
    correct_answers is a dictionary of (movieid, customerid) : (actual    rating) pairs.
    """
    s = 0.0
    for mc, rating in our_answers.items():
        s += (rating - correct_answers[mc])**2
    return math.sqrt(s/len(our_answers))
