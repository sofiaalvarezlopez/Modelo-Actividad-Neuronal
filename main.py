# imports
from tkinter import *            
import tkinter as tk
from pathlib import Path
from matplotlib.backend_bases import key_press_handler
from tkinter import *               # wild card import para evitar llamar tk cada vez
from  tkinter import ttk

from tkinter import filedialog      # elegir archivos
from tkinter import messagebox      # mensaje de cerrar
import PIL.ImageTk 
import PIL.Image      # insersion de imagenes
import datetime as dt               # fecha para que la carpeta de datos tenga un nombre bonito
import struct as st
from pathlib import Path
from time import time
import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) # graficas y toolbar de graficas
# from Logica import *                # importo todos los metodos implementados en la logica



class Interfaz:
    ''' Clase que modela toda la interfaz del app, por comodidad y orden se define asi y se llama en la llave main al final del script
    '''
    def __init__(self, window):
        self.window = window # La ventana de la aplicacion
        self.directorio_actual = Path(__file__).parent
        # =================== Lista de ejecuciones de cada algoritmo para guardar ==========================
        # guardo tuplas de los listados de x y y de la ejecucion de cada algoritmo mientras no se limpie la grafica
        self.eForSet = []
        self.eBackSet = []
        self.eModSet = []
        self.RK2Set = []
        self.RK4Set = []
        self.scipySet = []
        # ======================================= PANEL SUPERIOR ===========================================
        self.panel_superior = Frame(self.window)
        titulo = Label(self.panel_superior, text="Modelo neuronal de Izhikevich") # Creo un label con el titulo.
        titulo.config(font =("Montserrat", 28)) # Configuro el tamanio y la fuente del titulo.
        titulo.grid(row=0, column=1, padx=400) # Pongo el titulo en el panel., text="Modelo neuronal de Izhikevich")
        # --- BOTON CERRAR ---
        cerrar_img = PIL.Image.open(self.directorio_actual.joinpath('assets/close.png').absolute()) # Abro la ruta de la imagen de cerrar
        cerrar_icon = PIL.ImageTk.PhotoImage(cerrar_img) # Creo una imagen de Pillow para el icono de cerrar
        self.boton_cerrar = Button(self.panel_superior, image=cerrar_icon, command=self.cerrar_aplicacion) # Creo el boton de cerrar
        self.boton_cerrar.image = cerrar_icon # Asigno la imagen al boton cerrar
        self.boton_cerrar.place(x=1170,y=0) #pack(side=RIGHT) # Coloco el boton cerrar 
        # --- BOTON EXPORTAR ---
        exportar_img = PIL.Image.open(self.directorio_actual.joinpath('assets/exportar.png').absolute()) # Abro la ruta de la imagen de exportar
        exportar_icon = PIL.ImageTk.PhotoImage(exportar_img) # Creo una imagen de Pillow para el icono de exportar
        self.boton_exportar = Button(self.panel_superior, image=exportar_icon, command=self.exportar) # Creo el boton de exportar
        self.boton_exportar.image = exportar_icon # Asigno la imagen al boton exportar
        self.boton_exportar.place(x=1140,y=0) #pack(side=RIGHT) # Coloco el boton exportar
        # --- BOTON IMPORTAR --- 
        importar_img = PIL.Image.open(self.directorio_actual.joinpath('assets/importar.png').absolute()) # Abro la ruta de la imagen de importar
        importar_icon = PIL.ImageTk.PhotoImage(importar_img) # Creo una imagen de Pillow para el icono de importar
        self.boton_importar = Button(self.panel_superior, image=importar_icon, command=self.importar) # Creo el boton de importar
        self.boton_importar.image = importar_icon # Asigno la imagen al boton importar
        self.boton_importar.place(x=1110,y=0) #pack(side=RIGHT) # Coloco el boton importar
        # --- EMPACAR EL PANEL ---
        self.panel_superior.pack(side=TOP,fill=X) # Empaco el panel
        # ======================================= PANEL IZQUIERDA ===========================================
        self.panel_izquierda = Frame(self.window, bd=5, width=600) # Creo un panel para almacenar todos los objetos de esta parte de la interfaz.
        # """""""""""""""""" PANEL GRAFICA """"""""""""""""""
        self.frame_plot = Frame(self.panel_izquierda, bd = 5, height=450, width=600) 
        self.fig = plt.Figure(figsize=(7.0, 4.0)) # figura principal
        self.plot = self.fig.add_subplot(1,1,1) # plto principal donde se dibujara todos los datos
        self.plot.set_xlabel(r'Tiempo (ms)')       # Título del eje x
        self.plot.set_ylabel(r'Voltaje (mV)')        # Título del eje y
        self.plot.grid(1) # Activo la grilla
        self.fig.tight_layout() # Para que todo se vea juntito y bonito
        self.imagen_grafica = FigureCanvasTkAgg(self.fig, master=self.panel_izquierda)  # canvas que dibujara la grafica en la interfaz
        self.imagen_grafica.get_tk_widget().place(x=48,y=0) # le asigno su posicion
    
        self.herramientas_grafica = NavigationToolbar2Tk(self.imagen_grafica, self.panel_izquierda, pack_toolbar=False) # creo la barra de herramientas que manipularan la grafica
        self.herramientas_grafica.update() # lo añado a la interfaz
        self.herramientas_grafica.place(x=64, y=300) # Lo ubico
        #  """""""""""""""""" PANEL OPCIONES """"""""""""""""""
        self.frame_opciones = Frame(self.panel_izquierda, bd = 5, height=250, width=600)
        self.frame_opciones.place(x=48, y=352)
        self.titulo_metodo_sol = Label(self.frame_opciones, text="Método solución:") # Creo un label con el titulo.
        self.titulo_metodo_sol.config(font =("Montserrat", 18)) # Configuro el tamanio y la fuente del titulo.
        self.titulo_metodo_sol.grid(row=1, column=1) # Pongo el titulo
        row = 2 # Inicializo una variable con la fila
        metodos_sol = ['Runge-Kutta 4', 'Euler Adelante', 'Euler Atrás', 'Euler Modificado'] # Creo un arreglo con los metodos de solucion
        self.diccionario_metodos = {}

        for metodo in metodos_sol: # Itero sobre todos los metodos de solucion
            self.var = IntVar()
            self.c = Checkbutton(self.frame_opciones, text=metodo, variable=self.var) # Creo cada checkbutton
            self.c.config(font=("Montserrat", 14)) # Configuro la fuente
            self.diccionario_metodos[metodo] = self.var
            self.c.grid(row=row, column=1, sticky='w') # Lo empaco
            row += 1 # Agrego uno a la fila para que me queden todos en columna.
        #  """""""""""""""""" PANEL VARIABLES """"""""""""""""""
        self.titulo_variables = Label(self.frame_opciones, text="Variables:") # Creo un label con el titulo.
        self.titulo_variables.config(font =("Montserrat", 18)) # Configuro el tamanio y la fuente del titulo.
        self.titulo_variables.grid(row=1, column=2, padx=16) # Pongo el titulo
        variables = ['V(t)', 'u(t)']
        self.diccionario_variables = {}
        row = 2
        for var in variables:
            self.is_checked = IntVar()
            self.c = Checkbutton(self.frame_opciones, text=var, variable=self.is_checked) # Creo cada checkbutton
            self.c.config(font=("Montserrat", 14)) # Configuro la fuente
            self.c.grid(row=row, column=2, sticky='w', padx=16, pady=4) # Lo empaco
            self.diccionario_variables[var] = self.is_checked
            row += 1 # Agrego uno a la fila para que me queden todos en columna.
        # """""""""""""""""" PANEL PARAMETROS """"""""""""""""""
        self.titulo_parametros = Label(self.frame_opciones, text="Parámetros:") # Creo un label con el titulo.
        self.titulo_parametros.config(font =("Montserrat", 18)) # Configuro el tamanio y la fuente del titulo.
        self.titulo_parametros.grid(row=row, column=2, padx=16) # Pongo el titulo
        pars = ['a', 'b', 'c', 'd'] # Creo una lista con los parametros de la ecuacion
        self.dict_parametros_valores = {} # Creo un diccionario vacio para guardar los parametros ingresados
        row += 1
        for p in pars: # Itero sobre todos los parametros
            self.label_parametro=Label(self.frame_opciones, text=p)
            self.label_parametro.config(font=("Montserrat", 14))
            self.label_parametro.grid(row=row, column=2, sticky='w', padx=16, pady=4)

            self.input_parametro=DoubleVar()
            self.box_input_parametro=Entry(self.frame_opciones,textvariable=self.input_parametro,width=16, bg='white', fg='grey')
            self.box_input_parametro.config(font=("Montserrat", 14))
            self.box_input_parametro.grid(row=row, column=2, sticky='w', padx=32, pady=4)
            self.box_input_parametro.focus_force()
            self.dict_parametros_valores[p] = self.input_parametro
            row += 1
        # """""""""""""""""" PANEL VALORES PREDEFINIDOS """"""""""""""""""
        self.titulo_valores_predefinidos = Label(self.frame_opciones, text="Valores predefinidos:") # Creo un label con el titulo.
        self.titulo_valores_predefinidos.config(font =("Montserrat", 18)) # Configuro el tamanio y la fuente d
        self.titulo_valores_predefinidos.grid(row=1, column=3) # Pongo el titulo
        vals_predefinidos = ["Regular spiking","Intrinsic bursting","Chattering","Fast spiking","Talamo-cortical","Resonador"]
        self.valorPredefinido = StringVar(self.frame_opciones)
        self.valorPredefinido.set(vals_predefinidos[0]) # Valor por default
        self.comboValorPredefinido = OptionMenu(self.frame_opciones, self.valorPredefinido, *vals_predefinidos)
        self.comboValorPredefinido.grid(row=2, column=3)

        # --- EMPACAR EL PANEL ---
        self.panel_izquierda.pack(side=LEFT,fill=Y) # Empaco el panel
        # ======================================= PANEL DERECHA ===========================================
        self.panel_derecha = Frame(self.window, bd=5, width=600) # Creo un panel para almacenar todos los objetos de esta parte de la interfaz.
        # """""""""""""""""" PANEL ESTIMULACION """"""""""""""""""
        self.frame_estimulacion = Frame(self.panel_derecha, bd = 5, height=450, width=600) # Creo el panel para la estimulacion (corriente)
        self.frame_estimulacion.place(x=0,y=0) # Ubico el panel de la estimulacion (corriete).
        self.titulo_estimulacion = Label(self.frame_estimulacion, text="Estimulación:") # Creo un label con el titulo.
        self.titulo_estimulacion.config(font =("Montserrat", 18)) # Configuro el tamanio y la fuente d
        self.titulo_estimulacion.grid(row=1, column=1) # Pongo el titulo
        # Label de la izquierda
        self.label_izq = Label(self.frame_estimulacion, text="-100 mA")
        self.label_izq.config(font =("Montserrat", 14)) # Configuro el tamanio y la fuente d
        self.label_izq.grid(row=2, column=1)
        # Control de la corriente
        self.corriente_elegida = DoubleVar()
        self.slider_estimulacion = Scale(self.frame_estimulacion, command=self.corriente_elegida, from_=-100, to=100, orient=HORIZONTAL, variable=self.corriente_elegida , length=400, resolution=0.5)
        self.slider_estimulacion.config(font =("Montserrat", 14))
        self.slider_estimulacion.grid(row=2, column=2)
        self.slider_estimulacion.focus()
        # Label de la derecha
        self.label_der = Label(self.frame_estimulacion, text="100 mA")
        self.label_der.config(font =("Montserrat", 14)) # Configuro el tamanio y la fuente d
        self.label_der.grid(row=2, column=3)
        # Label de abajo
        self.label_der = Label(self.frame_estimulacion, text="0 mA")
        self.label_der.config(font =("Montserrat", 14)) # Configuro el tamanio y la fuente d
        self.label_der.grid(row=3, column=2)
        # """""""""""""""""" PANEL TIEMPOS """"""""""""""""""
        self.frame_tiempos = Frame(self.panel_derecha, bd = 5, height=450, width=600) # Creo el panel de los tiempos 
        self.frame_tiempos.place(x=0,y=104)
        variables = ['Tiempo de simulación', 'Tiempo de inicio estimulación', 'Tiempo de fin estimulación', 'Valor de estimulación']
        unidades = ['ms']*3 + ['mA']
        self.diccionario_valores_tiempos = {}
        row = 1
        for i in range(len(variables)):
            self.state = 'readonly' if i == 3 else 'normal'
            self.label_tiempo = Label(self.frame_tiempos, text=variables[i])
            self.label_tiempo.config(font=("Montserrat", 14))
            self.label_tiempo.grid(row=row, column=1, sticky='w', padx=16, pady=4)

            self.input_parametro_tiempo=DoubleVar(None)
            self.box_input_parametro=Entry(self.frame_tiempos,textvariable=self.input_parametro_tiempo,width=16, bg='white', fg='grey', state=self.state)
            self.box_input_parametro.config(font=("Montserrat", 14))
            self.box_input_parametro.grid(row=row, column=2, sticky='w', padx=32, pady=4)
            self.box_input_parametro.focus_force()
            self.diccionario_valores_tiempos[variables[i]] = self.input_parametro_tiempo

            self.label = Label(self.frame_tiempos, text=unidades[i])
            self.label.config(font=("Montserrat", 14))
            self.label.grid(row=row, column=3, sticky='w', padx=16, pady=4)
            row += 1
        ### """""""""""""""""" PANEL CARGAR """"""""""""""""""
        self.frame_cargar = Frame(self.panel_derecha, bd = 5, height=450, width=600)
        self.frame_cargar.place(x=0,y=280)
        self.boton_cargar = Button(self.frame_cargar, text="Cargar", command=self.cargar_variables)
        self.boton_cargar.place(x=500, y=0)
        # --- EMPACAR EL PANEL ---
        self.panel_derecha.pack(side=RIGHT,fill=Y) # Empaco el panel



    # ======================================= FUNCIONES DE APOYO ===========================================
    ''' Funcion que es llamada al hacer click en el boton cerrar, pregunta si realmente se desea cerrar o retornar a la aplicacion
        '''
    def cerrar_aplicacion(self):
        # creo la caja de mensaje y su valor
        MsgBox =  messagebox.askquestion('Cerrar Aplicación','¿Está seguro que desea cerrar la aplicación?', icon = 'warning')
        # si el valor es yes entonces cierro la apliacion
        if MsgBox == 'yes':
            print('yes')
            self.window.destroy()     
            self.window.quit()
            # en caso contrario se notifica el retorono a la aplicacion
        else:
            messagebox.showinfo('Retornar','Será retornado a la aplicación')

    ''' Funcion que abre un dialogo para ingresar el nombre de un archivo para guardar el resultado de una ejecucion de algoritmo en formato double
    '''
    def exportar(self):
        ahora = time() # obtengo el timestamp actual
        fecha = dt.datetime.utcfromtimestamp(ahora).strftime("%Y-%m-%d_%H-%M-%S") # genero la fecha actual con el time stamp obtenido previamente
        nombre_carpeta = 'Datos_' + fecha # contruyo el nombre de la carpeta donde se guardaran los archivos con el nombre Datos_Fecha
        # pido el directorio donde se creara la carpeta en la que se guardaran los datos
        nombre_directorio = filedialog.askdirectory(parent = self.window,initialdir=self.directorio_actual,title="Directorio de guardado de datos") 
        # si el directorio es vacio quiere decir que se cerro la ventana sin escojer por lo que la funcion no hara nada y se retorna
        if nombre_directorio == '':
            return
        # si hay algo en el directorio se procede a crear una clase path con el parametro obtenido en el dialog para asi manejar de manera mas simple el path
        directorio_datos = Path(nombre_directorio)
        # se crea el path a la carpeta nueva con el nombre previamente generaro y se manda el comando al sistema para que la cree como carpeta
        carpetaDatos = directorio_datos.joinpath(str(nombre_carpeta))
        carpetaDatos.mkdir(parents=True, exist_ok=True)
        # TODO: Guardar los datos generados. Todavia no se realiza pues la interfaz es un esqueleto.
        # Se realizara en una funcion auxiliar. 
    

    ''' Funcion que abre un dialogo para seleccionar un archivo del cual se cargaran los datos de una ejecucion previa en formato double
    '''
    def importar(self):
        # pido el directorio donde se encuentran los datos previamente generados
        nombre_directorio = filedialog.askdirectory(parent = self.window,initialdir=self.directorio_actual,title="Directorio de datos generados")
        # si el directorio es vacio quiere decir que se cerro la ventana sin escojer por lo que la funcion no hara nada y se retorna
        if nombre_directorio == '':
            return
        # si hay algo en el directorio se procede a crear una clase path con el parametro obtenido en el dialog para asi manejar de manera mas simple el path
        directorio_datos = Path(nombre_directorio)
        # se llama a la funcion auxiliar que lee los archivos con la extencion y añade los datos a la grafica
        # TODO: Llamar a la funcion auxiliar para cargar los datos cuando ya los haya. La interfaz es un esqueleto entonces todavia no funciona.

    '''Funcion que carga las variables que actualmente tiene el usuario en la interfaz y muestra una tabla con ello'''
    def cargar_variables(self):
        # Metodos de solucion elegidos por el usuario
        self.diccionario_todos = {}
        for metodo in self.diccionario_metodos:
            self.diccionario_todos[metodo] = int(self.diccionario_metodos[metodo].get()) # Obtener los metodos seleccionados por el usuario
        # Variables
        for v in self.diccionario_variables:
            self.diccionario_todos[v] = int(self.diccionario_variables[v].get()) # Obtener las variables que el usuario tendra en cuenta
        # Parametros
        for p in self.dict_parametros_valores:
            self.diccionario_todos[p] = float(self.dict_parametros_valores[p].get())
        # Valor predefinido
        self.diccionario_todos['valor_predefinido_neurona'] = str(self.valorPredefinido.get()) # Obtener el valor predefinido de la neurona
        # Corriente elegida en el slider 
        self.diccionario_todos['corriente'] = float(self.corriente_elegida.get()) # Obtener el valor de la corriente 
        # Obtener los valores de los tiempos de simulacion
        lista = list(self.diccionario_valores_tiempos) # Obtengo los valores de tiempos
        for i in range(len(self.diccionario_valores_tiempos)):
            if i < len(self.diccionario_valores_tiempos) - 1: # Cualquiera de las labels de tiempo 
                self.diccionario_todos[lista[i]] = self.diccionario_valores_tiempos[lista[i]].get() # Obtengo el valor de los tiempos
            else:
                self.diccionario_valores_tiempos[lista[i]].set(self.diccionario_todos['corriente']) # Si es la text box de solo lectura (estimulacion), pongo el valor del slider. 
        # Crear la funcion I(t) de acuerdo a los parametros dados
        # Primero, obtengo los parametros de tiempo (inic) y corriente
        self.t_ini_est, self.t_fini_est, self.t_final = self.diccionario_todos['Tiempo de inicio estimulación'], self.diccionario_todos['Tiempo de fin estimulación'], self.diccionario_todos['Tiempo de simulación']
        self.I = self.diccionario_todos['corriente'] # Obtengo el valor de la corriente
        self.t_estimulacion = np.arange(self.t_ini_est, self.t_fini_est, 1) # Obtengo el tiempo de estimulacion
        self.t_antes_estimulacion = np.arange(0, self.t_ini_est, 1) # Obtengo el tiempo antes de la estimulacion
        self.t_despues_estimulacion = np.arange(self.t_fini_est, self.t_final, 1) # Obtengo el tiempo despues de la estimulacion
        normal = 0 # Indica si la estimulacion es en el rango de tiempo dado, no al inicio ni al final
        if 0 < self.t_ini_est < self.t_final and 0 < self.t_fini_est < self.t_final: # Si el tiempo de inicio y fin de la estimulacion esta en el rango
            I_t = [0]*len(self.t_antes_estimulacion) + [self.I]*len(self.t_estimulacion) + [0]*len(self.t_despues_estimulacion)   # Se ve como una funcion escalon
        elif float(self.t_ini_est) == float(0): # Si el tiempo de inicio de la estimulacion coincide con el de la simulacionn
            I_t = [self.I]*len(self.t_estimulacion) + [0]*len(self.t_despues_estimulacion) # Empieza estimulada, termina no estimulada
            normal = 1 # La estimulacion es al inicio
        elif float(0) == self.t_ini_est and self.t_fini_est == self.t_final:
            I_t = [self.I]*len(self.t_estimulacion)
            normal = 3 # La estimulacion dura toda la simulacion
        elif float(self.t_fini_est) == float(self.t_final): # Si el tiempo de fin de la estimulacion coincide con el final de la simulacion
            I_t = [0]*len(self.t_antes_estimulacion) + [self.I]*len(self.t_estimulacion) # Empieza no estimulada, termina estimulada
            normal = 2 # La estimulacion es al final
        else: # En el caso por defecto, asumo que no se quiere estimulacion sobre la neurona
            I_t = [0]*len(np.arange(0, self.t_final, 1)) # Dejo la corriente en 0
        self.diccionario_todos['I_t'] = I_t # Almaceno mi arreglo de corriente 
        # Crear la tablita con los datos ingresados
        total_filas = 3 if normal else 2 # Numero de filas
        total_columnas = 3 # Numero de columnas
        # Pongo el heading
        self.tabla = ttk.Treeview(self.frame_cargar)
        self.tabla['columns'] = ('T inicial (ms)', 'T final (ms)', 'Estimulación (mA)')
        self.tabla.column("#0", width=0,  stretch=NO)
        self.tabla.column('T inicial (ms)',anchor=CENTER, width=120)
        self.tabla.column('T final (ms)',anchor=CENTER, width=120)
        self.tabla.column('Estimulación (mA)',anchor=CENTER, width=120)

        self.tabla.heading("#0",text="",anchor=CENTER)
        self.tabla.heading('T inicial (ms)',text='T inicial (ms)', anchor=CENTER)
        self.tabla.heading('T final (ms)',text='T final (ms)', anchor=CENTER)
        self.tabla.heading('Estimulación (mA)',text='Estimulación (mA)', anchor=CENTER)
        """
        self.e = Text(self.frame_cargar, width=20, bg='gray', fg='white', font=('Montserrat',18))    # Vacia para dar espacio   
        self.e.grid(row=0, column=0)
        # Aqui empiezan las labels
        self.e = Text(self.frame_cargar, width=20, bg='gray', fg='white', font=('Montserrat',14))        
        self.e.grid(row=1, column=0)
        self.e.insert(END, 'T inicial (ms)') # Primero, tiempo inicial

        self.e = Text(self.frame_cargar, width=20, bg='gray', fg='white', font=('Montserrat',14))        
        self.e.grid(row=1, column=1)
        self.e.insert(END, 'T final (ms)') # Luego, tiempo final

        self.e = Text(self.frame_cargar, width=20, bg='gray', fg='white', font=('Montserrat',14))        
        self.e.grid(row=1, column=2)
        self.e.insert(END, 'Estimulación (mA)') # Por ultimo, estimulacion
        color_oscuro = True # Para intercalar colores
        """
        # Ahora, verifico si es normal la estimulacion o no y con ello, pongo los cuadritos de la tabla e inserto las filas
        if normal == 0: # La estimulacion ocurre en el rango dado, no al inicio ni al final
            self.tabla.insert(parent='',index='end',iid=0,text='',values=(0, self.t_ini_est, 0))
            self.tabla.insert(parent='',index='end',iid=1,text='',values=(self.t_ini_est, self.t_fini_est, self.I))
            self.tabla.insert(parent='',index='end',iid=2,text='',values=(self.t_fini_est, self.t_final, 0))
        elif normal == 1: # La estimulacion ocurre al inicio
            self.tabla.insert(parent='',index='end',iid=3,text='',values=(self.t_ini_est, self.t_fini_est, self.I))
            self.tabla.insert(parent='',index='end',iid=4,text='',values=(self.t_fini_est, self.t_final,0))
        elif normal == 2: # La estimulacion ocurre al final
            self.tabla.insert(parent='',index='end',iid=5,text='',values=(0, self.t_ini_est, 0))
            self.tabla.insert(parent='',index='end',iid=6,text='',values=(self.t_ini_est, self.t_final, self.I))
        else: # La estimulacion dura toda la simulacion
            self.tabla.insert(parent='',index='end',iid=7,text='',values=(self.t_ini_est, self.t_final, self.I))
        self.tabla.place(x=100, y=80)
        print(self.diccionario_todos)

        return self.diccionario_todos





    def iniciar(self):
        ''' Metodo que inicia la interfaz con el main loop, este metodo se define por tener orden en toda la clase y no hacer accesos externos al parametro de ventana
        '''
        self.window.mainloop()


