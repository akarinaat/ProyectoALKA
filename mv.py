from dataclasses import dataclass
from operator import indexOf
import sys
from typing import Any
from Cuadruplos import Alcance, Cuadruplo
from Memoria import Memoria
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
# Ejecucion


class MaquinaVirtual:

    # La máquina virtual empieza a leer el archivo con
    # el código intermedio (cuádruplos) generados en compilación
    # Le llega el nombre del archivo
    def __init__(self, cuadruplos):

        self.lista_cuadruplos = cuadruplos.split("\n")

        self.memoria_constantes = np.empty(5000, dtype=object)
        self.stack_direcciones_return = []
        self.pila_brincos_endFunc = []
        self.instruccion_actual = 0

        self.memoria_global = Memoria()
        self.memoria_stack: list[Memoria] = [
            Memoria()]  # La memoria inicial es del main

        self.memoria_funcion_a_llamar: Memoria = None

        diccionario_consts = eval(self.lista_cuadruplos.pop())
        for key, value in diccionario_consts.items():
            self.memoria_constantes[int(value)] = key

    def ejecutar_programa(self) -> Any:
        while(int(self.instruccion_actual) < len(self.lista_cuadruplos)):
            cuadruplo_actual_split = self.lista_cuadruplos[int(self.instruccion_actual)].split(
                ",")

            # Del string de cuadruplos voy sacando el str de cada uno

            operacion = cuadruplo_actual_split[0]
            op1 = cuadruplo_actual_split[1]
            op2 = cuadruplo_actual_split[2]
            direccion = cuadruplo_actual_split[3]

            self.instruccion_actual += 1

            if operacion == "+":
                izq = self.obtener_valor(op1)
                der = self.obtener_valor(op2)
                self.guardar_valor(izq+der, direccion)
            elif operacion == "-":
                izq = self.obtener_valor(op1)
                der = self.obtener_valor(op2)
                self.guardar_valor(izq-der, direccion)
            elif operacion == "*":
                izq = self.obtener_valor(op1)
                der = self.obtener_valor(op2)
                self.guardar_valor(izq*der, direccion)
            elif operacion == "/":
                izq = self.obtener_valor(op1)
                der = self.obtener_valor(op2)
                self.guardar_valor(izq/der, direccion)
            elif operacion == "<":
                izq = self.obtener_valor(op1)
                der = self.obtener_valor(op2)
                self.guardar_valor(izq < der, direccion)
            elif operacion == ">":
                izq = self.obtener_valor(op1)
                der = self.obtener_valor(op2)
                self.guardar_valor(izq > der, direccion)
            elif operacion == "==":
                izq = self.obtener_valor(op1)
                der = self.obtener_valor(op2)
                self.guardar_valor(izq == der, direccion)
            elif operacion == "!=":
                izq = self.obtener_valor(op1)
                der = self.obtener_valor(op2)
                self.guardar_valor(izq != der, direccion)
            elif operacion == "=":
                izq = self.obtener_valor(op1)
                self.guardar_valor(izq, direccion)
            elif operacion == "ver":
                indice = self.obtener_valor(op1)
                limite = self.obtener_valor(op2)

                if indice > limite or indice < 0:
                    raise RuntimeError(
                        f"Index out of bounds! index is {indice}, limit is {limite}")
            elif operacion == "goto":
                self.instruccion_actual = int(op1)
            elif operacion == "gotof":
                condicion = self.obtener_valor(op1)
                if condicion == False:
                    self.instruccion_actual = int(direccion)

            elif operacion == "gosub":
                # Me regreso a donde estaba antes de que se ejecutara la funcion
                self.pila_brincos_endFunc.append(self.instruccion_actual)

                self.memoria_stack.append(self.memoria_funcion_a_llamar)

                self.instruccion_actual = int(op1)
                cantidad_parametros = op2

                direccion_resultado = direccion

                self.stack_direcciones_return.append(direccion_resultado)

            elif operacion == "return":
                resultado = self.obtener_valor(direccion)

                # Checar si es el  del main
                if len(self.stack_direcciones_return) == 0:
                    # Imprimir resultado a consola
                    print(resultado, "El resultado!")
                    return resultado

                donde_guardar_resultado = self.stack_direcciones_return.pop()

                # borrar la memoria local a la funcion
                self.memoria_stack.pop()

                # Guardar valor en el que llamo
                self.guardar_valor(resultado, donde_guardar_resultado)
                # regresar a la instruccion despues del gosub
                self.instruccion_actual = self.pila_brincos_endFunc.pop()

            elif operacion == "ERA":
                # Se ejecuta el cuadruplo ERA y se aparta la memoria
                self.memoria_funcion_a_llamar = Memoria()
                self.memoria_parametros_es = []
            elif operacion == "param":
                valor_argumento = self.obtener_valor(op1)

                self.memoria_funcion_a_llamar.espacio_memoria[int(
                    direccion[1:])] = valor_argumento

            elif operacion == "write":
                print(self.obtener_valor(op1))
            elif operacion == "mean":
                resultado = np.mean(self.obtener_arreglo(
                    op1, self.obtener_valor(op2)))
                self.guardar_valor(resultado, direccion)
            elif operacion == "mode":
                vals,counts = np.unique(self.obtener_arreglo(
                    op1, self.obtener_valor(op2)), return_counts=True)
                index = np.argmax(counts)
                self.guardar_valor(vals[index], direccion)

            elif operacion == "variance":
                resultado = np.var(self.obtener_arreglo(
                    op1, self.obtener_valor(op2)))
                self.guardar_valor(resultado, direccion)
            elif operacion == "hist":
                print("JOLA")
                tamaño = self.obtener_valor(op2)
                arreglo_para_hist = self.obtener_arreglo(op1, tamaño)
                plt.hist(arreglo_para_hist)
                plt.show()
                print(arreglo_para_hist)
                # dim1 = self.obtener_valor(op2)
                # dim2 = self.obtener_valor(direccion)

                # tamaño = dim1*dim2

                # matriz = np.reshape(self.obtener_arreglo(
                #     op1, tamaño), (dim1, dim2))
                # hist, bins = np.histogram(matriz)
                # plt.hist()
            elif operacion == "read":
                direccion_arg = op1
                nombre_arch = self.obtener_valor(op2)[1:-1] # para quitar comillas
                tamano = self.obtener_valor(direccion)

                # puse el [:tamano] para asegurar que solo la cantidad de
                # datos correctos se escriban.
                datos = np.loadtxt(nombre_arch,delimiter=",",dtype=np.number).flatten()[:tamano]

                self.guardar_arreglo(direccion_arg,tamano,datos)
  
  
    def guardar_arreglo(self, inicio: str, tamaño: int,valor):
        prefijo = inicio[0]
        if prefijo == "(":
            inicio = str(self.obtener_valor(inicio[1:-1]))
            prefijo = inicio[0]
        direccion_inicio = int(inicio[1:])
        direccion_fin = direccion_inicio + tamaño
        if prefijo == "1":
            self.memoria_global.espacio_memoria[direccion_inicio:direccion_inicio+direccion_fin]= valor
        elif prefijo == "2":
            self.memoria_stack[-1].espacio_memoria[direccion_inicio:direccion_inicio+direccion_fin] = valor

    def obtener_arreglo(self, inicio: str, tamaño: int):
        prefijo = inicio[0]
        if prefijo == "(":
            inicio = str(self.obtener_valor(inicio[1:-1]))
            prefijo = inicio[0]
        direccion_inicio = int(inicio[1:])
        direccion_fin = direccion_inicio + tamaño
        if prefijo == "1":
            return np.copy(self.memoria_global.espacio_memoria[direccion_inicio:direccion_inicio+direccion_fin])
        elif prefijo == "2":
            return np.copy(self.memoria_stack[-1].espacio_memoria[direccion_inicio:direccion_inicio+direccion_fin])

    def obtener_valor(self, direccion: str):
        # checar si es apuntador
        if direccion[0] == "(":
            # para acceder al valor de la dirección
            direccion = str(self.obtener_valor(direccion[1:-1]))
            # de manera recursiva [1:-1] --> direccion
            # en medio de los paréntesis porque tengo que hacer doble por lo del apuntador (tp1)

        if int(direccion) < 0:
            raise RuntimeError(
                "No se puede acceder a una dirección void: Error de Segmentación")
        # Encontrar en qué memoria está (local global)
        prefijo = direccion[0]
        # Acceder a lo qu eno es el prefijo
        direccion = direccion[1:]

        if prefijo == '0':
            return self.memoria_constantes[int(direccion)]
        elif prefijo == '1':

            # Regresa el valor que está en esta direccin en la memoria global
            return self.memoria_global.espacio_memoria[int(direccion)]

        elif prefijo == '2':
            # Regresa
            return self.memoria_stack[-1].espacio_memoria[int(direccion)]

    def guardar_valor(self, valor, direccion_index: str):
        # checar si es apuntador
        if direccion_index[0] == "(":
            direccion_index = str(self.obtener_valor(direccion_index[1:-1]))

        if int(direccion_index) < 0:
            return
       # Encontrar en qué memoria está (local global)
        prefijo = direccion_index[0]
        # Acceder a lo qu eno es el prefijo
        direccion_index = direccion_index[1:]
        if prefijo == '0':
            pass
        elif prefijo == '1':
            # Regresa el valor que está en esta direccin en la memoria global
            self.memoria_global.espacio_memoria[int(
                direccion_index)] = valor

        elif prefijo == '2':
            # Regresa
            self.memoria_stack[-1].espacio_memoria[int(
                direccion_index)] = valor


if __name__ == "__main__":

    cuadruplos = ""

    with open(sys.argv[1], "r") as archivo:
        cuadruplos = archivo.read()
    # MaquinaVirtual()
    MaquinaVirtual(cuadruplos).ejecutar_programa()
