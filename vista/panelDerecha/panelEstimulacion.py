
from tkinter import *


def panel_estimulacion(frame_derecha):        
    frame_plot = Frame(frame_derecha, bd = 5, height=450, width=600)
    frame_plot.place(x=0,y=0)
    corriente_elegida = control_corriente(frame_plot)
    return corriente_elegida

def control_corriente(frame):
    titulo_estimulacion = Label(frame, text="Estimulación:") # Creo un label con el titulo.
    titulo_estimulacion.config(font =("Montserrat", 18)) # Configuro el tamanio y la fuente d
    titulo_estimulacion.grid(row=1, column=1) # Pongo el titulo
    # Label de la izquierda
    label_izq = Label(frame, text="-100 mA")
    label_izq.config(font =("Montserrat", 14)) # Configuro el tamanio y la fuente d
    label_izq.grid(row=2, column=1)
    # Control de la corriente
    corriente_elegida = DoubleVar()
    slider_estimulacion = Scale(frame, command=corriente_elegida, from_=-100, to=100, orient=HORIZONTAL, length=400, resolution=0.5)
    slider_estimulacion.config(font =("Montserrat", 14))
    slider_estimulacion.grid(row=2, column=2)
    slider_estimulacion.focus()
    # Label de la derecha
    label_der = Label(frame, text="100 mA")
    label_der.config(font =("Montserrat", 14)) # Configuro el tamanio y la fuente d
    label_der.grid(row=2, column=3)
    # Label de abajo
    label_der = Label(frame, text="0 mA")
    label_der.config(font =("Montserrat", 14)) # Configuro el tamanio y la fuente d
    label_der.grid(row=3, column=2)
    return corriente_elegida


