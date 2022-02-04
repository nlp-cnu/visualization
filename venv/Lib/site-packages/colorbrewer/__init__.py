#!/usr/bin/env python
from __future__ import absolute_import, division
__version__ = "0.2.0"
from six.moves import map

"""
__init__: DESCRIPTION

data copyright Cynthia Brewer, Mark Harrower, and The Pennsylvania State University
"""


# Copyright 2009, 2012 Michael M. Hoffman <mmh1@washington.edu>

from collections import defaultdict

from pkg_resources import resource_string
from csv import DictReader, reader as csv_reader

try:
    # Python 2.6+
    PKG = __name__
except NameError:
    PKG = "colorbrewer"

try:
    # Python 2.6+
    next
except NameError:
    def next(obj):
        return obj.__next__()

PKG_DATA = ".".join([PKG, "data"])

RES_COLORBREWER = "ColorBrewer_all_schemes_RGBonly3.csv"

DIALECT= "excel-tab"

def read_colorbrewer(iterable):
    res = defaultdict(dict)

    iterator = iter(iterable)
    fieldnames = next(csv_reader(iterator, DIALECT))
    reader = DictReader(iterator, fieldnames, dialect = DIALECT)

    for row in reader:
        def int_cell(colname):
            return int(row[colname])

        color_name = row["ColorName"]

        if color_name:
            num_of_colors = int_cell("NumOfColors")

            colors = []
            res[color_name][num_of_colors] = colors

        try:
            colors.append(tuple(map(int_cell, "RGB")))
        except ValueError:
            # data section is over
            break

    return res

def _load_schemes():
    lines = [line.decode() \
             for line in resource_string(PKG_DATA, RES_COLORBREWER).splitlines()]

    schemes = read_colorbrewer(lines)

    # copy schemes to module global variables
    globals().update(schemes)

_load_schemes()
