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

# metrics.py
# Created by Greg Kiar on 2016-06-06.
# Email: gkiar@jhu.edu

from collections import OrderedDict
from scipy.stats import gaussian_kde

import numpy as np
import nibabel as nb
import networkx as nx
import os


def compute_scan_statistic(mygs, names, i=1):
    """
    Computes scan statistic-i on a set of graphs

    Required Parameters:
        mygs:
            - Dictionary of graphs
        names:
            - List of names of the datasets
     Optional Parameters:
        i:
            - which scan statistic to compute
    """
    ss_final = OrderedDict()
    for idx, name in enumerate(names):
        ss = OrderedDict()
        for key in mygs.keys():
            g = mygs[key]
            tmp = np.array(())
            for n in g.nodes():
                sg = nx.ego_graph(g, n, radius=i)
                tmp = np.append(tmp, np.sum([sg.get_edge_data(e[0], e[1])['weight']
                                for e in sg.edges()]))
            ss[key] = tmp
        ss_final[name] = density(ss)
    return ss_final


def compute_nnz(mygs, names):
    """
    Computes the number of non-zero edge weights on a set of graphs

    Required Parameters:
        mygs:
            - Dictionary of graphs
        names:
            - List of names of the datasets
    """
    nnz = OrderedDict()
    for idx, name in enumerate(names):
        nnz[name] = OrderedDict((subj, len(nx.edges(graphs[name][subj])))
                                for subj in graphs[name])
    return nnz


def compute_degree_sequence(mygs, names):
    """
    Computes the degree sequence on a set of graphs

    Required Parameters:
        mygs:
            - Dictionary of graphs
        names:
            - List of names of the datasets
    """
    deg = OrderedDict()
    for idx, name in enumerate(names):
        temp_deg = OrderedDict((subj, np.array(nx.degree(graphs[name][subj]).values()))
                               for subj in graphs[name])
        deg[name] = density(temp_deg)
    return deg


def compute_edge_weights(mygs, names):
    """
    Computes the distribution of edge weights on a set of graphs

    Required Parameters:
        mygs:
            - Dictionary of graphs
        names:
            - List of names of the datasets
    """
    ew = OrderedDict()
    for idx, name in enumerate(names):
        temp_ew = OrderedDict((subj, [graphs[name][subj].get_edge_data(e[0], e[1])['weight']
                              for e in graphs[name][subj].edges()])
                              for subj in graphs[name])
        ew[name] = density(temp_ew)
    write(outdir, 'edgeweight', ew, atlas)


def compute_clustering_coeffs(mygs, names):
    """
    Computes the clustering coefficients on a set of graphs

    Required Parameters:
        mygs:
            - Dictionary of graphs
        names:
            - List of names of the datasets
    """
    ccoefs = OrderedDict()
    nxc = nx.clustering  # For PEP8 line length...
    for idx, name in enumerate(names):
        temp_cc = OrderedDict((subj, nxc(graphs[name][subj]).values())
                              for subj in graphs[name])
        ccoefs[name] = density(temp_cc)
    write(outdir, 'ccoefs', ccoefs, atlas)


def compute_eigen_values(mygs, names):
    """
    Computes the eigen values on a set of graphs

    Required Parameters:
        mygs:
            - Dictionary of graphs
        names:
            - List of names of the datasets
    """
    laplacian = OrderedDict()
    eigs = OrderedDict()
    for idx, name in enumerate(names):
        laplacian[name] = OrderedDict((subj, nx.normalized_laplacian_matrix(graphs[name][subj]))
                                      for subj in graphs[name])
        eigs[name] = OrderedDict((subj, np.sort(np.linalg.eigvals(laplacian[name][subj].A))[::-1])
                                 for subj in graphs[name])
    write(outdir, 'eigs', eigs, atlas)


def compute_betweenness_centrality(mygs, names):
    """
    Computes the betweenness centraliry on a set of graphs

    Required Parameters:
        mygs:
            - Dictionary of graphs
        names:
            - List of names of the datasets
    """
    centrality = OrderedDict()
    nxbc = nx.algorithms.betweenness_centrality  # For PEP8 line length...
    for idx, name in enumerate(names):
        temp_bc = OrderedDict((subj, nxbc(graphs[name][subj]).values())
                              for subj in graphs[name])
        centrality[name] = density(temp_bc)
    write(outdir, 'centrality', centrality, atlas)


def compute_density(data):
    """
    Computes density for metrics which return vectors

    Required parameters:
        data:
            - Dictionary of the vectors of data
    """
    density = OrderedDict()
    xs = OrderedDict()
    for subj in data:
        dens = gaussian_kde(data[subj])
        xs[subj] = np.linspace(0, 1.2*np.max(data[subj]), 1000)
        density[subj] = dens.pdf(xs[subj])

    return {"xs": xs, "pdfs": density}

