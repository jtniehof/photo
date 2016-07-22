set grid
set title "Canon PowerShot SD1100 IS, 8.3 mm, f/3.2, ∞ m"
plot "Canon_PowerShot_SD1100_IS--8.3--3.2--inf-all_points.dat" with dots title "samples", "Canon_PowerShot_SD1100_IS--8.3--3.2--inf-bins.dat" with linespoints lw 4 title "average", \
     14710.683849256384 * (1 + (-0.32849132633844264) * x**2 + (0.07597189763055762) * x**4 + (-0.002434529028890637) * x**6) title "fit"
pause -1
