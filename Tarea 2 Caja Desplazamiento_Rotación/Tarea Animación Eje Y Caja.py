# Import libraries and packages
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

# create the fig and ax objects to handle figure and axes of the fixed frame
fig,ax = plt.subplots()

# Use 3d view 
ax = plt.axes(projection = "3d")


def setaxis(x1, x2, y1, y2, z1, z2):
    # Ajusta los límites de la vista 3D
    ax.set_xlim3d(x1,x2)
    ax.set_ylim3d(y1,y2)
    ax.set_zlim3d(z1,z2)
    ax.view_init(elev=30, azim=40)


def fix_system(axis_length, linewidth=5):
    # Dibuja los ejes coordenados fijos (X en rojo, Y en azul, Z en verde)
    x = [-axis_length, axis_length]
    y = [-axis_length, axis_length] 
    z = [-axis_length, axis_length]
    zp = [0, 0]
    ax.plot3D(x, zp, zp, color='red', linewidth=linewidth)
    ax.plot3D(zp, y, zp, color='blue',linewidth=linewidth)
    ax.plot3D(zp, zp, z, color='green',linewidth=linewidth)
    

def sind(t):
    # seno en grados
    res = np.sin(t*np.pi/180)
    return res

def cosd(t):
    # coseno en grados
    res = np.cos(t*np.pi/180)
    return res


def RotZ(t):
    # matriz de rotación alrededor del eje Z
    Rz = np.array(([cosd(t),-sind(t),0],
                   [sind(t), cosd(t),0],
                   [0,0,1]))
    return Rz

def drawVector(p_fin, p_init=[0,0,0], color='black',linewidth=1):
    # Dibuja un vector entre dos puntos 3D
    deltaX = [p_init[0], p_fin[0]]
    deltaY = [p_init[1], p_fin[1]]
    deltaZ = [p_init[2], p_fin[2]]
    ax.plot3D(deltaX, deltaY, deltaZ,color=color, linewidth=linewidth)


def drawBox(p1, p2, p3, p4, p5, p6, p7, p8, color = 'black'):
    # Dibuja la caja conectando sus 8 vértices
    drawScatter(p1) 
    drawScatter(p2)
    drawScatter(p3)
    drawScatter(p4)
    drawScatter(p5)
    drawScatter(p6)
    drawScatter(p7)
    drawScatter(p8)

    drawVector(p1,p2,color = color)
    drawVector(p2,p3,color = color)
    drawVector(p3,p4,color = color)
    drawVector(p4,p1,color = color)
    drawVector(p5,p6,color = color)
    drawVector(p6,p7,color = color)
    drawVector(p7,p8,color = color)
    drawVector(p8,p5,color = color)
    drawVector(p4,p8,color = color)
    drawVector(p1,p5,color = color)
    drawVector(p3,p7,color = color)
    drawVector(p2,p6,color = color)


def drawScatter(point,color='black',marker='o'):
    # Dibuja un punto en 3D
    ax.scatter(point[0],point[1],point[2],marker='o')


# Animación del desplazamiento en Y
def animate_shift_Y(steps=20, shift=10):
    """
    Esta función anima el desplazamiento de la caja en el eje Y.
    steps → número de pasos de la animación (controla suavidad/velocidad).
    shift → cuánto se mueve en total la caja en Y.
    """

    # Definición de los puntos iniciales de la caja (posición de arranque en el origen)
    p1_init = np.array([0,0,0])
    p2_init = np.array([7,0,0])
    p3_init = np.array([7,0,3])
    p4_init = np.array([0,0,3])
    p5_init = np.array([0,2,0])
    p6_init = np.array([7,2,0])
    p7_init = np.array([7,2,3])
    p8_init = np.array([0,2,3])

    n = 0
    while n <= steps:
        ax.cla()  # Limpia la gráfica en cada paso (borrando la posición anterior de la caja)

        # Ejes y cámara
        setaxis(-5,20,-5,20,-5,20)
        fix_system(10,1)

        # Desplazamiento proporcional en Y
        # (shift/steps) es cuánto avanza la caja por cada paso
        dy = (shift/steps)*n

        # Aplicar desplazamiento a cada punto de la caja en Y
        p1 = p1_init + [0,dy,0]
        p2 = p2_init + [0,dy,0]
        p3 = p3_init + [0,dy,0]
        p4 = p4_init + [0,dy,0]
        p5 = p5_init + [0,dy,0]
        p6 = p6_init + [0,dy,0]
        p7 = p7_init + [0,dy,0]
        p8 = p8_init + [0,dy,0]

        # Dibuja la caja en su nueva posición desplazada en Y
        drawBox(p1,p2,p3,p4,p5,p6,p7,p8,color='red')

        # Aumenta el contador y dibuja
        n += 1
        plt.draw()
        plt.pause(0.1) # pausa pequeña → da el efecto de movimiento


# Ejecuta la animación: 
# la caja se moverá 15 unidades en Y en 30 pasos
animate_shift_Y(steps=30, shift=15)

plt.show()
