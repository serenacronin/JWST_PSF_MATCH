#!/bin/bash

# Author: Serena A. Cronin
# 5 October 2023



"""
========================================================================== 
This script uses pypher to compute convolution kernels between two PSFs.

INPUT
-----

psf1 : str
	filename of psf1 (format: FITS)
psf2 : str
	filename of psf2 (format: FITS)
pixscale : float
	pixel scale
kernel_name : str
	filename of kernel to be generated (format: FITS)
 

===========================================================================
"""

psf1=$1
psf2=$2
pixscale=$3
kernel_name=$4

# use pypher's 'addpixscl' to add the pixel scale to each PSF
addpixscl psf1 pixscale
addpixscl psf2 pixscale

# now generate a kernel using the following format:
# pypher psf_a.fits psf_b.fits kernel_a_to_be.fits
pypher psf1 psf2 kernel_name
