import numpy as np

#============================================== ECUACIONES DIFERENCIALES ===============================================
def dvdt(v, u, I):  #Defino la primera ecuacion diferencial de la variacion del potencial respecto al tiempo
    return 0.04*(v**2) + (5*v) + 140 - u + I

def dudt(v, u, a, b): #Defino la segunda ecuacion diferencial de la variacion de la variable de recuperación respecto al tiempo
    return a*((b*v) - u)

#==============================================    MÉTODOS NUMÉRICOS   =================================================
def EulerFor(a, b, c, d, T0, TF, I, h=0.01): #Defino una función que implementa el metodo de euler hacia adelante
    T = np.arange(T0, TF + h, h)  #Creo un arreglo con los tiempos ingresados por el usuario
    v = np.zeros(len(T))   #Creo un arreglo de ceros para la variable v
    v[0] = -65            #Pongo la condicion inicial de la primera ecuacion diferencial
    u = np.zeros(len(T))  #Creo un arreglo de ceros para la variable u
    u[0] = b*v[0]         #Pongo la condicion inicial de la segunda ecuacion diferencial
    for iter in range(1, len(T)):   #Hago un ciclo para iterar sobre cada valor de tiempo

        if(v[iter-1] >= 30):        #Hago la condicion de que si la condicion inicial de la ecuacion llegase a ser mayor a 30, se establecen valores fijos para cada arreglo 
            v[iter] = c
            u[iter] = u[iter-1] + d
        else:                     #Si no se cumple la anterior condicion, se implementa el metodo de euler hacia adelante
            v[iter] = v[iter - 1] + h * dvdt(v[iter - 1], u[iter - 1], I[iter - 1])  #Se aplica la formula que itera en el tiempo para hallar la funcion que resuelve la ecuacion
            u[iter] = u[iter - 1] + h * dudt(v[iter - 1], u[iter - 1], a, b) 
    
    return T, v, u

def Eulerback(a, b, c, d, T0, TF, I, h=0.01): #Defino una función que implementa el metodo de euler hacia atrás
    
    def V_EulerBack(v, u, I_actual, h=0.01):  #Defino una funcion auxiliar para la variable v que resulta de resolver la formula de este metodo
        a_c = -0.04 * h
        b_c = 1 - 5 * h
        c_c = - (v + h*(140 - u + I_actual))
        
        return (-b_c + np.sqrt(b_c**2 - 4*a_c*c_c))/(2*a_c)

    def U_EulerBack(v, u, h=0.01):            #Defino una funcion auxiliar para la variable u que resulta de resolver la formula de este metodo
        return (u + h * a * b * v) / (1 + h * a)

    T = np.arange(T0, TF + h, h) #Creo un arreglo con los tiempos ingresados por el usuario
    v = np.zeros(len(T))      #Creo un arreglo de ceros para la variable u
    v[0] = -65                #Pongo la condicion inicial de la primera ecuacion diferencial
    u = np.zeros(len(T))      #Creo un arreglo de ceros para la variable u
    u[0] = -14                #Pongo la condicion inicial de la segunda ecuacion diferencial
    
    for iter in range(1, len(T)): #Hago un ciclo para iterar sobre cada valor de tiempo
        if(v[iter-1] >= 30):  #Hago la condicion de que si la condicion inicial de la ecuacion llegase a ser mayor a 30, se establecen valores fijos para cada arreglo
            v[iter] = c
            u[iter] = u[iter-1] + d
        else:             #Si no se cumple la anterior condicion, se implementa el metodo de euler hacia atrás
            v[iter] = V_EulerBack(v[iter - 1], u[iter - 1], I[iter], h=0.01) #Se aplica la formula que itera en el tiempo para hallar la funcion que resuelve la ecuacion
            u[iter] = U_EulerBack(v[iter - 1], u[iter - 1], h=0.01)
    
    return T, v, u

def Eulermod(a, b, c, d, T0, TF, I, h=0.01):
    
    T = np.arange(T0, TF + h, h)  #Creo un arreglo con los tiempos ingresados por el usuario
    v = np.zeros(len(T))      #Creo un arreglo de ceros para la variable u
    v[0] = -65                #Pongo la condicion inicial de la primera ecuacion diferencial
    u = np.zeros(len(T))      #Creo un arreglo de ceros para la variable u
    u[0] = b*v[0]               #Pongo la condicion inicial de la segunda ecuacion diferencial

    for iter in range(1, len(T)): #Hago un ciclo para iterar sobre cada valor de tiempo

        if(v[iter-1] >= 30):    #Hago la condicion de que si la condicion inicial de la ecuacion llegase a ser mayor a 30, se establecen valores fijos para cada arreglo
            v[iter] = c
            u[iter] = u[iter-1] + d

        else:   #Si no se cumple la anterior condicion, se implementa el metodo de euler modificado

            v[iter] = v[iter - 1] + ((h/2)*((dvdt(v[iter-1], u[iter-1], I[iter-1])) + dvdt(v[iter - 1] + h*v[iter - 1], u[iter-1] + h*u[iter - 1], I[iter-1]))) #Se aplica la formula que itera en el tiempo para hallar la funcion que resuelve la ecuacion
            u[iter] = u[iter-1] + ((h/2)*((dudt(v[iter - 1], u[iter - 1],a,b) + dudt(v[iter-1] + h*v[iter - 1],u[iter -1] + h*u[iter - 1], a, b))))  
    
    return T, v, u

