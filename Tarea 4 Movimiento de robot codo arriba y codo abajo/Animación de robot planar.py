# Importamos librerías necesarias
import numpy as np              # Para operaciones matemáticas
import matplotlib.pyplot as plt # Para graficar
from mpl_toolkits.mplot3d import Axes3D  # Para proyecciones en 3D

# Funciones trigonométricas en grados
def sind(t): return np.sin(np.deg2rad(t))  # Seno en grados
def cosd(t): return np.cos(np.deg2rad(t))  # Coseno en grados

# Longitudes de los eslabones
L1 = 15
L2 = 10

# -------------------------------
# Punto final deseado
x_target, y_target, z_target = 10, 15, 0

# Distancia al punto
r = np.sqrt(x_target**2 + y_target**2)

# Cinemática inversa (ley de cosenos)
cos_theta2 = (r**2 - L1**2 - L2**2) / (2*L1*L2)
theta2 = np.rad2deg(np.arccos(cos_theta2))   # solución codo arriba
theta2 = -theta2                             # solución codo abajo

theta1 = np.rad2deg(
    np.arctan2(y_target, x_target) -
    np.arctan2(L2*np.sin(np.deg2rad(theta2)), L1 + L2*np.cos(np.deg2rad(theta2)))
)
# -------------------------------

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
    # Posiciones
    p0 = np.array([0, 0, 0, 1])                        # Base
    p1 = np.dot(T1, np.array([0,0,0,1]))               # Final del eslabón 1
    p2 = np.dot(np.dot(T1, T2), np.array([0,0,0,1]))   # Efector final
    return p0, p1, p2

# Función para dibujar el robot
def draw_robot(p0, p1, p2):
    ax.scatter(p0[0], p0[1], p0[2], color="red", s=50)   # Base
    ax.scatter(p1[0], p1[1], p1[2], color="blue", s=50)  # Articulación 1
    ax.scatter(p2[0], p2[1], p2[2], color="green", s=50) # Efector final
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]], color="black", linewidth=3)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color="black", linewidth=3)

# Animación desde 0 hasta los ángulos que llevan a (10,15,0)
steps = 100
for step in range(steps+1):
    ax.cla()
    setaxis()
    t1 = theta1 * step / steps
    t2 = theta2 * step / steps
    p0, p1, p2 = forward_kinematics(t1, t2)
    draw_robot(p0, p1, p2)
    plt.draw()
    plt.pause(0.05)

plt.show()

print(f"Ángulo 1 calculado: {theta1:.2f}°")
print(f"Ángulo 2 calculado: {theta2:.2f}°")
