set grid
set title "Canon PowerShot SD1100 IS, 9.7 mm, f/3.5, ∞ m"
plot "Canon_PowerShot_SD1100_IS--9.7--3.5--inf-all_points.dat" with dots title "samples", "Canon_PowerShot_SD1100_IS--9.7--3.5--inf-bins.dat" with linespoints lw 4 title "average", \
     14684.524131894235 * (1 + (-0.2570600038461627) * x**2 + (0.023698055098757023) * x**4 + (0.021572832382994008) * x**6) title "fit"
pause -1
