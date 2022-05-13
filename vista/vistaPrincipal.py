import tkinter as tk
from tkinter import *
from turtle import window_width
from vista.panelIzquierda import panel_izquierda
from vista.panelSuperior import panel_superior
from vista.panelPlot import panel_plot

"""Esta funcion crea la ventana principal del programa."""
def ventana_principal(directorioActual):
    window = tk.Tk() # Inicializo la app.
    window.geometry("1200x700") # Inicializo el tamanio de la ventana.
    posicion_derecha, posicion_abajo = obtener_dimensiones(window) # Obtengo las dimensiones para centrar
    window.geometry("+{}+{}".format(posicion_derecha-500, posicion_abajo-250)) # Centro la ventana
    window.title("Proyecto Final - IBIO 2240") # Titulo de la ventana
    panel_superior(window, directorioActual) # Llamo a la funcion del panel superior y le paso por parametro la ventana
    panel_izquierda(window)
    window.mainloop()

"""Esta funcion retorna las dimensiones de la pantalla para centrar la ventana """
def obtener_dimensiones(window):
    window_width = window.winfo_reqwidth() # Obtener el ancho
    window_height = window.winfo_reqheight() # Obtener la altura

    posicion_derecha = int(window.winfo_screenwidth()/2 - window_width/2) # Obtener la mitad entre pantalla y ventana a la derecha
    posicion_abajo = int(window.winfo_screenheight()/2 - window_height/2) # Obtener la mitad entre pantalla y ventana a la izquierda

    return posicion_derecha, posicion_abajo

    
