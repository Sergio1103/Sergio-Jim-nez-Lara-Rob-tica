# Importar librerías para gráficos 3D y cálculos numéricos
import matplotlib.pyplot as plt  # Librería principal de gráficos
from mpl_toolkits import mplot3d  # Herramientas 3D
import numpy as np  # Librería para cálculos numéricos


#Crear figura y ejes 3D
fig, ax = plt.subplots()  # Crear ventana de gráficos
ax = plt.axes(projection="3d")  # Activar proyección 3D


#Función para ajustar la vista 3D
def setaxis(x1, x2, y1, y2, z1, z2):
    ax.set_xlim3d(x1, x2)  # Establecer límite eje X
    ax.set_ylim3d(y1, y2)  # Establecer límite eje Y
    ax.set_zlim3d(z1, z2)  # Establecer límite eje Z
    ax.view_init(elev=30, azim=40)  # Ajustar ángulo de vista 3D


#Función para dibujar ejes fijos X, Y, Z
def fix_system(axis_length, linewidth=5):
    x = [-axis_length, axis_length]  # Límites eje X
    y = [-axis_length, axis_length]  # Límites eje Y
    z = [-axis_length, axis_length]  # Límites eje Z
    zp = [0, 0]  # Vector cero para dibujar líneas de los otros ejes

    ax.plot3D(x, zp, zp, color='red', linewidth=linewidth)   # Dibujar eje X en rojo
    ax.plot3D(zp, y, zp, color='blue', linewidth=linewidth)  # Dibujar eje Y en azul
    ax.plot3D(zp, zp, z, color='green', linewidth=linewidth) # Dibujar eje Z en verde


#Funciones trigonométricas en grados
def sind(t):
    return np.sin(t * np.pi / 180)  # Seno usando grados

def cosd(t):
    return np.cos(t * np.pi / 180)  # Coseno usando grados


#Matrices de rotación para X, Y y Z
def RotX(t):
    return np.array([  # Matriz 3x3 para rotación sobre X
        [1, 0, 0],
        [0, cosd(t), -sind(t)],
        [0, sind(t), cosd(t)]
    ])

def RotY(t):
    return np.array([  # Matriz 3x3 para rotación sobre Y
        [cosd(t), 0, sind(t)],
        [0, 1, 0],
        [-sind(t), 0, cosd(t)]
    ])

def RotZ(t):
    return np.array([  # Matriz 3x3 para rotación sobre Z
        [cosd(t), -sind(t), 0],
        [sind(t), cosd(t), 0],
        [0, 0, 1]
    ])


#Función para dibujar un vector entre dos puntos
def drawVector(p_fin, p_init=[0, 0, 0], color='black', linewidth=1):
    deltaX = [p_init[0], p_fin[0]]  # Diferencia X
    deltaY = [p_init[1], p_fin[1]]  # Diferencia Y
    deltaZ = [p_init[2], p_fin[2]]  # Diferencia Z
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


#Animación secuencial de rotación X -> Y -> Z
def animate_rotation_sequential(steps=10, pause_time=0.1):
    """
    Rotación secuencial de la caja:
    1) Rotación X
    2) Rotación Y sobre posición final de X
    3) Rotación Z sobre posición final de Y
    """
    # Definir puntos iniciales de la caja
    p1_init = np.array([0, 0, 0])
    p2_init = np.array([7, 0, 0])
    p3_init = np.array([7, 0, 3])
    p4_init = np.array([0, 0, 3])
    p5_init = np.array([0, 2, 0])
    p6_init = np.array([7, 2, 0])
    p7_init = np.array([7, 2, 3])
    p8_init = np.array([0, 2, 3])

    #Rotación sobre X
    for n in range(steps + 1):
        ax.cla()  # Limpiar fotograma anterior
        setaxis(-10, 10, -10, 10, -10, 10)  # Ajustar vista
        fix_system(10, 1)  # Dibujar ejes fijos

        R = RotX(n)  # Calcular matriz de rotación X paso a paso

        # Aplicar rotación X a cada vértice
        p1 = R.dot(p1_init)
        p2 = R.dot(p2_init)
        p3 = R.dot(p3_init)
        p4 = R.dot(p4_init)
        p5 = R.dot(p5_init)
        p6 = R.dot(p6_init)
        p7 = R.dot(p7_init)
        p8 = R.dot(p8_init)

        drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color='orange')  # Dibujar caja
        plt.draw()
        plt.pause(pause_time)  # Pausa para animación

    # Guardar posición final de X
    final_X = [p1, p2, p3, p4, p5, p6, p7, p8]

    #Rotación sobre Y
    for n in range(steps + 1):
        ax.cla()
        setaxis(-10, 10, -10, 10, -10, 10)
        fix_system(10, 1)

        R = RotY(n)  # Matriz de rotación Y paso a paso

        # Aplicar rotación Y sobre posición final de X
        p1 = R.dot(final_X[0])
        p2 = R.dot(final_X[1])
        p3 = R.dot(final_X[2])
        p4 = R.dot(final_X[3])
        p5 = R.dot(final_X[4])
        p6 = R.dot(final_X[5])
        p7 = R.dot(final_X[6])
        p8 = R.dot(final_X[7])

        drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color='purple')
        plt.draw()
        plt.pause(pause_time)

    # Guardar posición final de Y
    final_Y = [p1, p2, p3, p4, p5, p6, p7, p8]

    #Rotación sobre Z
    for n in range(steps + 1):
        ax.cla()
        setaxis(-10, 10, -10, 10, -10, 10)
        fix_system(10, 1)

        R = RotZ(n)  # Matriz de rotación Z paso a paso

        # Aplicar rotación Z sobre posición final de Y
        p1 = R.dot(final_Y[0])
        p2 = R.dot(final_Y[1])
        p3 = R.dot(final_Y[2])
        p4 = R.dot(final_Y[3])
        p5 = R.dot(final_Y[4])
        p6 = R.dot(final_Y[5])
        p7 = R.dot(final_Y[6])
        p8 = R.dot(final_Y[7])

        drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color='magenta')
        plt.draw()
        plt.pause(pause_time)


#Ejecutar animación secuencial
animate_rotation_sequential(steps=36, pause_time=0.5)  # Ejecutar rotación con pausa
plt.show()  # Mostrar ventana final
