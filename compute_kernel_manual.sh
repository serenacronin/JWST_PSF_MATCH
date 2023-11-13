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

# use pypher's 'addpixscl' to add the pixel scale to each PSF
addpixscl ../data/test_conv2/f250m_psf_0.008.fits 0.008

addpixscl ../data/test_conv2/f360m_psf_0.008.fits 0.008

# now generate a kernel using the following format:
# pypher psf_a.fits psf_b.fits kernel_a_to_be.fits
pypher ../data/test_conv2/f250m_psf_0.008.fits ../data/test_conv2/f360m_psf_0.008.fits ../data/test_conv2/relaxation_1/kernel_f250m_to_f360m.fits -r 1
