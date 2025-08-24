# Importar librerías necesarias para gráficos 3D y cálculos numéricos
import matplotlib.pyplot as plt  # Librería principal para gráficos
from mpl_toolkits import mplot3d  # Herramientas para gráficos 3D
import numpy as np  # Librería para cálculos matemáticos y matrices

#Crear figura y ejes 3D
fig, ax = plt.subplots()  # Crear ventana de gráficos
ax = plt.axes(projection="3d")  # Activar proyección 3D para dibujar objetos en 3D

#Función para ajustar la vista 3D
def setaxis(x1, x2, y1, y2, z1, z2):
    ax.set_xlim3d(x1, x2)  # Establecer límite eje X
    ax.set_ylim3d(y1, y2)  # Establecer límite eje Y
    ax.set_zlim3d(z1, z2)  # Establecer límite eje Z
    ax.view_init(elev=30, azim=40)  # Ajustar elevación y ángulo de cámara

#Función para dibujar ejes fijos X, Y, Z
def fix_system(axis_length, linewidth=5):
    x = [-axis_length, axis_length]  # Definir línea eje X
    y = [-axis_length, axis_length]  # Definir línea eje Y
    z = [-axis_length, axis_length]  # Definir línea eje Z
    zp = [0, 0]  # Vector cero para dibujar líneas de los otros ejes
    ax.plot3D(x, zp, zp, color='red', linewidth=linewidth)   # Dibujar eje X en rojo
    ax.plot3D(zp, y, zp, color='blue', linewidth=linewidth)  # Dibujar eje Y en azul
    ax.plot3D(zp, zp, z, color='green', linewidth=linewidth) # Dibujar eje Z en verde

#Funciones trigonométricas en grados
def sind(t):
    return np.sin(t * np.pi / 180)  # Calcular seno de ángulo en grados

def cosd(t):
    return np.cos(t * np.pi / 180)  # Calcular coseno de ángulo en grados

#Matrices de rotación para X, Y y Z
def RotX(t):
    return np.array([  # Retorna matriz de rotación 3x3 sobre X
        [1, 0, 0],
        [0, cosd(t), -sind(t)],
        [0, sind(t), cosd(t)]
    ])

def RotY(t):
    return np.array([  # Retorna matriz de rotación 3x3 sobre Y
        [cosd(t), 0, sind(t)],
        [0, 1, 0],
        [-sind(t), 0, cosd(t)]
    ])

def RotZ(t):
    return np.array([  # Retorna matriz de rotación 3x3 sobre Z
        [cosd(t), -sind(t), 0],
        [sind(t), cosd(t), 0],
        [0, 0, 1]
    ])

#Función para dibujar un vector entre dos puntos
def drawVector(p_fin, p_init=[0, 0, 0], color='black', linewidth=1):
    deltaX = [p_init[0], p_fin[0]]  # Coordenadas X desde inicio hasta fin
    deltaY = [p_init[1], p_fin[1]]  # Coordenadas Y desde inicio hasta fin
    deltaZ = [p_init[2], p_fin[2]]  # Coordenadas Z desde inicio hasta fin
    ax.plot3D(deltaX, deltaY, deltaZ, color=color, linewidth=linewidth)  # Dibujar línea 3D

#Función para dibujar la caja conectando sus 8 vértices
def drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color='black'):
    drawScatter(p1)  # Dibujar vértice 1
    drawScatter(p2)  # Dibujar vértice 2
    drawScatter(p3)  # Dibujar vértice 3
    drawScatter(p4)  # Dibujar vértice 4
    drawScatter(p5)  # Dibujar vértice 5
    drawScatter(p6)  # Dibujar vértice 6
    drawScatter(p7)  # Dibujar vértice 7
    drawScatter(p8)  # Dibujar vértice 8

    drawVector(p1, p2, color=color)  # Dibujar arista 1-2
    drawVector(p2, p3, color=color)  # Dibujar arista 2-3
    drawVector(p3, p4, color=color)  # Dibujar arista 3-4
    drawVector(p4, p1, color=color)  # Dibujar arista 4-1
    drawVector(p5, p6, color=color)  # Dibujar arista 5-6
    drawVector(p6, p7, color=color)  # Dibujar arista 6-7
    drawVector(p7, p8, color=color)  # Dibujar arista 7-8
    drawVector(p8, p5, color=color)  # Dibujar arista 8-5
    drawVector(p4, p8, color=color)  # Dibujar arista 4-8
    drawVector(p1, p5, color=color)  # Dibujar arista 1-5
    drawVector(p3, p7, color=color)  # Dibujar arista 3-7
    drawVector(p2, p6, color=color)  # Dibujar arista 2-6

#Función para dibujar un punto (vértice)
def drawScatter(point, color='black', marker='o'):
    ax.scatter(point[0], point[1], point[2], marker=marker, color=color)  # Dibujar punto 3D

#Animación fluida rotación secuencial X->Y->Z
def animate_rotation_fluida(total_steps=100, pause_time=0.03):
    """
    Animación fluida:
    - Rotación X, Y y Z combinada
    - Cada fotograma interpola ángulos de 0 hasta valor final
    """
    # Puntos iniciales de la caja
    p1_init = np.array([0, 0, 0])
    p2_init = np.array([7, 0, 0])
    p3_init = np.array([7, 0, 3])
    p4_init = np.array([0, 0, 3])
    p5_init = np.array([0, 2, 0])
    p6_init = np.array([7, 2, 0])
    p7_init = np.array([7, 2, 3])
    p8_init = np.array([0, 2, 3])

    # Definir ángulos finales de cada eje
    final_angle_X = 90  # Rotación X final
    final_angle_Y = 90  # Rotación Y final
    final_angle_Z = 90  # Rotación Z final

    # Bucle principal para animación fluida
    for step in range(total_steps + 1):
        ax.cla()  # Limpiar fotograma anterior
        setaxis(-10, 10, -10, 10, -10, 10)  # Ajustar vista
        fix_system(10, 1)  # Dibujar ejes fijos

        # Interpolación de ángulos para animación fluida
        angle_X = final_angle_X * step / total_steps
        angle_Y = final_angle_Y * step / total_steps
        angle_Z = final_angle_Z * step / total_steps

        # Matriz de rotación combinada: X -> Y -> Z
        R = RotX(angle_X) @ RotY(angle_Y) @ RotZ(angle_Z)

        # Aplicar rotación a todos los vértices de la caja
        p1 = R.dot(p1_init)
        p2 = R.dot(p2_init)
        p3 = R.dot(p3_init)
        p4 = R.dot(p4_init)
        p5 = R.dot(p5_init)
        p6 = R.dot(p6_init)
        p7 = R.dot(p7_init)
        p8 = R.dot(p8_init)

        drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color='magenta')  # Dibujar caja rotada

        plt.draw()  # Dibujar fotograma actual
        plt.pause(pause_time)  # Pausa corta para animación fluida

#Ejecutar animación fluida
animate_rotation_fluida(total_steps=100, pause_time=0.03)  # Llamada a función de animación
plt.show()  # Mostrar ventana final con animación completa
