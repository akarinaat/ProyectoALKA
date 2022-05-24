# Para saber cuántos de cada un voy a tener
from dataclasses import dataclass


class Memoria:

    def __init__(self) -> None:

        self.rango_espacios = 1000
        self.direccion_base_ints = 0
        self.direccion_base_floats = self.direccion_base_ints + self.rango_espacios
        self.direccion_base_bool = self.direccion_base_floats + self.rango_espacios
        self.direccion_base_str = self.direccion_base_bool + self.rango_espacios
        self.direccion_base_temporales = self.direccion_base_str + self.rango_espacios

        self.espacio_variables_unidimensionales = []
        self.espacio_variables_arreglo = []

        self.direcciones_base = {
            "int": self.direccion_base_ints,
            "float": self.direccion_base_floats,
            "bool": self.direccion_base_bool,
            "str": self.direccion_base_str,
            "temporal": self.direccion_base_temporales
        }

        # para generacion de codigo
        self.contadores_tipo_variables = {"int":  0,
                                          "float": 0,
                                          "bool": 0,
                                          "str": 0,
                                          "temporal": 0
                                          }

        self.contadores_tipo_temporales = {"int":  0,
                                           "float": 0,
                                           "bool": 0,
                                           "str": 0,
                                           "temporal": 0
                                           }

        self.contadores_tipo_constantes = {"int":  0,
                                           "float": 0,
                                           "bool": 0,
                                           "str": 0,
                                           "temporal": 0
                                           }

# importante tener la tabla de variables para poder generar direcciones
