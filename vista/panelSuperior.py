import tkinter as tk
import datetime as dt              
from time import time
from tkinter import *
from pathlib import Path
from functools import partial
from PIL import ImageTk ,Image
from tkinter import messagebox, filedialog

"""Este panel contiene todos los elementos de """
def panel_superior(window, directorio_actual):
    panel = Frame(window) # Creo un panel para almacenar todos los objetos de esta parte de la interfaz.
    etiqueta_titulo(panel) # Pongo el titulo
    menu_opciones(window, panel, directorio_actual) # Pongo el menu de opciones
    panel.pack(side=TOP,fill=X) # Empaco el panel

'''Esta funcion agrega el titulo al panel superior
params:
panel: el panel en el que debe pintarse el titulo
'''
def etiqueta_titulo(panel):
    titulo = Label(panel, text="Modelo neuronal de Izhikevich") # Creo un label con el titulo.
    titulo.config(font =("Montserrat", 28)) # Configuro el tamanio y la fuente del titulo.
    titulo.grid(row=0, column=1, padx=400)  #pack(side=LEFT, padx= 200) # Pongo el titulo en el panel.

'''Esta funcion agrega el menu de opciones para cerrar la aplicacion.
Las opciones son:
Exportar: Almacena los datos de la grafica, asi como la configuracion de los parametros del usuario.
Importar: Importar de un archivo los datos y cargarlos en una grafica, asi como en las distintas partes de la app.
Cerrar: Cierra la aplicacion.
 '''
def menu_opciones(window, panel, directorio_actual):
    # --- BOTON CERRAR ---
    cerrar_img = Image.open(directorio_actual.joinpath('assets/close.png').absolute()) # Abro la ruta de la imagen de cerrar
    cerrar_icon = ImageTk.PhotoImage(cerrar_img) # Creo una imagen de Pillow para el icono de cerrar
    boton_cerrar = Button(panel, image=cerrar_icon, command=partial(cerrar_aplicacion, window)) # Creo el boton de cerrar
    boton_cerrar.image = cerrar_icon # Asigno la imagen al boton cerrar
    boton_cerrar.place(x=1170,y=0) #pack(side=RIGHT) # Coloco el boton cerrar 
    # --- BOTON EXPORTAR ---
    exportar_img = Image.open(directorio_actual.joinpath('assets/exportar.png').absolute()) # Abro la ruta de la imagen de exportar
    exportar_icon = ImageTk.PhotoImage(exportar_img) # Creo una imagen de Pillow para el icono de exportar
    boton_exportar = Button(panel, image=exportar_icon, command=partial(exportar, window, directorio_actual)) # Creo el boton de exportar
    boton_exportar.image = exportar_icon # Asigno la imagen al boton exportar
    boton_exportar.place(x=1140,y=0) #pack(side=RIGHT) # Coloco el boton exportar
    # --- BOTON IMPORTAR --- 
    importar_img = Image.open(directorio_actual.joinpath('assets/importar.png').absolute()) # Abro la ruta de la imagen de importar
    importar_icon = ImageTk.PhotoImage(importar_img) # Creo una imagen de Pillow para el icono de importar
    boton_importar = Button(panel, image=importar_icon, command=partial(importar, window, directorio_actual)) # Creo el boton de importar
    boton_importar.image = importar_icon # Asigno la imagen al boton importar
    boton_importar.place(x=1110,y=0) #pack(side=RIGHT) # Coloco el boton importar


''' Funcion que es llamada al hacer click en el boton cerrar, pregunta si realmente se desea cerrar o retornar a la aplicacion
'''
def cerrar_aplicacion(window):
    # creo la caja de mensaje y su valor
    MsgBox =  messagebox.askquestion('Cerrar Aplicación','¿Está seguro que desea cerrar la aplicación?', icon = 'warning')
     # si el valor es yes entonces cierro la apliacion
    if MsgBox == 'yes':
        print('yes')
        window.destroy()     
        window.quit()
    # en caso contrario se notifica el retorono a la aplicacion
    else:
        messagebox.showinfo('Retornar','Será retornado a la aplicación')

''' Funcion que abre un dialogo para ingresar el nombre de un archivo para guardar el resultado de una ejecucion de algoritmo en formato double
    '''
def exportar(window, directorio_actual):
    ahora = time() # obtengo el timestamp actual
    fecha = dt.datetime.utcfromtimestamp(ahora).strftime("%Y-%m-%d_%H-%M-%S") # genero la fecha actual con el time stamp obtenido previamente
    nombre_carpeta = 'Datos_' + fecha # contruyo el nombre de la carpeta donde se guardaran los archivos con el nombre Datos_Fecha
    # pido el directorio donde se creara la carpeta en la que se guardaran los datos
    nombre_directorio = filedialog.askdirectory(parent = window,initialdir=directorio_actual,title="Directorio de guardado de datos") 
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
def importar(window, directorio_actual):
    # pido el directorio donde se encuentran los datos previamente generados
    nombre_directorio = filedialog.askdirectory(parent = window,initialdir=directorio_actual,title="Directorio de datos generados")
    # si el directorio es vacio quiere decir que se cerro la ventana sin escojer por lo que la funcion no hara nada y se retorna
    if nombre_directorio == '':
        return
    # si hay algo en el directorio se procede a crear una clase path con el parametro obtenido en el dialog para asi manejar de manera mas simple el path
    directorio_datos = Path(nombre_directorio)
    # se llama a la funcion auxiliar que lee los archivos con la extencion y añade los datos a la grafica
    # TODO: Llamar a la funcion auxiliar para cargar los datos cuando ya los haya. La interfaz es un esqueleto entonces todavia no funciona.