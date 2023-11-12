import numpy as np
import matplotlib.pyplot as plt

# Parameters
m = 0.6 # Mass
k = 201600  # Stiffness
c_r = 2*np.sqrt(k*m) # critical damping coeffecient

# Time vector
t = np.linspace(0, 0.2, 1000)

# Angular frequency (omega_n)
omega_n = np.sqrt(k/m)

# Impulse at t=0
impulse_amplitude = 6  # Adjust as needed
initial_displacement = 0.0

# Different damping coefficients
damping_coefficients = [400,500,695]

# Plot the results for different damping coefficients
plt.figure(figsize=(10, 6))

for c in damping_coefficients:
    # Initial velocity for the impulse
    initial_velocity = impulse_amplitude / m

    zeta = c/c_r

    omega_d = omega_n*(np.sqrt(1-(zeta)*(zeta)))

    # Displacement as a function of time (assuming a damped harmonic motion)
    A = initial_velocity/omega_d

    displacement = A * np.exp(-zeta*omega_n* t) * np.sin(omega_d * t)

    # Plot the results for each damping coefficient
    plt.plot(t, displacement, label=f'Damping Coefficient: {c}')

plt.title('Impulse Response of SDOF System with Different Damping Coefficients')
plt.xlabel('Time (s)')
plt.ylabel('Displacement')
plt.legend()
plt.grid(True)
plt.show()