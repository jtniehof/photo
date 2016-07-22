set grid
set title "Canon PowerShot SD1100 IS, 18.6 mm, f/5.0, ∞ m"
plot "Canon_PowerShot_SD1100_IS--18.6--5.0--inf-all_points.dat" with dots title "samples", "Canon_PowerShot_SD1100_IS--18.6--5.0--inf-bins.dat" with linespoints lw 4 title "average", \
     14289.75837511965 * (1 + (-0.1524379964358093) * x**2 + (-0.05443218859985939) * x**4 + (0.04561516564404133) * x**6) title "fit"
pause -1
