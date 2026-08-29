import numpy as np
import matplotlib.pyplot as plt
from physicslib.ode import *

# Physics
class Body:
    def __init__(self, mass, state):
        self.mass = mass
        self.state = state.flatten()

sun = Body(10000, np.array([[0, 0, 0],
                                 [0, -0.1, 0]]))


planet = Body(100, np.array([[10, 0, 0],
                                  [0, 20-0.13, 0]]))

moon = Body(1, np.array([[11, 0, 0],
                               [0, 13, 0]]))

bodies_list = [sun, planet, moon]

G = 1

t = np.linspace(0, 8, 1000)

system_state = np.zeros((len(bodies_list), 6))
for i, body in enumerate(bodies_list):
    system_state[i, :] = body.state


def state_derivative(t, state, bodies):
    state = state.reshape((len(bodies), 6))

    r = state[:, :-3]
    v = state[:, 3:]
    a = np.zeros_like(r)

    for i, body_on in enumerate(bodies):
        acceleration = np.zeros(3)

        for j, body_due in enumerate(bodies):
            if i == j:
                continue

            acceleration += - G * body_due.mass * (r[i] - r[j]) / np.linalg.norm(r[i] - r[j]) ** 3

        a[i] = acceleration

    derivative = np.concatenate((v, a), 1)

    return derivative.flatten()

system_state = np.concatenate([body.state for body in bodies_list])

solution = rk4(t, system_state, state_derivative, args=(bodies_list,))

solution = solution.reshape((len(t), len(bodies_list), 6))

fig, ax = plt.subplots()
ax.set_aspect('equal')

# Plot the trajectory of the sun
ax.plot(solution[:, 0, 0], solution[:, 0, 1], color='r')

# Plot the trajectory of the planet
ax.plot(solution[:, 1, 0], solution[:, 1, 1], color='b')

# Plot the trajectory of the moon
ax.plot(solution[:, 2, 0], solution[:, 2, 1], color='g')
'''
ax.plot(solution[0, 0], solution[0, 1], marker='o', label='Moon startpoint', color='#730202')
ax.plot(solution[-1, 0], solution[-1, 1], marker='o', label='Moon endpoint', color='#ed0202')

# Plot the trajectory of the planet
ax.plot(solution[:, 6], solution[:, 7], color='b')
ax.plot(solution[0, 6], solution[0, 7], marker='o', label='Planet startpoint', color='#015457')
ax.plot(solution[-1, 6], solution[-1, 7], marker='o', label='Planet endpoint', color='#00cfd6')

plt.legend()
'''
plt.show()
