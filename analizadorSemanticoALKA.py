
from typing import List
from alkaparser import ALKA_parser

from lark import Token, Tree, tree
from dataclasses import dataclass


class SemanticError(Exception):
    pass


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
            self.declarar_variable(nombre, tipo)

    def declarar_variable(self, nombre, tipo):
        # checar si ya existe la variable en la lista de directorios
        for directorio in self.directoriosVariables:
            if nombre in directorio:
                raise SemanticError("ID ya existe")
        # Si no existe declararlo en el último directorio (-1)
        self.directoriosVariables[-1][nombre] = Variable(tipo, nombre)

    def analizar_decfunc(self, subtree: Tree) -> None:

        self.directoriosVariables.append({})
        tipo = subtree.children[0].children[0]
        nombre = subtree.children[1].children[0]
        if nombre in self.directorioFunciones:
            raise SemanticError("funcion ya existe")
        else:
            self.directorioFunciones[nombre] = Funcion(tipo, nombre)
        # declarar los argumentos
        # print(subtree.children[2:-2], len(subtree.children[2:-2]))
        for argumento in chunker(subtree.children[2:-2], 2):
            nombre_argumento = argumento[0].children[0]
            tipo_argumento = argumento[1].children[0]
            self.declarar_variable(nombre_argumento, tipo_argumento)

        decvars = subtree.children[-2]
        estatutos = subtree.children[-1].children

        for decvar in decvars.children:
            self.analizar_decvar(decvar)

        # analizar el cuerpo de la función
        self.analizar_estatutos(estatutos)

    def analizar_estatutos(self, estatutos: List[Tree]) -> None:
        for estatuto in estatutos:
            self.analizar_estatuto(estatuto)

    def analizar_estatuto(self, estatuto: Tree) -> None:
        if estatuto.children[0].data == "expresion":
            self.analizar_expresion(estatuto.children[0])

# regresa booleano si es > o < else el tipo de la exp
    def analizar_expresion(self, expresion: Tree):
        print(expresion.pretty())
        if len(expresion.children) == 1:
            exp = expresion.children[0]
            return self.analizar_exp(exp)
            # si es una comoparación
        elif len(expresion.children) == 3:
            exp1 = expresion.children[0]
            exp2 = expresion.children[2]
            tipo_exp1 = self.analizar_exp(exp1)
            tipo_exp2 = self.analizar_exp(exp2)

            if tipo_exp1 == tipo_exp2:
                return "bool"
            else:
                raise SemanticError("No se pueden comparar")

        else:
            raise SemanticError("Expresion mal formada")

    def analizar_exp(self, exp: Tree):
        return self.analizar_operacion_binaria(exp, self.analizar_termino)

    def analizar_termino(self, termino: Tree):
        return self.analizar_operacion_binaria(termino, self.analizar_factor)

    def analizar_factor(self, factor: Tree):
        if len(factor.children) == 1:
            expresion = factor.children[0]
            if expresion.data == "expresion":
               return self.analizar_expresion(expresion)
            else:
                return self.analizar_atomo(expresion)
        elif len(factor.children) == 2:
            atomo = factor.children[2]
            return self.analizar_atomo(atomo)

        else:
            raise SemanticError("Factor mal formad")

    def analizar_atomo(self, atomo: Tree):
        atomo = atomo.children[0]
        if isinstance(atomo, Token):           
            print(atomo.type)
            if atomo.type == "CTEI":
                return "int"
            elif atomo.type == "CTEF":
                return "float"
            elif atomo.type == "CTESTR":
                return "string"
        else:
            print("no es token")
         
        

    def analizar_operacion_binaria(self, operacion: Tree, funcion):
        lista_operandos = operacion.children[::2]
        tipo = funcion(lista_operandos[0])
        # para que no se cheque el primero dos veces
        for operando in lista_operandos[1:]:
            if funcion(operando) != tipo:
                raise SemanticError("Tipos incompatibles")

        return tipo


def get_token(subtree: Tree, token_type: str):
    return [token.value for token in filter(lambda t: t.type == token_type,
                                            subtree.scan_values(
                                                lambda v: isinstance(v, Token))  # Los tokens del subtree
                                            )]


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
