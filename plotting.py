import numpy as np
import matplotlib.pyplot as plt

def draw_scene(ax, solution, frame):

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
    '''

    for i in range(solution.shape[1]):
        # Plot the trajectory
        ax.plot(solution[:frame+1, i, 0], solution[:frame+1, i, 1])

        # Plot the position at a particular frame
        ax.plot(solution[frame, i, 0], solution[frame, i, 1], marker='o', color='#730202')
