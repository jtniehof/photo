#sd1100

This directory contains progress towards full (distortion + TCA + vignetting) lens information for the Canon Powershot SD1100 IS. This is supposedly the same as the IXUS 80 [Wikipedia](https://en.wikipedia.org/wiki/Canon_Digital_IXUS#IXUS.2FELPH.2FIXY_cameras_using_SD_storage), added to lensfun in February of 2010 (version 0.2.5, commit decca5b0ed9316d589787f7847e94f83c9f03a2c).

## Aperture and ND filter
This camera doesn't have an adjustable aperture, but an ND8 filter; when the filter is in, the camera reports the "effective" aperture in the EXIF data, i.e. an aperture that would give the same brightness. I'm assuming the ND filter doesn't affect the distortion, vignetting, or TCA.

Focal length and various reported apertures, with and without ND filter: from exif data or camera screen while half-pressing shutter button. x means I didn't bother to check.

    FL (exif)  Ap (exif) Ap (screen) Ap w/ND (exif) Ap w/ND (screen)
    6.2        2.8       2.8         7.7            8.0
    7.2        3.0       3.2         8.2            9.0
    8.3        3.2       3.2         8.7            9.0
    9.7        3.5       3.5         9.5            10
    11.6       3.8       4.0         10             11
    14.3       4.3       4.5         x              13
    18.6       5.0       4.9         x              14

CHDK forums say it's supposed to emulate f/8 w/ND filter. Other on forums say ND4 (i.e. 2 stops). Further reading indicates f/8 equivalent at maximum aperture (f/2.8, i.e., minimum focal length). So that's a reduction in brightness of about a factor of 8, ND8. This matches 4.9 to 14 (at the longest)

## General

I shot with CHDK to DNG 1.3 raws. This is supposed to embed the badpixels.bin data (bad pixels reported from the camera firmware) into DNG opcodes so it can be removed by the raw converter; however, I found a lot of obvious dead pixels (e.g. cyan blotches) in the dcraw converted raws. I pulled the CHDK-generated badpixels.bin and parsed it into the format that dcraw uses for its -P option. I converted all vignetting images with no interpolation ("dcraw -v -t 0 -4 -o 0 -M -D foo.DNG") and checked the pgm for zero-value (totally dead) pixels. All the vignetting images gave identical results, which I merged with the badpixels.bin list, and then edited calibrate.py to add the appropriate -P option to all dcraw calls. Python code is in this repository.

I made a lenses.txt file with the distortion from the existing IXUS80 in lensfun.xml (from a, b, c; assumed would recognize as ptlens from having three parameters), but with a changed first line: "Canon PowerShot SD1100 IS: Canon, canonSD100IS, 5.9". (matching Exif.Image.Model ,same as Exif.Image.UniqueCameraModel) I edited line 169 of calibrate.py to default to "Canon PowerShot SD1100 IS" instead of "Standard".

LensInfo is 62/10 186/10 28/10 49/10 and exiv2 finds no match.

## TCA

For TCA, I made several attempts with buildings before giving up. I bought two black-and-white checkered tablecloths on Amazon, 137x274cm, and hung them up. I set up a tripod about 6-7m away. Because at the shorter focal lengths the pattern didn't fill the frame, I did five shots: one with the pattern in each corner (filling as much of the frame as possible) and one with the camera brought closer (about 4m for the shortest focal length) so the pattern filled the frame. At longer focal lengths (filling the frame), I took a couple of exposures with slight movements of the camera between to get some differences. I shot at ISO 80 (base), exposure on automatic, auto focus, with a 2sec timer to avoid vibrations from pressing the shutter button. I shot at all six. All exposure were without the ND filter (although I didn't force that.)

On a first try for TCA, I got the error "read_image_bands_and_alpha: expecting exactly one alpha band error on several images"; this was fixed in a later version of hugin <https://bugs.launchpad.net/hugin/+bug/1529902> so I built that from source.

I ran calibrate.py against all the images with a one-, two-, and three-parameter fits. For each focal length, I parsed the .tca file and plotted distortion vs. radius (r and b) for all images, looking for reasonable agreement between the images. I took the mean of parameters for all images at each focal length to plot parameter as a function of focal length, looking for smooth variation with focal length. (Code available.) The three-parameter (bcv) fit has poor agreement between images and noisy variation with focal length. At the shorter focal lengths, the two-parameter (b and v) was clearly very good. The images taken closer in were clear outliers and I threw them out. At longer focal length, neither one- nor two-parameter had perfect agreemnt, but the two- had better, and in all cases the deviation from no correction was larger than the difference between the images. So I used the means of the two-parameter fits.

