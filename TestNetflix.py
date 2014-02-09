#!/usr/bin/env python3

# ------------------------------
# projects/netflix/TestNetflix.py
# Copyright (C) 2013
# Josh Kelle
# Pratik Patel
# -------------------------------


"""
To test the program:
    % python TestNetflix.py > TestNetflix.out
    % chmod ugo+x TestNetflix.py
    % TestNetflix.py > TestNetflix.out
"""

# -------
# imports
# -------

import io
import unittest

from Netflix import *

# -----------
# TestNetflix
# -----------

class TestNetflix (unittest.TestCase) :
    # ----
    # read
    # ----

    def test_read_1 (self) :
        r = io.StringIO("1:\n106\n")
        p = netflix_read(r)
        (i, j) = p.__next__()
        self.assertTrue(i ==  1)
        self.assertTrue(j == True)
        (i, j) = p.__next__()
        self.assertTrue(i ==  106)
        self.assertTrue(j == False)

    def test_read_2 (self) :
        r = io.StringIO("1:\n106")
        p = netflix_read(r)
        (i, j) = p.__next__()
        self.assertTrue(i ==  1)
        self.assertTrue(j == True)
        (i, j) = p.__next__()
        self.assertTrue(i ==  106)
        self.assertTrue(j == False)

    def test_read_3 (self) :
        r = io.StringIO("1:\n106\n506")
        p = netflix_read(r)
        (i, j) = p.__next__()
        self.assertTrue(i ==  1)
        self.assertTrue(j == True)
        (i, j) = p.__next__()
        self.assertTrue(i ==  106)
        self.assertTrue(j == False)
        (i, j) = p.__next__()
        self.assertTrue(i ==  506)
        self.assertTrue(j == False)

    def test_read_4 (self) :
        r = io.StringIO("")
        try:
            p = netflix_read(r)
            (i, j) = p.__next__()
        except StopIteration as e :
            self.assertTrue(True)
        else:
            self.assertTrue(False) 

    # ----
    # netflix_predict
    # ----

    def test_predictor_1 (self) :
        movieid = 1
        custid = 30878
        self.assertTrue(netflix_predict(movieid, custid) == 3) 

    def test_predictor_2 (self) :
        movieid = 1
        custid = 2647871
        self.assertTrue(netflix_predict(movieid, custid) == 3) 

    def test_predictor_3 (self) :
        movieid = 10
        custid = 1952305
        self.assertTrue(netflix_predict(movieid, custid) == 3) 

    # ----
    # solve
    # ----

    def test_solve_1 (self) :
        r = io.StringIO("1:\n30878\n2647871\n1283744")
        w = io.StringIO()
        netflix_solve(r, w)
        self.assertTrue(w.getvalue() == "1:\n3\n3\n3\nRMSE: 0.8165\n")

    def test_solve_2 (self) :
        r = io.StringIO("1000:\n2326571\n977808\n1010534\n")
        w = io.StringIO()
        netflix_solve(r, w)
        self.assertTrue(w.getvalue() == "1000:\n3\n3\n3\nRMSE: 0.5774\n")

    def test_solve_3 (self) :
        r = io.StringIO("1:\n30878\n2647871\n1283744\n1000:\n2326571\n977808\n1010534\n")
        w = io.StringIO()
        netflix_solve(r, w)
        self.assertTrue(w.getvalue() == "1:\n3\n3\n3\n1000:\n3\n3\n3\nRMSE: 0.7071\n")

    # ----
    # read_correct_answer
    # ----

    def test_check_1 (self) :
        corr_ans = read_correct_answers()
        self.assertTrue(corr_ans[(1, 30878)] == 4)

    def test_check_2 (self) :
        corr_ans = read_correct_answers()
        self.assertTrue(corr_ans[(1, 1283744)] == 3)

    def test_check_3 (self) :
        corr_ans = read_correct_answers()
        self.assertTrue(corr_ans[(1000, 2326571)] == 3)

    # ----
    # is_movieid
    # ----

    def test_check_movieid_1 (self) :
        self.assertTrue(is_movieid("1:"))

    def test_check_movieid_2 (self) :
        self.assertTrue(not is_movieid("10"))

    def test_check_movieid_3 (self) :
        self.assertTrue(is_movieid("1000000: \n"))

    # ----
    # rmse
    # ----

    def test_rmse_1 (self) :
        dict1 = {(1,1) : 0, (1,2) : 0, (1,3) : 0, (1,4) : 0}
        dict2 = {(1,1) : 1, (1,2) : 1, (1,3) : 1, (1,4) : 1}
        self.assertTrue(rmse(dict1, dict2) == 1.0)

    def test_rmse_2 (self) :
        dict1 = {(1,30878) : 3, (1,2647871) : 3, (1,1283744) : 3}
        dict2 = {(1,30878) : 4, (1,2647871) : 4, (1,1283744) : 3}
        self.assertTrue("%.4f" % rmse(dict1, dict2) == "0.8165")

    def test_rmse_3 (self) :
        dict1 = {(1000,2326571) : 3, (1000,977808) : 3, (1000,1010534) : 3}
        dict2 = {(1000,2326571) : 3, (1000,977808) : 3, (1000,1010534) : 2}
        self.assertTrue("%.4f" % rmse(dict1, dict2) == "0.5774")



unittest.main()