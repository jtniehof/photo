set grid
set title "Canon PowerShot SD1100 IS, 9.7 mm, f/3.5, ∞ m"
plot "Canon_PowerShot_SD1100_IS--9.7--3.5--inf-all_points.dat" with dots title "samples", "Canon_PowerShot_SD1100_IS--9.7--3.5--inf-bins.dat" with linespoints lw 4 title "average", \
     14710.140139928137 * (1 + (-0.2591352776286087) * x**2 + (0.030503689229752825) * x**4 + (0.01567801988499457) * x**6) title "fit"
pause -1
