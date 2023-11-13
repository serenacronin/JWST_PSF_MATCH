"""
Author: Serena A. Cronin
Date: 12 October 2023

"""

import webbpsf
import matplotlib.pyplot as plt
import numpy as np

def get_pixscale(filename, scale_factor):

    """
    Output the original pixel size (arcsec) 
    and new pixel size (arcsecc) after scaling by a desired factor. 

    Input:
        filename : str
            FITS file path.
        scale_factor : int or float

    Output:
        old_pixscl : float
        new_pixscl : float
                    
    
    """

    inst = webbpsf.setup_sim_to_match_file(filename)
    old_pixscl = inst.pixelscale
    new_pixscl = old_pixscl / scale_factor

    print(' ')
    print('=================================================')
    print('Original pixelscale: ', old_pixscl)
    print('New pixelscale: ', new_pixscl)
    print('=================================================')
    print(' ')

    return(old_pixscl, np.round(new_pixscl, 3))


def get_psf(filename, pixscale, savepath, plot=True):

    """
    Input:
        filename: str
            FITS file path.
        pixscale: int or float
            Desired pixel scale in arcsec.
        savepath : str
            Path to save output.
        plot : bool; default=True
    """

    inst = webbpsf.setup_sim_to_match_file(filename)
    inst.pixelscale = pixscale
    psf = inst.calc_psf(oversample=1)

    # if isinstance(pixscale, np.floating):
    #     pixscale_str = str(pixscale).replace('.', 'p')

    psf.writeto('%s_psf_%s.fits' % (savepath,pixscale), 
                overwrite=True)

    if plot == True:
        webbpsf.display_psf(psf)
        plt.savefig('%s_psf_%s.png' % (savepath,pixscale))

    return