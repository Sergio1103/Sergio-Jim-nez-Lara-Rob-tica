import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# --- Funciones trigonométricas en grados ---
# Las funciones sind y cosd convierten los ángulos a radianes para usar con numpy
def sind(x): return np.sin(np.deg2rad(x))
def cosd(x): return np.cos(np.deg2rad(x))

# --- Matriz de transformación homogénea Denavit–Hartenberg ---
# Esta matriz representa la relación entre dos marcos consecutivos
def dh_matrix(theta, d, a, alpha):
    return np.array([
        [cosd(theta), -cosd(alpha)*sind(theta), sind(alpha)*sind(theta), a*cosd(theta)],
        [sind(theta),  cosd(alpha)*cosd(theta), -sind(alpha)*cosd(theta), a*sind(theta)],
        [0,            sind(alpha),              cosd(alpha),              d],
        [0,            0,                        0,                        1]
    ])

# --- Entrada de datos del usuario ---
print("=== ROBOT 2R tipo codo arriba (plano X–Z, rotación sobre eje Z) ===")
theta1 = float(input("Ángulo θ1 (grados): "))
theta2 = float(input("Ángulo θ2 (grados): "))
a1 = float(input("Longitud del brazo 1 (a1): "))
a2 = float(input("Longitud del brazo 2 (a2): "))

# Parámetros DH: el robot es plano, así que α = 0°, d = 0
alpha1 = 0
alpha2 = 0
d1 = 0
d2 = 0

# --- Calcular matrices DH ---
T01 = dh_matrix(theta1, d1, a1, alpha1)
T12 = dh_matrix(theta2, d2, a2, alpha2)
T02 = np.dot(T01, T12)

np.set_printoptions(precision=3, suppress=True)
print("\nMatriz T01 =\n", T01)
print("\nMatriz T12 =\n", T12)
print("\nMatriz T02 (total) =\n", T02)

# --- Cinemática directa: obtener coordenadas ---
def puntos(theta1, theta2):
    # Calcula las transformaciones DH para cada articulación
    T01 = dh_matrix(theta1, 0, a1, 0)
    T12 = dh_matrix(theta2, 0, a2, 0)
    T02 = np.dot(T01, T12)

    # Posiciones de cada articulación
    O0 = np.array([0, 0, 0])
    O1 = T01[0:3, 3]
    O2 = T02[0:3, 3]

    # Intercambio ejes para que el movimiento esté en el plano X–Z (de pie)
    # Aquí el eje Y se mantiene fijo y usamos Z como altura
    O0 = np.array([O0[0], 0, O0[1]])
    O1 = np.array([O1[0], 0, O1[1]])
    O2 = np.array([O2[0], 0, O2[1]])

    return np.column_stack((O0, O1, O2))

# --- Configuración del gráfico ---
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Limites del entorno donde se moverá el robot
ax.set_xlim(- (a1 + a2 + 2), a1 + a2 + 2)
ax.set_ylim(-5, 5)
ax.set_zlim(0, a1 + a2 + 5)

ax.set_xlabel("X (cm)")
ax.set_ylabel("Y (cm)")
ax.set_zlabel("Z (cm)")
ax.set_title("Cinemática matriz de hangover y denavit ")

# Ajusto la vista: azim=–90 muestra el plano X–Z desde un costado
ax.view_init(elev=20, azim=-90)

# Creo las líneas del brazo y el trazo del efector final
line, = ax.plot([], [], [], 'o-', lw=3, color='blue')
trace, = ax.plot([], [], [], 'r--', lw=1)
path_x, path_y, path_z = [], [], []

# --- Inicialización de la animación ---
def init():
    line.set_data([], [])
    line.set_3d_properties([])
    trace.set_data([], [])
    trace.set_3d_properties([])
    return line, trace

# --- Actualización de frames ---
def update(frame):
    t1, t2 = frame
    pts = puntos(t1, t2)
    x, y, z = pts
    line.set_data(x, y)
    line.set_3d_properties(z)
    path_x.append(x[2])
    path_y.append(y[2])
    path_z.append(z[2])
    trace.set_data(path_x, path_y)
    trace.set_3d_properties(path_z)
    return line, trace

# --- Frames de movimiento (rotación eje Z) ---
frames = []
for t1 in np.linspace(0, theta1, 60):
    frames.append([t1, 0])
for t2 in np.linspace(0, theta2, 60):
    frames.append([theta1, t2])

# --- Animación ---
ani = FuncAnimation(fig, update, frames=frames, init_func=init,
                    blit=True, interval=60, repeat=False)

plt.show()
