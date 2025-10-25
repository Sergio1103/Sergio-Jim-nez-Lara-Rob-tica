"""
Este programa implementa LA CINEMÁTICA DIRECTA de un robot SCARA usando
matrices de Denavit–Hartenberg (DH), tal como se explica en los apuntes:

1) Se construyen matrices homogéneas DH por eslabón:
       T_i = Rz(theta_i) · Tz(d_i) · Tx(a_i) · Rx(alpha_i)

2) Se obtiene la pose de los puntos articulados mediante el producto matricial:
       T_0_2 = T_0_1 · T_1_2
       T_0_3 = T_0_2 · T_2_3
   (Esto corresponde a las operaciones M2, M3, ... que aparecen en los apuntes.)

3) El pistón se modela como un par RP (rotación Z + traslación en Z_local)
   respetando el mismo formalismo DH, SIN alterar estéticamente el dibujo.

4) ENTREGABLES DEL FK (cinemática directa):
   Se calculan las posiciones:
       p1 = origen de J1
       p2 = origen de J2 (este sube/baja en Z_local)
       base del pistón = p2 (nunca se despega)
       punta del pistón = p2 + Rz(theta3)*[0,0,322]
       círculo del platillo solidario a la punta

5) BASE_HEIGHT NO se mete en DH (como en el código inicial original),
   únicamente se Suma para el DIBUJO, manteniendo la estética del robot
   igual a la simulación previa para no alterar la apariencia visual.

Conclusión:
- La estructura matemática del código cumple con el método de DH de los apuntes.
- El dibujo respeta la estética y el comportamiento deseado (pistón toca siempre, no se alarga).
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# ------------------ Utilidades ------------------
def ask_float(prompt, default=None):
    while True:
        s = input(prompt).strip().replace(',', '.')
        if s == '' and default is not None:
            return float(default)
        try:
            return float(s)
        except ValueError:
            print("Valor inválido, intenta de nuevo.")

# ------------------ Bloque DH ------------------
def DH(theta_deg, d, a, alpha_deg=0.0):
    th = np.deg2rad(theta_deg)
    al = np.deg2rad(alpha_deg)
    c, s = np.cos(th), np.sin(th)
    ca, sa = np.cos(al), np.sin(al)
    return np.array([
        [ c, -s*ca,  s*sa, a*c],
        [ s,  c*ca, -c*sa, a*s],
        [ 0,    sa,    ca,   d],
        [ 0,     0,     0,   1]
    ], dtype=float)

# ------------------ Cinemática directa (con DH) ------------------
def fkine(theta1, theta2, l_barra_abs, theta3,
          A1, A2, BASE_HEIGHT, BRAZO_OFFSET_Z, R_PLATILLO):

    Lp = 322.0  # pistón fijo

    delta_z = float(l_barra_abs - BASE_HEIGHT)

    T01 = DH(theta1, 0.0, A1, 0.0)
    T12 = DH(theta2, BRAZO_OFFSET_Z + delta_z, A2, 0.0)
    T23_R = DH(theta3, 0.0, 0.0, 0.0)

    T02 = T01 @ T12
    T03 = T02 @ T23_R

    p_base = np.array([0,0,0])
    p_eje  = np.array([0,0,BASE_HEIGHT])

    p1 = (T01 @ np.array([0,0,BASE_HEIGHT,1]))[:3]
    p2 = (T02 @ np.array([0,0,BASE_HEIGHT,1]))[:3]

    p_piston_base = p2.copy()
    p_barra_top = (T03 @ np.array([0,0,BASE_HEIGHT+Lp,1]))[:3]

    t3 = np.deg2rad(theta3)
    angs = np.linspace(0,2*np.pi,60)

    circ_x = p_barra_top[0] + R_PLATILLO*np.cos(angs+t3)
    circ_y = p_barra_top[1] + R_PLATILLO*np.sin(angs+t3)
    circ_z = np.full_like(circ_x,p_barra_top[2])

    punto_x = p_barra_top[0] + R_PLATILLO*np.cos(t3)
    punto_y = p_barra_top[1] + R_PLATILLO*np.sin(t3)
    punto_z = p_barra_top[2]

    pmx,pmy,pmz = p_piston_base

    return (p_base, p_eje, p1, p2, p_barra_top,
            circ_x, circ_y, circ_z,
            punto_x, punto_y, punto_z,
            pmx, pmy, pmz)

# ------------------ Dibujo ------------------
def dibujar_robot(ax, p_base, p_eje, p1, p2, p_barra_top,
                  circ_x, circ_y, circ_z,
                  punto_x, punto_y, punto_z,
                  pmx, pmy, pmz, lim):

    ax.set_xlim(-lim,lim)
    ax.set_ylim(-lim,lim)
    ax.set_zlim(0,max(1600,lim))
    ax.set_xlabel('X (mm)'); ax.set_ylabel('Y (mm)'); ax.set_zlabel('Z (mm)')
    ax.set_title("SCARA i4-850H — θ1=30° fijo (DH + pistón rígido)")
    ax.set_facecolor('white')
    ax.view_init(elev=25,azim=45)

    ax.scatter(*p_base,color='red',s=60)
    ax.plot([p_base[0],p_eje[0]],[p_base[1],p_eje[1]],[p_base[2],p_eje[2]],color='red',linewidth=3)

    ax.plot([p_eje[0],p1[0]],[p_eje[1],p1[1]],[p_eje[2],p1[2]],color='blue',linewidth=5)

    p2_h = np.array([p2[0],p2[1],p1[2]])
    ax.plot([p1[0],p2_h[0]],[p1[1],p2_h[1]],[p1[2],p2_h[2]],color='cyan',linewidth=5)
    if abs(p2[2]-p2_h[2])>1e-6:
        ax.plot([p2_h[0],p2[0]],[p2_h[1],p2[1]],[p2_h[2],p2[2]],color='cyan',linewidth=1.5)

    ax.plot([pmx,p_barra_top[0]],[pmy,p_barra_top[1]],[pmz,p_barra_top[2]],color='orange',linewidth=4)

    ax.plot(circ_x,circ_y,circ_z,color='green',linewidth=3)
    ax.scatter(punto_x,punto_y,punto_z,color='red',s=40)
    ax.scatter(p1[0],p1[1],p1[2],color='black',s=18)
    ax.scatter(p2[0],p2[1],p2[2],color='black',s=18)

# ------------------ Animación ------------------
def animar_movimiento_unico(theta1_fixed,A1,A2,BAR_MIN,BAR_MAX,R_PLATILLO,BRAZO_OFFSET_Z,
                            frames=240,theta2_final=90.0,theta3_total=360.0):

    BASE_HEIGHT=776.0

    if BAR_MAX < BAR_MIN: BAR_MIN,BAR_MAX = BAR_MAX,BAR_MIN

    l_vals = np.linspace(BAR_MAX,BAR_MIN,frames)
    th2 = np.linspace(0,theta2_final,frames)
    th3 = np.linspace(0,theta3_total,frames)

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111,projection='3d')
    lim = max(1600,A1+A2+300)

    def update(i):
        ax.cla()
        (p_base,p_eje,p1,p2,p_top,
         cx,cy,cz,
         px,py,pz,
         pmx,pmy,pmz)=fkine(theta1_fixed,th2[i],l_vals[i],th3[i],
                             A1,A2,BASE_HEIGHT,BRAZO_OFFSET_Z,R_PLATILLO)
        dibujar_robot(ax,p_base,p_eje,p1,p2,p_top,
                      cx,cy,cz,px,py,pz,pmx,pmy,pmz,lim)
        return []

    ani = animation.FuncAnimation(fig,update,frames=frames,interval=40,
                                  blit=False,repeat=False)
    plt.show()

# ------------------ Main ------------------
if __name__=="__main__":
    theta1_fixed = 30.0   # <<--- AQUÍ SE FIJA θ1 = 30°
    A1 = ask_float("A1 [715]: ",715.0)
    A2 = ask_float("A2 [850]: ",850.0)
    BAR_MIN = ask_float("BAR_MIN [418.5]: ",418.5)
    BAR_MAX = ask_float("BAR_MAX [880.0]: ",880.0)
    R_PLATILLO = ask_float("R_PLATILLO [100.0]: ",100.0)
    BRAZO_OFFSET_Z = ask_float("BRAZO_OFFSET_Z [-40.0]: ",-40.0)

    frames = int(ask_float("Frames [240]: ",240))
    theta2_final = ask_float("θ2_final [90]: ",90.0)
    theta3_total = ask_float("θ3_total [360]: ",360.0)

    animar_movimiento_unico(theta1_fixed,A1,A2,BAR_MIN,BAR_MAX,
                             R_PLATILLO,BRAZO_OFFSET_Z,
                             frames=frames,theta2_final=theta2_final,theta3_total=theta3_total)
