import pandas as pd
import random
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import mplcursors


mochila = {}
posicion_valor_diferencia = {}
poblacion = []
el_mejor = []
arreglo_de_claves = []
arreglo_mejor = []
arreglo_peor = []



#valores que introduce el usuario
valores_atributos = []

numero_de_poblacion_iniical = 0#2

poblacion_maxima = 0#7

posibilidad_cruza = 0#80

posibilidad_mut_individuo = 0#60

posibilidad_mut_gen = 0#10

numero_iteraciones = 0#30


# un escript que lea el exel y lo deje en este formato
def leer_exel():
    df = pd.read_excel('datos.xlsx')
    df = df.iloc[:, 1:]
    inicio = 0
    for index, row in df.iterrows():
        if inicio <= 3:
            inicio = inicio + 1
        else: 
            mochila[index+1-4] = [row[col] for col  in range(13)]
   
def restricciones():
    return 0


def generar_n_individuos_aleatorios():
    global arreglo_de_claves
    poblacion_inicial = []
    auxiliar_claves = []
    for clave in mochila:
        arreglo_de_claves.append(clave)
    auxiliar_claves = arreglo_de_claves
    
    for i in range(numero_de_poblacion_iniical):
        auxiliar_claves_copia = auxiliar_claves[:] # crea una copia de la lista
        random.shuffle(auxiliar_claves_copia) # baraja la copia
        poblacion_inicial.append(auxiliar_claves_copia) # agrega la copia barajada a la población inicial
    return poblacion_inicial
   
def seleccion_parejas():
    numero_de_parejas = 5
    parejas_aleatorias = [random.sample(poblacion, 2) for _ in range(numero_de_parejas)]
    return parejas_aleatorias

def cruza(parejas_aleatorias):
    punto_de_cruce = 8
    hijos = []
    for pareja in parejas_aleatorias:
        if random.randrange(0,100) <= posibilidad_cruza:
            tupla1 = pareja[0]
            tupla2 = pareja[1]
            # Realizar el cruce por punto fijo
            hijo1 = tupla1[:punto_de_cruce] + tupla2[punto_de_cruce:]
            hijo2 = tupla2[:punto_de_cruce] + tupla1[punto_de_cruce:]
            # Agregar las tuplas cruzadas a la lista de parejas cruzadas
            hijos.append(hijo1)
            hijos.append(hijo2)

    return hijos

def reparar_hijos(hijos_sin_reparar):#cambio de valores
    #Elemento duplicado cambio de valor por posicion
    global arreglo_de_claves
    hijos_reparados = []
    for hijo in hijos_sin_reparar:

        auxiliar_elementos_usados = []

        for elemanto in hijo:

            if elemanto in auxiliar_elementos_usados:
                 
                 for claves in arreglo_de_claves: 
                     
                     if claves not in auxiliar_elementos_usados:
                         auxiliar_elementos_usados.append(claves)
                         break
            else:       
                auxiliar_elementos_usados.append(elemanto)

        hijos_reparados.append(auxiliar_elementos_usados)
    return hijos_reparados
        
# 2,1,3,5,4,6

def mutacion(hijos_reparados):
    
    for hijo in hijos_reparados:
        arreglo_posiciones_que_mutan=[]

        if random.randint(0,100) <= posibilidad_mut_individuo :

            for posicion in range(len(hijo)):

                if random.randint(0,100) <= posibilidad_mut_gen :
                    arreglo_posiciones_que_mutan.append(posicion)

            Intercambio_de_valor(arreglo_posiciones_que_mutan, hijo)

        else:
            poblacion.append(hijo)
# 0 1 2 3 4 5
# 2,1,3,5,4,6
# . * * * . *

#metodo de modificar gen por intercambio de valor por posicion
def Intercambio_de_valor(arreglo_posiciones_que_mutan,hijo):
    global poblacion
    for elemento in arreglo_posiciones_que_mutan:
        posicion_random = random.randint(0,len(hijo)-1)
     
        #hace referencia al valor que va cambiar

        elemento_1 = hijo[elemento]#2
        #hace referencia al valor por el que se cambiara
        elemento_2 = hijo[posicion_random]#3

        hijo[elemento] = elemento_2

        hijo[posicion_random] = elemento_1

    poblacion.append(hijo)
  
  #3,1,3,5,4,6
  #3,1,2,5,4,6

                    #mochila    #poblacion