def rungekutta2(a, b, c, d, T0, TF, I, h=0.01): 
    T = np.arange(T0, TF + h, h) #Creo un arreglo con los tiempos ingresados por el usuario
    v = np.zeros(len(T))      #Creo un arreglo de ceros para la variable u
    v[0] = -65                #Pongo la condicion inicial de la primera ecuacion diferencial
    u = np.zeros(len(T))      #Creo un arreglo de ceros para la variable u
    u[0] = b*v[0]               #Pongo la condicion inicial de la segunda ecuacion diferencial

    for iter in range(1, len(T)): #Hago un ciclo para iterar sobre cada valor de tiempo

        if(v[iter-1] >= 30):    #Hago la condicion de que si la condicion inicial de la ecuacion llegase a ser mayor a 30, se establecen valores fijos para cada arreglo
            v[iter] = c
            u[iter] = u[iter-1] + d

        else:     #Si no se cumple la anterior condicion, se implementa el metodo de runge-kutta 2
            kv1 = dvdt(v[iter - 1], u[iter - 1], I[iter- 1])    #Hago una variable para la evaluacion de la pendiente en un punto del intervalo de tiempo para v
            ku1 = dudt(v[iter - 1], u[iter - 1], a, b)          #Hago una variable para la evaluacion de la pendiente en un punto del intervalo de tiempo para u
            kv2 = dvdt(v[iter - 1] + (1/2*kv1*h), u[iter - 1] + (1/2*ku1*h), I[iter- 1])  #Hago otra variable para la evaluacion de la pendiente en un punto distinto del intervalo de tiempo para v
            ku2 = dudt(v[iter - 1] + (1/2*kv1*h), u[iter - 1] + (1/2*ku1*h), a, b)      #Hago otra variable para la evaluacion de la pendiente en un punto distinto del intervalo de tiempo para u

            v[iter] = v[iter - 1] + h * kv2    #Se aplica la formula que itera en el tiempo para hallar la funcion que resuelve la ecuacion
            u[iter] = u[iter - 1] + h * ku2
    
    return T, v, u 

def rungekutta4(a, b, c, d, T0, TF, I, h=0.01): 
    T = np.arange(T0, TF + h, h)#Creo un arreglo con los tiempos ingresados por el usuario
    v = np.zeros(len(T))      #Creo un arreglo de ceros para la variable u
    v[0] = -65                #Pongo la condicion inicial de la primera ecuacion diferencial
    u = np.zeros(len(T))      #Creo un arreglo de ceros para la variable u
    u[0] = b*v[0]               #Pongo la condicion inicial de la segunda ecuacion diferencial

    for iter in range(1,len(T)): #Hago un ciclo para iterar sobre cada valor de tiempo
        if(v[iter-1] >= 30):      #Hago la condicion de que si la condicion inicial de la ecuacion llegase a ser mayor a 30, se establecen valores fijos para cada arreglo
            v[iter] = c
            u[iter] = u[iter-1] + d
        else:       #Si no se cumple la anterior condicion, se implementa el metodo de runge-kutta 4
            kv1 = dvdt(v[iter - 1], u[iter - 1], I[iter - 1])  #En este caso se crean 4 variables con el valor de la evaluacion de la pendiente en 4 puntos distintos para v
            ku1 = dudt(v[iter - 1], u[iter - 1], a, b)        #En este caso se crean 4 variables con el valor de la evaluacion de la pendiente en 4 puntos distintos para u

            kv2 = dvdt(v[iter - 1] + 1/2*kv1*h, u[iter - 1] + 1/2*ku1*h, I[iter-1])
            ku2 = dudt(v[iter - 1] + 1/2*kv1*h, u[iter - 1] + 1/2*ku1*h, a, b)
        
            kv3 = dvdt(v[iter - 1] + 1/2*kv2*h, u[iter - 1] + 1/2*ku2*h, I[iter-1])
            ku3 = dudt(v[iter - 1] + 1/2*kv2*h, u[iter - 1] + 1/2*ku2*h, a, b)

            kv4 = dvdt(v[iter-1] + kv3*h, u[iter-1] + ku3*h, I[iter - 1])
            ku4 = dudt(v[iter - 1] + kv3*h, u[iter - 1] + ku3*h, a, b)

            v[iter] = v[iter-1] + h/6*(kv1+2*kv2+2*kv3+kv4) #Se aplica la formula que itera en el tiempo para hallar la funcion que resuelve la ecuacion
            u[iter] = u[iter-1] + h/6*(ku1+2*ku2+2*ku3+ku4)
    
    return T, v, u