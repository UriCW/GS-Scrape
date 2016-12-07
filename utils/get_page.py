#!/usr/bin/env python
import sys
import os


if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from src.Helpers import *

    url="http://www.globalspec.com/search/products?page=ms#comp=2940&show=products&sqid=18975208"
    page=get(url)
    print(page)
