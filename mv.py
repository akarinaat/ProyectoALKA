from dataclasses import dataclass
import sys
from Cuadruplos import Cuadruplo


class MaquinaVirtual:
    def __init__(self, archivo_cuadruplos) -> None:
        cuadruplos = ""

        with open(archivo_cuadruplos, "r") as archivo:
            cuadruplos = archivo.read()

        self.lista_cuadruplos = cuadruplos.split("\n")

        self.memoria_parametros = []
        self.memoria_temporales = []
        self.memoria_funciones = []

        self.instruccion_actual = 0

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


if __name__ == "__main__":
    MaquinaVirtual(sys.argv[1])