Because the TCA images have the front of my house, they're not included here.

## Vignetting
I shot vignetting images against a white ceiling about 2m from the camera, mounted on a tripod facing up. A lamp was positioned right next to the tripod and emitting from just above lens level, to avoid camera shadow. I sandwiched a sheet of Rosco 216 white diffusion gel between the lens below and glass above (two pieces, a sort of "floating picture frame" that I had handy.) Focus distance was set at maximum: I did not bring an image at infinity to focus. Again 80ISO, auto exposure, 2sec timer, no ND filter. I shot all focal lengths, then rotated the camera and gel so that the relationship between ceiling, camera, and gel were all different (lamp and ceiling remained in the same orientation) before shooting another set.

Using gnuplot output from calibrate.py, I verifying vignetting images were generally smooth (and threw out two other sets of vignetting photos where I tried a different approach to holding the gel, which had obvious defects.) The two images for each focal length provided very similar outputs.

## XML changes

For the XML, I copied the IXUS 80 verbatim (both camera and lens), then changed model tag to match Exif.Image.Model (which is the same as Exif.Image.UniqueCameraModel), made the lang en a short version, and named the mount similarly. I populated both the IXUS 80 and the copied SD1100 lens calibration with the new TCA and vignetting data. The vignetting already had two lines per focal length (near and far distances); I added two more lines for smaller aperture, based on the camera-reported effective aperture with the ND filter in.

## Crop factor

The IXUS 80 calibration has the crop factor at 6.1 for the camera and 5.9 for the lens (based perhaps on full area vs. JPEG area?) Torsten says these really should be the same.

JPG is 3264x2448 (matches EXIF DefaultCropSize); DNG is 3298x2470 (matches ActiveArea). EXIF ImageWidth x ImageLength is 3336 x 2480

EXIF FocalLength  Exif FocalLengthIn35mmFilm  Factor
6.2               38.0                        6.13
7.2               44.0                        6.11
8.3               50.0                        6.02
9.7               59.0                        6.08
11.6              71.0                        6.12
14.3              87.0                        6.08
18.6              114.0                       6.13

A standard 1/2.5" sensor is 6.02. digicamdb claims 6.02 for SD1100, but with slightly different dimensions than 1/2.5". I used 6.02 for the distortion calibration via hugin.

## Distortion
I took a set of distortion images (raws in dng/distortion) and calibrated them with hugin. The edges used were the top of the building and the line of the siding closest to one-third of the way from the top; as far as I could tell, there weren't discontinuities at the joints. There's a tutorial similar to Torsten's technique with a newer version of hugin at <http://hugin.sourceforge.net/tutorials/calibration/en.shtml>

I had to edit the hugin source to get rid of the extra lines, per Torsten's email at <https://groups.google.com/forum/#!topic/hugin-ptx/isjUEIzVsXU>.

Hugin includes an automatic calibration tool documented at <http://wiki.panotools.org/Calibrate_lens_gui>. With a bit of parameter tweaking and taking out obviously bad lines, this seems to do a very good job.

dist_compare/parameters has a script, dist_compare.py, that compares all the calibrations. The output plots are also in that directory. The various parameter sets are:

new: taken by me using Torsten's procedure, two horizontal lines one close to the top and one about one-third of the way down, roughly 15-20 pairs of control points per line.

newer: also manual, but after processing the tiffs in GIMP to pull in the white and black points, improving contrast. I used three lines with 40-50 control point pairs each.

old: the values from the current database.

auto: using the automatic calibration tool on the tiffs directly from calibrate.py, using default parameters

tuned: automatic calibration tool, playing with the detection parameters.

tuned_contrast: automatic calibration tool, tiffs stretched as above, tweaking detection parameters to maximize number of good lines and removing some erroneous detections. These seemed to be the best results and are in the final sd1100.xml, plus the comparison images described below.

The old calibrations seem a bit much. Example images are provided in distortion_compare for: OOC JPG (ooc_jpg), uncorrected from the RAW (uncorrected), and corrected from the RAW with both old (old_distortion) and new values (for the new values, there are both with TCA/vignetting, new_all, and without, new_distortion). It appears the OOC JPG is completely uncorrected. Note the comparison images were not used for calibration (those are in dng/distortion).

The automatic calibration tool seems pretty effective; and since it's quick it's probably worth taking a few images at each focal length to get hopefully reproducible parameters. The manual method seems to go weird at the center of the image (R to 0), probably from a lack of sampling in that region.

calibrate.py creates the distortion tiffs using ``dcraw -T -t 0 -w infile.dng`. It may be worth tweaking the white and black levels for your specific distortion image with the `-W`, `-S`, and `-k` options.