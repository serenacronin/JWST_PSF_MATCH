import numpy as np
import astropy.io.fits as fits
from reproject import reproject_interp
from astropy.convolution import convolve_fft


def resample(infile, outfile, target_pixscale, infile_ext=False):
    
    """
    Resample an image to a desired pixel scale.
    
    infile : str
    outfile : str
    target_pixscale : int or float
        Desired pixel scale (arcsec).
    infile_ext : int
        hdu extention
    
    """
    
    # open the data file
    if infile_ext != False:
        img_hdu = fits.open(infile)
        img = img_hdu[infile_ext].data
        img_hdr_copy = img_hdu[infile_ext].header.copy()  # copy of the header
    else:
        img_hdu = fits.open(infile)
        img = img_hdu[0].data
        img_hdr_copy = img_hdu[0].header.copy()  # copy of the header

    # find the new naxis (num of pixels) to preserve the width of the image
    # given a new pixel scale
    img_width = img_hdr_copy['CDELT1'] * img_hdr_copy['NAXIS1']  # width of the image = pixscale * number of pixels
    new_cdelt1 = target_pixscale / 3600  # convert from arcsec to degrees
    new_naxis1 = int(np.round(img_width / new_cdelt1) - 3.5) # must be an integer

    img_width = img_hdr_copy['CDELT2'] * img_hdr_copy['NAXIS2']  # width of the image = pixscale * number of pixels
    new_cdelt2 = target_pixscale / 3600  # convert from arcsec to degrees
    new_naxis2 = int(np.round(img_width / new_cdelt2) - 2.5) # must be an integer

    # need to also change CRPIX, which provides reference points to convert pixels to skycoords.
    crpix1_ratio = img_hdr_copy['NAXIS1'] / img_hdr_copy['CRPIX1']
    crpix2_ratio = img_hdr_copy['NAXIS2'] / img_hdr_copy['CRPIX2']
    new_crpix1 = new_naxis1 / crpix1_ratio
    new_crpix2 = new_naxis2 / crpix2_ratio

    # update the new header
    img_hdr_copy['CDELT1'] = new_cdelt1
    img_hdr_copy['NAXIS1'] = new_naxis1
    img_hdr_copy['CDELT2'] = new_cdelt2
    img_hdr_copy['NAXIS2'] = new_naxis2
    img_hdr_copy['CRPIX1'] = new_crpix1
    img_hdr_copy['CRPIX2'] = new_crpix2

    # now, reproject the image in the new header
    if infile_ext != False:
        img_reproj, _ = reproject_interp(img_hdu[infile_ext], img_hdr_copy, shape_out=(new_naxis2,new_naxis1))
    else:
        img_reproj, _ = reproject_interp(img_hdu[0], img_hdr_copy, shape_out=(new_naxis2,new_naxis1))
    
    fits.writeto(outfile, img_reproj, img_hdr_copy, overwrite=True)
    
    return


def resample_and_match_to(match_to_file, infile, outfile, delt1, delt2):

    """
    Same as resample, but this time with a spatial shift in pixels
    to better match all filters.
    """

    match_to_hdu = fits.open(match_to_file)
    match_to_data = match_to_hdu[0].data
    match_to_hdr = match_to_hdu[0].header

    print(match_to_data.shape[0])

    infile_hdu = fits.open(infile)
    infile_data = infile_hdu[1].data
    infile_hdr = infile_hdu[1].header.copy()

    old_cdelt1 = infile_hdr['CDELT1']
    new_cdelt1 = match_to_hdr['CDELT1']

    infile_hdr['CDELT1'] = match_to_hdr['CDELT1']
    infile_hdr['CDELT2'] = match_to_hdr['CDELT2']
    infile_hdr['NAXIS1'] = match_to_hdr['NAXIS1']
    infile_hdr['NAXIS2'] = match_to_hdr['NAXIS2']
    infile_hdr['CRPIX1'] = match_to_hdr['CRPIX1'] + delt1 #+ 0.85 #- 1.3
    infile_hdr['CRPIX2'] = match_to_hdr['CRPIX2'] + delt2 #+ 2.77 #+ 1.47


    img_reproj, _ = reproject_interp(infile_hdu[1], infile_hdr, 
                                      shape_out=(match_to_data.shape[0], match_to_data.shape[1]))
    
    fits.writeto(outfile, img_reproj, infile_hdr, overwrite=True)

    return


def get_convolution(infile, kernel_infile, outfile):

    """
    Perform a Fast Fourier Transform (FFT) convolution
    of a FITs image with a kernel.

    infile : str
    kernel_infile : str
    outfile : str
    
    """
    
    img_hdu = fits.open(infile)
    img = img_hdu[0].data
    
    kernel_hdu = fits.open(kernel_infile) 
    kernel = kernel_hdu[0].data

    conv = convolve_fft(img, kernel, allow_huge=True)
    fits.writeto(outfile, conv, img_hdu[0].header, overwrite=True)
    
    return
