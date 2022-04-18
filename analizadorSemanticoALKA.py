from alkaparser import ALKA_parser

from lark import Token, Tree, tree


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
        ids = get_ids(subtree)
        print(ids)
        # todo
        # Crear diccionario de variables
        # Crear diccionario de funciones
        # Crear funciones getter y setters
        # Crear la clase de analizador semántico que va a contener los diccionarios

        # TODO EXPRESION ESTÁ MAL


def get_ids(subtree: Tree):
    # print(array_tokens[3:-1:2])
    return [token.value for token in filter(lambda t: t.type == "ID",
                                            subtree.scan_values(
                                                lambda v: isinstance(v, Token))  # Los tokens del subtree
                                            )]


programa = """var int : num, b ;
                          
                         main(){}"""

analizador = AnalizadorSemantico(programa)

analizador.analizarArbol()
