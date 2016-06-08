#!/usr/bin/env python

# Copyright 2014 Open Connectome Project (http://openconnecto.me)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# transform_graphs.py
# Created by Greg Kiar on 2016-06-03.
# Email: gkiar@jhu.edu

from argparse import ArgumentParser
from collections import OrderedDict
from compute_metrics import loadGraphs, constructGraphDict, write
from metrics import .

import numpy as np
import pickle
import os


def processGraphs(names, fs, outdir, atlas, verb=False)
    """
    Given sets of graphs, we perform the following procedure:
        compute metrics -> cluster graphs in metric space -> compute mean
        graph of each cluster -> compute transforms between clusters -> 
        transform graphs -> recompute metrics on transformed graphs
    """
    graphs = constructGraphDict(names, fs, verb=False)
    feat = computeFeatures(names, graphs)
    pass


def computeFeatures(names, graphs):
    """
    
    """
    feat = OrderedDict()

    # feat['ss1'] = compute_scan_statistic(graphs, names, 1)
    feat['deg'] = compute_degree(graphs, names)
    return feat


def computeTransforms():

    pass


def computeClusters(feat):
    """
    """
    pass


def flatten(diction):
    """
    """
    flat = OrderedDict()
    for keys in diction:
        flat.update(diction[keys])
    return flat

def loadGraphs(filenames, verb=False):
    """
    Given a list of files, returns a dictionary of graphs

    Required parameters:
        filenames:
            - List of filenames for graphs
    Optional parameters:
        verb:
            - Toggles verbose output statements
    """
    #  Initializes empty dictionary
    gstruct = OrderedDict()
    for idx, files in enumerate(filenames):
        if verb:
            print "Loading: " + files
        #  Adds graphs to dictionary with key being filename
        fname = os.path.basename(files)
        gstruct[fname] = nx.read_graphml(files)
    return gstruct


def constructGraphDict(names, fs, verb=False):
    """
    Given a set of files and a directory to put things, loads graphs.

    Required parameters:
        names:
            - List of names of the datasets
        fs:
            - Dictionary of lists of files in each dataset
    Optional parameters:
        verb:
            - Toggles verbose output statements
    """
    #  Loads graphs into memory for all datasets
    graphs = OrderedDict()
    for idx, name in enumerate(names):
        if verb:
            print "Loading Dataset: " + name
        # The key for the dictionary of graphs is the dataset name
        graphs[name] = loadGraphs(fs[name], verb=verb)


def main():
    """
    Argument parser and directory crawler. Takes organization and atlas
    information and produces a dictionary of file lists based on datasets
    of interest and then passes it off for processing.

    Required parameters:
        atlas:
            - Name of atlas of interest as it appears in the directory titles
        basepath:
            - Basepath for which data can be found directly inwards from
        outdir:
            - Path to derivative save location
    Optional parameters:
        fmt:
            - Determines file organization; whether graphs are stored as
              .../atlas/dataset/graphs or .../dataset/atlas/graphs. If the
              latter, use the flag.
        verb:
            - Toggles verbose output statements
    """
    parser = ArgumentParser(description="Computes Graph Metrics")
    parser.add_argument("atlas", action="store", help="atlas directory to use")
    parser.add_argument("basepath", action="store", help="base directory loc")
    parser.add_argument("outdir", action="store", help="base directory loc")
    parser.add_argument("-f", "--fmt", action="store_true", help="Formatting \
                        flag. True if bc1, False if greg's laptop.")
    parser.add_argument("-v", "--verb", action="store_true", help="")
    result = parser.parse_args()

    #  Currently hardcoding the datasets I care about.
    #  GK TODO: Fix eventually
    # dataset_names = list(('KKI2009', 'MRN114', 'MRN1313', 'SWU4',
    #                       'BNU1', 'BNU3', 'NKI1', 'NKIENH'))
    dataset_names = list(('KKI2009', 'MRN114', 'SWU4'))

    #  Sets up directory to crawl based on the system organization you're
    #  working on. Which organizations are pretty clear by the code, methinks..
    basepath = result.basepath
    atlas = result.atlas
    if result.fmt:
        dir_names = [basepath + '/' + d + '/' + atlas for d in dataset_names]
    else:
        dir_names = [basepath + '/' + atlas + '/' + d for d in dataset_names]

    #  Crawls directories and creates a dictionary entry of file names for each
    #  dataset which we plan to process.
    fs = OrderedDict()
    for idx, dd in enumerate(dataset_names):
        fs[dd] = [root + "/" + fl
                  for root, dirs, files in os.walk(dir_names[idx])
                  for fl in files if fl.endswith(".graphml")]

    print "Datasets: " + ", ".join([fkey + ' (' + str(len(fs[fkey])) + ')'
                                    for fkey in fs])

    p = Popen("mkdir -p " + result.outdir, shell=True)
    #  The fun begins and now we load our graphs and process them.
    driver(dataset_names, fs, result.outdir, atlas, result.verb)


if __name__ == "__main__":
    main()