def sumar_valores(diccionario, lista_claves, opcion):
    # Inicializar variables para sumar los valores
    contador = 0

    for individuo in lista_claves:

        resultado = []
        nombre_elementos = []
        categorias = []
        valores = [0] * 11
        num_elemtos = 30   
        aux = individuo[:num_elemtos]
        # Iterar a través de las claves en la lista
        #aux son los primeros 30 elementos de l individuo
        for clave in aux:
            # Obtener el elemento correspondiente y agregar su nombre
            elemento = diccionario[clave]
            nombre_elementos.append(elemento[0])
            categorias.append(elemento[1])

            # Sumar los valores del elemento
            for i in range(2, len(elemento)):
                if i in [5, 6, 9, 10, 12] :
                    valores[i-2] += elemento[i]/1000
                elif i in  [7 , 11]:
                    valores[i-2] += elemento[i]/1000
                else:
                    valores[i-2] += elemento[i]

        # Retornar el resultado como una lista
        resultado.append(nombre_elementos)
        resultado.append(categorias)
        resultado.append(valores)
        posicion_valor_diferencia[contador] = resultado
        contador += 1
        if opcion == 1:
            data_fin_tabla = resultado
            return data_fin_tabla
    
        

#


def obtener_diferencia():
    for elemento in range(len(posicion_valor_diferencia)):
        aux_valores = []
        aux = 0
        for atributos in posicion_valor_diferencia[elemento][2]:
            valor = atributos - float(valores_atributos[aux])
            aux_valores.append(valor)
            aux = aux + 1
        posicion_valor_diferencia[elemento].append(aux_valores)


def calcular_suma_distancias():
    arreglo_suma_distancias_aux = []
    for elemento in posicion_valor_diferencia.values():
        suma_distancias = sum(abs(elemento) for elemento in elemento[3])
        arreglo_suma_distancias_aux.append(suma_distancias)

    for i in posicion_valor_diferencia:
        posicion_valor_diferencia[i].append(arreglo_suma_distancias_aux[i])

    return suma_distancias

def ordenar_elitsta():
    global poblacion
    combinado = list(zip(posicion_valor_diferencia.values(), poblacion))
    ordenado = sorted(combinado, key=lambda x: x[0][4])
    arreglos_ordenados = [tupla[1] for tupla in ordenado]
    obtener_valores_grafica([arreglos_ordenados[0]],[arreglos_ordenados[-1]])
    poblacion = arreglos_ordenados[:poblacion_maxima]


def obtener_valores_grafica(mayor,menor):
    
    mejor = sumar_valores(mochila,mayor,1)
    mejor = obtener_diferencia_final(mejor)
    mejor = sum(abs(elemento) for elemento in mejor[0])
    arreglo_mejor.append(mejor)
    peor = sumar_valores(mochila ,menor,1)
    peor = obtener_diferencia_final(peor)
    peor = sum(abs(elemento) for elemento in peor[0])
    arreglo_peor.append(peor)



def obtener_valores_tabla():
    global poblacion
    global mochila
    arreglo2 = []
    for clave in poblacion[0][:30]:
        valores = mochila.get(clave)
        arreglo2.append(valores)
    return arreglo2

def obtener_diferencia_final(arreglo2):
    arreglo4 = []
    aux_valores = []
    aux = 0
    for atributos in arreglo2[2]:
            valor = atributos - float(valores_atributos[aux])
            aux_valores.append(valor)
            aux = aux + 1
    arreglo4.append(aux_valores)
    return arreglo4




