import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import pandas as pd
from sys import exit


def update_lines(num, data, line):
    # NOTE: there is no .set_data() for 3 dim data...
    line.set_data(data[0:2, :num])    
    line.set_3d_properties(data[2, :num])    
    return line

def plot(filename):
    
    # Attaching 3D axises to the figure
    fig, (acc_ax,gyr_ax,mag_ax) = plt.subplots(1,3, num=filename, subplot_kw=dict(projection="3d"))
    fig.set_figwidth(16)
    fig.set_figheight(6)

    axes = { 0 : (acc_ax , "Acc (mg)"),
            1 : (gyr_ax, "Gyro (DPS)"),
            2 : (mag_ax, "Mag (uT)")}

    # Reading the data from a CSV file using pandas
    repo = pd.read_csv(filename, sep=',',header=0)
    acc_data = np.array((repo['Acc x (mg) '].values, repo['Acc y (mg) '].values, repo['Acc z (mg) '].values))
    gyr_data = np.array((repo['Gyr x (DPS) '].values, repo['Gyr y (DPS) '].values, repo['Gyr z (DPS) '].values))
    mag_data = np.array((repo['Mag x (uT) '].values, repo['Mag y (uT) '].values, repo['Mag z (uT) '].values))

    data_list = [acc_data, gyr_data, mag_data]

    # print(acc_data[0])
    # print(gyr_data[1])
    # print(mag_data[2])

    acc_line = axes.get(0)[0].plot(acc_data[0, 0:1], acc_data[1, 0:1], acc_data[2, 0:1])[0] 
    gyr_line = axes.get(1)[0].plot(gyr_data[0, 0:1], gyr_data[1, 0:1], gyr_data[2, 0:1])[0] 
    mag_line = axes.get(2)[0].plot(mag_data[0, 0:1], mag_data[1, 0:1], mag_data[2, 0:1])[0] 

    for x in range(3):

        # Setting the axes properties
        axes.get(x)[0].set_xlim3d([data_list[x][0].min(), data_list[x][0].max()])
        axes.get(x)[0].set_xlabel('X')
        axes.get(x)[0].set_ylim3d([data_list[x][1].min(), data_list[x][1].max()])
        axes.get(x)[0].set_ylabel('Y')
        axes.get(x)[0].set_zlim3d([data_list[x][2].min(), data_list[x][2].max()])
        axes.get(x)[0].set_zlabel('Z')

        axes.get(x)[0].set_title(axes.get(x)[1])

    # Creating the Animation object
    acc_line_ani = animation.FuncAnimation(fig, update_lines, acc_data.shape[1], fargs=(acc_data, acc_line), interval=1, blit=False)
    gyr_line_ani = animation.FuncAnimation(fig, update_lines, gyr_data.shape[1], fargs=(gyr_data, gyr_line), interval=1, blit=False)
    mag_line_ani = animation.FuncAnimation(fig, update_lines, mag_data.shape[1], fargs=(mag_data, mag_line), interval=1, blit=False)
    
    plt.show()
    
plot("example.csv")