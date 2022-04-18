from alkaparser import ALKA_parser

from lark import Tree, tree


class AnalizadorSemantico:

    def __init__(self, input) -> None:
        self.directorioVariables = {}  # Directorio de variables
        self.directorioFunciones = {}  # Directorio de funciones
        self.arbol: Tree = ALKA_parser.parse(input)

    def analizarArbol(self):
        for subtree in self.arbol.iter_subtrees():
            if subtree.data == "decvar":
                self.declarar_variable(subtree)

    def declarar_variable(self, subtree: Tree) -> None:
        tipo = subtree.children[1]
        ids = get_ids(subtree.children)
        # todo
        # Crear diccionario de variables
        # Crear diccionario de funciones
        # Crear funciones getter y setters
        # Crear la clase de analizador semántico que va a contener los diccionarios

        # TODO EXPRESION ESTÁ MAL


def get_ids(array_tokens):
    print(array_tokens[3:-1:2])


programa = """var int : num, b ;
                          
                         main(){}"""

analizador = AnalizadorSemantico(programa)

analizador.analizarArbol()
