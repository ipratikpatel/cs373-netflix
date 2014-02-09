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

def netflix_solve (r, w) :
    """
    read, eval, print ratings
    r is a reader
    w is a writer
    """
    for t in netflix_read(r) :
    	print (t)
