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
    g1.set_xdata(np.append(g1.get_xdata(), float(x)))
    g1.set_ydata(np.append(g1.get_ydata(), float(y)))
    # g1.set_data(float(x), float(y))
    g1.set_3d_properties(zs=z)
    plt.draw()

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
        update_line(g1, x, y, z)
        # counter+=10
        plt.pause(0.05)



