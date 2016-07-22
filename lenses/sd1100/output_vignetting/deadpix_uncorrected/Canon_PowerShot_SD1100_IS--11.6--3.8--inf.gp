set grid
set title "Canon PowerShot SD1100 IS, 11.6 mm, f/3.8, ∞ m"
plot "Canon_PowerShot_SD1100_IS--11.6--3.8--inf-all_points.dat" with dots title "samples", "Canon_PowerShot_SD1100_IS--11.6--3.8--inf-bins.dat" with linespoints lw 4 title "average", \
     14561.84247220015 * (1 + (-0.19183274355246965) * x**2 + (-0.009563147967272183) * x**4 + (0.02373549937384581) * x**6) title "fit"
pause -1
