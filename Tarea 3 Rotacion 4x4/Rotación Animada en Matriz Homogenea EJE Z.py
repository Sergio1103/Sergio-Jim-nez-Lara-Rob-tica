# Import libraries and packages
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

# create the fig and ax objects to handle figure and axes of the fixed frame
fig,ax = plt.subplots()
ax = plt.axes(projection = "3d")  # Vista 3D

def setaxis(x1, x2, y1, y2, z1, z2):
    # Ajusta los límites visibles de la gráfica y la cámara
    ax.set_xlim3d(x1,x2)
    ax.set_ylim3d(y1,y2)
    ax.set_zlim3d(z1,z2)
    ax.view_init(elev=30, azim=40)  # Ángulo de cámara

def fix_system(axis_length):
    # Dibuja el sistema de referencia (ejes XYZ)
    x = [-axis_length, axis_length]
    y = [-axis_length, axis_length]
    z = [-axis_length, axis_length]
    zp = [0, 0]
    ax.plot3D(x, zp, zp, color='red')    # eje X
    ax.plot3D(zp, y, zp, color='blue')   # eje Y
    ax.plot3D(zp, zp, z, color='green')  # eje Z

def sind(t):
    # Calcula el seno en grados
    return np.sin(t*np.pi/180)

def cosd(t):
    # Calcula el coseno en grados
    return np.cos(t*np.pi/180)

def RotZ(t):
    # Matriz 4x4 homogénea de rotación en Z
    Rz = np.array([
        [cosd(t), -sind(t), 0, 0],
        [sind(t),  cosd(t), 0, 0],
        [0,        0,       1, 0],
        [0,        0,       0, 1]
    ])
    return Rz

def drawVector(v):
    # Dibuja un vector 3D desde el origen
    deltaX = [0, v[0]]
    deltaY = [0, v[1]]
    deltaZ = [0, v[2]]
    ax.plot3D(deltaX, deltaY, deltaZ,color='orange')

def rotate(final_angle): 
    # Animación de rotación desde 0 hasta final_angle
    for ang in range(0, final_angle+1):
        ax.cla()                    # Limpia la gráfica para el siguiente frame
        setaxis(-1,1,-1,1,-1,1)    # Ajusta los límites de la vista
        fix_system(1)               # Dibuja los ejes de referencia

        # Vector inicial desde Y = 0 (origen)
        v1 = np.array([1,0,1,1])   # [X,Y,Z,1], Y=0 para que comience desde cero
        drawVector(v1[:3])          # Dibuja el vector inicial

        # Vector rotado en Z
        v2 = RotZ(ang).dot(v1)
        drawVector(v2[:3])          # Dibuja el vector rotado

        plt.draw()                  # Refresca la gráfica
        plt.pause(0.01)             # Pausa para animación visible

# Ejecutar animación hasta 90 grados
rotate(90)
plt.draw()
plt.show()
