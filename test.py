
from Cuadruplos import GeneracionCuadruplos
from analizadorSemanticoALKA import AnalizadorSemantico
from lark import tree

programa = """
        var int:a[1][2][3];

        main(){
            3.52+6.75;
            True;
            False;
            "hola mundo";
        }"""

generador = GeneracionCuadruplos(programa)
generador.generar_cuadruplos_programa()
print(generador.hacer_string_cuadruplos())
print(generador.diccionarioConstates)
# tree.pydot__tree_to_png(analizador.arbol,"test_conParametros.png")
