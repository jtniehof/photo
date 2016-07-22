set grid
set title "Canon PowerShot SD1100 IS, 7.2 mm, f/3.0, ∞ m"
plot "Canon_PowerShot_SD1100_IS--7.2--3.0--inf-all_points.dat" with dots title "samples", "Canon_PowerShot_SD1100_IS--7.2--3.0--inf-bins.dat" with linespoints lw 4 title "average", \
     14900.260063158034 * (1 + (-0.35302023511417185) * x**2 + (0.05568596419567414) * x**4 + (-0.00026849798330039583) * x**6) title "fit"
pause -1
