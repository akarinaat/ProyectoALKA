from dataclasses import dataclass
from operator import indexOf
import sys
from Cuadruplos import Alcance, Cuadruplo
from Memoria import Memoria
import numpy as np

# Ejecucion


class MaquinaVirtual:

    # La máquina virtual empieza a leer el archivo con
    # el código intermedio (cuádruplos) generados en compilación
    # Le llega el nombre del archivo
    def __init__(self, archivo_cuadruplos) -> None:
        cuadruplos = ""

        with open(archivo_cuadruplos, "r") as archivo:
            cuadruplos = archivo.read()

        self.lista_cuadruplos = cuadruplos.split("\n")

# osea de tipos
# local temporal etc
        self.memoria_constantes = np.empty(5000)
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

        self.ejecutar_programa()

    def ejecutar_programa(self):
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
                limite = int(op2)

                if indice > limite or indice < 0:
                    raise RuntimeError(
                        f"Index out of bounds! index is {indice}, limit is {limite}")
            elif operacion == "goto":
                self.instruccion_actual = int(op1)
            elif operacion == "gotof":
                condicion = self.obtener_valor(op1)
                if condicion is False:
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
                    print(resultado)
                    return resultado

                donde_guardar_resultado = self.stack_direcciones_return.pop()

                self.guardar_valor(resultado, donde_guardar_resultado)
                # borrar la memoria local a la funcion
                self.memoria_stack.pop()
                # regresar a la instruccion despues del gosub
                self.instruccion_actual = self.pila_brincos_endFunc.pop()

            elif operacion == "ERA":
                self.memoria_funcion_a_llamar = Memoria()

    def obtener_valor(self, direccion: str):
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

    def guardar_valor(self, valor, direccion_index):
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
    # MaquinaVirtual(sys.argv[1])
    MaquinaVirtual("test.out")
