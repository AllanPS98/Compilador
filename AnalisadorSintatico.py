import Sync


class AnalisadorSintatico:

    def __init__(self, resposta):
        self.texto = ""
        self.numero_linha = []
        self.tipo_token = []
        self.valor_token = []
        self.indice_token = 0
        self.tipos = ['int', 'real', 'boolean', 'string', 'struct']
        self.booleanLiteral = ['true', 'false']
        self.teve_erro = False
        self.resposta = resposta

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
        if not self.teve_erro:
            self.resposta.append('Arquivo compilado com sucesso!\n')
        return self.resposta

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
                                            else:
                                                self.erro(self.numero_linha[self.indice_token], '}',
                                                          self.valor_token[self.indice_token],
                                                          'StartBlock')
                                        else:
                                            self.erro_fim_arquivo_inesperado()
                                    else:
                                        self.erro(self.numero_linha[self.indice_token], '{',
                                                  self.valor_token[self.indice_token],
                                                  'StartBlock')
                                else:
                                    self.erro_fim_arquivo_inesperado()
                            else:
                                self.erro(self.numero_linha[self.indice_token], ')',
                                          self.valor_token[self.indice_token], 'StartBlock')
                        else:
                            self.erro_fim_arquivo_inesperado()
                    else:
                        self.erro(self.numero_linha[self.indice_token], '(', self.valor_token[self.indice_token],
                                  'StartBlock')
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                self.erro(self.numero_linha[self.indice_token], 'start', self.valor_token[self.indice_token],
                          'StartBlock')
        else:
            # print('entrou aq 32')
            self.erro_fim_arquivo_inesperado()

    def Decls(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['procedure', 'function', 'struct', 'typedef']:
                self.Decl()
                self.Decls()

    def Decl(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['struct', 'typedef']:
                self.StructBlock()
            elif self.valor_token[self.indice_token] == 'procedure':
                self.ProcDecl()
            elif self.valor_token[self.indice_token] == 'function':
                self.FuncDecl()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'function, procedure, struct, typedef',
                          self.valor_token[self.indice_token],
                          'Decl')
        else:
            self.erro_fim_arquivo_inesperado()

    def StructBlock(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == 'struct':
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.tipo_token[self.indice_token] == 'IDE':
                        self.indice_token += 1
                        self.Extends()
                        if not self.fimArquivo():
                            if self.valor_token[self.indice_token] == '{':
                                self.indice_token += 1
                                self.VarDecls()
                                if not self.fimArquivo():
                                    if self.valor_token[self.indice_token] == '}':
                                        self.indice_token += 1
                                    else:
                                        self.erro(self.numero_linha[self.indice_token], '}',
                                                  self.valor_token[self.indice_token],
                                                  'StructBlock')
                                else:
                                    self.erro_fim_arquivo_inesperado()
                            else:
                                self.erro(self.numero_linha[self.indice_token], '{',
                                          self.valor_token[self.indice_token],
                                          'StructBlock')
                        else:
                            self.erro_fim_arquivo_inesperado()
                    else:
                        self.erro(self.numero_linha[self.indice_token], 'Type(Identifier)',
                                  self.valor_token[self.indice_token],
                                  'StructBlock')
                else:
                    self.erro_fim_arquivo_inesperado()
            elif self.valor_token[self.indice_token] == 'typedef':
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == 'struct':
                        self.indice_token += 1
                        self.Extends()
                        if not self.fimArquivo():
                            if self.valor_token[self.indice_token] == '{':
                                self.indice_token += 1
                                self.VarDecls()
                                if not self.fimArquivo():
                                    if self.valor_token[self.indice_token] == '}':
                                        self.indice_token += 1
                                        if not self.fimArquivo():
                                            if self.tipo_token[self.indice_token] == 'IDE':
                                                self.indice_token += 1
                                                if not self.fimArquivo():
                                                    if self.valor_token[self.indice_token] == ';':
                                                        self.indice_token += 1
                                                    else:
                                                        self.erro(self.numero_linha[self.indice_token],
                                                                  ';',
                                                                  self.valor_token[self.indice_token],
                                                                  'StructBlock')
                                                else:
                                                    self.erro_fim_arquivo_inesperado()
                                            else:
                                                self.erro(self.numero_linha[self.indice_token], 'Type(Identifier)',
                                                          self.valor_token[self.indice_token],
                                                          'StructBlock')
                                        else:
                                            self.erro_fim_arquivo_inesperado()
                                    else:
                                        self.erro(self.numero_linha[self.indice_token], '}',
                                                  self.valor_token[self.indice_token],
                                                  'StructBlock')
                                else:
                                    self.erro_fim_arquivo_inesperado()
                            else:
                                self.erro(self.numero_linha[self.indice_token], '{',
                                          self.valor_token[self.indice_token],
                                          'StructBlock')
                        else:
                            self.erro_fim_arquivo_inesperado()
            else:
                self.erro(self.numero_linha[self.indice_token], 'struct, typedef',
                          self.valor_token[self.indice_token],
                          'StructBlock')
        else:
            self.erro_fim_arquivo_inesperado()

    def Extends(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == 'extends':
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.tipo_token[self.indice_token] == 'IDE':
                        self.indice_token += 1
                    else:
                        self.erro(self.numero_linha[self.indice_token], 'Type(Identifier)',
                                  self.valor_token[self.indice_token],
                                  'Extends')
                else:
                    self.erro_fim_arquivo_inesperado()

    def ConstBlock(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == 'const':
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == '{':
                        self.indice_token += 1
                        self.ConstDecls()
                        if not self.fimArquivo():
                            if self.valor_token[self.indice_token] == '}':
                                self.indice_token += 1
                            else:
                                self.erro(self.numero_linha[self.indice_token], '}',
                                          self.valor_token[self.indice_token],
                                          'ConstBlock')
                        else:
                            self.erro_fim_arquivo_inesperado()
                    else:
                        self.erro(self.numero_linha[self.indice_token], '{', self.valor_token[self.indice_token],
                                  'ConstBlock')
                else:
                    self.erro_fim_arquivo_inesperado()

    def VarBlock(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == 'var':
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == '{':
                        self.indice_token += 1
                        self.VarDecls()
                        if not self.fimArquivo():
                            if self.valor_token[self.indice_token] == '}':
                                self.indice_token += 1
                            else:
                                self.erro(self.numero_linha[self.indice_token], '}',
                                          self.valor_token[self.indice_token],
                                          'VarBlock')
                        else:
                            self.erro_fim_arquivo_inesperado()
                    else:
                        self.erro(self.numero_linha[self.indice_token], '{', self.valor_token[self.indice_token],
                                  'VarBlock')
                else:
                    self.erro_fim_arquivo_inesperado()

    def Typedef(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == 'typedef':
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.valor_token in ['int', 'real', 'boolean', 'string', 'struct']:
                        if self.valor_token[self.indice_token] == 'struct':
                            self.indice_token += 1
                            if not self.fimArquivo():
                                if self.tipo_token[self.indice_token] == 'IDE':
                                    self.indice_token += 1
                                else:
                                    self.erro(self.numero_linha[self.indice_token], 'Type(Identifier)',
                                              self.valor_token[self.indice_token],
                                              'Typedef')
                            else:
                                self.erro_fim_arquivo_inesperado()
                        self.indice_token += 1
                        if not self.fimArquivo():
                            if self.tipo_token[self.indice_token] == 'IDE':
                                self.indice_token += 1
                                if not self.fimArquivo():
                                    if self.valor_token[self.indice_token] == ';':
                                        self.indice_token += 1
                                    else:
                                        self.erro(self.numero_linha[self.indice_token], ';',
                                                  self.valor_token[self.indice_token],
                                                  'Typedef')
                                else:
                                    self.erro_fim_arquivo_inesperado()
                            else:
                                self.erro(self.numero_linha[self.indice_token], 'Type(Identifier)',
                                          self.valor_token[self.indice_token],
                                          'Typedef')
                        else:
                            self.erro_fim_arquivo_inesperado()
                    else:
                        self.erro(self.numero_linha[self.indice_token], 'int, real, boolean, string, struct',
                                  self.valor_token[self.indice_token],
                                  'Typedef')
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                self.erro(self.numero_linha[self.indice_token], 'typedef',
                          self.valor_token[self.indice_token],
                          'Typedef')
        else:
            self.erro_fim_arquivo_inesperado()

    def VarDecls(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['int', 'real', 'boolean', 'string', 'struct', 'typedef'] \
                    or self.tipo_token[self.indice_token] == 'IDE':
                self.VarDecl()
                self.VarDecls()

    def VarDecl(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['int', 'real', 'boolean', 'string']:
                self.indice_token += 1
                self.Var()
                self.VarList()
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == ';':
                        self.indice_token += 1
                    else:
                        self.erro(self.numero_linha[self.indice_token], ';',
                                  self.valor_token[self.indice_token],
                                  'VarDecl')
                else:
                    self.erro_fim_arquivo_inesperado()
            elif self.valor_token[self.indice_token] == 'struct':
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.tipo_token[self.indice_token] == 'IDE':
                        self.indice_token += 1
                        self.Var()
                        self.VarList()
                        if not self.fimArquivo():
                            if self.valor_token[self.indice_token] == ';':
                                self.indice_token += 1
                            else:
                                self.erro(self.numero_linha[self.indice_token], ';',
                                          self.valor_token[self.indice_token],
                                          'VarDecl')
                        else:
                            self.erro_fim_arquivo_inesperado()
            elif self.valor_token[self.indice_token] == 'typedef':
                self.Typedef()
            elif self.tipo_token[self.indice_token] == 'IDE':
                self.indice_token += 1
                self.VarId()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'int, real, boolean, string, struct, typedef, Type(Identifier)',
                          self.valor_token[self.indice_token],
                          'VarDecl')
        else:
            self.erro_fim_arquivo_inesperado()

    def VarId(self):
        if not self.fimArquivo():
            if self.tipo_token[self.indice_token] == 'IDE':
                self.Var()
            elif self.valor_token[self.indice_token] in ['=', '[', '.', '(']:
                self.StmId()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          '=, [, ., (, Type(Identifier)',
                          self.valor_token[self.indice_token],
                          'VarId')
        else:
            self.erro_fim_arquivo_inesperado()

    def Var(self):
        if not self.fimArquivo():
            if self.tipo_token[self.indice_token] == 'IDE':
                self.indice_token += 1
                self.Arrays()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(Identifier)',
                          self.valor_token[self.indice_token],
                          'Var')
        else:
            self.erro_fim_arquivo_inesperado()

    def VarList(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == ',':
                self.indice_token += 1
                self.Var()
                self.VarList()
            elif self.valor_token[self.indice_token] == '=':
                self.indice_token += 1
                self.Expr()
                self.VarList()

    def ConstDecls(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['string', 'int', 'real', 'boolean']:
                self.ConstDecl()
                self.ConstDecls()

    def ConstDecl(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['string', 'int', 'real', 'boolean']:
                self.indice_token += 1
                self.Const()
                self.ConstList()
            else:
                self.erro(self.numero_linha[self.indice_token], 'string, int, real, boolean',
                          self.valor_token[self.indice_token],
                          'ConstDecl')
        else:
            self.erro_fim_arquivo_inesperado()

    def Const(self):
        if not self.fimArquivo():
            if self.tipo_token[self.indice_token] == 'IDE':
                self.indice_token += 1
                self.Arrays()
            else:
                self.erro(self.numero_linha[self.indice_token], 'Type(Identifier)', self.valor_token[self.indice_token],
                          'Const')
        else:
            self.erro_fim_arquivo_inesperado()

    def ConstList(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == ',':
                self.indice_token += 1
                self.Const()
                self.ConstList()
            elif self.valor_token[self.indice_token] == '=':
                self.indice_token += 1
                self.DeclAtribute()
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == ';':
                        self.indice_token += 1
                    else:
                        self.erro(self.numero_linha[self.indice_token], ';',
                                  self.valor_token[self.indice_token], 'ConstList')
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                self.erro(self.numero_linha[self.indice_token], ', ou =',
                          self.valor_token[self.indice_token], 'ConstList')
        else:
            self.erro_fim_arquivo_inesperado()

    def DeclAtribute(self):
        if not self.fimArquivo():
            if self.tipo_token[self.indice_token] in ['IDE', 'CAD', 'NRO'] \
                    or self.valor_token[self.indice_token] in ['true', 'false']:
                self.indice_token += 1
            elif self.valor_token[self.indice_token] == '{':
                self.ArrayDecl()
            else:
                self.erro(self.numero_linha[self.indice_token], 'Type(Identifier), Type(String), Type(Boolean), '
                                                                'Type(Array)',
                          self.valor_token[self.indice_token], 'DeclAtribute')
        else:
            self.erro_fim_arquivo_inesperado()

    def ArrayDecl(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '{':
                self.indice_token += 1
                self.ArrayDef()
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == '}':
                        self.indice_token += 1
                        self.ArrayVector()
                    else:
                        self.erro(self.numero_linha[self.indice_token], '}',
                                  self.valor_token[self.indice_token], 'ArrayDecl')
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                self.erro(self.numero_linha[self.indice_token], '{',
                          self.valor_token[self.indice_token], 'ArrayDecl')
        else:
            self.erro_fim_arquivo_inesperado()

    def ArrayVector(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == ',':
                self.indice_token += 1
                self.ArrayDecl()

    def ArrayDef(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['false', 'local', 'true', '!', '(', 'global'] \
                    or self.tipo_token[self.indice_token] in ['CAD', 'IDE']:
                self.indice_token += 1
                self.Expr()
                self.ArrayExpr()
            else:
                self.erro(self.numero_linha[self.indice_token], 'Type(Identifier), Type(String), Type(Boolean), global'
                                                                ', local, !, (',
                          self.valor_token[self.indice_token], 'ArrayDef')
        else:
            self.erro_fim_arquivo_inesperado()

    def ArrayExpr(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == ',':
                self.indice_token += 1
                self.ArrayDef()

    def Array(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '[':
                self.indice_token += 1
                self.Index()
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == ']':
                        self.indice_token += 1
                    else:
                        self.erro(self.numero_linha[self.indice_token], ']',
                                  self.valor_token[self.indice_token], 'Array')
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                self.erro(self.numero_linha[self.indice_token], '[',
                          self.valor_token[self.indice_token], 'Array')
        else:
            self.erro_fim_arquivo_inesperado()

    def Index(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['false', 'local', 'true', '!', '(', 'global'] \
                    or self.tipo_token[self.indice_token] in ['CAD', 'IDE', 'NRO']:
                self.Expr()

    def Arrays(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '[':
                self.Array()
                self.Arrays()

    def Assign(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '=':
                self.indice_token += 1
                self.Expr()
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == ';':
                        self.indice_token += 1
                    else:
                        self.erro(self.numero_linha[self.indice_token], ';',
                                  self.valor_token[self.indice_token], 'Assign')
                else:
                    self.erro_fim_arquivo_inesperado()
            elif self.valor_token[self.indice_token] in ['++', '--']:
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == ';':
                        self.indice_token += 1
                    else:
                        self.erro(self.numero_linha[self.indice_token], ';',
                                  self.valor_token[self.indice_token], 'Assign')
            else:
                self.erro(self.numero_linha[self.indice_token], '=, ++ ou --',
                          self.valor_token[self.indice_token], 'Assign')
        else:
            self.erro_fim_arquivo_inesperado()

    def Access(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '.':
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.tipo_token[self.indice_token] == 'IDE':
                        self.indice_token += 1
                        self.Arrays()
                    else:
                        self.erro(self.numero_linha[self.indice_token], 'Type(Identifier)',
                                  self.valor_token[self.indice_token], 'Access')
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                self.erro(self.numero_linha[self.indice_token], '.',
                          self.valor_token[self.indice_token], 'Access')
        else:
            self.erro_fim_arquivo_inesperado()

    def Accesses(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '.':
                self.Access()
                self.Accesses()

    def Args(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['!', '(', 'true', 'false'] \
                    or self.tipo_token[self.indice_token] in ['NRO', 'CAD', 'IDE']:
                self.Expr()
                self.ArgsList()

    def ArgsList(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == ',':
                self.indice_token += 1
                self.Expr()
                self.ArgsList()

    def FuncDecl(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == 'function':
                self.indice_token += 1
                self.ParamType()
                if not self.fimArquivo():
                    if self.tipo_token[self.indice_token] == 'IDE':
                        self.indice_token += 1
                        if not self.fimArquivo():
                            if self.valor_token[self.indice_token] == '(':
                                self.indice_token += 1
                                self.Params()
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
                                                    else:
                                                        self.erro(self.numero_linha[self.indice_token], '}',
                                                                  self.valor_token[self.indice_token], 'FuncDecl')
                                                else:
                                                    self.erro_fim_arquivo_inesperado()
                                            else:
                                                self.erro(self.numero_linha[self.indice_token], '{',
                                                          self.valor_token[self.indice_token], 'FuncDecl')
                                        else:
                                            self.erro_fim_arquivo_inesperado()
                                    else:
                                        self.erro(self.numero_linha[self.indice_token], ')',
                                                  self.valor_token[self.indice_token], 'FuncDecl')
                                else:
                                    self.erro_fim_arquivo_inesperado()
                            else:
                                self.erro(self.numero_linha[self.indice_token], '(',
                                          self.valor_token[self.indice_token], 'FuncDecl')
                        else:
                            self.erro_fim_arquivo_inesperado()
                    else:
                        self.erro(self.numero_linha[self.indice_token], 'Type(Identifier)',
                                  self.valor_token[self.indice_token], 'FuncDecl')
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                self.erro(self.numero_linha[self.indice_token], 'function',
                          self.valor_token[self.indice_token], 'FuncDecl')
        else:
            self.erro_fim_arquivo_inesperado()

    def ProcDecl(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == 'procedure':
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.tipo_token[self.indice_token] == 'IDE':
                        self.indice_token += 1
                        if not self.fimArquivo():
                            if self.valor_token[self.indice_token] == '(':
                                self.indice_token += 1
                                self.Params()
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
                                                    else:
                                                        self.erro(self.numero_linha[self.indice_token], '}',
                                                                  self.valor_token[self.indice_token], 'ProcDecl')
                                                else:
                                                    self.erro_fim_arquivo_inesperado()
                                            else:
                                                self.erro(self.numero_linha[self.indice_token], '{',
                                                          self.valor_token[self.indice_token], 'ProcDecl')
                                        else:
                                            self.erro_fim_arquivo_inesperado()
                                    else:
                                        self.erro(self.numero_linha[self.indice_token], ')',
                                                  self.valor_token[self.indice_token], 'ProcDecl')
                                else:
                                    self.erro_fim_arquivo_inesperado()
                            else:
                                self.erro(self.numero_linha[self.indice_token], '(',
                                          self.valor_token[self.indice_token], 'ProcDecl')
                        else:
                            self.erro_fim_arquivo_inesperado()
                    else:
                        self.erro(self.numero_linha[self.indice_token], 'Type(Identifier)',
                                  self.valor_token[self.indice_token], 'ProcDecl')
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                self.erro(self.numero_linha[self.indice_token], 'function',
                          self.valor_token[self.indice_token], 'ProcDecl')
        else:
            self.erro_fim_arquivo_inesperado()

    def ParamType(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['int', 'real', 'boolean', 'string', 'struct']:
                if self.valor_token[self.indice_token] == 'struct':
                    if not self.fimArquivo():
                        if self.tipo_token[self.indice_token] == 'IDE':
                            self.indice_token += 1
                        else:
                            self.erro(self.numero_linha[self.indice_token], 'Type(Identifier)',
                                      self.valor_token[self.indice_token],
                                      'ParamType')
                    else:
                        self.erro_fim_arquivo_inesperado()
                self.indice_token += 1
            elif self.tipo_token[self.indice_token] == 'IDE':
                self.indice_token += 1
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'int, real, boolean, string, struct,Type(Identifier)',
                          self.valor_token[self.indice_token],
                          'ParamType')
        else:
            self.erro_fim_arquivo_inesperado()

    def Params(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['int', 'real', 'boolean', 'string', 'struct']:
                self.Param()
                self.ParamsList()

    def Param(self):
        if not self.fimArquivo():
            self.ParamType()
            if self.tipo_token[self.indice_token] == 'IDE':
                self.indice_token += 1
                self.ParamArrays()
            else:
                self.erro(self.numero_linha[self.indice_token], 'Type(Identifier)',
                          self.valor_token[self.indice_token],
                          'Param')
        else:
            self.erro_fim_arquivo_inesperado()

    def ParamsList(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == ',':
                self.indice_token += 1
                self.Param()
                self.ParamsList()

    def ParamArrays(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '[':
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == ']':
                        self.indice_token += 1
                        self.ParamMultArrays()
                    else:
                        self.erro(self.numero_linha[self.indice_token], ']',
                                  self.valor_token[self.indice_token],
                                  'ParamArrays')

    def ParamMultArrays(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '[':
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.tipo_token[self.indice_token] == 'NRO':
                        self.indice_token += 1
                        if not self.fimArquivo():
                            if self.valor_token[self.indice_token] == ']':
                                self.indice_token += 1
                                self.ParamMultArrays()
                            else:
                                self.erro(self.numero_linha[self.indice_token], ']',
                                          self.valor_token[self.indice_token],
                                          'ParamMultArrays')
                        else:
                            self.erro_fim_arquivo_inesperado()
                    else:
                        self.erro(self.numero_linha[self.indice_token], 'Type(Number)',
                                  self.valor_token[self.indice_token],
                                  'ParamMultArrays')
                else:
                    self.erro_fim_arquivo_inesperado()

    def FuncBlock(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == 'var':
                self.VarBlock()
                self.FuncStms()
            else:
                self.erro(self.numero_linha[self.indice_token], 'var',
                          self.valor_token[self.indice_token],
                          'FuncBlock')
        else:
            self.erro_fim_arquivo_inesperado()

    def FuncStms(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in \
                    ['local', 'print', 'if', ';', 'return', 'read', 'global', 'while', '{'] or \
                    self.tipo_token[self.indice_token] == 'IDE':
                self.FuncStm()
                self.FuncStms()

    def FuncStm(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == 'if':
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == '(':
                        self.indice_token += 1
                        self.LogExpr()
                        if not self.fimArquivo():
                            if self.valor_token[self.indice_token] == ')':
                                self.indice_token += 1
                                if not self.fimArquivo():
                                    if self.valor_token[self.indice_token] == 'then':
                                        self.indice_token += 1
                                        self.FuncNormalStm()
                                        self.ElseStm()
                                    else:
                                        self.erro(self.numero_linha[self.indice_token], 'then',
                                                  self.valor_token[self.indice_token],
                                                  'FuncStm')
                                else:
                                    self.erro_fim_arquivo_inesperado()
                            else:
                                self.erro(self.numero_linha[self.indice_token], ')',
                                          self.valor_token[self.indice_token],
                                          'FuncStm')
                        else:
                            self.erro_fim_arquivo_inesperado()
                    else:
                        self.erro(self.numero_linha[self.indice_token], '(',
                                  self.valor_token[self.indice_token],
                                  'FuncStm')
                else:
                    self.erro_fim_arquivo_inesperado()
            elif self.valor_token[self.indice_token] == 'while':
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == '(':
                        self.indice_token += 1
                        self.LogExpr()
                        if not self.fimArquivo():
                            if self.valor_token[self.indice_token] == ')':
                                self.indice_token += 1
                                self.FuncStm()
                            else:
                                self.erro(self.numero_linha[self.indice_token], ')',
                                          self.valor_token[self.indice_token],
                                          'FuncStm')
                        else:
                            self.erro_fim_arquivo_inesperado()
                    else:
                        self.erro(self.numero_linha[self.indice_token], '(',
                                  self.valor_token[self.indice_token],
                                  'FuncStm')
                else:
                    self.erro_fim_arquivo_inesperado()
            elif self.valor_token[self.indice_token] in ['local', 'print', ';', 'return', 'read', 'global', '{'] \
                    or self.tipo_token[self.indice_token] == 'IDE':
                self.FuncNormalStm()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'if, while, local, print, ;, return, read, global, {, Type(Identifier)',
                          self.valor_token[self.indice_token],
                          'FuncStm')
        else:
            self.erro_fim_arquivo_inesperado()

    def ElseStm(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == 'else':
                self.indice_token += 1
                self.FuncNormalStm()

    def FuncNormalStm(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '{':
                self.indice_token += 1
                self.FuncStms()
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == '}':
                        self.indice_token += 1
                    else:
                        self.erro(self.numero_linha[self.indice_token], '}',
                                  self.valor_token[self.indice_token],
                                  'FuncNormalStm')
                else:
                    self.erro_fim_arquivo_inesperado()
            elif self.valor_token[self.indice_token] in ['local', 'print', 'read', 'global'] \
                    or self.tipo_token[self.indice_token] == 'IDE':
                self.VarStm()
            elif self.valor_token[self.indice_token] == 'return':
                self.indice_token += 1
                self.Expr()
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == ';':
                        self.indice_token += 1
                    else:
                        self.erro(self.numero_linha[self.indice_token], ';',
                                  self.valor_token[self.indice_token],
                                  'FuncNormalStm')
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          '{, local, print, Type(Identifier), read, global, return',
                          self.valor_token[self.indice_token],
                          'FuncNormalStm')
        else:
            self.erro_fim_arquivo_inesperado()

    def VarStm(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['local', 'global']:
                self.StmScope()
            elif self.tipo_token[self.indice_token] == 'IDE':
                self.indice_token += 1
                self.StmId()
            elif self.valor_token[self.indice_token] in ['print', 'read']:
                self.StmCmd()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'local, print, Type(Identifier), read, global',
                          self.valor_token[self.indice_token],
                          'VarStm')
        else:
            self.erro_fim_arquivo_inesperado()

    def StmId(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['+', '-', '=', '++', '--']:
                self.Assign()
            elif self.valor_token[self.indice_token] == '[':
                self.Array()
                self.Arrays()
                self.Accesses()
                self.Assign()
            elif self.valor_token[self.indice_token] == '.':
                self.Access()
                self.Accesses()
                self.Assign()
            elif self.valor_token[self.indice_token] == '(':
                self.indice_token += 1
                self.Args()
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == ')':
                        self.indice_token += 1
                        if not self.fimArquivo():
                            if self.valor_token[self.indice_token] == ';':
                                self.indice_token += 1
                            else:
                                self.erro(self.numero_linha[self.indice_token],
                                          ';',
                                          self.valor_token[self.indice_token],
                                          'StmId')
                        else:
                            self.erro_fim_arquivo_inesperado()
                    else:
                        self.erro(self.numero_linha[self.indice_token],
                                  ')',
                                  self.valor_token[self.indice_token],
                                  'StmId')
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          '+, -, =, [, (, ++, --',
                          self.valor_token[self.indice_token],
                          'StmId')
        else:
            self.erro_fim_arquivo_inesperado()

    def StmScope(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == 'local':
                self.indice_token += 1
                self.Access()
                self.Accesses()
                self.Assign()
            elif self.valor_token[self.indice_token] == 'global':
                self.indice_token += 1
                self.Access()
                self.Accesses()
                self.Assign()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'global, local',
                          self.valor_token[self.indice_token],
                          'StmScope')
        else:
            self.erro_fim_arquivo_inesperado()

    def StmCmd(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['print', 'read']:
                self.indice_token += 1
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == '(':
                        self.indice_token += 1
                        self.Args()
                        if not self.fimArquivo():
                            if self.valor_token[self.indice_token] == ')':
                                self.indice_token += 1
                                if not self.fimArquivo():
                                    if self.valor_token[self.indice_token] == ';':
                                        self.indice_token += 1
                                    else:
                                        self.erro(self.numero_linha[self.indice_token],
                                                  ';',
                                                  self.valor_token[self.indice_token],
                                                  'StmCmd')
                                else:
                                    self.erro_fim_arquivo_inesperado()
                            else:
                                self.erro(self.numero_linha[self.indice_token],
                                          ')',
                                          self.valor_token[self.indice_token],
                                          'StmCmd')
                        else:
                            self.erro_fim_arquivo_inesperado()
                    else:
                        self.erro(self.numero_linha[self.indice_token],
                                  '(',
                                  self.valor_token[self.indice_token],
                                  'StmCmd')
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'print, read',
                          self.valor_token[self.indice_token],
                          'StmCmd')

    def Expr(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['false', 'true', '!', '('] \
                    or self.tipo_token[self.indice_token] in ['IDE', 'CAD', 'NRO']:
                self.Or()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(String), Type(Boolean), !, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'Expr')
        else:
            self.erro_fim_arquivo_inesperado()

    def Or(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['false', 'true', '!', '('] \
                    or self.tipo_token[self.indice_token] in ['IDE', 'CAD', 'NRO']:
                self.And()
                self.Or_()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(String), Type(Boolean), !, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'Or')
        else:
            self.erro_fim_arquivo_inesperado()

    def Or_(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '||':
                self.indice_token += 1
                self.And()
                self.Or_()

    def And(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['false', 'true', '!', '('] \
                    or self.tipo_token[self.indice_token] in ['IDE', 'CAD', 'NRO']:
                self.Equate()
                self.And_()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(String), Type(Boolean), !, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'And')
        else:
            self.erro_fim_arquivo_inesperado()

    def And_(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '&&':
                self.indice_token += 1
                self.Equate()
                self.And_()

    def Equate(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['false', 'true', '!', '('] \
                    or self.tipo_token[self.indice_token] in ['IDE', 'CAD', 'NRO']:
                self.Compare()
                self.Equate_()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(String), Type(Boolean), !, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'Equate')
        else:
            self.erro_fim_arquivo_inesperado()

    def Equate_(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['==', '!=']:
                self.indice_token += 1
                self.Compare()
                self.Equate_()

    def Compare(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['false', 'true', '!', '('] \
                    or self.tipo_token[self.indice_token] in ['IDE', 'CAD', 'NRO']:
                self.Add()
                self.Compare_()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(String), Type(Boolean), !, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'Compare')
        else:
            self.erro_fim_arquivo_inesperado()

    def Compare_(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['>', '<', '>=', '<=']:
                self.indice_token += 1
                self.Add()
                self.Compare_()

    def Add(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['false', 'true', '!', '('] \
                    or self.tipo_token[self.indice_token] in ['IDE', 'CAD', 'NRO']:
                self.Mult()
                self.Add_()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(String), Type(Boolean), !, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'Add')
        else:
            self.erro_fim_arquivo_inesperado()

    def Add_(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['+', '-']:
                self.indice_token += 1
                self.Mult()
                self.Add_()

    def Mult(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['false', 'true', '!', '('] \
                    or self.tipo_token[self.indice_token] in ['IDE', 'CAD', 'NRO']:
                self.Unary()
                self.Mult_()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(String), Type(Boolean), !, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'Mult')
        else:
            self.erro_fim_arquivo_inesperado()

    def Mult_(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['*', '/']:
                self.indice_token += 1
                self.Unary()
                self.Mult_()

    def Unary(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '!':
                self.indice_token += 1
                self.Unary()
            elif self.valor_token[self.indice_token] in ['false', 'true', '('] \
                    or self.tipo_token[self.indice_token] in ['IDE', 'CAD', 'NRO']:
                self.Value()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(String), Type(Boolean), !, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'Unary')
        else:
            self.erro_fim_arquivo_inesperado()

    def Value(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '-':
                self.indice_token += 1
                self.Value()
            elif self.valor_token[self.indice_token] in ['true', 'false'] \
                    or self.tipo_token[self.indice_token] in ['CAD', 'NRO']:
                self.indice_token += 1
            elif self.valor_token[self.indice_token] in ['global', 'local']:
                self.indice_token += 1
                self.Access()
            elif self.tipo_token[self.indice_token] == 'IDE':
                self.indice_token += 1
                self.IdValue()
            elif self.valor_token[self.indice_token] == '(':
                self.indice_token += 1
                self.Expr()
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == ')':
                        self.indice_token += 1
                    else:
                        self.erro(self.numero_linha[self.indice_token],
                                  ')',
                                  self.valor_token[self.indice_token],
                                  'Value')
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(Boolean), Type(String), -, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'Value')
        else:
            self.erro_fim_arquivo_inesperado()

    def IdValue(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in \
                    ['[', '.', '+', '>=', '&&', '-', '>', '!=', '||', ',', ']', '<=', '==', '*', '<', '/', ')']:
                self.Arrays()
                self.Accesses()
            elif self.valor_token[self.indice_token] == '(':
                self.indice_token += 1
                self.Args()
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == ')':
                        self.indice_token += 1
                    else:
                        self.erro(self.numero_linha[self.indice_token],
                                  ')',
                                  self.valor_token[self.indice_token],
                                  'IdValue')
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                print('aq')
                self.erro(self.numero_linha[self.indice_token],
                          '[, (',
                          self.valor_token[self.indice_token],
                          'IdValue')
        else:
            self.erro_fim_arquivo_inesperado()

    def LogExpr(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['false', 'true', '!', '('] \
                    or self.tipo_token[self.indice_token] in ['IDE', 'CAD', 'NRO']:
                self.LogOr()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(String), Type(Boolean), !, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'LogExpr')
        else:
            self.erro_fim_arquivo_inesperado()

    def LogOr(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['false', 'true', '!', '('] \
                    or self.tipo_token[self.indice_token] in ['IDE', 'CAD', 'NRO']:
                self.LogAnd()
                self.LogOr_()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(String), Type(Boolean), !, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'LogOr')
        else:
            self.erro_fim_arquivo_inesperado()

    def LogOr_(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '||':
                self.indice_token += 1
                self.LogAnd()
                self.LogOr_()

    def LogAnd(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['false', 'true', '!', '('] \
                    or self.tipo_token[self.indice_token] in ['IDE', 'CAD', 'NRO']:
                self.LogEquate()
                self.LogAnd_()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(String), Type(Boolean), !, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'LogAnd')
        else:
            self.erro_fim_arquivo_inesperado()

    def LogAnd_(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '&&':
                self.indice_token += 1
                self.LogEquate()
                self.LogAnd_()

    def LogEquate(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['false', 'true', '!', '('] \
                    or self.tipo_token[self.indice_token] in ['IDE', 'CAD', 'NRO']:
                self.LogCompare()
                self.LogEquate_()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(String), Type(Boolean), !, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'LogEquate')
        else:
            self.erro_fim_arquivo_inesperado()

    def LogEquate_(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['==', '!=']:
                self.indice_token += 1
                self.LogCompare()
                self.LogEquate_()

    def LogCompare(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['false', 'true', '!', '('] \
                    or self.tipo_token[self.indice_token] in ['IDE', 'CAD', 'NRO']:
                self.LogUnary()
                self.LogCompare_()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(String), Type(Boolean), !, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'LogCompare')
        else:
            self.erro_fim_arquivo_inesperado()

    def LogCompare_(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['>', '<', '>=', '<=']:
                self.indice_token += 1
                self.LogUnary()
                self.LogCompare_()

    def LogUnary(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] == '!':
                self.indice_token += 1
                self.LogUnary()
            elif self.valor_token[self.indice_token] in ['false', 'true', '('] \
                    or self.tipo_token[self.indice_token] in ['IDE', 'CAD', 'NRO']:
                self.LogValue()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(String), Type(Boolean), !, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'Unary')
        else:
            self.erro_fim_arquivo_inesperado()

    def LogValue(self):
        if not self.fimArquivo():
            if self.valor_token[self.indice_token] in ['true', 'false'] \
                    or self.tipo_token[self.indice_token] in ['CAD', 'NRO']:
                self.indice_token += 1
            elif self.valor_token[self.indice_token] in ['global', 'local']:
                self.indice_token += 1
                self.Access()
            elif self.tipo_token[self.indice_token] == 'IDE':
                self.indice_token += 1
                self.IdValue()
            elif self.valor_token[self.indice_token] == '(':
                self.indice_token += 1
                self.LogExpr()
                if not self.fimArquivo():
                    if self.valor_token[self.indice_token] == ')':
                        self.indice_token += 1
                    else:
                        self.erro(self.numero_linha[self.indice_token],
                                  ')',
                                  self.valor_token[self.indice_token],
                                  'Value')
                else:
                    self.erro_fim_arquivo_inesperado()
            else:
                self.erro(self.numero_linha[self.indice_token],
                          'Type(Boolean), Type(String), -, (, Type(Identifier), Type(Number)',
                          self.valor_token[self.indice_token],
                          'Value')
        else:
            self.erro_fim_arquivo_inesperado()

    def erro(self, numero_linha, esperava, recebido, nao_terminal):
        self.teve_erro = True
        print(f'Linha {int(numero_linha)}'
              f' - Erro Sintático'
              f' - Esperava: ', f'{esperava}', f' / Recebido: {recebido}')
        self.resposta.append(f'Linha {int(numero_linha)} - Erro Sintático - '
                             f'Esperava: {esperava} / Recebido: {recebido}')
        self.procurar_token_sincronizacao(nao_terminal)

    def procurar_token_sincronizacao(self, nao_terminal):
        conjuntoFollow = Sync.Sync().sync_tokens[nao_terminal]
        while not self.fimArquivo():
            if self.valor_token[self.indice_token] in conjuntoFollow \
                    or self.tipo_token[self.indice_token] in conjuntoFollow:
                break
            self.indice_token += 1
        if self.fimArquivo():
            self.erro_fim_arquivo_inesperado()
        else:
            self.reiniciar(nao_terminal, self.valor_token[self.indice_token])

    def reiniciar(self, nao_terminal, token_atual):
        if nao_terminal == 'StartBlock':
            self.ErroStartBlock(token_atual)
        elif nao_terminal == 'ConstBlock':
            self.ErroConstBlock(token_atual)

    def ErroStartBlock(self, token_atual):
        if token_atual == '{':
            self.indice_token += 1
            self.FuncBlock()
        elif token_atual == ['if', 'while', 'return', 'local', 'global', 'print', 'read', 'var'] \
                or self.tipo_token[self.indice_token] == 'IDE':
            self.FuncBlock()

    def ErroConstBlock(self, token_atual):
        self.indice_token += 1
        if token_atual == '{':
            self.ConstDecls()

    def erro_fim_arquivo_inesperado(self):
        if self.fimArquivo():
            print(f'Linha {self.numero_linha[len(self.numero_linha) - 1]}'
                  f' - Erro Sintático'
                  f' - Esperava: ', 'Token', f' / Recebido: EOF')
            self.resposta.append(f'Linha {self.numero_linha[len(self.numero_linha) - 1]}'
                                 f' - Erro Sintático'
                                 f' - Esperava: ', 'Token', f' / Recebido: EOF')
