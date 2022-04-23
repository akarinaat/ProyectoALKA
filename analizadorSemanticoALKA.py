from xml.dom import SYNTAX_ERR
from alkaparser import ALKA_parser

from lark import Token, Tree, tree
from dataclasses import dataclass


@dataclass  # son para guardar información
class Variable:

    tipo: str
    nombre: str


@dataclass
class Funcion:

    tipo: str
    nombre: str


class AnalizadorSemantico:

    def __init__(self, input) -> None:
        self.directorioVariables = {}  # Directorio de variables
        self.directorioFunciones = {}  # Directorio de funciones
        self.arbol: Tree = ALKA_parser.parse(input)

    def analizarArbol(self):
        for subtree in self.arbol.iter_subtrees():
            if subtree.data == "decvar":
                self.declarar_variable(subtree)
            elif subtree.data == "decfunc":
                self.declarar_funcion(subtree)

    def declarar_variable(self, subtree: Tree) -> None:
        tipo = subtree.children[0].children[0]
        print(subtree)
        ids = get_ids(subtree)
        for id in ids:
            # checar si ya existe la variable
            if id in self.directorioVariables:
                raise SyntaxError("ID ya existe")
            else:
                self.directorioVariables[id] = Variable(tipo, id)

    def declarar_funcion(self, subtree: Tree) -> None:
        print(subtree.pretty())
        tipo = subtree.children[0].children[0]
        nombre = subtree.children[1].children[0]
        if nombre in self.directorioFunciones:
            raise SyntaxError("funcion ya existe")
        else:
            self.directorioFunciones[nombre] = Funcion(tipo, nombre)


def get_ids(subtree: Tree):
    return [token.value for token in filter(lambda t: t.type == "ID",
                                            subtree.scan_values(
                                                lambda v: isinstance(v, Token))  # Los tokens del subtree
                                            )]