def show(arreglo1,arreglo2,arreglo3,arreglo4):
    def update_graph():
    # Datos de ejemplo
        iteraciones = np.arange(0, numero_iteraciones) 

        # Asegurar que los arreglos tengan la misma longitud que 'iteraciones'
        linea1 = arreglo_mejor[:numero_iteraciones]
        linea2 = arreglo_peor[:numero_iteraciones]
        plt.figure(figsize=(10, 6))
        plt.plot(iteraciones, linea1, marker='o', linestyle='-', label='El mejor')
        plt.plot(iteraciones, linea2, marker='o', linestyle='-', label='El peor')
        plt.ylim(0, 6000)
        # Ajustar los ticks del eje x para mostrar todos los puntos
        plt.xticks(iteraciones)
        plt.xlabel('Iteraciones')
        plt.ylabel('Valor')
        plt.title('Gráfico de Líneas')
        plt.legend()
        mplcursors.cursor(hover=True)
        plt.show()

    root = tk.Tk()
    treeview = ttk.Treeview(root, columns=[str(i) for i in range(13)], show="headings")

    headers = ['Nombre', 'Categoria', 'Energía (Kcal)', 'Proteina (g)', 'Grasa(g)', 'calcio (mg)',
           'Hierro (mg)', 'Vitamina A(mg)', 'Tiamina (mg)', 'Riboflavina (mg)', 'Niacina (mg)', 'Folato(mg)', 'Vitamina C(mg)']

    for i, col in enumerate(headers):
        treeview.heading(f'{i}', text=col)
        treeview.column(f'{i}', width=120)


    for row in arreglo1:
        treeview.insert('', 'end', values=row)

    treeview.insert('', 'end', values=["Total"] + [""] + arreglo2)
    treeview.insert('', 'end', values=["Requerido"] + [""] + arreglo3)
    treeview.insert('', 'end', values=["Diferencia"] + [""]  + arreglo4)
    treeview.configure(height=33)
    treeview.pack()
    update_button = tk.Button(root, text="Actualizar gráfica", command=update_graph)
    update_button.pack()
    root.mainloop()


def create_input_window():
      # Función para obtener los datos de los inputs al hacer clic en el botón
    def get_input_values():
        global valores_atributos
        global numero_de_poblacion_iniical 
        global posibilidad_mut_individuo  
        global posibilidad_mut_gen 
        global numero_iteraciones 
        global poblacion_maxima
        global posibilidad_cruza
        input_values = [entry.get() for entry in entry_list[:11]]
        remaining_values = [entry.get() for entry in entry_list[11:]]
        root.destroy()
        valores_atributos = input_values
        numero_de_poblacion_iniical = int(remaining_values[0])
        poblacion_maxima = int(remaining_values[1])
        posibilidad_cruza = int(remaining_values[2])
        posibilidad_mut_individuo = int(remaining_values[3])
        posibilidad_mut_gen = int(remaining_values[4])
        numero_iteraciones = int(remaining_values[5])
        print(remaining_values)
        return input_values, remaining_values

    root = tk.Tk()
    root.title("Ventana de Inputs")

    # Crea una etiqueta a la izquierda y un Entry a la derecha
    def create_label_and_entry(parent, label_text):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)

        label = ttk.Label(frame, text=label_text, width=30, anchor="e", font=("Arial", 15))
        label.pack(side="left", padx=(10, 5))

        entry = ttk.Entry(frame)
        entry.pack(side="right", fill="x", expand=True, padx=(0, 10))

        return entry
    
    atributos = ["Energía","Proteína","Grasa","Calcio","Hierro","Vitamina A","Tiamina","Riboflavina","Niacina","Folato","Vitamina C"]
    entrdas = ["cantidad de poblacion inicial","poblacion Maxima","probabilidad de cruza","probabilidad de mutacion del individuo", "probabilidad de mutacion del gen", "cantidad de iteraciones"]
    entry_list = []
    for i in range(11):
        entry = create_label_and_entry(root, f"{atributos[i]}:")
        entry_list.append(entry)

    separator = ttk.Separator(root, orient="horizontal")
    separator.pack(fill="x", pady=10)

    for i in range(0, 6):
        entry = create_label_and_entry(root, f"{entrdas[i]}:")
        entry_list.append(entry)

    button = ttk.Button(root, text="Obtener valores", command=get_input_values)
    button.pack(pady=10)
    root.mainloop()
    
    

def main():
    create_input_window()
    global poblacion
    global el_mejor

    leer_exel()

    
    
    poblacion = generar_n_individuos_aleatorios()
  
      ##inicia el bucle
    for i in range(numero_iteraciones):
        parejas_aleatorias = seleccion_parejas()
            

        hijos_sin_reparar = cruza(parejas_aleatorias)
            

        hijos_reparados = reparar_hijos(hijos_sin_reparar)
        

        mutacion(hijos_reparados)

        sumar_valores(mochila, poblacion, 0)

        obtener_diferencia()

        calcular_suma_distancias()

        ordenar_elitsta()
    

        
        ##termina el bucle
        ## despues de la mutacion

    ##obtener datospara la tabla
    el_mejor.append(poblacion[0])
    arreglo1 = obtener_valores_tabla()
    arreglo2 = sumar_valores(mochila, el_mejor, 1)
    arreglo3 = valores_atributos
    arreglo4 = obtener_diferencia_final(arreglo2)
    show(arreglo1,arreglo2[2],arreglo3,arreglo4[0])
   
   


main()



