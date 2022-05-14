from tkinter import *
from vista.panelIzquierda.panelPlot import panel_plot
from vista.panelIzquierda.panelOpciones import panel_opciones


"""Este panel contiene todos los elementos de """
def panel_izquierda(window):
    panel = Frame(window, bd=5, width=600) # Creo un panel para almacenar todos los objetos de esta parte de la interfaz.
    panel_plot(panel) # Pongo el menu del plot
    panel_opciones(panel)
    panel.pack(side=LEFT,fill=Y) # Empaco el panel