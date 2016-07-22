set grid
set title "Canon PowerShot SD1100 IS, 14.3 mm, f/4.3, ∞ m"
plot "Canon_PowerShot_SD1100_IS--14.3--4.3--inf-all_points.dat" with dots title "samples", "Canon_PowerShot_SD1100_IS--14.3--4.3--inf-bins.dat" with linespoints lw 4 title "average", \
     14348.81001646677 * (1 + (-0.16083161123743867) * x**2 + (-0.03354928107459278) * x**4 + (0.033628858874507415) * x**6) title "fit"
pause -1
