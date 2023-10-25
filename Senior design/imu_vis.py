import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import pandas as pd
import imufusion
import sys

def update(num, data, time, line):
    # NOTE: there is no .set_data() for 3 dim data...
    line.set_data(time[:num],data[:num])  
    #line.axes.axis([0, time.size, 0, data.size])
    return line

def plot(filename):
    
    # Reading the data from a CSV file using pandas
    repo = pd.read_csv(filename, sep=',',header=0)
    acc_data = (np.array((repo['Acc x (mg) '].values, repo['Acc y (mg) '].values, repo['Acc z (mg) '].values))/1000).transpose()
    
    print(acc_data.shape)
    gyr_data = np.array((repo['Gyr x (DPS) '].values, repo['Gyr y (DPS) '].values, repo['Gyr z (DPS) '].values)).transpose()
    mag_data = np.array((repo['Mag x (uT) '].values, repo['Mag y (uT) '].values, repo['Mag z (uT) '].values)).transpose()
    timestamp = np.array((repo[' Time (ms) '].values))



    # Plot sensor data
    _, axes = plt.subplots(num=filename, nrows=4, sharex=True)

    _.set_figheight(10)
    _.set_figwidth(10)

    gry_line_x, = axes[0].plot(timestamp, gyr_data[:, 0], "tab:red", label="X")
    gry_line_y, = axes[0].plot(timestamp, gyr_data[:, 1], "tab:green", label="Y")
    gry_line_z, = axes[0].plot(timestamp, gyr_data[:, 2], "tab:blue", label="Z")
    axes[0].set_title("Gyroscope")
    axes[0].set_ylabel("Degrees/s")
    axes[0].grid()
    axes[0].legend()

    acc_line_x, = axes[1].plot(timestamp, acc_data[:, 0], "tab:red", label="X")
    acc_line_y, = axes[1].plot(timestamp, acc_data[:, 1], "tab:green", label="Y")
    acc_line_z, = axes[1].plot(timestamp, acc_data[:, 2], "tab:blue", label="Z")
    axes[1].set_title("Accelerometer")
    axes[1].set_ylabel("g")
    axes[1].grid()
    axes[1].legend()

    # Process sensor data
    ahrs = imufusion.Ahrs()
    euler = np.empty((len(timestamp), 3))

    for index in range(len(timestamp)):
        ahrs.update_no_magnetometer(gyr_data[index], acc_data[index], 1 / 100)  # 100 Hz sample rate
        euler[index] = ahrs.quaternion.to_euler()

    # Plot Euler angles
    euler_line_r, = axes[2].plot(timestamp, euler[:, 0], "tab:red", label="Roll")
    euler_line_p, = axes[2].plot(timestamp, euler[:, 1], "tab:green", label="Pitch")
    euler_line_y, = axes[2].plot(timestamp, euler[:, 2], "tab:blue", label="Yaw")
    axes[2].set_title("Euler angles")
    axes[2].set_ylabel("Degrees")
    axes[2].grid()
    axes[2].legend()
    
    mag_line_x, = axes[3].plot(timestamp, mag_data[:, 0], "tab:red", label="X")
    mag_line_y, = axes[3].plot(timestamp, mag_data[:, 1], "tab:green", label="Y")
    mag_line_z, = axes[3].plot(timestamp, mag_data[:, 2], "tab:blue", label="Z")
    axes[3].set_title("Magnetic Field")
    axes[3].set_xlabel("ms")
    axes[3].set_ylabel("uT")
    axes[3].grid()
    axes[3].legend()

    # Uncomment to enable animation

    # acc_xline_ani = animation.FuncAnimation(_, update, acc_data[:,0].size, fargs=(acc_data[:,0], timestamp, acc_line_x), interval=1, blit=False)
    # acc_yline_ani = animation.FuncAnimation(_, update, acc_data[:,1].size, fargs=(acc_data[:,1], timestamp, acc_line_y), interval=1, blit=False)
    # acc_zline_ani = animation.FuncAnimation(_, update, acc_data[:,2].size, fargs=(acc_data[:,2], timestamp, acc_line_z), interval=1, blit=False)
    
    # gyr_xline_ani = animation.FuncAnimation(_, update, gyr_data[:,0].size, fargs=(gyr_data[:,0], timestamp, gry_line_x), interval=1, blit=False)
    # gyr_yline_ani = animation.FuncAnimation(_, update, gyr_data[:,1].size, fargs=(gyr_data[:,1], timestamp, gry_line_y), interval=1, blit=False)
    # gyr_zline_ani = animation.FuncAnimation(_, update, gyr_data[:,2].size, fargs=(gyr_data[:,2], timestamp, gry_line_z), interval=1, blit=False)
    
    # mag_xline_ani = animation.FuncAnimation(_, update, mag_data[:,0].size, fargs=(mag_data[:,0], timestamp, mag_line_x), interval=1, blit=False)
    # mag_yline_ani = animation.FuncAnimation(_, update, mag_data[:,1].size, fargs=(mag_data[:,1], timestamp, mag_line_y), interval=1, blit=False)
    # mag_zline_ani = animation.FuncAnimation(_, update, mag_data[:,2].size, fargs=(mag_data[:,2], timestamp, mag_line_z), interval=1, blit=False)
    
    # euler_rline_ani = animation.FuncAnimation(_, update, euler[:,0].size, fargs=(euler[:,0], timestamp, euler_line_r), interval=1, blit=False)
    # euler_pline_ani = animation.FuncAnimation(_, update, euler[:,1].size, fargs=(euler[:,1], timestamp, euler_line_p), interval=1, blit=False)
    # euler_yline_ani = animation.FuncAnimation(_, update, euler[:,2].size, fargs=(euler[:,2], timestamp, euler_line_y), interval=1, blit=False)

    plt.show()  # don't block when script run by CI 
    
    
    
    
#plot("example.csv")