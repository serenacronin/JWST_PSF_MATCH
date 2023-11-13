"""
Author: Serena A. Cronin
Date: 12 October 2023

"""
import subprocess
# import pypher

def get_kernel(psf1, psf2, pixscale, outfile):

    """
    Use python's os module to run compute_kernel.sh
    
    """

    subprocess.call(['bash','compute_kernel.sh', f'{psf1}', f'{psf2}',
                    f'{pixscale}', f'{outfile}'])

    return