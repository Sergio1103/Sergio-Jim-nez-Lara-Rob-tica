# Import libraries and packages
import matplotlib.pyplot as plt      # Librería para graficar en 2D/3D
from mpl_toolkits import mplot3d     # Permite graficar en 3D
import numpy as np                   # Librería para cálculos con matrices y vectores

# Crear la figura y ejes
fig,ax = plt.subplots()              
ax = plt.axes(projection = "3d")     # Transformamos los ejes a vista 3D

def setaxis(x1, x2, y1, y2, z1, z2):
    # Ajusta los límites visibles de la gráfica y la cámara
    ax.set_xlim3d(x1,x2)             # Límite en X
    ax.set_ylim3d(y1,y2)             # Límite en Y
    ax.set_zlim3d(z1,z2)             # Límite en Z
    ax.view_init(elev=30, azim=40)   # Ángulo de cámara (elevación y azimut)

def fix_system(axis_length):
    # Dibuja el sistema de referencia (ejes XYZ)
    x = [-axis_length, axis_length]   # Coordenadas eje X
    y = [-axis_length, axis_length]   # Coordenadas eje Y
    z = [-axis_length, axis_length]   # Coordenadas eje Z
    zp = [0, 0]                       # Origen de cada eje
    ax.plot3D(x, zp, zp, color='red')    # Dibuja eje X en rojo
    ax.plot3D(zp, y, zp, color='blue')   # Dibuja eje Y en azul
    ax.plot3D(zp, zp, z, color='green')  # Dibuja eje Z en verde

def sind(t):
    # Calcula el seno de un ángulo en grados
    return np.sin(t*np.pi/180)

def cosd(t):
    # Calcula el coseno de un ángulo en grados
    return np.cos(t*np.pi/180)

def RotY(t):
    # Matriz 4x4 homogénea de rotación en Y
    Ry = np.array([
        [ cosd(t), 0, sind(t), 0],   # Fila 1
        [ 0,       1, 0,       0],   # Fila 2
        [-sind(t), 0, cosd(t), 0],   # Fila 3
        [ 0,       0, 0,       1]    # Fila 4 (homogénea)
    ])
    return Ry                        # Devuelve la matriz 4x4

def drawVector(v):
    # Dibuja un vector 3D desde el origen
    deltaX = [0, v[0]]               # Coordenadas X del vector
    deltaY = [0, v[1]]               # C
