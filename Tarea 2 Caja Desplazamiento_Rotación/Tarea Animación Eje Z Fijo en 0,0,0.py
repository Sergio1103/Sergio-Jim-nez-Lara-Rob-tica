# Importar librerías necesarias para gráficos 3D y cálculos
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

# Crear la figura y los ejes 3D
fig, ax = plt.subplots()
ax = plt.axes(projection="3d")  # Activar proyección 3D


#Función para ajustar la vista 3D
def setaxis(x1, x2, y1, y2, z1, z2):
    ax.set_xlim3d(x1, x2)  # Limite en X
    ax.set_ylim3d(y1, y2)  # Limite en Y
    ax.set_zlim3d(z1, z2)  # Limite en Z
    ax.view_init(elev=30, azim=40)  # Ajuste de elevación y ángulo de cámara


#Función para dibujar ejes fijos X, Y, Z
def fix_system(axis_length, linewidth=5):
    x = [-axis_length, axis_length]
    y = [-axis_length, axis_length]
    z = [-axis_length, axis_length]
    zp = [0, 0]  # Vector cero para dibujar líneas en los otros ejes

    # Dibujar ejes en colores
    ax.plot3D(x, zp, zp, color='red', linewidth=linewidth)   # Eje X
    ax.plot3D(zp, y, zp, color='blue', linewidth=linewidth)  # Eje Y
    ax.plot3D(zp, zp, z, color='green', linewidth=linewidth) # Eje Z


#Funciones trigonométricas en grados
def sind(t):
    return np.sin(t * np.pi / 180)  # Seno en grados

def cosd(t):
    return np.cos(t * np.pi / 180)  # Coseno en grados


#Matriz de rotación alrededor del eje Z
def RotZ(t):
    Rz = np.array([
        [cosd(t), -sind(t), 0],
        [sind(t),  cosd(t), 0],
        [0, 0, 1]
    ])
    return Rz


#Función para dibujar un vector entre dos puntos
def drawVector(p_fin, p_init=[0, 0, 0], color='black', linewidth=1):
    deltaX = [p_init[0], p_fin[0]]  # Componente X
    deltaY = [p_init[1], p_fin[1]]  # Componente Y
    deltaZ = [p_init[2], p_fin[2]]  # Componente Z
    ax.plot3D(deltaX, deltaY, deltaZ, color=color, linewidth=linewidth)  # Dibujar línea


#Función para dibujar la caja conectando sus 8 vértices
def drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color='black'):
    # Dibujar los vértices como puntos
    drawScatter(p1)
    drawScatter(p2)
    drawScatter(p3)
    drawScatter(p4)
    drawScatter(p5)
    drawScatter(p6)
    drawScatter(p7)
    drawScatter(p8)

    # Dibujar aristas de la caja conectando los vértices
    drawVector(p1, p2, color=color)
    drawVector(p2, p3, color=color)
    drawVector(p3, p4, color=color)
    drawVector(p4, p1, color=color)
    drawVector(p5, p6, color=color)
    drawVector(p6, p7, color=color)
    drawVector(p7, p8, color=color)
    drawVector(p8, p5, color=color)
    drawVector(p4, p8, color=color)
    drawVector(p1, p5, color=color)
    drawVector(p3, p7, color=color)
    drawVector(p2, p6, color=color)


#Función para dibujar un punto (vértice)
def drawScatter(point, color='black', marker='o'):
    ax.scatter(point[0], point[1], point[2], marker=marker, color=color)


#Animación de rotación fija alrededor del eje Z
def animate_rotation_Z(steps=36):
    """
    Rotación de la caja alrededor del eje Z sin desplazamiento.
    steps: número de pasos de la animación
    """
    # Definición de los puntos iniciales de la caja
    p1_init = np.array([0, 0, 0])
    p2_init = np.array([7, 0, 0])
    p3_init = np.array([7, 0, 3])
    p4_init = np.array([0, 0, 3])
    p5_init = np.array([0, 2, 0])
    p6_init = np.array([7, 2, 0])
    p7_init = np.array([7, 2, 3])
    p8_init = np.array([0, 2, 3])

    n = 0  # Contador de pasos
    while n <= steps:
        ax.cla()  # Limpiar todo para el nuevo fotograma

        # Dibujar ejes fijos
        setaxis(-10, 10, -10, 10, -10, 10)
        fix_system(10, 1)

        # Calcular matriz de rotación para el paso actual
        R = RotZ(n)

        # Aplicar rotación a cada vértice de la caja
        p1 = R.dot(p1_init)
        p2 = R.dot(p2_init)
        p3 = R.dot(p3_init)
        p4 = R.dot(p4_init)
        p5 = R.dot(p5_init)
        p6 = R.dot(p6_init)
        p7 = R.dot(p7_init)
        p8 = R.dot(p8_init)

        # Dibujar la caja rotada
        drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color='violet')

        n += 1  # Incrementar paso
        plt.draw()  # Dibujar el fotograma actual
        plt.pause(0.1)  # Pausa corta para efecto de animación


#Ejecutar la animación
animate_rotation_Z(steps=36)  # 36 pasos cubre 360° si cada paso equivale a 10°
plt.show()  # Mostrar ventana de la animación
