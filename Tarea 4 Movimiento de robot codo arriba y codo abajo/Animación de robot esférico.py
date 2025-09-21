import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def sind(t): return np.sin(np.deg2rad(t))
def cosd(t): return np.cos(np.deg2rad(t))

L1 = 15
L2 = 13

theta1 = 56.31
theta2 = -20.946833
theta3 = 92.93429754

def rot_z(angle):
    return np.array([
        [cosd(angle), -sind(angle), 0, 0],
        [sind(angle),  cosd(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def rot_y(angle):
    return np.array([
        [ cosd(angle), 0, sind(angle), 0],
        [ 0, 1, 0, 0],
        [-sind(angle), 0, cosd(angle), 0],
        [ 0, 0, 0, 1]
    ])

def trasl_x(L):
    return np.array([
        [1, 0, 0, L],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def forward_kinematics(theta1, theta2, theta3):
    # Multiplicación de matrices homogéneas para la primera articulación
    T1 = rot_z(theta1) @ rot_y(theta2) @ trasl_x(L1)  # @ = multiplicación de matrices (rotación Z * rotación Y * traslación X)
    # Multiplicación para la segunda articulación (codo abajo)
    T2 = T1 @ rot_y(-theta3) @ trasl_x(L2)           # @ = multiplicación de matrices (T1 * rotación Y de codo abajo * traslación X)
    p0 = np.array([0,0,0,1])
    p1 = T1 @ np.array([0,0,0,1])                     # @ = aplicar la matriz homogénea T1 al punto inicial
    p2 = T2 @ np.array([0,0,0,1])                     # @ = aplicar la matriz homogénea T2 al punto inicial (efector final)
    return p0, p1, p2

def draw_robot(p0, p1, p2):
    ax.scatter(p0[0], p0[1], p0[2], color="red", s=50)
    ax.scatter(p1[0], p1[1], p1[2], color="blue", s=50)
    ax.scatter(p2[0], p2[1], p2[2], color="green", s=50)
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]], color="black", linewidth=3)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color="black", linewidth=3)

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
def setaxis():
    ax.set_xlim3d(-30,30)
    ax.set_ylim3d(-30,30)
    ax.set_zlim3d(-30,30)
    ax.view_init(elev=30, azim=40)

steps = 100
trajectory = []

for step in range(steps+1):
    ax.cla()
    setaxis()
    
    t1 = theta1 * step / steps
    t2 = theta2 * step / steps
    t3 = theta3 * step / steps
    
    p0, p1, p2 = forward_kinematics(t1, t2, t3)
    
    trajectory.append([p2[0], p2[1], p2[2]])
    
    draw_robot(p0, p1, p2)
    
    traj_array = np.array(trajectory)
    ax.plot(traj_array[:,0], traj_array[:,1], traj_array[:,2], color="green", linewidth=2, alpha=0.6)
    
    plt.draw()
    plt.pause(0.05)

plt.show()
