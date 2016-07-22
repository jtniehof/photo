set grid
set title "Canon PowerShot SD1100 IS, 6.2 mm, f/2.8, ∞ m"
plot "Canon_PowerShot_SD1100_IS--6.2--2.8--inf-all_points.dat" with dots title "samples", "Canon_PowerShot_SD1100_IS--6.2--2.8--inf-bins.dat" with linespoints lw 4 title "average", \
     15291.761564956412 * (1 + (-0.40932137067543917) * x**2 + (0.20196081078233052) * x**4 + (-0.18450711979408654) * x**6) title "fit"
pause -1
