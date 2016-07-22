set grid
set title "Canon PowerShot SD1100 IS, 11.6 mm, f/3.8, ∞ m"
plot "Canon_PowerShot_SD1100_IS--11.6--3.8--inf-all_points.dat" with dots title "samples", "Canon_PowerShot_SD1100_IS--11.6--3.8--inf-bins.dat" with linespoints lw 4 title "average", \
     14584.136996494768 * (1 + (-0.19004914044285676) * x**2 + (-0.012441708148290079) * x**4 + (0.023817561632310257) * x**6) title "fit"
pause -1
