import numpy as np
import matplotlib.pyplot as plt

def draw_scene(ax, solution, frame, view_mode):
    ax.clear()

    for i in range(solution.shape[1]):
        # Plot the trajectory
        ax.plot(solution[:frame + 1, i, 0], solution[:frame + 1, i, 1])

        # Plot the position at a particular frame
        ax.plot(solution[frame, i, 0], solution[frame, i, 1], marker='o')

    if view_mode == "solar_system":
        ax.set_xlim(-31, 31)
        ax.set_ylim(-31, 31)

    elif view_mode == "earth_moon":
        earth_x = solution[frame, 3, 0]
        earth_y = solution[frame, 3, 1]
        dist = 0.004

        ax.set_xlim(earth_x - dist, earth_x + dist)
        ax.set_ylim(earth_y - dist, earth_y + dist)

    ax.set_aspect('equal')
    ax.set_xlabel("x / a.u.")
    ax.set_ylabel("y / a.u.")


def draw_energy_plot(ax, t, relative_energy_error, frame):
    ax.clear()

    ax.plot(t, relative_energy_error)
    ax.axvline(t[frame], linestyle='dashed',
              label=f'{relative_energy_error[frame]}')

    ax.set_title("Rel. energy error vs time")
    ax.set_ylabel("error")
    ax.legend()



def draw_momentum_plot(ax, t, momentum, x, frame):
    ax.clear()

    ax.plot(t, momentum[:, x])
    ax.axvline(t[frame], linestyle='dashed', label=f'{momentum[frame, x]}')

    if x == 0:
        x = 'x'
    elif x == 1:
        x = 'y'
    else:
        x = 'z'

    ax.set_title(f'{x} momentum vs time')
    ax.set_xlabel("t / years")
    ax.set_ylabel("momentum / m_e * a.u./year")
    ax.legend()
