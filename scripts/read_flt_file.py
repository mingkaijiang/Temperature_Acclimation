#!/usr/bin/env python

"""
Read the AWAP .FLT file header and binary file into a useable numpy format

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (12.12.2014)"
__email__ = "mdekauwe@gmail.com"

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import re

class ReadFltFile(object):

    def __init__(self):
        self.meta = {}
        self.r = re.compile("^(\S+)\s+(\S+)$")
        
    def _read_met_header(self, fname):
        path = os.path.dirname(fname)
        hdr_fname = os.path.basename(fname).split(".")[0]
        
        # Some of the header files do not exist so to catch this we are just
        # going to hardwire the reading bit here, probably reduce the I/O too.
        #if os.path.isfile(hdr_fname) :        
        #    f = open(os.path.join(path, hdr_fname + '.hdr'), 'r')
        #    for line in f:
        #        line = line.strip()
        #        m = re.match(self.r, line)
        #        if m:
        #            if m.group(1).lower() == 'byteorder':
        #                self.meta[m.group(1).lower()] = m.group(2)
        #            else:
        #                self.meta[m.group(1).lower()] = float(m.group(2))
        #    f.close()
        #else:
        #    self.meta = {'ncols': 841.0, 'cellsize': 0.05, 'nrows': 681.0, 
        #                 'xllcorner': 111.975, 'yllcorner': -44.025, 
        #                 'nodata_value': -999.0}
        
        self.meta = {'ncols': 841.0, 'cellsize': 0.05, 'nrows': 681.0, 
                     'xllcorner': 111.975, 'yllcorner': -44.025, 
                     'nodata_value': -999.0}
        
    def load_flt_file(self, fname):
        self._read_met_header(fname)
        data = np.fromfile(fname, dtype=np.float32)
        data = data.reshape(int(self.meta['nrows']), int(self.meta['ncols']))
        
        return data
        
       

if __name__ == '__main__':
    
    import glob
    
    F = ReadFltFile()
    
    land_mask_fname = "../GWAP_ancillary_files/land_mask_made_from_fapar_mvc.bin"
    
    fdir = "../test_files"
    var = "tmax"
    fnames = glob.glob(os.path.join(fdir, var) + "/*.flt")
    for fname in fnames:
        data = F.load_flt_file(fname)
        
        land_mask = np.fromfile(land_mask_fname, dtype=np.float32)
        land_mask = land_mask.reshape(int(F.meta['nrows']), int(F.meta['ncols']))
        
        data = np.where(land_mask>=0.0, data, np.nan)
        plt.imshow(data)
        plt.colorbar()
        plt.savefig("../plots/tmax.png", dpi=100)
        #plt.show()
        plt.clf()
        
    var = "tmin"
    fnames = glob.glob(os.path.join(fdir, var) + "/*.flt")
    for fname in fnames:
        data = F.load_flt_file(fname)
        data = np.where(land_mask>=0.0, data, np.nan)
        
        plt.imshow(data)
        plt.colorbar()
        #plt.show()    
        plt.savefig("../plots/tmin.png", dpi=100)
        plt.clf()
        
    var = "rain"
    fnames = glob.glob(os.path.join(fdir, var) + "/*.flt")
    for fname in fnames:
        data = F.load_flt_file(fname)
        data = np.where(land_mask>=0.0, data, np.nan)
        
        plt.imshow(data)
        plt.colorbar()
        #plt.show()     
        plt.savefig("../plots/rain.png", dpi=100)
        plt.clf()
        
    var = "rad"
    fnames = glob.glob(os.path.join(fdir, var) + "/*.flt")
    for fname in fnames:
        data = F.load_flt_file(fname)
        data = np.where(land_mask>=0.0, data, np.nan)
        plt.imshow(data)
        plt.colorbar()
        #plt.show()     
        plt.savefig("../plots/rad.png", dpi=100)
        plt.clf()
        
    var = "vph09"
    fnames = glob.glob(os.path.join(fdir, var) + "/*.flt")
    for fname in fnames:
        data = F.load_flt_file(fname)
        data = np.where(land_mask>=0.0, data, np.nan)
        plt.imshow(data)
        plt.colorbar()
        #plt.show()
        plt.savefig("../plots/vph09.png", dpi=100)
        plt.clf()
        
    var = "vph15"
    fnames = glob.glob(os.path.join(fdir, var) + "/*.flt")
    for fname in fnames:
        data = F.load_flt_file(fname)
        data = np.where(land_mask>=0.0, data, np.nan)
        plt.imshow(data)
        plt.colorbar()
        #plt.show() 
        plt.savefig("../plots/vph15.png", dpi=100) 
        plt.clf()