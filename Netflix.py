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
	return 3

# -------------
# netflix_solve
# -------------

def netflix_solve (r, w) :
    """
    read, eval, print ratings
    r is a reader
    w is a writer
    """

    correct_answers = read_correct_answers()
    our_answers = {}

    for t in netflix_read(r) :
    	if t[1] :
    		movieid = t[0]
    		w.write(str(movieid) + ":" + "\n")
    	else :
    		rating = netflix_predict(movieid, t[0])
    		our_answers[(movieid, t[0])] = rating
    		w.write(str(rating) + "\n")

    w.write("RMSE: %.4f\n" % rmse(our_answers, correct_answers))

def read_correct_answers():
	ratings_path = "../netflix-tests/irvin-probe_ratings.txt"
	custid_path = "/u/downing/cs/netflix/probe.txt"
	correct_answers = {}
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

def is_movieid(line):
	return ":" in line

def rmse(our_answers, correct_answers):
	s = 0.0
	for mc, rating in our_answers.items():
		#print("%s - %s = %s" % (rating, correct_answers[mc], rating - correct_answers[mc]))
		s += (rating - correct_answers[mc])**2
	#print("s = %s" % s)
	return math.sqrt(s/len(our_answers))