#!/usr/bin/env python
"""Get the residuals after removing the radial fit"""

import os.path
import subprocess
import xml.etree.ElementTree

import numpy

import pgm


params = {}
tree = xml.etree.ElementTree.parse('lensfun.xml')
root = tree.getroot()
params = dict(((
    '{0:03.0f}_{1:04.1f}_{2:.2f}'.format(
        float(c.attrib['focal']), float(c.attrib['aperture']),
        float(c.attrib['distance'])),
    [float(c.attrib[i]) for i in ('k1', 'k2', 'k3')])
    for c in root.iter(tag='vignetting')))
for p in params:
    f, ap, d = p.split('_')
    if d > 2.:
        d = None
    rawf = os.path.join('vignetting_' + d if d else 'vignetting',
                        '{0}_{1}.CR2'.format(f, ap))
    dcp = subprocess.Popen(
        ["dcraw", "-T", "-t", "0", "-4", "-M", "-o", "0", "-c", rawf],
        stdout=subprocess.PIPE)
    image_data = subprocess.check_output(
        ["convert", "tiff:-", "-set", "colorspace", "RGB", "pgm:-"],
        stdin=dcp.stdout,
        stderr=open(os.devnull, "w"))
    img = pgm.pgm_from_string(image_data)
    r = numpy.indices(img.shape, dtype=numpy.float32) + 0.5
    r[0, ...] -= img.shape[0] / 2.
    r[1, ...] -= img.shape[1] / 2.
    r = numpy.sqrt(r[0] ** 2 + r[1] ** 2) / \
        math.hypot(img.shape[0] / 2., img.shape[1] / 2.)
    img = img / (1 + params[p][0] * r ** 2 + params[p][1] * r ** 4 +
                 params[p][2] * r ** 6)
    outf = os.path.join('vignetting_' + d if d else 'vignetting',
                        '{0}_{1}_resid.pgm'.format(f, ap))
    with open(outf, 'wb') as f:
        f.write(b'P5\n')
        f.write(b'{0} {1} {2}\n'.format(img.shape[1], img.shape[0],
                                      numpy.max(img)))
        numpy.require(img, dtype=numpy.uint16).tofile(f)

