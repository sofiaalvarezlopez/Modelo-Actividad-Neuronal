
from tkinter import *

from numpy import var

def panel_tiempos(frame_derecha, corriente_elegida):        
    frame_tiempos = Frame(frame_derecha, bd = 5, height=450, width=600)
    frame_tiempos.place(x=0,y=104)
    tiempos_simulacion_estimulacion(frame_tiempos, corriente_elegida)


def tiempos_simulacion_estimulacion(frame, corriente_elegida):
    variables = ['Tiempo de simulación', 'Tiempo de inicio estimulación', 'Tiempo de fin estimulación', 'Valor de estimulación']
    unidades = ['ms']*3 + ['mA']
    diccionario_valores = {}
    row = 1
    for i in range(len(variables)):
        state = 'readonly' if i == 3 else 'normal'
        label = Label(frame, text=variables[i])
        label.config(font=("Montserrat", 14))
        label.grid(row=row, column=1, sticky='w', padx=16, pady=4)

        input_parametro=DoubleVar(None)
        box_input_parametro=Entry(frame,textvariable=input_parametro,width=16, bg='white', fg='grey', state=state)
        box_input_parametro.config(font=("Montserrat", 14))
        box_input_parametro.grid(row=row, column=2, sticky='w', padx=32, pady=4)
        box_input_parametro.focus_force()
        diccionario_valores[variables[i]] = input_parametro

        label = Label(frame, text=unidades[i])
        label.config(font=("Montserrat", 14))
        label.grid(row=row, column=3, sticky='w', padx=16, pady=4)
        row += 1



    


