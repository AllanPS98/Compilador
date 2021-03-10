import re


class Regex:
    def __init__(self):
        pass

    def identificaComentarioBloco(self, palavra):
        x = re.search("[\/][*][\s\S]*[*][\/]", palavra)
        if x:
            return True
        return False

    def identificaComentarioLinha(self, palavra):
        x = re.search("[\/][\/][\s\S]*", palavra)
        return x

    def identificaIdentificador(self, palavra):
        x = re.search("\A[a-zA-Z]\w*\Z", palavra)
        if x:
            return True
        return False

    def identificadorNumero(self, palavra):
        x = re.search("[0-9]+(\.[0-9]+$)*", palavra)
        if len(x.string) == len(x.group()) and x:
            return True
        return False

    def identificadorNumeroNegativo(self, palavra):
        x = re.search("\-[0-9]+(\.[0-9]+$)*", palavra)
        if len(x.string) == len(x.group()) and x:
            return True
        return False

    def identificadorCadeiaCaracteres(self, palavra):
        x = re.search("\"[a-zA-Z0-9\ \!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\]\\\^\_\`\{\}\|\~]*\"", palavra)
        if x:
            return True
        return False
