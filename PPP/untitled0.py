# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 19:55:20 2023

@author: beLIVE
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Define the Lotka-Volterra model equations
def predator_prey_equations(x, t, a, b, c, d):
    n, p = x
    dxdt = [a*n - b*n*p, c*n*p - d*p]
    return dxdt

# Define the model parameters
a = 1.5
b = 0.1
c = 0.1
d = 1.0

# Define the initial populations of prey and predators
n0 = 10
p0 = 1

# Define the time points to simulate
t = np.linspace(0, 50, 1000)

# Simulate the model using the odeint function from scipy.integrate

x0 = [n0, p0]
x = odeint(predator_prey_equations, x0, t, args=(a, b, c, d))

# Plot the results
plt.plot(t, x[:,0], label='Prey')
plt.plot(t, x[:,1], label='Predators')
plt.xlabel('Time')
plt.ylabel('Population')
plt.title('Lotka-Volterra Model')
plt.legend()
plt.show()