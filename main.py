import numpy as np
import matplotlib.pyplot as plt
from physicslib.ode import *

# Physics
class Body:
    def __init__(self, mass, state):
        self.mass = mass
        self.state = state

planet = Body(100, np.array([[0, 0, 0],
                                  [0, -0.13, 0]]))

moon = Body(1, np.array([[1, 0, 0],
                               [0, 13, 0]]))

G = 1

t = np.linspace(0, 8, 1000)

def acceleration(on, due):
    return (- G * due.mass * (on.state[0] - due.state[0]) /
            np.linalg.norm(on.state[0] - due.state[0])**3)

# print(acceleration(moon, planet))
# print(acceleration(planet, moon))

system_state = np.concatenate((moon.state.flatten(), planet.state.flatten()))

# print(system_state)

def state_derivative(t, state, moon, planet):
    r_moon = state[:3]
    v_moon = state[3:6]
    r_planet = state[6:9]
    v_planet = state[9:]

    a_moon = - G * planet.mass * (r_moon - r_planet) / np.linalg.norm(r_moon - r_planet) ** 3

    a_planet = - G * moon.mass * (r_planet - r_moon) / np.linalg.norm(r_planet - r_moon) ** 3

    return np.concatenate([v_moon, a_moon, v_planet, a_planet])

solution = rk4(t, system_state, state_derivative, args=(moon, planet,))
# solution_planet = rk4(t, planet.state.flatten(), state_derivative, args=(moon,))

fig, ax = plt.subplots()
ax.set_aspect('equal')

# Plot the trajectory of the moon
ax.plot(solution[:, 0], solution[:, 1], color='r')
ax.plot(solution[0, 0], solution[0, 1], marker='o', label='Moon startpoint', color='#730202')
ax.plot(solution[-1, 0], solution[-1, 1], marker='o', label='Moon endpoint', color='#ed0202')

# Plot the trajectory of the planet
ax.plot(solution[:, 6], solution[:, 7], color='b')
ax.plot(solution[0, 6], solution[0, 7], marker='o', label='Planet startpoint', color='#015457')
ax.plot(solution[-1, 6], solution[-1, 7], marker='o', label='Planet endpoint', color='#00cfd6')

plt.legend()
plt.show()
