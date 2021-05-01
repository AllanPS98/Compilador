import Sync


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
        self.ConstBlock()
        self.VarBlock()
        self.Decls()
        self.StartBlock()
        self.Decls()

    def StartBlock(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == 'start':
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == '(':
                        self.indice_token += 1
                        if not self.fimArquivo():
                            if self.valor_token[self.indice_token] == ')':
                                self.indice_token += 1
                                if not self.fimArquivo():
                                    if self.valor_token[self.indice_token] == '{':
                                        self.indice_token += 1
                                        self.FuncBlock()
                                        if not self.fimArquivo():
                                            if self.valor_token[self.indice_token] == '}':
                                                self.indice_token += 1
                                                self.Decls()
                                            else:
                                                self.erro(self.indice_token, '}', self.valor_token[self.indice_token],
                                                          'StartBlock')
                                        else:
                                            self.erro_fim_arquivo_inesperado()
                                    else:
                                        self.erro(self.indice_token, '{', self.valor_token[self.indice_token],
                                                  'StartBlock')
                                else:
                                    self.erro_fim_arquivo_inesperado()
                            else:
                                self.erro(self.indice_token, ')', self.valor_token[self.indice_token], 'StartBlock')
                        else:
                            self.erro_fim_arquivo_inesperado()
                    else:
                        self.erro(self.indice_token, '(', self.valor_token[self.indice_token], 'StartBlock')
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                self.erro(self.indice_token, 'start', self.valor_token[self.indice_token], 'StartBlock')
        else:
            self.erro_fim_arquivo_inesperado()

    def Decls(self):
        pass

    def Decl(self):
        pass

    def StructBlock(self):
        pass

    def Extends(self):
        pass

    def ConstBlock(self):
        pass

    def VarBlock(self):
        pass

    def Typedef(self):
        pass

    def VarDecls(self):
        pass

    def VarDecl(self):
        pass

    def VarId(self):
        pass

    def Var(self):
        pass

    def VarList(self):
        pass

    def ConstDecls(self):
        pass

    def ConstDecl(self):
        pass

    def ConstId(self):
        pass

    def Const(self):
        pass

    def ConstList(self):
        pass

    def DeclAtribute(self):
        pass

    def ArrayDecl(self):
        pass

    def ArrayVector(self):
        pass

    def ArrayDef(self):
        pass

    def ArrayExpr(self):
        pass

    def Array(self):
        pass

    def Index(self):
        pass

    def Arrays(self):
        pass

    def Assign(self):
        pass

    def Access(self):
        pass

    def Accesses(self):
        pass

    def Args(self):
        pass

    def ArgsList(self):
        pass

    def FuncDecl(self):
        pass

    def ProcDecl(self):
        pass

    def ParamType(self):
        pass

    def Params(self):
        pass

    def Param(self):
        pass

    def ParamsList(self):
        pass

    def ParamArrays(self):
        pass

    def ParamMultArrays(self):
        pass

    def FuncBlock(self):
        pass

    def FuncStms(self):
        pass

    def FuncStm(self):
        pass

    def ElseStm(self):
        pass

    def FuncNormalStm(self):
        pass

    def VarStm(self):
        pass

    def StmId(self):
        pass

    def StmScope(self):
        pass

    def StmCmd(self):
        pass

    def Expr(self):
        pass

    def Or(self):
        pass

    def Or_(self):
        pass

    def And(self):
        pass

    def And_(self):
        pass

    def Equate(self):
        pass

    def Equate_(self):
        pass

    def Compare(self):
        pass

    def Compare_(self):
        pass

    def Add(self):
        pass

    def Add_(self):
        pass

    def Mult(self):
        pass

    def Mult_(self):
        pass

    def Unary(self):
        pass

    def Value(self):
        pass

    def IdValue(self):
        pass

    def LogExpr(self):
        pass

    def LogOr(self):
        pass

    def LogOr_(self):
        pass

    def LogAnd(self):
        pass

    def LogAnd_(self):
        pass

    def LogEquate(self):
        pass

    def LogEquate_(self):
        pass

    def LogCompare(self):
        pass

    def LogCompare_(self):
        pass

    def LogUnary(self):
        pass

    def LogValue(self):
        pass

    def erro(self, numero_linha, esperava, recebido, nao_terminal):
        print(f'Linha {int(numero_linha) - 1}'
              f' - Erro Sintático'
              f' - Esperava: ', f'{esperava}', f' / Recebido: {recebido}')
        self.procurar_token_sincronizacao(nao_terminal)

    def procurar_token_sincronizacao(self, nao_terminal):
        conjuntoFollow = Sync.Sync().sync_tokens[nao_terminal]
        while not self.fimArquivo():
            if self.valor_token[self.indice_token] not in conjuntoFollow \
                    or self.tipo_token[self.indice_token] not in conjuntoFollow:
                break
            self.indice_token += 1
        if self.fimArquivo():
            self.erro_fim_arquivo_inesperado()
        else:
            self.reiniciar(nao_terminal, self.valor_token[self.indice_token])

    def reiniciar(self, nao_terminal, token_atual):
        if nao_terminal == 'StartBlock':
            self.ErroStartBlock(token_atual)

    def ErroStartBlock(self, token_atual):
        if token_atual in ['function', 'procedure', 'struct', 'typedef']:
            self.Decls()
        elif token_atual == '{':
            self.indice_token += 1
            self.FuncBlock()
            self.Decls()
        elif token_atual == ['if', 'while', 'return', 'local', 'global', 'print', 'read', 'var'] \
                or self.tipo_token[self.indice_token] == 'IDE':
            self.FuncBlock()
            self.Decls()

    def erro_fim_arquivo_inesperado(self):
        if self.fimArquivo():
            print(f'Linha {self.numero_linha[len(self.numero_linha) - 1]}'
                  f' - Erro Sintático'
                  f' - Esperava: ', 'Token', f' / Recebido: EOF')
            exit()
