'''
Versão Python: 3.8
'''
import AnalisadorLexico
import AnalisadorSintatico
import Arquivos
import os

lexan = AnalisadorLexico.AnalisadorLexico()
arquivosEntrada = os.listdir("input")
print(arquivosEntrada)
leitor = Arquivos.Arquivos()
texto = ""
contadorArquivo = 1
for arquivo in arquivosEntrada:
    caminho = "input/" + arquivo
    texto = leitor.ler(caminho)
    print(texto)
    resposta, teve_erro_lexico = lexan.analisar(texto)
    caminho_saida_lexico = f"output/saida{contadorArquivo}.txt"
    leitor.escrever(caminho_saida_lexico, resposta)
    if not teve_erro_lexico:
        caminho_entrada_sintatico = caminho_saida_lexico
        texto_sintatico = leitor.ler(caminho_entrada_sintatico)
        sinan = AnalisadorSintatico.AnalisadorSintatico(resposta)
        resposta = sinan.analisar(texto_sintatico)
        leitor.escrever(caminho_saida_lexico, resposta)
    contadorArquivo += 1
