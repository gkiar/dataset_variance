#!/usr/bin/env python

# Copyright 2016 NeuroData (http://neurodata.io)
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

# plotly_panels.py
# Created by Greg Kiar on 2016-09-19.
# Email: gkiar@jhu.edu

import numpy as np
from scipy.stats import gaussian_kde
from itertools import product
from plotly.graph_objs import *
from plotly import tools


def plot_density(xs, ys, name=None):
    data = list()
    for idx, x in enumerate(xs):
        data += [
                 Scatter(
                         x=xs[idx],
                         y=ys[idx],
                         line=Line(
                                   color='rgba(0,0,0,0.05)'
                                  ),
                         hoverinfo='x',
                         name=name
                        )
                ]
    layout = std_layout(name)
    fig = Figure(data=data, layout=layout)
    return fig
    
def plot_rugdensity(series, name=None):
    dens = gaussian_kde(series)
    x = np.linspace(np.min(series), np.max(series), 1000)
    y = dens.evaluate(x)

    d_dens = Scatter(
                x=x,
                y=y,
                line=Line(
                       color='rgb(0,0,0)'
                     ),
                hoverinfo='x',
                name=name
           )
    d_rug = Scatter(
                x=series,
                y=[0]*len(series),
                mode='markers',
                marker=Marker(
                         color='rgb(0,0,0)',
                         symbol='line-ns-open',
                         size=10,
                         opacity=0.5
                       ),
                name=name
          )
    data = [d_dens, d_rug]
    layout = std_layout(name)
    fig = Figure(data=data, layout=layout)
    return fig


def std_layout(name=None):
    return Layout(
            title=name,
            showlegend=False,
            xaxis={'nticks':5},
            yaxis={'nticks':3}
          )

def fig_to_trace(fig):
    data = fig['data']
    for item in data:
        item.pop('xaxis', None)
        item.pop('yaxis', None)
    return data


def traces_to_panels(traces, names=[]):
    r, c, locs = panel_arrangement(len(traces))
    multi = tools.make_subplots(rows=r, cols=c, subplot_titles=names)
    for idx, loc in enumerate(locs):
        if idx < len(traces):
            for component in traces[idx]:
                multi.append_trace(component, *loc)
        else:
            multi = panel_invisible(multi, idx+1)
    multi.layout['showlegend']=False
    return multi


def panel_arrangement(num):
    dims = list()
    count = 0
    while len(dims) == 0:
        dims = list(factors(num+count))
        count += 1

    if len(dims) == 1:
        row = col = dims[0]
    else:
        row = dims[0]
        col = dims[-1]

    locations = [(a+1, b+1) for a,b in product(range(row), range(col))]
    return row, col, locations


def panel_invisible(plot, idx):
    for c in ['x', 'y']:
        axe = c+'axis'+str(idx)
        plot.layout[axe]['showgrid'] = False
        plot.layout[axe]['zeroline'] = False
        plot.layout[axe]['showline'] = False
        plot.layout[axe]['showticklabels'] = False
    return plot

def rand_jitter(arr):
    stdev = .03*(max(arr)-min(arr)+2)
    return arr + np.random.randn(len(arr)) * stdev


def factors(N): 
    return set([item for subitem in 
                [(i, N//i) for i in range(1, int(N**0.5) + 1) if N % i == 0 and i > 1]
                for item in subitem])