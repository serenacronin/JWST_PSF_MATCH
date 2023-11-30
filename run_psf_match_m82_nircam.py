"""
Author: Serena A. Cronin
13 October 2023

"""
import sys
sys.path.append('../JWST_PSF_MATCH')
import generate_psf
import generate_kernel
import psf_matching_check
import convolution

get_psfs = False
check_psfs = False
do_convolution = True
savepath = 'data/kernels/'

# prompt the user to give us the filters

def grab_file_info(filt):
    if filt == 'f140m':
        filename = 'data/liz-original-images/jw01701052001_nircam_sub640_f140m_jhat_i2d.fits'
        scale_factor = 4
        # kern_file = savepath + 'kernel_f250m_to_f360m.fits'
    elif filt == 'f150w2_f164n':
        filename = 'data/liz-original-images/jw01701052001_nircam_sub640_f150w2-f164n_jhat_1fcor_i2d.fits'
        scale_factor = 4
    elif filt == 'f212n':
        filename = 'data/liz-original-images/jw01701052001_nircam_sub640_f212n_jhat_1fcor_i2d.fits'
        scale_factor = 4
    elif filt == 'f250m':
        filename = 'data/liz-original-images/jw01701052001_nircam_sub640_f250m_jhat_i2d.fits'
        scale_factor = 8
        # kern_file = savepath + 'kernel_f250m_to_f360m.fits'
        delt1, delt2 = 1.18, 2.26
    elif filt == 'f335m':
        filename = 'data/liz-original-images/jw01701052001_nircam_sub640_f335m_jhat_i2d.fits'
        scale_factor = 8
        # kern_file = savepath + 'kernel_f335m_to_f360m.fits'
        delt1, delt2 = -1.23, 1.43
    elif filt == 'f360m':
        filename = 'data/liz-original-images/jw01701052001_nircam_sub640_f360m_jhat_i2d.fits'
        scale_factor = 8
        delt1, delt2 = None, None  # hacky plz fix this later
    else:
        raise Exception('Please input f140m, f150w2_f164n, f212n, f250m, f335m, or f360m.')
    
    return(filename, scale_factor, delt1, delt2)
    
if get_psfs == True:
    # prompt an input of a filter
    filt = str(input('Filter: '))
    filename, scale_factor = grab_file_info(filt)

    # generate the psfs
    _, pixscale = generate_psf.get_pixscale(filename, scale_factor)
    full_savepath = savepath + filt
    generate_psf.get_psf(filename, pixscale, full_savepath, plot=True)

if check_psfs == True:

    print('Match and check the PSFs....')

    # this is stupid but i'm just writing what the pixscale is
    pixscale = 0.008

    # prompt more inputs
    filt1 = str(input('Shorter wavelength filter: '))
    desired_filt = str(input('Longer wavelength filter: '))

    # set up the files
    desired_filename, scale_factor = grab_file_info(desired_filt)
    filename, scale_factor = grab_file_info(filt1)

    # get the psf and kernel files
    psf1 = savepath + filt1 + '_psf_0.008.fits'
    psf2 = savepath + desired_filt + '_psf_0.008.fits'
    kern_file = savepath + 'kernel_' + filt1 + '_to_' + desired_filt + '.fits'
    # generate_kernel.get_kernel(psf1, psf2, pixscale, kern_file)

    # produce plots to check the kernel and psfs
    psf_matching_check.get_visual(psf1, psf2, filt1, desired_filt, kern_file, pixscale, savepath)

    psf_conv_file = savepath + filt1 + '_matched_to_' + desired_filt + '.fits'
    # psf_conv_file = '%s_matched_to_%s.fits' % (full_savepath, desired_filt)
    psf_matching_check.calc_power_annuli(psf_conv_file, psf2, step=2, plot=True, savepath=savepath,
                        psf_conv_label=filt1, psf_desired_label=desired_filt,pixscale=pixscale)

if do_convolution == True:

    filt1 = str(input('Shorter wavelength filter: '))
    desired_filt = str(input('Longer wavelength filter: '))
    desired_filename, scale_factor, _, _ = grab_file_info(filt1)
    filename, scale_factor, delt1, delt2 = grab_file_info(filt1)

    # manually putting in pixel scale
    pixscale = 0.008

    # first, resample the desired image
    outfile_resamp = savepath + desired_filt + '_resamp.fits'
    convolution.resample(desired_filename, outfile_resamp, pixscale, infile_ext=1)

    # now resample the images and perform the convolution
    outfile_resamp = savepath + filt1 + '_resamp.fits'
    convolution.resample(filename, outfile_resamp, pixscale, infile_ext=1)

    # now resample the other images and shift to spatially match the f360m filter
    # outfile_shift = savepath + filt1 + '_resamp_and_shift.fits'
    # convolution.resample_and_match_to(outfile_resamp, filename, outfile_shift, delt1, delt2)

    # now do the convolution
    outfile_conv = savepath + filt1 + '_resamp_conv.fits'
    kern_file = savepath + 'kernel_' + filt1 + '_to_' + desired_filt + '.fits'
    convolution.get_convolution(outfile_resamp, kern_file, outfile_conv)

    # resample back to original size
    # outfile_conv_resamp = full_savepath + '_resamp_conv_resamp.fits'
    # convolution.resample(outfile_conv, outfile_conv_resamp, target_pixscale=0.042, infile_ext=False)


    # resample back to original size
    # convolution.resample(infile, outfile, target_pixscale, infile_ext=False)