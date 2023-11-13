"""
Author: Serena A. Cronin
13 October 2023

"""
import generate_psf
import generate_kernel
import psf_matching_check
import convolution

scale_factor = 8
desired_filt = 'f360m'
desired_filename = '../data/jw01701052001_nircam_sub640_f360m_jhat_i2d.fits'
savepath = '../data/FINAL/'

# toggle which images we want to work with
f250 = False
f335 = True
if f250 == True:
    filt = 'f250m'
    filename = '../data/jw01701052001_nircam_sub640_f250m_jhat_i2d.fits'
    kern_file = savepath + 'kernel_f250m_to_f360m.fits'
    delt1, delt2 = 1.18, 2.26
if f335 == True:
    filt = 'f335m'
    filename = '../data/jw01701052001_nircam_sub640_f335m_jhat_i2d.fits'
    kern_file = savepath + 'kernel_f335m_to_f360m.fits'
    delt1, delt2 = -1.23, 1.43
    
# generate the psfs
_, pixscale = generate_psf.get_pixscale(filename, scale_factor)

full_savepath_desired = savepath + desired_filt
full_savepath = savepath + filt
generate_psf.get_psf(filename, pixscale, full_savepath, plot=True)
generate_psf.get_psf(desired_filename, pixscale, full_savepath_desired, plot=True)

# generate the kernel
psf1 = '%s_psf_%s.fits' % (full_savepath,pixscale)
psf2 = '%s_psf_%s.fits' % (full_savepath_desired,pixscale)
# generate_kernel.get_kernel(psf1, psf2, pixscale, kern_file)

# produce plots to check the kernel and psfs
psf_matching_check.get_visual(psf1, psf2, filt, desired_filt, kern_file, pixscale, savepath)

psf_conv_file = '%s_matched_to_%s.fits' % (full_savepath, desired_filt)
psf_matching_check.calc_power_annuli(psf_conv_file, psf2, step=2, plot=True, savepath=savepath,
                      psf_conv_label=filt, psf_desired_label=desired_filt,pixscale=pixscale)

# first, resample the desired image
outfile_resamp = full_savepath_desired + '_resamp.fits'
convolution.resample(desired_filename, outfile_resamp, pixscale, infile_ext=1)

# # now resample the images and perform the convolution
# outfile_resamp = full_savepath + '_resamp.fits'
# convolution.resample(filename, outfile_resamp, pixscale, infile_ext=1)

# now resample the other images and shift to spatially match the f360m filter
outfile_shift = full_savepath + '_resamp_and_shift.fits'
convolution.resample_and_match_to(outfile_resamp, filename, outfile_shift, delt1, delt2)

# now do the convolution
outfile_conv = full_savepath + '_resamp_conv.fits'
convolution.get_convolution(outfile_shift, kern_file, outfile_conv)

# resample back to original size
# outfile_conv_resamp = full_savepath + '_resamp_conv_resamp.fits'
# convolution.resample(outfile_conv, outfile_conv_resamp, target_pixscale=0.042, infile_ext=False)


# resample back to original size
# convolution.resample(infile, outfile, target_pixscale, infile_ext=False)