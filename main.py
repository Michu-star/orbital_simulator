import numpy as np
import matplotlib.pyplot as plt
from physicslib.ode import *

# Physics
class Body:
    def __init__(self, mass, state):
        self.mass = mass
        self.state = state

planet = Body(100, np.array([[0, 0, 0],
                                  [0, 0, 0]]))

moon = Body(1, np.array([[1, 0, 0],
                               [0, 13, 0]]))

G = 1

t = np.linspace(0, 2, 1000)

def acceleration(on, due):
    return (- G * due.mass * (on.state[0] - due.state[0]) /
            np.linalg.norm(on.state[0] - due.state[0])**3)

# print(acceleration(moon, planet))
# print(acceleration(planet, moon))

def state_derivative(t, state, due):
    r = state[:3]
    v = state[3:]
    r_due = due.state[0]

    a = - G * due.mass * (r - r_due) / np.linalg.norm(r - r_due) ** 3

    return np.array([v, a]).flatten()

solution_moon = rk4(t, moon.state.flatten(), state_derivative, args=(planet,))
# solution_planet = rk4(t, planet.state.flatten(), state_derivative, args=(moon,))

fig, ax = plt.subplots()
ax.set_aspect('equal')

ax.plot(solution_moon[:, 0], solution_moon[:, 1])
ax.plot(solution_moon[0, 0], solution_moon[0, 1], marker='o', label='Moon startpoint')
ax.plot(solution_moon[-1, 0], solution_moon[-1, 1], marker='o', label='Moon endpoint')
# ax.plot(solution_planet[:, 0], solution_planet[:, 1])
plt.legend()
plt.show()
