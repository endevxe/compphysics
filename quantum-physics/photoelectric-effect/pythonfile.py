import numpy as np
import matplotlib.pyplot as plt

# Constants
h = 6.626e-34  # Planck's constant (J·s)
e = 1.602e-19  # Elementary charge (C)

# Sample metals with work functions in eV
metals = {
    'Cesium': 2.14,
    'Potassium': 2.30,
    'Sodium': 2.36,
    'Zinc': 4.3,
    'Copper': 4.7
}

def photoelectric_simulation(frequency, intensity, metal):
    phi = metals[metal] * e  # Convert work function to joules
    energy = h * frequency
    
    if energy < phi:
        print("No electrons emitted. Energy is below the work function.")
        return 0, 0
    
    KE = energy - phi
    num_electrons = int(intensity * 1e15)  # Arbitrary scaling
    
    print(f"Photon Energy: {energy:.2e} J")
    print(f"Work Function (φ): {phi:.2e} J")
    print(f"Kinetic Energy of Electrons: {KE:.2e} J")
    print(f"Number of Electrons Emitted: {num_electrons}")
    
    return KE, num_electrons

# Example usage
freq = 7e14  # Frequency in Hz
intensity = 0.8  # Arbitrary scale
metal = 'Sodium'

photoelectric_simulation(freq, intensity, metal)
