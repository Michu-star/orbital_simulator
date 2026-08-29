import numpy as np
import matplotlib.pyplot as plt
from physicslib.ode import *

# Physics
class Body:
    def __init__(self, mass, state):
        self.mass = mass
        self.state = state.flatten()

# The units used are:
# a.u. for distance
# earth years for time
# earth masses for mass

sun = Body(332950, np.array([[0, 0, 0],
                                   [0, 0, 0]]))


earth = Body(1, np.array([[1, 0, 0],
                                [0, 2*np.pi, 0]]))


moon = Body(0.012, np.array([[1 + 2.57e-3, 0, 0],
                                   [0, 2*np.pi + 0.216, 0]]))


mars = Body(0.107, np.array([[1.524, 0, 0],
                                   [0, 5.09, 0]]))

bodies_list = [sun, earth, moon, mars]

G = 6.674 * 10 ** -11 * 5.97e24 * 1.496e11**-3 * (3600*24*365.25)**2
print(G)

t = np.linspace(0, 3, 10000)

system_state = np.concatenate([body.state for body in bodies_list])

def state_derivative(t, state, bodies):
    state = state.reshape((len(bodies), 6))

    r = state[:, :-3]
    v = state[:, 3:]
    a = np.zeros_like(r)

    for i in range(len(bodies)):
        for j, body_due in enumerate(bodies):
            if i == j:
                continue

            dr = r[i] - r[j]

            a[i] += (
                    -G * body_due.mass
                    * dr
                    / np.linalg.norm(dr) ** 3
            )

    return np.concatenate((v, a), axis=1).flatten()


solution = rk4(t, system_state, state_derivative, args=(bodies_list,))

solution = solution.reshape((len(t), len(bodies_list), 6))

fig, ax = plt.subplots()
ax.set_aspect('equal')

# Plot the trajectory of the Sun
ax.plot(solution[:, 0, 0], solution[:, 0, 1], color='r')
ax.plot(solution[0, 0, 0], solution[0, 0, 1], marker='o', label='Sun startpoint', color='#730202')
ax.plot(solution[-1, 0, 0], solution[-1, 0, 1], marker='o', label='Sun endpoint', color='#ed0202')

# Plot the trajectory of the Earth
ax.plot(solution[:, 1, 0], solution[:, 1, 1], color='b')

# Plot the trajectory of the Moon
ax.plot(solution[:, 2, 0], solution[:, 2, 1], color='g')

# Plot the trajectory of Mars
ax.plot(solution[:, 3, 0], solution[:, 3, 1], color='r')

'''
ax.plot(solution[0, 0], solution[0, 1], marker='o', label='Moon startpoint', color='#730202')
ax.plot(solution[-1, 0], solution[-1, 1], marker='o', label='Moon endpoint', color='#ed0202')

# Plot the trajectory of the planet
ax.plot(solution[0, 6], solution[0, 7], marker='o', label='Planet startpoint', color='#015457')
ax.plot(solution[-1, 6], solution[-1, 7], marker='o', label='Planet endpoint', color='#00cfd6')

plt.legend()
'''
plt.show()
