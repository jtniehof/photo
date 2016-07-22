set grid
set title "Canon PowerShot SD1100 IS, 7.2 mm, f/3.0, ∞ m"
plot "Canon_PowerShot_SD1100_IS--7.2--3.0--inf-all_points.dat" with dots title "samples", "Canon_PowerShot_SD1100_IS--7.2--3.0--inf-bins.dat" with linespoints lw 4 title "average", \
     14927.962828921347 * (1 + (-0.3531493488608546) * x**2 + (0.05489427635487907) * x**4 + (0.00014420997880757293) * x**6) title "fit"
pause -1
