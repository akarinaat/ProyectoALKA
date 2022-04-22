from xml.dom import SYNTAX_ERR
from alkaparser import ALKA_parser

from lark import Token, Tree, tree
from dataclasses import dataclass


@dataclass  # son para guardar información
class Variable:

    tipo: str
    nombre: str

# de parse tree a ast ()


class AnalizadorSemantico:

    def __init__(self, input) -> None:
        self.directorioVariables = {}  # Directorio de variables
        self.directorioFunciones = {}  # Directorio de funciones
        self.arbol: Tree = ALKA_parser.parse(input)

    def analizarArbol(self):
        for subtree in self.arbol.iter_subtrees():
            if subtree.data == "decvar":
                self.declarar_variable(subtree)
                if subtree.data == "decfunc":
                    self.declarar_funcion(subtree)

    def declarar_variable(self, subtree: Tree) -> None:
        tipo = subtree.children[1].children[0]
        ids = get_ids(subtree)
        for id in ids:
            # checar si ya existe la variable
            if id in self.directorioVariables:
                raise SyntaxError("ID ya existe")
            else:
                self.directorioVariables[id] = Variable(tipo, id)

    def declarar_funcion(self, subtree: Tree) -> None:
        print(subtree)
        # tipo = subtree.children[1].children[0]
        # ids = get_ids(subtree)
        # for id in ids:
        #     # checar si ya existe la variable
        #     if id in self.directorioVariables:
        #         raise SyntaxError("ID ya existe")
        #     else:
        #         self.directorioVariables[id] = Variable(tipo, id)

        # print(ids)
        # todo
        # Crear funciones getter y setters


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
