import matplotlib
import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) # graficas y toolbar de graficas


matplotlib.use("TkAgg")
#plt.style.use('bmh')


def panel_plot(frame_izquierda):        
    frame_plot = Frame(frame_izquierda, bd=5, width=600)
    plot(frame_plot)
    frame_plot.pack(side=LEFT, fill=Y)                                                        
    

    # boton que se encargara de limpiar las ejecuciones de algoritmos en la grafica
    #limpiar_btn = Button(master=panel, text="Clean data",  command = limpiar_grafica)#, bg=self.color_3, fg = self.color_blanco,  width=20, height=1, font=self.fuente_ppal,border="0")
    #limpiar_btn.place(x=350,y=410)

def plot(frame_izquierda):
    fig = plt.Figure(figsize=(5.75, 4.0)) # figura principal
    plot = fig.add_subplot(1,1,1) # plto principal donde se dibujara todos los datos
    plot.set_xlabel(r'Tiempo (ms)')       # Título del eje x
    plot.set_ylabel(r'Voltaje (mV)')        # Título del eje y
    plot.grid(1) # Activo la grilla
    fig.tight_layout() # Para que todo se vea juntito y bonito
    imagen_grafica = FigureCanvasTkAgg(fig, master=frame_izquierda)  # canvas que dibujara la grafica en la interfaz
    imagen_grafica.get_tk_widget().place(x=64,y=0) # le asigno su posicion
    
    herramientas_grafica = NavigationToolbar2Tk(imagen_grafica, frame_izquierda, pack_toolbar=False) # creo la barra de herramientas que manipularan la grafica
    herramientas_grafica.update()                                                                           # lo añada a la interfaz
    herramientas_grafica.place(x=64, y=300)