"""Esta funcion retorna las dimensiones de la pantalla para centrar la ventana """
def obtener_dimensiones(window):
    window_width = window.winfo_reqwidth() # Obtener el ancho
    window_height = window.winfo_reqheight() # Obtener la altura

    posicion_derecha = int(window.winfo_screenwidth()/2 - window_width/2) # Obtener la mitad entre pantalla y ventana a la derecha
    posicion_abajo = int(window.winfo_screenheight()/2 - window_height/2) # Obtener la mitad entre pantalla y ventana a la izquierda

    return posicion_derecha, posicion_abajo

# Proceso que inicia la ventana y carga el app proceso que solo se llamara si se ejecuta este archivo y no si se lo importa

if __name__ == '__main__':
    directorioActual = Path(__file__).parent
    window = tk.Tk() # Inicializo la app.
    style = ttk.Style(window)
    # set ttk theme to "clam" which support the fieldbackground option
    #style.theme_use("clam")
    style.configure("Treeview", background="system", 
                fieldbackground="system")
    window.geometry("1200x700") # Inicializo el tamanio de la ventana.
    window.title("Proyecto final IBIO 2240: Modelo neuronal de Izhikevich")
    window.resizable(False, False) # Hace que no se pueda cambiar el tamanio de la ventana
    posicion_derecha, posicion_abajo = obtener_dimensiones(window) # Obtengo las dimensiones para centrar
    window.geometry("+{}+{}".format(posicion_derecha-500, posicion_abajo-250)) # Centro la ventana
    app = Interfaz(window) # Genero el objeto interfaz
    app.iniciar() # Corro la interfaz
    


