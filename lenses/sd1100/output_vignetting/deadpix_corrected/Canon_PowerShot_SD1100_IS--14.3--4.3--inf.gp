set grid
set title "Canon PowerShot SD1100 IS, 14.3 mm, f/4.3, ∞ m"
plot "Canon_PowerShot_SD1100_IS--14.3--4.3--inf-all_points.dat" with dots title "samples", "Canon_PowerShot_SD1100_IS--14.3--4.3--inf-bins.dat" with linespoints lw 4 title "average", \
     14380.801654485973 * (1 + (-0.16646710183929644) * x**2 + (-0.01750890577925115) * x**4 + (0.02097580637165342) * x**6) title "fit"
pause -1
