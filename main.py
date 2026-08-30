import numpy as np
import matplotlib.pyplot as plt
from physicslib.ode import *

from gui import draw_window

# Physics
class Body:
    def __init__(self, mass, initial_state):
        self.mass = mass
        self.initial_state = initial_state.flatten()

class Simulation:
    def __init__(self, bodies):
        self.bodies = bodies

    def state_derivative(self, t, state, bodies, G):
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

    def evolve(self, t, G):
        initial_system_state = np.concatenate([body.initial_state for body in self.bodies])

        sol = rk4(t, initial_system_state, self.state_derivative, args=(self.bodies, G,))

        sol = sol.reshape((len(t), len(self.bodies), 6))

        return sol

# The units used are:
# a.u. for distance
# earth years for time
# earth masses for mass

def main():
    sun = Body(332950, np.array([
        [0, 0, 0],
        [0, -0.003369, 0]
    ]))

    mercury = Body(0.055, np.array([
        [0.387, 0, 0],
        [0, 10.1, 0]
    ]))

    venus = Body(0.815, np.array([
        [0.724, 0, 0],
        [0, 7.38, 0]
    ]))

    earth = Body(1, np.array([
        [1, 0, 0],
        [0, 2*np.pi, 0]
    ]))

    moon = Body(0.012, np.array([
        [1 + 2.57e-3, 0, 0],
        [0, 2*np.pi + 0.216, 0]
    ]))

    mars = Body(0.107, np.array([
        [1.524, 0, 0],
        [0, 5.09, 0]
    ]))

    jupiter = Body(317.8, np.array([
        [5.204, 0, 0],
        [0, 2.754, 0]
    ]))

    saturn = Body(95.16, np.array([
        [9.583, 0, 0],
        [0, 2.030, 0]
    ]))

    uranus = Body(14.54, np.array([
        [19.218, 0, 0],
        [0, 1.433, 0]
    ]))

    neptune = Body(17.15, np.array([
        [30.11, 0, 0],
        [0, 1.145, 0]
    ]))

    bodies_list = [sun, mercury, venus, earth, moon, mars, jupiter, saturn, uranus, neptune]

    G = 6.674 * 10 ** -11 * 5.97e24 * 1.496e11**-3 * (3600*24*365.25)**2
    print(G)

    t = np.linspace(0, 10, 20000)

    simulation = Simulation(bodies_list)

    solution = simulation.evolve(t, G)

    draw_window(simulation, solution)

'''
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

plt.show()
'''

if __name__ == "__main__":
    main()