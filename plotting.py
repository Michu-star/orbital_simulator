import numpy as np
import matplotlib.pyplot as plt

def draw_scene(ax, solution, frame, view_mode):
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

    '''
    if view_mode == "solar_system":
        for i in range(solution.shape[1]):
            # Plot the trajectory
            ax.plot(solution[:frame + 1, i, 0], solution[:frame + 1, i, 1])

            # Plot the position at a particular frame
            ax.plot(solution[frame, i, 0], solution[frame, i, 1], marker='o')

    elif view_mode == "earth_moon":
        earth_position = solution[:, 3, :2]
        moon_position = solution[:, 4, :2]

        moon_relative = moon_position - earth_position

        ax.plot(
            moon_relative[:frame + 1, 0],
            moon_relative[:frame + 1, 1]
        )

        ax.plot(
            moon_relative[frame, 0],
            moon_relative[frame, 1],
            marker='o'
        )

        ax.plot(0, 0, marker='o')
    '''