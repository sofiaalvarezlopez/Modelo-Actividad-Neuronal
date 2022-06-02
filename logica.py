import numpy as np

#============================================== ECUACIONES DIFERENCIALES ===============================================
def dvdt(v, u, I):
    return 0.04*(v**2) + (5*v) + 140 - u + I

def dudt(v, u, a, b):
    return a*((b*v) - u)

#==============================================    MÉTODOS NUMÉRICOS   =================================================
def EulerFor(a, b, c, d, T0, TF, I, h=0.01):
    T = np.arange(T0, TF + h, h)
    v = np.zeros(len(T))
    v[0] = -65
    u = np.zeros(len(T))
    u[0] = b*v[0]
    for iter in range(1, len(T)):

        if(v[iter-1] >= 30):
            v[iter] = c
            u[iter] = u[iter-1] + d
        else:
            v[iter] = v[iter - 1] + h * dvdt(v[iter - 1], u[iter - 1], I[iter - 1])
            u[iter] = u[iter - 1] + h * dudt(v[iter - 1], u[iter - 1], a, b) 
    
    return T, v, u

def Eulerback(a, b, c, d, T0, TF, I, h=0.01): 
    
    def V_EulerBack(v, u, I_actual, h=0.01):
        a_c = -0.04 * h
        b_c = 1 - 5 * h
        c_c = - (v + h*(140 - u + I_actual))
        
        return (-b_c + np.sqrt(b_c**2 - 4*a_c*c_c))/(2*a_c)

    def U_EulerBack(v, u, h=0.01):
        return (u + h * a * b * v) / (1 + h * a)

    T = np.arange(T0, TF + h, h)
    v = np.zeros(len(T))
    v[0] = -65
    u = np.zeros(len(T))
    u[0] = -14
    print(len(T))
    print(len(I))
    for iter in range(1, len(T)):
        if(v[iter-1] >= 30):
            v[iter] = c
            u[iter] = u[iter-1] + d
        else:
            v[iter] = V_EulerBack(v[iter - 1], u[iter - 1], I[iter], h=0.01)
            u[iter] = U_EulerBack(v[iter - 1], u[iter - 1], h=0.01)
    
    return T, v, u

def Eulermod(a, b, c, d, T0, TF, I, h=0.01):
    
    T = np.arange(T0, TF + h, h)
    v = np.zeros(len(T))
    v[0] = -65
    u = np.zeros(len(T))
    u[0] = b*v[0]

    for iter in range(1, len(T)):

        if(v[iter-1] >= 30):    
            v[iter] = c
            u[iter] = u[iter-1] + d

        else:

            v[iter] = v[iter - 1] + ((h/2)*((dvdt(v[iter-1], u[iter-1], I[iter-1])) + dvdt(v[iter - 1] + h*v[iter - 1], u[iter-1] + h*u[iter - 1], I[iter-1])))
            u[iter] = u[iter-1] + ((h/2)*((dudt(v[iter - 1], u[iter - 1],a,b) + dudt(v[iter-1] + h*v[iter - 1],u[iter -1] + h*u[iter - 1], a, b))))  
    
    return T, v, u

def rungekutta2(a, b, c, d, T0, TF, I, h=0.01): 
    T = np.arange(T0, TF + h, h)
    v = np.zeros(len(T))
    v[0] = -65
    u = np.zeros(len(T))
    u[0] = b*v[0]

    for iter in range(1, len(T)):

        if(v[iter-1] >= 30):
            v[iter] = c
            u[iter] = u[iter-1] + d

        else:
            kv1 = dvdt(v[iter - 1], u[iter - 1], I[iter- 1])
            ku1 = dudt(v[iter - 1], u[iter - 1], a, b)
            kv2 = dvdt(v[iter - 1] + (1/2*kv1*h), u[iter - 1] + (1/2*ku1*h), I[iter- 1])
            ku2 = dudt(v[iter - 1] + (1/2*kv1*h), u[iter - 1] + (1/2*ku1*h), a, b)

            v[iter] = v[iter - 1] + h * kv2
            u[iter] = u[iter - 1] + h * ku2
    
    return T, v, u 

def rungekutta4(a, b, c, d, T0, TF, I, h=0.01): 
    T = np.arange(T0, TF + h, h)
    v = np.zeros(len(T))
    v[0] = -65
    u = np.zeros(len(T))
    u[0] = b*v[0]

    for iter in range(1,len(T)):
        if(v[iter-1] >= 30):
            v[iter] = c
            u[iter] = u[iter-1] + d
        else:
            kv1 = dvdt(v[iter - 1], u[iter - 1], I[iter - 1])
            ku1 = dudt(v[iter - 1], u[iter - 1], a, b)

            kv2 = dvdt(v[iter - 1] + 1/2*kv1*h, u[iter - 1] + 1/2*ku1*h, I[iter-1])
            ku2 = dudt(v[iter - 1] + 1/2*kv1*h, u[iter - 1] + 1/2*ku1*h, a, b)
        
            kv3 = dvdt(v[iter - 1] + 1/2*kv2*h, u[iter - 1] + 1/2*ku2*h, I[iter-1])
            ku3 = dudt(v[iter - 1] + 1/2*kv2*h, u[iter - 1] + 1/2*ku2*h, a, b)

            kv4 = dvdt(v[iter-1] + kv3*h, u[iter-1] + ku3*h, I[iter - 1])
            ku4 = dudt(v[iter - 1] + kv3*h, u[iter - 1] + ku3*h, a, b)

            v[iter] = v[iter-1] + h/6*(kv1+2*kv2+2*kv3+kv4)
            u[iter] = u[iter-1] + h/6*(ku1+2*ku2+2*ku3+ku4)
    
    return T, v, u
