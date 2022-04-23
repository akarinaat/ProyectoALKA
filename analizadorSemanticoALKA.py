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
        self.directoriosVariables = [{}]  # Directorio de variables
        self.directorioFunciones = {}  # Directorio de funciones
        self.arbol: Tree = ALKA_parser.parse(input)

    def analizarArbol(self):
        for subtree in self.arbol.children:
            # print(subtree)
            if subtree.data == "decvars":
                self.analizar_decvars(subtree)
            elif subtree.data == "decfuncs":
                self.analizar_decfuncs(subtree)

    def analizar_decvars(self, subtree: Tree) -> None:
        for decvar in subtree.children:
            self.analizar_decvar(decvar)

    def analizar_decfuncs(self, subtree: Tree) -> None:
        for decfunc in subtree.children:
            self.analizar_decfunc(decfunc)

    def analizar_decvar(self, subtree: Tree) -> None:
        tipo = subtree.children[0].children[0]
        ids = get_token(subtree, "ID")
        for nombre in ids:
            print(nombre, tipo)
            self.declarar_variable(nombre, tipo)

    def declarar_variable(self, nombre, tipo):
        # checar si ya existe la variable en la lista de directorios
        for directorio in self.directoriosVariables:
            if nombre in directorio:
                raise SyntaxError("ID ya existe")
        # Si no existe declararlo en el último directorio (-1)
        self.directoriosVariables[-1][nombre] = Variable(tipo, nombre)

    def analizar_decfunc(self, subtree: Tree) -> None:

        self.directoriosVariables.append({})
        tipo = subtree.children[0].children[0]
        nombre = subtree.children[1].children[0]
        if nombre in self.directorioFunciones:
            raise SyntaxError("funcion ya existe")
        else:
            self.directorioFunciones[nombre] = Funcion(tipo, nombre)
        # declarar los argumentos
        # print(subtree.children[2:-2], len(subtree.children[2:-2]))
        for argumento in chunker(subtree.children[2:-2], 2):
            nombre_argumento = argumento[0].children[0]
            tipo_argumento = argumento[1].children[0]
            self.declarar_variable(nombre_argumento, tipo_argumento)
            print(nombre_argumento, tipo_argumento)

        decvars = subtree.children[-2]
        estatutos = subtree.children[-1]

        for decvar in decvars.children:
            self.analizar_decvar(decvar)

        for estatuto in estatutos:
            self.analizar_estatuto(estatuto)
        # analizar el cuerpo de la función

    def analizar_estatuto(self, subtree: Tree) -> None:
        pass


def get_token(subtree: Tree, token_type: str):
    return [token.value for token in filter(lambda t: t.type == token_type,
                                            subtree.scan_values(
                                                lambda v: isinstance(v, Token))  # Los tokens del subtree
                                            )]


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
