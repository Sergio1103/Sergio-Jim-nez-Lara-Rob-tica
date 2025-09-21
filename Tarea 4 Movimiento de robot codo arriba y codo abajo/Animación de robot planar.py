# Importamos librerías necesarias
import numpy as np              # Para operaciones matemáticas
import matplotlib.pyplot as plt # Para graficar
from mpl_toolkits.mplot3d import Axes3D  # Para proyecciones en 3D
import time                     # Para manejar pausas en la animación

# Funciones trigonométricas en grados
def sind(t):
    return np.sin(np.deg2rad(t))  # Seno en grados
def cosd(t):
    return np.cos(np.deg2rad(t))  # Coseno en grados

# Longitudes de los eslabones
L1 = 15
L2 = 10

# Ángulos dados en grados
theta1 = 101.518221
theta2 = 100.1785133

# Creamos la figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Función para fijar los ejes de la animación
def setaxis():
    ax.set_xlim3d(-30, 30)
    ax.set_ylim3d(-30, 30)
    ax.set_zlim3d(-5, 30)
    ax.view_init(elev=30, azim=40)  # Vista de cámara

# Cinemática directa (con matrices homogéneas 4x4)
def forward_kinematics(theta1, theta2):
    """
    Calcula la posición de cada articulación
    usando matrices homogéneas en 3D (rotación en Z + traslación en X)
    """
    # Matriz homogénea de la primera articulación
    T1 = np.array([
        [cosd(theta1), -sind(theta1), 0, L1*cosd(theta1)],
        [sind(theta1),  cosd(theta1), 0, L1*sind(theta1)],
        [0,             0,            1, 0],
        [0,             0,            0, 1]
    ])
    
    # Matriz homogénea de la segunda articulación
    T2 = np.array([
        [cosd(theta2), -sind(theta2), 0, L2*cosd(theta2)],
        [sind(theta2),  cosd(theta2), 0, L2*sind(theta2)],
        [0,             0,            1, 0],
        [0,             0,            0, 1]
    ])
    
    # Posiciones en coordenadas homogéneas
    p0 = np.array([0, 0, 0, 1])         # Origen (base del robot)
    p1 = np.dot(T1, np.array([0,0,0,1])) # Final del eslabón 1
    p2 = np.dot(np.dot(T1, T2), np.array([0,0,0,1])) # Final del eslabón 2 (efector)
    
    return p0, p1, p2

# Función para dibujar el robot
def draw_robot(p0, p1, p2):
    # Dibujar articulaciones
    ax.scatter(p0[0], p0[1], p0[2], color="red", s=50)   # Base
    ax.scatter(p1[0], p1[1], p1[2], color="blue", s=50)  # Articulación 1
    ax.scatter(p2[0], p2[1], p2[2], color="green", s=50) # Efector final
    
    # Dibujar eslabones
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]], color="black", linewidth=3)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color="black", linewidth=3)

# Animación desde 0 hasta los ángulos finales
steps = 100
for step in range(steps+1):
    ax.cla()        # Limpiar el frame anterior
    setaxis()       # Fijar límites de la vista
    
    # Interpolar los ángulos para animación
    t1 = theta1 * step / steps
    t2 = theta2 * step / steps
    
    # Como es codo abajo, el segundo ángulo rota hacia abajo (se resta)
    p0, p1, p2 = forward_kinematics(t1, -t2)
    
    # Dibujar robot en este paso
    draw_robot(p0, p1, p2)
    
    plt.draw()
    plt.pause(0.05)

plt.show()
