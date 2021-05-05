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
            if self.valor_token[self.indice_token] in ['int', 'real', 'boolean', 'string', 'struct'] \
                    or self.tipo_token[self.indice_token] == 'IDE':
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
                    or self.tipo_token[self.indice_token] in ['CAD', 'IDE']:
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
                                          'ParamType')
                        else:
                            self.erro_fim_arquivo_inesperado()
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
            if self.valor_token in ['int', 'real', 'boolean', 'string', 'struct']:
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
            exit()
