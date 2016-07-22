set grid
set title "Canon PowerShot SD1100 IS, 8.3 mm, f/3.2, ∞ m"
plot "Canon_PowerShot_SD1100_IS--8.3--3.2--inf-all_points.dat" with dots title "samples", "Canon_PowerShot_SD1100_IS--8.3--3.2--inf-bins.dat" with linespoints lw 4 title "average", \
     14740.908684348824 * (1 + (-0.33369247251507334) * x**2 + (0.08889171341037426) * x**4 + (-0.011624695749682714) * x**6) title "fit"
pause -1
