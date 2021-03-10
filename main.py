import AnalisadorLexico
import Arquivos
import os

lexan = AnalisadorLexico.AnalisadorLexico()
arquivosEntrada = os.listdir("input")
print(arquivosEntrada)
leitor = Arquivos.Arquivos()
texto = ""

for arquivo in arquivosEntrada:
    caminho = "input/" + arquivo
    texto = leitor.ler(caminho)
    print(texto)
    lexan.analisar(texto)


















































