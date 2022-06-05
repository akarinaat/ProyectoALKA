
from Cuadruplos import GeneracionCuadruplos
from analizadorSemanticoALKA import AnalizadorSemantico
from lark import tree

programa = """
        

        main(){
            var int:a,b;
            a = 3;
            b = 8;
            return a+b;

        }"""

generador = GeneracionCuadruplos(programa)
generador.generar_cuadruplos_programa()
# print(generador.hacer_string_cuadruplos())
# print(generador.diccionarioConstates)
tree.pydot__tree_to_png(generador.arbol,"test_sumasimple.png")
