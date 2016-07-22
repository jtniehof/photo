set grid
set title "Canon PowerShot SD1100 IS, 18.6 mm, f/5.0, ∞ m"
plot "Canon_PowerShot_SD1100_IS--18.6--5.0--inf-all_points.dat" with dots title "samples", "Canon_PowerShot_SD1100_IS--18.6--5.0--inf-bins.dat" with linespoints lw 4 title "average", \
     14318.051532787731 * (1 + (-0.1571266950393965) * x**2 + (-0.0412152507137097) * x**4 + (0.03602364614079427) * x**6) title "fit"
pause -1
