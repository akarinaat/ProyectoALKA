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

    contador_ints = 0
    contador_floats = 0
    contador_bool = 0
    contador_str = 0
    contador_temporales = 0
