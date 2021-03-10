class Arquivos:

    def __init__(self):
        pass


    def ler(self, caminho):
        arquivo = open(caminho, 'r')
        texto = ""
        '''for linha in arquivo:
            texto += linha
        '''
        texto = arquivo.readlines()
        return texto

    def escrever(self):
        pass
