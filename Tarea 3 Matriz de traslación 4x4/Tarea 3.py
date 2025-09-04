# Importar librerías necesarias
import matplotlib.pyplot as plt  # Librería principal para gráficos
from mpl_toolkits import mplot3d  # Herramientas para gráficos 3D
import numpy as np  # Librería para cálculos matemáticos y matrices

# Crear figura y ejes 3D
fig, ax = plt.subplots()              # Crear ventana de gráficos
ax = plt.axes(projection="3d")       # Activar proyección 3D para dibujar objetos en 3D

# Funciones auxiliares

# Ajustar la vista de la gráfica 3D
def setaxis(x1, x2, y1, y2, z1, z2):
    ax.set_xlim3d(x1, x2)  # Límite eje X
    ax.set_ylim3d(y1, y2)  # Límite eje Y
    ax.set_zlim3d(z1, z2)  # Límite eje Z
    ax.view_init(elev=30, azim=40)  # Vista inclinada de la cámara

# Dibujar ejes fijos X, Y, Z
def fix_system(axis_length, linewidth=5):
    x = [-axis_length, axis_length]
    y = [-axis_length, axis_length]
    z = [-axis_length, axis_length]
    zp = [0, 0]
    ax.plot3D(x, zp, zp, color='red', linewidth=linewidth)    # Eje X rojo
    ax.plot3D(zp, y, zp, color='blue', linewidth=linewidth)   # Eje Y azul
    ax.plot3D(zp, zp, z, color='green', linewidth=linewidth)  # Eje Z verde

# Funciones trigonométricas en grados
def sind(t):
    return np.sin(t * np.pi / 180)

def cosd(t):
    return np.cos(t * np.pi / 180)

# Conversión entre coordenadas normales y homogéneas

def to_homogeneous(p):
    """Convierte un punto [x,y,z] en homogéneo [x,y,z,1]"""
    return np.append(p, 1)

def from_homogeneous(p):
    """Convierte un punto homogéneo [x,y,z,1] a coordenada normal [x,y,z]"""
    return p[:3] / p[3]

# Matrices de transformación homogénea 4x4

def RotZ_4x4(t):
    """Matriz de rotación homogénea 4x4 alrededor de Z"""
    return np.array([
        [cosd(t), -sind(t), 0, 0],
        [sind(t),  cosd(t), 0, 0],
        [0,        0,       1, 0],
        [0,        0,       0, 1]
    ])

def TransZ(dz):
    """Matriz de traslación homogénea 4x4 sobre Z"""
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])

# Funciones de dibujo

# Dibujar un vector entre dos puntos
def drawVector(p_fin, p_init=[0, 0, 0], color='black', linewidth=1):
    deltaX = [p_init[0], p_fin[0]]
    deltaY = [p_init[1], p_fin[1]]
    deltaZ = [p_init[2], p_fin[2]]
    ax.plot3D(deltaX, deltaY, deltaZ, color=color, linewidth=linewidth)

# Dibujar un punto (vértice)
def drawScatter(point, color='black', marker='o'):
    ax.scatter(point[0], point[1], point[2], marker=marker, color=color)

# Dibujar la caja conectando sus 8 vértices
def drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color='black'):
    # Dibujar vértices
    for p in [p1, p2, p3, p4, p5, p6, p7, p8]:
        drawScatter(p)

    # Dibujar aristas
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

# Animación: rotación + traslación en eje Z

def animate_rotation_translation(total_steps=100, pause_time=0.03):
    """
    Animación de una caja:
    - Se rota alrededor del eje Z
    - Se traslada en el mismo eje Z
    """

    # Definición de vértices iniciales de la caja
    p1_init = np.array([0, 0, 0])
    p2_init = np.array([7, 0, 0])
    p3_init = np.array([7, 0, 3])
    p4_init = np.array([0, 0, 3])
    p5_init = np.array([0, 2, 0])
    p6_init = np.array([7, 2, 0])
    p7_init = np.array([7, 2, 3])
    p8_init = np.array([0, 2, 3])

    # Ángulo final de rotación en Z
    final_angle_Z = 360  # Una vuelta completa

    # Desplazamiento máximo en Z
    max_translation_Z = 5

    # Bucle principal de animación
    for step in range(total_steps + 1):
        ax.cla()  # Limpiar fotograma anterior
        setaxis(-10, 10, -10, 10, -5, 15)  # Ajustar límites de los ejes
        fix_system(10, 1)  # Dibujar sistema fijo XYZ

        # Calcular ángulo y desplazamiento actuales
        angle_Z = final_angle_Z * step / total_steps
        dz = max_translation_Z * step / total_steps

        # Matriz de transformación: primero rotación, luego traslación
        T = np.dot(TransZ(dz), RotZ_4x4(angle_Z))

        # Transformar cada vértice (homogéneo -> aplicar T -> normal)
        p1 = from_homogeneous(np.dot(T, to_homogeneous(p1_init)))
        p2 = from_homogeneous(np.dot(T, to_homogeneous(p2_init)))
        p3 = from_homogeneous(np.dot(T, to_homogeneous(p3_init)))
        p4 = from_homogeneous(np.dot(T, to_homogeneous(p4_init)))
        p5 = from_homogeneous(np.dot(T, to_homogeneous(p5_init)))
        p6 = from_homogeneous(np.dot(T, to_homogeneous(p6_init)))
        p7 = from_homogeneous(np.dot(T, to_homogeneous(p7_init)))
        p8 = from_homogeneous(np.dot(T, to_homogeneous(p8_init)))

        # Dibujar caja transformada
        drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color='magenta')

        # Actualizar gráfico
        plt.draw()
        plt.pause(pause_time)

# Ejecutar animación

animate_rotation_translation(total_steps=100, pause_time=0.03)
plt.show()
