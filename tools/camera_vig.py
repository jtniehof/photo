#!/usr/bin/env python
"""Get vignetting from the raw preview JPG"""

import math
import os
import os.path
import subprocess
import sys
import xml.etree.ElementTree

import matplotlib.pyplot as plt
import numpy
import scipy.optimize

import pgm

def fit_preview(filename):
    """Fit vignetting from a RAW's preview JPG

    Gets camera's internal vignetting correction: extracts
    preview JPG from a raw and compares brightness of JPG to RAW
    as a function of radius from center.

    Is this essentially just extracting the base curve?

    :param str filename: Raw file to open"""
    #yoinked from calibrate.py
    dcraw_cmd = ["dcraw", "-T", "-t", "0", "-4", "-M", "-o", "0", "-c",
                 filename]
    dcraw_process = subprocess.Popen(dcraw_cmd, stdout=subprocess.PIPE)
    image_data = subprocess.check_output(
                ["convert", "tiff:-", "-set", "colorspace", "RGB",
                 "-resize", "250", "pgm:-"], stdin=dcraw_process.stdout,
                stderr=open(os.devnull, "w"))
    img = numpy.require(pgm.pgm_from_string(image_data), dtype=numpy.float64)
    dcraw_cmd = ["dcraw", "-e", "-t", "0", "-4", "-M", "-o", "0", "-c",
                 filename]
    dcraw_process = subprocess.Popen(dcraw_cmd, stdout=subprocess.PIPE)
    image_data = subprocess.check_output(
                ["convert", "jpg:-", "-set", "colorspace", "RGB",
                 "-resize", "250", "pgm:-"], stdin=dcraw_process.stdout,
                stderr=open(os.devnull, "w"))
    img_preview = numpy.require(pgm.pgm_from_string(image_data),
                                dtype=numpy.float64)
    r = numpy.indices(img.shape, dtype=numpy.float64) + 0.5
    r[0, ...] -= img.shape[0] / 2.
    r[1, ...] -= img.shape[1] / 2.
    r = numpy.sqrt(r[0] ** 2 + r[1] ** 2) / \
        math.hypot(img.shape[0] / 2., img.shape[1] / 2.)
    #This is the model of the idealized linear image: depends only on radius
    def fit_function(radius, A, k1, k2, k3):
        return A * (1 + k1 * radius**2 + k2 * radius**4 + k3 * radius**6)

    #Just get the base curve. The radius correction is small by comparison
    a, g = scipy.optimize.leastsq(
        lambda p, x, y: y - p[0] * x ** p[1],
        [numpy.mean(img_preview/img), 1.],
        args=(numpy.ravel(img), numpy.ravel(img_preview)))[0]
    #Remove gamma curve from preview, i.e., return to linear space
    #Although doing this fit full-size might make more sense!
    preview_lin = (img_preview / a) ** (1. / g)
    #We want to minimize error in this model:
    #the actual preview image is the fitted image with a gamma curve applied
    fitme = lambda p, x, y: y - fit_function(x, *p)
    A, k1, k2, k3 = scipy.optimize.leastsq(fitme,
        [numpy.max(img_preview/img), -0.3, 0, 0],
        args=(numpy.ravel(r), numpy.ravel(preview_lin)))[0]
    plt.scatter(r, img, lw=0, s=1)
    x = numpy.arange(0.0, 1.05, 0.05)
    plt.plot(x, A * (1 + k1 * x ** 2 + k2 * x ** 4 + k3 * x ** 6), hold=True,
             c='g', label='From preview')
    #Now do a direct fit
    A, k1, k2, k3 = scipy.optimize.leastsq(
        fitme, [numpy.max(img), -0.3, 0, 0],
        args=(numpy.ravel(r), numpy.ravel(img)))[0]
    plt.plot(x, A * (1 + k1 * x ** 2 + k2 * x ** 4 + k3 * x ** 6), hold=True,
             c='r', label='Direct leastsq fit')
    #calibrate.py output
    if os.path.exists('lensfun.xml') and filename.startswith('vignetting'):
        dirname, fname = os.path.split(filename)
        key = fname[:-4] + '_' + ('1000.00' if dirname == 'vignetting'
                                  else dirname.split('_')[1])
        tree = xml.etree.ElementTree.parse('lensfun.xml')
        root = tree.getroot()
        params = dict(((
            '{0:03.0f}_{1:04.1f}_{2:.2f}'.format(
                float(c.attrib['focal']), float(c.attrib['aperture']),
                float(c.attrib['distance'])),
            [float(c.attrib[i]) for i in ('k1', 'k2', 'k3')])
                       for c in root.iter(tag='vignetting')))
        if key in params:
            k1, k2, k3 = params[key]
            #        A, k1, k2, k3 = (numpy.max(img), -0.9091, 0.6287, -0.3432)
            A = numpy.mean(img / (1 + k1 * r ** 2 + k2 * r ** 4 + k3 * r ** 6))
            plt.plot(x, A * (1 + k1 * x ** 2 + k2 * x ** 4 + k3 * x ** 6),
                     hold=True, c='magenta', label='calibrate.py')
    plt.legend(loc='best')


if __name__ == '__main__':
    fit_preview(sys.argv[1])
    plt.show()
