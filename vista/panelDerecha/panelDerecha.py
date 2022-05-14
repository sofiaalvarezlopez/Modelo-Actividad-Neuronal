from tkinter import *
from vista.panelDerecha.panelEstimulacion import panel_estimulacion
from vista.panelDerecha.panelTiempos import panel_tiempos


"""Este panel contiene todos los elementos del panel de la derecha """
def panel_derecha(window):
    panel = Frame(window, bd=5, width=600) # Creo un panel para almacenar todos los objetos de esta parte de la interfaz.
    corriente_elegida = panel_estimulacion(panel)
    panel_tiempos(panel, corriente_elegida)
    panel.pack(side=RIGHT,fill=Y) # Empaco el panel