#!/usr/bin/env python

# nifti_to_r.py
# Created by Greg Kiar on 2016-03-02.
# Email: gkiar@jhu.edu
# Copyright (c) 2016. All rights reserved.

from argparse import ArgumentParser
import nibabel as nb
import numpy as np
import os
import glob

from rpy2.robjects import r
import rpy2.robjects as robj
from rpy2.robjects.numpy2ri import numpy2ri

def process(outf, dti_f, bval_f, python=False):
    """
    Take a list of lists of files DTI and b-val files, returns a
    gzip R file with all B0 data arrays stored on it.
    """
    if python:
        import collections
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
        if python:
            b0s[basename] = np.ravel(dti)
        else:
            ro = numpy2ri(np.ravel(dti+1))
            rr = robj.Matrix(ro)
            if idx is 0:
                myl = r.list(basename=rr)
            else:
                myl = r.c(myl, r.list(basename=rr))
    if python:
        import pickle
        # write python dict to a file
        #mydict = {'a': 1, 'b': 2, 'c': 3}
        output = open(outf, 'wb')
        pickle.dump(b0s, output)
        output.close()

        # read python dict back from the file
        # pkl_file = open('myfile.pkl', 'rb')
        # mydict2 = pickle.load(pkl_file)
        # pkl_file.close()
    else:
        r.assign('bar', myl)
        r("save(bar, file='"+outf+"', compress=TRUE)")

def main():
    parser = ArgumentParser(description="")
    parser.add_argument("outname", action="store", help="")
    parser.add_argument("inDirs", action="store", nargs="+", help="")
    parser.add_argument("-p", "--python", action="store_true", help="if you want in python instead")
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

    process(result.outname, dti, bval, result.python)

if __name__ == "__main__":
    main()

