set grid
set title "Canon PowerShot SD1100 IS, 6.2 mm, f/2.8, ∞ m"
plot "Canon_PowerShot_SD1100_IS--6.2--2.8--inf-all_points.dat" with dots title "samples", "Canon_PowerShot_SD1100_IS--6.2--2.8--inf-bins.dat" with linespoints lw 4 title "average", \
     15269.068372941829 * (1 + (-0.4129735540432298) * x**2 + (0.21110444410599136) * x**4 + (-0.19052946773555507) * x**6) title "fit"
pause -1
