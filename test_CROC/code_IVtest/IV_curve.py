"""
author: @oponcet
date: 2024-10

Ce script permet de lire deux fichiers Excel contenant des données IV (courant-tension) et de tracer les courbes IV

"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Lecture du premier fichier Excel avec les données IV
file_path_1 = '/Users/oponcet/cernbox/test/test_CROC/IV_18_09_24.xlsx'
df_1 = pd.read_excel(file_path_1)

# Lecture du second fichier Excel avec les données IV
file_path_2 = '/Users/oponcet/cernbox/test/test_CROC/IV_15_10_24.xlsx'
df_2 = pd.read_excel(file_path_2)

# Les colonnes du fichier s'appellent "Voltage (V)" et "Current (nA)"
tension_1 = df_1['Voltage (V)']
courant_1 = df_1['Current (nA)']
T_1 = -30.8  # Température pour le premier fichier
HR_1 = 10.1  # Humidité relative pour le premier fichier

# Données pour le second fichier
tension_2 = df_2['Voltage (V)']
courant_2 = df_2['Current (nA)']
T_2 = -29.2   # Température pour le second fichier
HR_2 = 9.2   # Humidité relative pour le second fichier

# Tracé du graphique Courant-Tension
plt.figure(figsize=(8, 6))

# Courbe 1: Données du premier fichier
plt.plot(tension_1, courant_1, marker='P', linestyle='', color='royalblue', label=f"T = {T_1}°C, HR = {HR_1}%")

# Courbe 2: Données du second fichier
plt.plot(tension_2, courant_2, marker='P', linestyle='', color='firebrick', label=f"T = {T_2}°C, HR = {HR_2}%")

plt.title("IV Curve")
plt.xlabel("Voltage (V)")
plt.ylabel("Current (nA)")  # Unité adaptée à vos données
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Flip x-axis (Voltage) from 0 to -100 and y-axis (Current) from 0 to -300
plt.xlim(0, -100)
plt.ylim(0, -300)

# Set major ticks on the x-axis and y-axis
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(10))

# Add the legend for both curves
plt.legend()

# Sauvegarder le graphique Courant-Tension avec deux courbes
plt.savefig('/Users/oponcet/cernbox/test/test_CROC/plots/courbe_courant_tension_flipped_double.png')
plt.savefig('/Users/oponcet/cernbox/test/test_CROC/plots/courbe_courant_tension_flipped_double.pdf')


# Calcul de la dérivée approximative (variation du courant par rapport à la tension) pour les deux fichiers
variation_courant_1 = np.diff(courant_1) / np.diff(tension_1)
variation_courant_2 = np.diff(courant_2) / np.diff(tension_2)

# Points milieu des tensions (car diff() réduit d'un élément) pour les deux fichiers
tension_milieu_1 = [(tension_1[i] + tension_1[i+1]) / 2 for i in range(len(tension_1) - 1)]
tension_milieu_2 = [(tension_2[i] + tension_2[i+1]) / 2 for i in range(len(tension_2) - 1)]

# Tracé de la variation du courant en fonction de la tension
plt.figure(figsize=(8, 6))

# Courbe 1: Variation du courant pour le premier fichier
plt.plot(tension_milieu_1, variation_courant_1, marker='P', linestyle='', color='royalblue', label=f"T = {T_1}°C, HR = {HR_1}%")

# Courbe 2: Variation du courant pour le second fichier
plt.plot(tension_milieu_2, variation_courant_2, marker='P', linestyle='', color='firebrick', label=f"T = {T_2}°C, HR = {HR_2}%")

plt.title("Variation of Current with Voltage")
plt.xlabel("Voltage (V)")
plt.ylabel("Current (nA/V)")
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Flip x-axis (Voltage) from 0 to -100
plt.xlim(0, -100)

# Set major ticks on the x-axis and y-axis
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(5))
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(2))

# Add the legend for both curves
plt.legend()

# Sauvegarder le graphique Variation du Courant-Tension avec deux courbes
plt.savefig('/Users/oponcet/cernbox/test/test_CROC/plots/variation_courant_tension_flipped_double.png')
plt.savefig('/Users/oponcet/cernbox/test/test_CROC/plots/variation_courant_tension_flipped_double.pdf')

