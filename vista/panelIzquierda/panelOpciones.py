from tkinter import *

def panel_opciones(frame_izquierda):
    frame_opciones = Frame(frame_izquierda, bd = 5, height=250, width=600)
    frame_opciones.place(x=48, y=352)
    checkboxes_metodo_solucion(frame_opciones)
    row_actual = variables(frame_opciones)
    parametros(frame_opciones, row_actual)
    valores_predefinidos(frame_opciones)


def checkboxes_metodo_solucion(frame):
    titulo_metodo_sol = Label(frame, text="Método solución:") # Creo un label con el titulo.
    titulo_metodo_sol.config(font =("Montserrat", 18)) # Configuro el tamanio y la fuente del titulo.
    titulo_metodo_sol.grid(row=1, column=1) # Pongo el titulo
    row = 2 # Inicializo una variable con la fila
    metodos_sol = ['Runge-Kutta 2', 'Runge-Kutta 4', 'Euler Adelante', 'Euler Atrás', 'Euler Modificado'] # Creo un arreglo con los metodos de solucion
    for metodo in metodos_sol: # Itero sobre todos los metodos de solucion
        c = Checkbutton(frame, text=metodo) # Creo cada checkbutton
        c.config(font=("Montserrat", 14)) # Configuro la fuente
        c.grid(row=row, column=1, sticky='w') # Lo empaco
        row += 1 # Agrego uno a la fila para que me queden todos en columna.

def variables(frame):
    titulo_variables = Label(frame, text="Variables:") # Creo un label con el titulo.
    titulo_variables.config(font =("Montserrat", 18)) # Configuro el tamanio y la fuente del titulo.
    titulo_variables.grid(row=1, column=2, padx=16) # Pongo el titulo
    variables = ['V(t)', 'u(t)']
    row = 2
    for var in variables:
        c = Checkbutton(frame, text=var) # Creo cada checkbutton
        c.config(font=("Montserrat", 14)) # Configuro la fuente
        c.grid(row=row, column=2, sticky='w', padx=16, pady=4) # Lo empaco
        row += 1 # Agrego uno a la fila para que me queden todos en columna.
    return row

def parametros(frame, row_actual):
    titulo_parametros = Label(frame, text="Parámetros:") # Creo un label con el titulo.
    titulo_parametros.config(font =("Montserrat", 18)) # Configuro el tamanio y la fuente del titulo.
    titulo_parametros.grid(row=row_actual, column=2, padx=16) # Pongo el titulo
    pars = ['a', 'b', 'c', 'd'] # Creo una lista con los parametros de la ecuacion
    dict_parametros_valores = {} # Creo un diccionario vacio para guardar los parametros ingresados
    row = row_actual + 1
    for p in pars: # Itero sobre todos los parametros
        label_parametro=Label(frame, text=p)
        label_parametro.config(font=("Montserrat", 14))
        label_parametro.grid(row=row, column=2, sticky='w', padx=16, pady=4)

        input_parametro=StringVar(None)
        box_input_parametro=Entry(frame,textvariable=input_parametro,width=16, bg='white', fg='grey')
        box_input_parametro.config(font=("Montserrat", 14))
        box_input_parametro.grid(row=row, column=2, sticky='w', padx=32, pady=4)
        box_input_parametro.focus_force()
        dict_parametros_valores[p] = input_parametro.get()
        row += 1
    return dict_parametros_valores

def valores_predefinidos(frame):
    titulo_valores_predefinidos = Label(frame, text="Valores predefinidos:") # Creo un label con el titulo.
    titulo_valores_predefinidos.config(font =("Montserrat", 18)) # Configuro el tamanio y la fuente d
    titulo_valores_predefinidos.grid(row=1, column=3) # Pongo el titulo
    vals_predefinidos = ["Regular spiking","Intrinsic bursting","Chattering","Fast spiking","Talamo-cortical","Resonador"]
    variable = StringVar(frame)
    variable.set(vals_predefinidos[0]) # Valor por default
    combo = OptionMenu(frame, variable, *vals_predefinidos)
    combo.grid(row=2, column=3)
    val_elegido = variable
    return val_elegido






