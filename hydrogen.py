import numpy as np


def potential(distance):
    # Constants for H2 molecule
    # De = 458.0  # Dissociation energy in kJ/mol
    De = 1
    re = 0.74   # Equilibrium bond distance in Angstroms
    a = 1.9426  # Width parameter in inverse Angstroms

    # Morse potential formula: V(r) = De * (1 - exp(-a(r - re)))^2
    potential = De * (1 - np.exp(-a * (distance - re)))**2 - De

    return potential
