import Regex
class AnalisadorSintatico:

    def __init__(self):
        self.texto = ""
        self.numero_linha = []
        self.tipo_token = []
        self.valor_token = []
        self.indice_token = 0
        self.tipos = ['int', 'real', 'boolean', 'string', 'struct']
        self.booleanLiteral = ['true', 'false']

    def fimArquivo(self):
        if self.indice_token >= len(self.valor_token):
            return True
        else:
            return False

    def analisar(self, texto):
        self.texto = texto
        # print("--------------------------TEXTO SINTATICO------------------------")
        # print(texto)
        # print("-----------------------------------------------------------------")
        for linha in texto:
            # print(linha)
            self.numero_linha.append(linha.split(' ')[0])
            self.tipo_token.append(linha.split(' ')[1])
            aux_valor = linha.split(' ')[2]
            self.valor_token.append(aux_valor.split('\n')[0])
        # print(numero_linha)
        # print(tipo_token)
        # print(valor_token)
        self.Program()

    def Program(self):
        self.Global_Decl()
        self.Decls()
        self.Start()

    def Global_Decl(self):
        if not self.fimArquivo() and self.valor_token[self.indice_token] == 'const':
            self.indice_token += 1
            self.Const_Decl()
            if not self.fimArquivo() and self.valor_token[self.indice_token] == 'var':
                self.indice_token += 1
                self.Var_Decl()
        elif not self.fimArquivo() and self.valor_token[self.indice_token] == 'var':
            self.indice_token += 1
            self.Var_Decl()
            if not self.fimArquivo() and self.valor_token[self.indice_token] == 'const':
                self.indice_token += 1
                self.Const_Decl()

    def Const_Decl(self):
        if not self.fimArquivo() and self.valor_token[self.indice_token] == '{':
            self.indice_token += 1
            self.ConstList()
            if not self.fimArquivo() and self.valor_token[self.indice_token] == '}':
                self.indice_token += 1
            else:
                if not self.fimArquivo():
                    print('entrou aq')
                    print(f'Linha {self.numero_linha[self.indice_token]}'
                          f' - Erro Sintático'
                          f' - Esperava: ', '}', f' / Recebido: {self.valor_token[self.indice_token]}')
                    self.indice_token += 1
                else:
                    self.erro_fim_arquivo_inesperado()
        else:
            if not self.fimArquivo():
                print(f'Linha {self.numero_linha[self.indice_token]}'
                      f' - Erro Sintático'
                      f' - Esperava: ', '{', f' / Recebido: {self.valor_token[self.indice_token]}')
                self.indice_token += 1
            else:
                self.erro_fim_arquivo_inesperado()

    def ConstList(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in self.tipos:
                self.indice_token += 1
                self.Const()
                self.ConstList()
        else:
            self.erro_fim_arquivo_inesperado()

    def Const(self):
        if not self.fimArquivo():
            if self.tipo_token[self.indice_token] == 'IDE':
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == '=':
                        self.indice_token += 1
                        self.Value()
                        self.Delimiter_Const()
                    else:
                        print(f'Linha {self.numero_linha[self.indice_token]}'
                              f' - Erro Sintático'
                              f' - Esperava: ', '=', f' / Recebido: {self.valor_token[self.indice_token]}')
                        self.indice_token += 1
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                print(f'Linha {self.numero_linha[self.indice_token]}'
                      f' - Erro Sintático'
                      f' - Esperava: ', 'Identificador', f' / Recebido: {self.valor_token[self.indice_token]}')
                self.indice_token += 1
        else:
            self.erro_fim_arquivo_inesperado()

    def Value(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in self.booleanLiteral:
                self.indice_token += 1
            elif self.tipo_token[self.indice_token] == 'NRO':
                self.indice_token += 1
            elif self.tipo_token[self.indice_token] == 'CAD':
                self.indice_token += 1
            else:
                print(f'Linha {self.numero_linha[self.indice_token]}'
                      f' - Erro Sintático'
                      f' - Esperava: ', 'Número, Boolean Literal ou StringLiteral', f' / Recebido: {self.valor_token[self.indice_token]}')
                self.indice_token += 1
        else:
            self.erro_fim_arquivo_inesperado()

    def Delimiter_Const(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == ',':
                self.indice_token += 1
                self.Const()
            elif self.valor_token[self.indice_token] == ';':
                self.indice_token += 1
            else:
                self.erro(self.numero_linha[self.indice_token], ', ou ;', self.valor_token[self.indice_token], 'Delimiter_Const')
        else:
            self.erro_fim_arquivo_inesperado()

    def Var_Decl(self):
        if self.valor_token[self.indice_token] == '{':
            self.indice_token += 1
            self.VariablesList()
            if not self.fimArquivo() and self.valor_token[self.indice_token] == '}':
                self.indice_token += 1
            else:
                if not self.fimArquivo():

                    print(f'Linha {self.numero_linha[self.indice_token]}'
                          f' - Erro Sintático'
                          f' - Esperava: ', '}', f' / Recebido: {self.valor_token[self.indice_token]}')
                    self.indice_token += 1
                else:
                    self.erro_fim_arquivo_inesperado()
        else:
            if not self.fimArquivo():
                print(f'Linha {self.numero_linha[self.indice_token]}'
                      f' - Erro Sintático'
                      f' - Esperava: ', '{', f' / Recebido: {self.valor_token[self.indice_token]}')
                self.indice_token += 1
            else:
                self.erro_fim_arquivo_inesperado()

    def VariablesList(self):
        pass

    def Start(self):
        pass

    def Decls(self):
        pass

    def Decl(self):
        pass

    def erro(self, numero_linha, esperava, recebido, nao_terminal):
        print(f'Linha {int(numero_linha) - 1}'
              f' - Erro Sintático'
              f' - Esperava: ', f'{esperava}', f' / Recebido: {recebido}')
        self.procurar_token_sincronizacao(nao_terminal)

    def procurar_token_sincronizacao(self, nao_terminal):
        conjuntoFollow = self.conjunto_Follow(nao_terminal)
        while not self.fimArquivo() and self.valor_token[self.indice_token] not in conjuntoFollow:
            self.indice_token += 1
        if self.fimArquivo():
            self.erro_fim_arquivo_inesperado()
        else:
            self.reiniciar(nao_terminal, self.valor_token[self.indice_token])

    def conjunto_Follow(self, nao_terminal):
        if nao_terminal == 'Delimiter_Const':
            return ['int', 'real', 'boolean', 'string', 'struct', '}']

    def reiniciar(self, nao_terminal, token_atual):
        if nao_terminal == 'Delimiter_Const':
            if token_atual == '}':
                self.Global_Decl()
            else:
                self.ConstList()

    def erro_fim_arquivo_inesperado(self):
        if self.fimArquivo():
            print(f'Linha {self.numero_linha[len(self.numero_linha) - 1]}'
                  f' - Erro Sintático'
                  f' - Esperava: ', 'Token', f' / Recebido: EOF')
            exit()