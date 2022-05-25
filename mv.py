from dataclasses import dataclass
from operator import indexOf
import sys
from Cuadruplos import Alcance, Cuadruplo
from Memoria import Memoria


class MaquinaVirtual:
    def __init__(self, archivo_cuadruplos) -> None:
        cuadruplos = ""

        with open(archivo_cuadruplos, "r") as archivo:
            cuadruplos = archivo.read()

        self.lista_cuadruplos = cuadruplos.split("\n")

# osea de tipos
# local temporal etc
        self.memoria_parametros = []
        self.memoria_funciones = []

        self.pila_brincos_endFunc = []

        self.instruccion_actual = 0

        self.memoria_global = Memoria()
        self.memoria_stack: list[Memoria] = [Memoria()]

        self.ejecutar_programa()

    def ejecutar_programa(self):
        while(self.instruccion_actual < len(self.lista_cuadruplos)):
            cuadruplo_actual_split = self.lista_cuadruplos[self.instruccion_actual].split(
                ",")
            operacion = cuadruplo_actual_split[0]
            op1 = cuadruplo_actual_split[1]
            op2 = cuadruplo_actual_split[2]
            direccion = cuadruplo_actual_split[3]

            if operacion == "+":
                pass
            elif operacion == "-":
                pass

            self.instruccion_actual += 1
    
    def obtener_valor(self, direccion):
        #Encontrar en qué memoria está (local global)
        prefijo = direccion[0]
        if prefijo == 0:
            alcance = Alcance.alcance_constante
        elif prefijo  == 1:
            alcance = Alcance.alcance_global
        elif prefijo == 2:
            alcance = Alcance.alcance_local
        

    def guardar_valor(self,valor,direccion_dondeguardarlo):
        pass


if __name__ == "__main__":
    MaquinaVirtual(sys.argv[1])
