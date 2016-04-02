#!/usr/bin/env python

# nifti_to_r.py
# Created by Greg Kiar on 2016-03-02.
# Email: gkiar@jhu.edu
# Copyright (c) 2016. All rights reserved.

from argparse import ArgumentParser
from scipy.stats import gaussian_kde
import nibabel as nb
import numpy as np
import os
import glob
import collections
import pickle


def process(outf, dti_f, bval_f):
    b0s = collections.OrderedDict()

    for idx, scan in enumerate(bval_f):
        print scan
        basename = os.path.basename(scan)
        print basename
        bval = np.loadtxt(scan)
        bval[np.where(bval==np.min(bval))] = 0
        im = nb.load(dti_f[idx])
        b0_loc = np.where(bval==np.min(bval))[0][0]
        dti = im.get_data()[:,:,:,b0_loc]
        b0s[basename] = np.ravel(dti)

    maxx = np.max([np.max(b0s[key]) for key in b0s])
    minn = np.min([np.min(b0s[key]) for key in b0s])

    print "Computing PDFs..."
    xs = np.linspace(minn, maxx, 1000)
    pdfs = {key:
            gaussian_kde(b0s[key]).pdf(xs)
            for key in b0s}

    output = open(outf+'_b0s.pkl', 'wb')
    pickle.dump(b0s, output)
    output.close()

    output = open(outf+'_b0_pdfs.pkl', 'wb')
    pickle.dump({"pdfs":pdfs, "xs":xs}, output)
    output.close()

def main():
    parser = ArgumentParser(description="")
    parser.add_argument("outname", action="store", help="")
    parser.add_argument("inDirs", action="store", nargs="+", help="")
    result = parser.parse_args()

    dti_types = ('*DTI.nii', '*DTI.nii.gz')
    bval_types = ('*DTI.b', '*DTI.bval')
    dti = [y for f in result.inDirs for x in os.walk(f) for z in dti_types
           for y in glob.glob(os.path.join(x[0],z))]
    bval = [y for f in result.inDirs for x in os.walk(f) for z in bval_types
            for y in glob.glob(os.path.join(x[0],z))]

    
    print len(bval)
    print len(dti)
    assert(len(bval) == len(dti))

    process(result.outname, dti, bval)

if __name__ == "__main__":
    main()

