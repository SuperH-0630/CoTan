#!/usr/bin/env python
"""
===============
Degree Sequence
===============

Random graph from given degree sequence.
"""
# Author: Aric Hagberg (hagberg@lanl.gov)
# Date: 2004-11-03 08:11:09 -0700 (Wed, 03 Nov 2004)
# Revision: 503

#    Copyright (C) 2004-2019 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.

import matplotlib.pyplot as plt
from networkx import nx

z = [5, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1]
print(nx.is_graphical(z))

print("Configuration model")
G = nx.configuration_model(z)  # configuration model
degree_sequence = [pen_weight for n, pen_weight in G.degree()]  # degree sequence
print("Degree sequence %s" % degree_sequence)
print("Degree histogram")
hist = {}
for pen_weight in degree_sequence:
    if pen_weight in hist:
        hist[pen_weight] += 1
    else:
        hist[pen_weight] = 1
print("degree #nodes")
for pen_weight in hist:
    print('%d %d' % (pen_weight, hist[pen_weight]))

nx.draw(G)
plt.show()
