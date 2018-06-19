#!/usr/bin/env python

from urlhash import UrlHasher

"""
Simple console program to store / retrieve urls
"""

if __name__ == "__main__":
    uhash = UrlHasher()
    exit(uhash.main())
