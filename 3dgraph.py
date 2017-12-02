import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import csv


mpl.rcParams['legend.fontsize'] = 10
# Configure the figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set up the plot
g1, = plt.plot([] ,[], [])

# Set size of axes
plt.axis([0, 600, 0, 400])

ax.set_zlim(0, 400)


def update_line(g1, x, y, z):
    ax.scatter(float(x),float(y),float(z),c='r', marker='_')
    
def update_sphere(counter, u, v, x, y, z):
    spherex = float(x) + (10 * np.outer(np.cos(u), np.sin(v)))
    spherey = float(y) + (10 * np.outer(np.sin(u), np.sin(v)))
    spherez = float(z) + (10 * np.outer(np.ones(np.size(u)), np.cos(v)))
    surfaceobject = create_sphere(spherex, spherey, spherez)    
    return surfaceobject

def create_sphere(x,y,z):
    sphere = ax.plot_surface(x,y,z,rstride=4, cstride=4, color='b', linewidth=0, alpha=0.5)
    return sphere

with open('data.csv', 'rt') as csvfile:
    filereader = csv.reader(csvfile, delimiter = ' ')
    # Initiate a counter for testing 
    counter = 0
    for row in filereader:
        # print(str(filereader))
        # print(', '.join(row))
        # print(str(type(row)) + ' ' + str(row))
        # mpl.rcParams['legend.fontsize'] = 10
        x = counter
        y = row[0]
        z = y
        u = np.linspace(100, 100 + (2 * np.pi), 100)
        v = np.linspace(100, 100 + np.pi, 100)
        update_line(g1, x, y, z)
        if counter == 0:
            surface = update_sphere(counter, u, v, x, y, z)
        else:
            surface.remove()
            surface = update_sphere(counter,u,v, x, y, z)
        counter+=10
        plt.pause(0.05)



