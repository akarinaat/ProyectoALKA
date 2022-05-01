
import pytest 
from Cuadruplos import GeneracionCuadruplos

def test_prueba_basica():
    programa = """ main(){2+3;} """
    generador = GeneracionCuadruplos(programa)
    generador.generar_cuadruplos()
    assert len(generador.listaCuadruplos) > 0

    