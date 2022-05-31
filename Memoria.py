# Para saber cuántos de cada un voy a tener
from dataclasses import dataclass
import numpy as np


class Memoria:

    def __init__(self) -> None:

        self.rango_espacios = 1000
        self.direccion_base_ints = 0
        self.direccion_base_floats = self.direccion_base_ints + self.rango_espacios
        self.direccion_base_bool = self.direccion_base_floats + self.rango_espacios
        self.direccion_base_str = self.direccion_base_bool + self.rango_espacios

        self.tamano_seccion = self.direccion_base_str+self.rango_espacios

        self.espacio_memoria = np.empty(20000, dtype=object)

        self.direcciones_base = {
            "int": self.direccion_base_ints,
            "float": self.direccion_base_floats,
            "bool": self.direccion_base_bool,
            "str": self.direccion_base_str,
            "variable": 0,
            "temporal": self.tamano_seccion
        }

        # para generacion de codigo
        self.contadores_tipo_variables = {"int":  0,
                                          "float": 0,
                                          "bool": 0,
                                          "str": 0
                                          }

        self.contadores_tipo_temporales = {"int":  0,
                                           "float": 0,
                                           "bool": 0,
                                           "str": 0
                                           }


# importante tener la tabla de variables para poder generar direcciones
