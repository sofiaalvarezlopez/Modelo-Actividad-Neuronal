# imports
from tkinter import *            
import tkinter as tk
from pathlib import Path
from matplotlib.backend_bases import key_press_handler
from tkinter import *               # wild card import para evitar llamar tk cada vez
from  tkinter import ttk
from logica import *

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
        self.eForSetV = []
        self.eForSetU = []
        self.eBackSetV = []
        self.eBackSetU = []
        self.eModSetV = []
        self.eModSetU = []
        self.RK2SetV = []
        self.RK2SetU = []
        self.RK4SetV = []
        self.RK4SetU = []
        # Colores definidos para las graficas
        self.color_efor = 'red'
        self.color_eback = '#fbb901'
        self.color_emod = 'darkgreen'
        self.color_rk2 = 'blue'
        self.color_rk4 = 'purple'

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
        metodos_sol = ['Runge-Kutta 2','Runge-Kutta 4', 'Euler Adelante', 'Euler Atrás', 'Euler Modificado'] # Creo un arreglo con los metodos de solucion
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
        self.comboValorPredefinido = OptionMenu(self.frame_opciones, self.valorPredefinido, *vals_predefinidos, command=self.actualizar)
        self.comboValorPredefinido.grid(row=2, column=3)
        # Poner como valores predefinidos los de las constantes
        self.actualizar(self.valorPredefinido)

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
        self.boton_limpiar = Button(master=self.frame_cargar, text="Limpiar gráfica",  command = self.limpiar_grafica)
        self.boton_limpiar.place(x=350, y=0)


        # --- EMPACAR EL PANEL ---
        self.panel_derecha.pack(side=RIGHT,fill=Y) # Empaco el panel
        # Mensaje de bienvenida
        messagebox.showinfo('¡Bienvenido!','Este proyecto, de la clase IBIO 2240, pretende modelar la actividad neuronal')

    # ======================================= FUNCIONES DE APOYO ===========================================
    """Funcion que actualiza los parametros de a,b,c,d basado en la neurona elegida"""
    def actualizar(self, eleccion):
        if eleccion == "Regular spiking":
            self.dict_parametros_valores['a'].set(0.02)
            self.dict_parametros_valores['b'].set(0.2)
            self.dict_parametros_valores['c'].set(-65)
            self.dict_parametros_valores['d'].set(4)
        elif eleccion == "Intrinsic bursting":
            self.dict_parametros_valores['a'].set(0.02)
            self.dict_parametros_valores['b'].set(0.2)
            self.dict_parametros_valores['c'].set(-55)
            self.dict_parametros_valores['d'].set(4)
        elif eleccion == "Chattering":
            self.dict_parametros_valores['a'].set(0.02)
            self.dict_parametros_valores['b'].set(0.2)
            self.dict_parametros_valores['c'].set(-50)
            self.dict_parametros_valores['d'].set(2)
        elif eleccion == "Fast spiking":
            self.dict_parametros_valores['a'].set(0.1)
            self.dict_parametros_valores['b'].set(0.2)
            self.dict_parametros_valores['c'].set(-65)
            self.dict_parametros_valores['d'].set(2)
        elif eleccion == "Talamo-Cortical":
            self.dict_parametros_valores['a'].set(0.02)
            self.dict_parametros_valores['b'].set(0.25)
            self.dict_parametros_valores['c'].set(-65)
            self.dict_parametros_valores['d'].set(0.05)
        else:
            self.dict_parametros_valores['a'].set(0.1)
            self.dict_parametros_valores['b'].set(0.25)
            self.dict_parametros_valores['c'].set(-65)
            self.dict_parametros_valores['d'].set(0.05)

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
        nombre_carpeta_v = 'Datos_V_' + fecha # contruyo el nombre de la carpeta donde se guardaran los archivos con el nombre Datos_Fecha
        nombre_carpeta_u = 'Datos_U_' + fecha # contruyo el nombre de la carpeta donde se guardaran los archivos con el nombre Datos_Fecha

        # pido el directorio donde se creara la carpeta en la que se guardaran los datos
        nombre_directorio = filedialog.askdirectory(parent = self.window,initialdir=self.directorio_actual,title="Directorio de guardado de datos") 
        # si el directorio es vacio quiere decir que se cerro la ventana sin escojer por lo que la funcion no hara nada y se retorna
        if nombre_directorio == '':
            return
        # si hay algo en el directorio se procede a crear una clase path con el parametro obtenido en el dialog para asi manejar de manera mas simple el path
        directorio_datos = Path(nombre_directorio)
        # se crea el path a la carpeta nueva con el nombre previamente generaro y se manda el comando al sistema para que la cree como carpeta
        carpeta_datos_v = directorio_datos.joinpath(str(nombre_carpeta_v))
        carpeta_datos_v.mkdir(parents=True, exist_ok=True)
        carpeta_datos_u = directorio_datos.joinpath(str(nombre_carpeta_u))
        carpeta_datos_u.mkdir(parents=True, exist_ok=True)
        # Se realizara en una funcion auxiliar el almacenado de datos de las graficas:
        if self.diccionario_todos['V(t)']:
            self.aux_exportar_metodo(carpeta_datos_v, '.efor_v', self.eForSetV)
            self.aux_exportar_metodo(carpeta_datos_v, '.eback_v', self.eBackSetV)
            self.aux_exportar_metodo(carpeta_datos_v, '.emod_v', self.eModSetV)
            self.aux_exportar_metodo(carpeta_datos_v, '.rk2_v', self.RK2SetV)
            self.aux_exportar_metodo(carpeta_datos_v, '.rk4_v', self.RK4SetV)
        if self.diccionario_todos['u(t)']:
            self.aux_exportar_metodo(carpeta_datos_u, '.efor_u', self.eForSetU)
            self.aux_exportar_metodo(carpeta_datos_u, '.eback_u', self.eBackSetU)
            self.aux_exportar_metodo(carpeta_datos_u, '.emod_u', self.eModSetU)
            self.aux_exportar_metodo(carpeta_datos_u, '.rk2_u', self.RK2SetU)
            self.aux_exportar_metodo(carpeta_datos_u, '.rk4_u', self.RK4SetU)


    def aux_exportar_metodo(self, directorio, extension, listaDatos):
        ''' Metodo auxiliar que ayudara al guardado de archivos, es definido para evitar redundacia en codigo
        '''         
        # genero un proceso iterativo para leer todas las lineas graficadas en el listado de datos el cual tiene en cada posicion un conjunto (X,Y)
        for i,val in enumerate(listaDatos):
            # obtengo el listado de datos de X 
            x_data = val[0]
            # obtengo el listado de datos deY
            y_data = val[1]
            # las empaqueto en formatodouble
            x_packed = st.pack('d'*len(x_data),*x_data)
            y_packed = st.pack('d'*len(y_data),*y_data)
            # creo el archivo con el nombre i.extencion para hacer la lectura despues de forma facil ejemplo 0.efor
            with open(directorio.joinpath(str(i)+extension).absolute(),'ab') as f:
                # escribo los datos de X en el archivo
                f.write(x_packed)
                # escribo los datos de Y en el archivo
                f.write(y_packed)
                # Nota: el orden es importante ya que en la lectura se obtendra un set completo por lo que la primera mitad sera X y la segunda mitad sera Y
    

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
        tmpSetEforV = self.aux_importar(directorio_datos,'.efor_v', self.color_efor)
        tmpSetEbackV = self.aux_importar(directorio_datos,'.eback_v', self.color_eback)
        tmpSetEmodV = self.aux_importar(directorio_datos,'.emod_v', self.color_emod)
        tmpSetRK2V = self.aux_importar(directorio_datos,'.rk2_v', self.color_rk2)
        tmpSetRK4V = self.aux_importar(directorio_datos,'.rk4_v',self.color_rk4)

        tmpSetEforU = self.aux_importar(directorio_datos,'.efor_u', self.color_efor)
        tmpSetEbackU = self.aux_importar(directorio_datos,'.eback_u', self.color_eback)
        tmpSetEmodU = self.aux_importar(directorio_datos,'.emod_u', self.color_emod)
        tmpSetRK2U = self.aux_importar(directorio_datos,'.rk2_u', self.color_rk2)
        tmpSetRK4U = self.aux_importar(directorio_datos,'.rk4_u',self.color_rk4)
        # agrego los datos cargados a los existentes en las listas que almacenan estos para la persistencia
        self.eForSetV +=tmpSetEforV
        self.eBackSetV+=tmpSetEbackV
        self.eModSetV+=tmpSetEmodV
        self.RK2SetV+=tmpSetRK2V
        self.RK4SetV+=tmpSetRK4V

        self.eForSetU +=tmpSetEforU
        self.eBackSetU+=tmpSetEbackU
        self.eModSetU+=tmpSetEmodU
        self.RK2SetU+=tmpSetRK2U
        self.RK4SetU+=tmpSetRK4U
        # Dibujo en la grafica
        self.imagen_grafica.draw()

    def aux_importar(self, directorio, extension, color_grafica):
        ''' Metodo auxiliar que ayudara a la carga de archivos, es definido para evitar redundacia en codigo
        retorna una lista con los valores leidos de X y Y de los archivos que encuentre en el path especificado con la extencion especificada
        '''
        # obtengo el nombre de todos los archivos con la extension deseada
        ext = '*'+extension
        files = [f.absolute() for f in directorio.glob(ext) if f.is_file()]
        tmpSet = [] # variable donde se guardaran los conjuntos
        # proceso iterativo que lee cada archivo
        for tmpF in files:
            with open(tmpF,'rb') as f:
                # leo el contenido del archivo
                data = f.read()
                # desempaqueto el contenido del arvhivo y lo convierto en lista para manipularlo
                unpacked = list(st.unpack('d'*(len(data)//8),data))
                # obtengo la mitad del tamaño para poder partir el array
                tam = len(unpacked)//2
                # genero los valores de X con la mitad de los datos y lo vuelvo un array de numpy
                t = np.array(unpacked[:tam])
                # genero los valores de Y con la segunda mitad de los datos y lo vuelvo un array de numpy
                V = np.array(unpacked[tam:])
                # grafico la linea con el color que debe ir
                self.plot.plot(t,V,color=color_grafica)
                # guardo los valore de X y Y en la lista temporal que se retornara al final de este metodo
                tmpSet.append((t,V))
        # retorno la lista resultante de la lectura de los archivos con la extencion
        return tmpSet

    def limpiar_grafica(self):
        ''' Funcion que limpia las grafica y las listas donde se guardan los datos para los metodos de persistencia
        '''
        self.plot.cla() # lipio toda la grafica, esto elimina incluso los titulos por lo que debo volver a ponerlos despues de esto                                                        # Define que las fuentes usadas en el gráfico son serifadas.
        self.plot.set_xlabel(r'Tiempo (ms)')       # Título del eje x
        self.plot.set_ylabel(r'Voltaje (mV)')        # Título del eje y
        self.plot.grid(1) # Activo la grilla
        self.imagen_grafica.draw()                                                              # Una vez agregado todo dibujo la grafica en la interfaz
        # vuelvo a poner el valor vacio en las listas que guardan los datos para los metodos de persistencia
        self.eForSetV = []
        self.eBackSetV = []
        self.eModSetV = []
        self.RK2SetV = []
        self.RK4SetV = []
        self.scipySetV = []

        self.eForSetU = []
        self.eBackSetU = []
        self.eModSetU = []
        self.RK2SetU = []
        self.RK4SetU = []
        self.scipySetU = []

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
        self.t_estimulacion = np.arange(self.t_ini_est, self.t_fini_est, 0.01) # Obtengo el tiempo de estimulacion
        self.t_antes_estimulacion = np.arange(0, self.t_ini_est, 0.01) # Obtengo el tiempo antes de la estimulacion
        self.t_despues_estimulacion = np.arange(self.t_fini_est, self.t_final + 0.01, 0.01) # Obtengo el tiempo despues de la estimulacion
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
            I_t = [0]*len(np.arange(0, self.t_final, 0.01)) # Dejo la corriente en 0
        self.diccionario_todos['I_t'] = I_t # Almaceno mi arreglo de corriente 
        # Crear la tablita con los datos ingresados
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
        self.metodoSolucion()
        # Creo una tabla para mostrar el codigo de colores
        self.tabla_colores = ttk.Treeview(self.frame_cargar)
        self.tabla_colores['columns'] = ('Color', 'Método')

        self.tabla_colores.column("#0", width=0,  stretch=NO)
        self.tabla_colores.column('Color',anchor=CENTER, width=120)
        self.tabla_colores.column('Método',anchor=CENTER, width=150)

        self.tabla_colores.heading("#0",text="",anchor=CENTER)
        self.tabla_colores.heading('Color',text='Color', anchor=CENTER)
        self.tabla_colores.heading('Método',text='Método', anchor=CENTER)

        self.tabla_colores.insert(parent='',index='end',iid=0,text='',values=('Rojo', 'Euler hacia adelante'))
        self.tabla_colores.insert(parent='',index='end',iid=1,text='',values=('Amarillo', 'Euler hacia atrás'))
        self.tabla_colores.insert(parent='',index='end',iid=2,text='',values=('Verde', 'Euler modificado'))
        self.tabla_colores.insert(parent='',index='end',iid=3,text='',values=('Azul', 'Runge-Kutta 2'))
        self.tabla_colores.insert(parent='',index='end',iid=4,text='',values=('Morado', 'Runge-Kutta 4'))

        self.tabla_colores.place(x=120, y=180)





        return self.diccionario_todos

    """Metodo que se encarga de mostrar las graficas de las checkboxes de metodos seleccionadas"""
    def metodoSolucion(self):
        if self.diccionario_todos['Euler Adelante']:
            self.llamadoEulerFor()
        if self.diccionario_todos['Euler Atrás']:
            self.llamadoEulerBack()
        if self.diccionario_todos['Euler Modificado']:
            self.llamadoEulerModificado()
        if self.diccionario_todos['Runge-Kutta 2']:
            self.llamadoRungeKutta2()
        if self.diccionario_todos['Runge-Kutta 4']:
            self.llamadoRungeKutta4()
            

    def llamadoEulerFor(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo euler forward con los parametros que tenga la interfaz en este momento
        '''
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        a, b, c, d = self.diccionario_todos['a'], self.diccionario_todos['b'], self.diccionario_todos['c'], self.diccionario_todos['d'] 
        T0, TF, I = 0, self.diccionario_todos['Tiempo de simulación'], self.diccionario_todos['I_t']
        t_eFor, V_eFor, U_eFor = EulerFor(a, b, c, d, T0, TF, I)
        # grafico los puntos con el respectivo color asignado para el metodo, variable que se puede cambiar en el init
        if self.diccionario_todos['V(t)']:
            self.plot.plot(t_eFor, V_eFor,color=self.color_efor)
            # Lo agrego para persistir
            self.eForSetV.append((t_eFor,V_eFor))
        if self.diccionario_todos['u(t)']: 
            self.plot.plot(t_eFor, U_eFor,color=self.color_efor)
            self.eForSetU.append((t_eFor,U_eFor))
        # una vez se añade todo al plot procedo a mostrarlo en la interfaz con el metodo draw del canvas definido para la grafica
        self.imagen_grafica.draw()
    
    def llamadoEulerBack(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo euler back con los parametros que tenga la interfaz en este momento
        '''
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        a, b, c, d = self.diccionario_todos['a'], self.diccionario_todos['b'], self.diccionario_todos['c'], self.diccionario_todos['d'] 
        T0, TF, I = 0, self.diccionario_todos['Tiempo de simulación'], self.diccionario_todos['I_t']
        t_eFor, V_eFor, U_eFor = Eulerback(a, b, c, d, T0, TF, I)
        # agregro los valores como una tupla en la variable que guarda las ejecuciones para los metodos de persistencia
        # grafico los puntos con el respectivo color asignado para el metodo, variable que se puede cambiar en el init
        if self.diccionario_todos['V(t)']:
            self.plot.plot(t_eFor, V_eFor,color=self.color_eback)
            self.eBackSetV.append((t_eFor, V_eFor))
        if self.diccionario_todos['u(t)']: 
            self.plot.plot(t_eFor, U_eFor,color=self.color_eback)
            self.eBackSetU.append((t_eFor, V_eFor))
        # una vez se añade todo al plot procedo a mostrarlo en la interfaz con el metodo draw del canvas definido para la grafica
        self.imagen_grafica.draw()

    def llamadoEulerModificado(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo euler modificado con los parametros que tenga la interfaz en este momento
        '''
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        a, b, c, d = self.diccionario_todos['a'], self.diccionario_todos['b'], self.diccionario_todos['c'], self.diccionario_todos['d'] 
        T0, TF, I = 0, self.diccionario_todos['Tiempo de simulación'], self.diccionario_todos['I_t']
        t_eFor, V_eFor, U_eFor = Eulermod(a, b, c, d, T0, TF, I)
        # agregro los valores como una tupla en la variable que guarda las ejecuciones para los metodos de persistencia
        # grafico los puntos con el respectivo color asignado para el metodo, variable que se puede cambiar en el init
        if self.diccionario_todos['V(t)']:
            self.plot.plot(t_eFor, V_eFor,color=self.color_emod)
            self.eModSetV.append((t_eFor, V_eFor))
        if self.diccionario_todos['u(t)']: 
            self.plot.plot(t_eFor, U_eFor,color=self.color_emod)
            self.eModSetU.append((t_eFor, V_eFor))

        # una vez se añade todo al plot procedo a mostrarlo en la interfaz con el metodo draw del canvas definido para la grafica
        self.imagen_grafica.draw()

    def llamadoRungeKutta2(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo Runge-Kutta 2 con los parametros que tenga la interfaz en este momento
        '''
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        a, b, c, d = self.diccionario_todos['a'], self.diccionario_todos['b'], self.diccionario_todos['c'], self.diccionario_todos['d'] 
        T0, TF, I = 0, self.diccionario_todos['Tiempo de simulación'], self.diccionario_todos['I_t']
        t_eFor, V_eFor, U_eFor = rungekutta2(a, b, c, d, T0, TF, I)
        # agregro los valores como una tupla en la variable que guarda las ejecuciones para los metodos de persistencia
        # TODO: self.eForSet.append((t_eFor,V_eFor))
        # grafico los puntos con el respectivo color asignado para el metodo, variable que se puede cambiar en el init
        if self.diccionario_todos['V(t)']:
            self.plot.plot(t_eFor, V_eFor,color=self.color_rk2)
            self.RK2SetV.append((t_eFor, V_eFor))
        if self.diccionario_todos['u(t)']: 
            self.plot.plot(t_eFor, U_eFor,color=self.color_rk2)
            self.RK2SetU.append((t_eFor, U_eFor))

        # una vez se añade todo al plot procedo a mostrarlo en la interfaz con el metodo draw del canvas definido para la grafica
        self.imagen_grafica.draw()

    def llamadoRungeKutta4(self):
        ''' Metodo que llamara la funcion definida en la logica para el metodo Runge-Kutta 4 con los parametros que tenga la interfaz en este momento
        '''
        # llamo la funcion de la logica para el metodo y obtengo los valores de x y y a graficar
        a, b, c, d = self.diccionario_todos['a'], self.diccionario_todos['b'], self.diccionario_todos['c'], self.diccionario_todos['d'] 
        T0, TF, I = 0, self.diccionario_todos['Tiempo de simulación'], self.diccionario_todos['I_t']
        t_eFor, V_eFor, U_eFor = rungekutta4(a, b, c, d, T0, TF, I)
        # agregro los valores como una tupla en la variable que guarda las ejecuciones para los metodos de persistencia
        # grafico los puntos con el respectivo color asignado para el metodo, variable que se puede cambiar en el init
        if self.diccionario_todos['V(t)']:
            self.plot.plot(t_eFor, V_eFor,color=self.color_rk4)
            self.RK4SetV.append((t_eFor, V_eFor))
        if self.diccionario_todos['u(t)']: 
            self.plot.plot(t_eFor, U_eFor,color=self.color_rk4)
            self.RK4SetU.append((t_eFor, V_eFor))
        # una vez se añade todo al plot procedo a mostrarlo en la interfaz con el metodo draw del canvas definido para la grafica
        self.imagen_grafica.draw()

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
    
    


