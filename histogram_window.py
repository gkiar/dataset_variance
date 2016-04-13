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

# histogram_window.py
# Created by Greg Kiar on 2016-03-29.
# Email: gkiar@jhu.edu

from ipywidgets import widgets
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys


class histogram_windowing():

    def __init__(self, fname, name, color=False):
        self.fname = fname
        self.name = name
        self.color = color
        self.gd()
        self.update()

    def gd(self):
        """
        Get pdf and xs from file
        """
        inf = open(self.fname)
        tdat = pickle.load(inf)
        self.tpdfs = tdat['pdfs']
        self.txs = tdat['xs']
        inf.close()

    def plotting(self, xl, xh):
        """
        Define interactive plot function for altering pdf range
        """
        # eps = np.min([np.min(self.tpdfs[key]) for key in self.tpdfs.keys() if np.min(self.tpdfs[key]) > 0])
        #print eps
        eps = 1e-9/2
        fig = plt.figure(figsize=(8, 6))
        ax = plt.subplot(111)
        plt.hold(True)
        for key in self.tpdfs.keys():
            if not self.color:
                plt.plot(self.txs[xl:xh]+1, self.tpdfs[key][xl:xh]+eps, alpha=0.4,
                         color='#888888')
            else:
                plt.plot(self.txs[xl:xh]+1, self.tpdfs[key][xl:xh]+eps, alpha=0.4)
            plt.title(self.name + ' histograms')
        plt.xlabel('Voxel Intensity')
        plt.ylabel('Probability Density')
        ax.set_xscale('log')
        ax.set_yscale('log')
        plt.show()
        print "X-Min:", self.txs[xl]
        print "X-Max:", self.txs[xh]

    def update(self):
        xl, xh = (widgets.IntSlider(description="Lower Bound Scaling",
                                    min=0,
                                    max=len(self.txs)-1,
                                    value=0,
                                    step=1.0),
                  widgets.IntSlider(description="Upper Bound Scaling",
                                    min=0,
                                    max=len(self.txs)-1,
                                    value=len(self.txs)-1,
                                    step=1.0))

        dl = widgets.jsdlink((xl, 'value'), (xh, 'min'))
        w = widgets.interact(self.plotting, xl=xl, xh=xh)
