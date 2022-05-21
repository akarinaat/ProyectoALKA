# Para saber cuántos de cada un voy a tener
from dataclasses import dataclass


@dataclass
class Memoria:
    rango_espacios: 1000

    direccion_base_ints = 0
    direccion_base_floats = direccion_base_ints + rango_espacios
    direccion_base_bool = direccion_base_floats + rango_espacios
    direccion_base_str = direccion_base_bool + rango_espacios
    direccion_base_temporales = direccion_base_str + rango_espacios

    espacio_variables_unidimensionales = []
    espacio_variables_arreglo = []

    direcciones_base = {
        "int": direccion_base_ints,
        "float": direccion_base_floats,
        "bool": direccion_base_bool,
        "str": direccion_base_str,
        "temporal": direccion_base_temporales
    }

    # para generacion de codigo
    contadores_tipo_unidimensional = {"int":  0,
                                      "float": 0,
                                      "bool": 0,
                                      "str": 0,
                                      "temporal": 0
                                      }

    contadores_tipo_multidimensional = {"int":  0,
                                        "float": 0,
                                        "bool": 0,
                                        "str": 0,
                                        "temporal": 0
                                        }

    # importante tener la tabla de variables para poder generar direcciones
