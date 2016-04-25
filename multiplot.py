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

# multiplot.py
# Created by Greg Kiar on 2016-03-29.
# Email: gkiar@jhu.edu

from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys


class hist_plot():

    def __init__(self, fnames, names, figname=None, color=False):
        """
        Plots multiple populations of histograms in the same figure.
        Expects:
            fnames: list of filenames, each of which is a pickle dictionary containing
                    pdfs and x values over which they were evaluated
            names: list of length equal to filenames, which is the coloquial name of the
                   dataset we want in the figure title
        """
        self.fnames = fnames
        self.names = names
        self.figname = figname
        self.color = color
        self.gd()
        self.plot()

    def gd(self):
        """
        Get pdf and xs from files
        """
        self.data = OrderedDict()
        for idx, curr in enumerate(self.fnames):
            inf = open(curr)
            self.data[self.names[idx]] = pickle.load(inf)
            inf.close()
        print self.data.keys()

    def plot(self):
        """
        Plots series of histograms in a single figure
        """
        eps = 1e-9/2
        N = len(self.fnames)

        ds = list()
        count = 0
        while len(ds) == 0:
            ds = list(self.factors(N+count))
            count += 1
            print ds
        
        if len(ds) == 1:
            ds = list((ds[0], ds[0]))
        fig = plt.figure(figsize=(4*ds[-1], 4*ds[0]))
        bl = ds[-1]*(ds[0]-1)
        for idx, key in enumerate(self.data.keys()):
            ax = plt.subplot(ds[0], ds[-1], idx+1)
            plt.hold(True)
            xs = self.data[key]['xs']
            pdfs = self.data[key]['pdfs']
            for key2 in pdfs:
                if not self.color:
                    plt.plot(xs+1, pdfs[key2]+eps, alpha=0.07, color='#000000')
                else:
                    plt.plot(xs+1, pdfs[key2]+eps, alpha=0.4)
            plt.title(key)
            if idx == bl:
                plt.xlabel('Voxel Intensity')
                plt.ylabel('Probability Density')
            ax.set_xscale('log')
            ax.set_yscale('log')
        plt.tight_layout()
        if self.figname is not None:
            plt.savefig(self.figname)
        plt.show()
        
        
    def factors(self, N): 
        return set([item for subitem in 
                    [(i, N//i) for i in range(1, int(N**0.5) + 1) if N % i == 0 and i > 1]
                    for item in subitem])


class feature_plot():

    def __init__(self, data, names, figtitle, figname=None, plotm='bar', ylims = None):
        """
        Plots multiple populations of histograms in the same figure.
        Expects:
            fnames: list of filenames, each of which is a pickle dictionary containing
                    pdfs and x values over which they were evaluated
            names: list of length equal to filenames, which is the coloquial name of the
                   dataset we want in the figure title
        """
        self.data = data
        self.names = names
        self.figname = figname
        self.figtitle = figtitle
        self.ylims = ylims
        if plotm == 'bar' :
            self.bar_plot()
        elif plotm == 'scatter' :
            self.scatter_plot()
        else :
            self.hist_plot()

    def bar_plot(self):
        """
        Plots series of histograms in a single figure
        """
        
        """
        Setup plot shape, etc.
        """
        eps = 1e-9/2
        N = len(self.names)
        ds = list()
        count = 0
        while len(ds) == 0:
            ds = list(self.factors(N+count))
            count += 1
            print ds
        if len(ds) == 1:
            ds = list((ds[0], ds[0]))
        fig = plt.figure(figsize=(4*ds[-1], 4*ds[0]))
        bl = ds[-1]*(ds[0]-1)

        """
        Actually plot things
        """
        for idx, set in enumerate(self.data.keys()):
            ax = plt.subplot(ds[0], ds[-1], idx+1)
            plt.hold(True)
            plt.bar(range(len(self.data[set])),self.data[set].values(), alpha=0.7, color='#888888')
            plt.title(set, y = 1.04)
            if idx == bl:
                plt.ylabel('Count')
                plt.xlabel('Graph')
            plt.xlim((0, len(self.data[set].keys())))
            if self.ylims is not None:
                plt.ylim(self.ylims)

            plt.tight_layout()

        if self.figname is not None:
            plt.savefig(self.figname)
        plt.show()

    def scatter_plot(self):
        """
        Plots series of histograms in a single figure
        """
        
        """
        Setup plot shape, etc.
        """
        N = len(self.names)
        fig = plt.figure(figsize=(1.2*N, 1*N))
        
        """
        Actually plot things
        """
        ax = plt.subplot(1,1,1)
        plt.hold(True)
        for idx, set in enumerate(self.data.keys()):
            plt.scatter([idx] * len(self.data[set].values()),self.data[set].values(), alpha=0.1, color='#000000')

        plt.title(self.figtitle, y = 1.04)
        plt.ylabel('Count')
        ax.set_xticks(np.arange(len(self.names)))
        ax.set_xticklabels(self.names, rotation=40)
        plt.xlabel('Dataset')
        plt.xlim([-0.5, len(self.names)-0.5])
        if self.ylims is not None:
            plt.ylim(self.ylims)

        plt.tight_layout()

        if self.figname is not None:
            plt.savefig(self.figname)
        plt.show()


    def hist_plot(self):
        """
        Plots series of histograms in a single figure
        """
        eps = 1e-9/2
        N = len(self.fnames)

        ds = list()
        count = 0
        while len(ds) == 0:
            ds = list(self.factors(N+count))
            count += 1
            print ds
        
        if len(ds) == 1:
            ds = list((ds[0], ds[0]))
        fig = plt.figure(figsize=(4*ds[-1], 4*ds[0]))
        bl = ds[-1]*(ds[0]-1)
        for idx, key in enumerate(self.data.keys()):
            ax = plt.subplot(ds[0], ds[-1], idx+1)
            plt.hold(True)
            xs = self.data[key]['xs']
            pdfs = self.data[key]['pdfs']
            for key2 in pdfs:
                if not self.color:
                    plt.plot(xs+1, pdfs[key2]+eps, alpha=0.07, color='#000000')
                else:
                    plt.plot(xs+1, pdfs[key2]+eps, alpha=0.4)
            plt.title(key)
            if idx == bl:
                plt.xlabel('Voxel Intensity')
                plt.ylabel('Probability Density')
            ax.set_xscale('log')
            ax.set_yscale('log')
        plt.tight_layout()
        if self.figname is not None:
            plt.savefig(self.figname)
        plt.show()
        
        
    def factors(self, N): 
        return set([item for subitem in 
                    [(i, N//i) for i in range(1, int(N**0.5) + 1) if N % i == 0 and i > 1]
                    for item in subitem])
