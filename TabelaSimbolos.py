import AnalisadorSemantico


class TabelaSimbolos:

    def __init__(self, texto_lexico):
        self.erro = ''
        self.texto_lexico = texto_lexico
        self.numero_linha = []
        self.tipo_token = []
        self.valor_token = []
        self.tabela_struct = []
        self.tabela_var_struct = []
        self.tabela_procedure = []
        self.tabela_var_procedure = []
        self.tabela_const = []
        self.tabela_var_global = []
        self.tabela_indice_vetor_struct = []
        self.tabela_function = []


    # ler arquivo de tokens
    def criarTabelas(self):
        lista = self.texto_lexico
        tamanho_atual = len(self.texto_lexico)
        for linha in lista:
            # print(linha)
            self.numero_linha.append(linha.split(' ')[0])
            self.tipo_token.append(linha.split(' ')[1])
            aux_valor = linha.split(' ')[2]
            self.valor_token.append(aux_valor.split('\n')[0])
        self.tabelaConst()
        self.tabelasStruct()
        self.tabelaVarGlobal()
        self.tabelasProcedure()
        self.tabelasFunction()
        self.tabelasStart()
        tamanho_pos_analise = len(self.texto_lexico)
        if tamanho_atual == tamanho_pos_analise:
            self.texto_lexico.append('Arquivo compilado com sucesso!\n')
        return self.texto_lexico


    # const
    def tabelaConst(self):
        tabela_const = []
        tabela_indice_vetor = []
        indice_token = 0
        while indice_token < len(self.valor_token):
            if self.valor_token[indice_token] == 'const':
                i = indice_token + 2
                tipo = ''
                while self.valor_token[i] != '}':
                    if self.valor_token[i] == ';':
                        pass
                    elif self.valor_token[i] == ',':
                        nome = self.valor_token[i + 1]
                        if tipo == 'int':
                            tabela_const.append([tipo, nome, 'int', self.numero_linha[i]])
                        elif tipo == 'real':
                            tabela_const.append([tipo, nome, 'real', self.numero_linha[i]])
                        elif tipo == 'string':
                            tabela_const.append([tipo, nome, 'string', self.numero_linha[i]])
                        elif tipo == 'boolean':
                            tabela_const.append([tipo, nome, 'boolean', self.numero_linha[i]])
                        i += 1
                    elif self.valor_token[i] == '=':
                        for linha in tabela_const:
                            if linha[3] == self.numero_linha[i] and linha[0] == tipo:
                                # colocar tipo e não o valor
                                atribuicao = tipo
                                if self.tipo_token[i + 1] == 'NRO':
                                    if self.valor_token[i + 1].__contains__('.'):
                                        atribuicao = 'real'
                                    else:
                                        atribuicao = 'int'
                                elif self.tipo_token[i + 1] == 'CAD':
                                    atribuicao = 'string'
                                elif self.valor_token[i + 1] in ['true', 'false']:
                                    atribuicao = 'boolean'
                                linha[2] = atribuicao
                        i += 1
                    elif self.valor_token[i] == '[':
                        i, novo_elm, tipo_elm = self.tabelaIndiceVetor(i)
                        if novo_elm != '':
                            tabela_indice_vetor.append([novo_elm, tipo_elm])
                    else:
                        tipo, nome = self.valor_token[i], self.valor_token[i + 1]
                        if tipo == 'int':
                            tabela_const.append(
                                [tipo, nome, 'int', self.numero_linha[i]])
                        elif tipo == 'real':
                            tabela_const.append(
                                [tipo, nome, 'real', self.numero_linha[i]])
                        elif tipo == 'string':
                            tabela_const.append(
                                [tipo, nome, 'string', self.numero_linha[i]])
                        elif tipo == 'boolean':
                            tabela_const.append(
                                [tipo, nome, 'boolean', self.numero_linha[i]])
                        i += 1
                    i += 1
            indice_token += 1
        print('\n\n----------------------------')
        print('Tabela Const')
        for elm in tabela_const:
            print(elm)
        print('Tabela Indice Vetor Const')
        for elm in tabela_indice_vetor:
            print(elm)
        print('**************************************************')
        self.tabela_const = tabela_const
        seman = AnalisadorSemantico.AnalisadorSemantico(self.texto_lexico)
        self.texto_lexico = seman.analisarConst(tabelaConst=tabela_const, tabelaIndiceVetor=tabela_indice_vetor)

    # var
    def tabelaVarGlobal(self):
        tabela_indice_vetor = []
        tabela_var = []
        indice_token = 0
        while indice_token < len(self.valor_token):
            # se a posição anterior ao var não for um abre chaves, significa que ele tá no escopo global
            if self.valor_token[indice_token] == 'var' and self.valor_token[indice_token - 1] != '{':
                i = indice_token + 2
                tipo = ''
                while self.valor_token[i] != '}':
                    if self.valor_token[i] in [';', 'struct']:
                        pass
                    elif self.valor_token[i] == ',':
                        nome = self.valor_token[i + 1]
                        if tipo == 'int':
                            tabela_var.append([tipo, nome, 'int', self.numero_linha[i], False])
                        elif tipo == 'real':
                            tabela_var.append([tipo, nome, 'real', self.numero_linha[i], False])
                        elif tipo == 'string':
                            tabela_var.append([tipo, nome, 'string', self.numero_linha[i], False])
                        elif tipo == 'boolean':
                            tabela_var.append([tipo, nome, 'boolean', self.numero_linha[i], False])
                        else:
                            tabela_var.append([tipo, nome, tipo, self.numero_linha[i], False])
                        i += 1
                    elif self.valor_token[i] == '=':
                        for linha in tabela_var:
                            if linha[3] == self.numero_linha[i] and linha[0] == tipo:
                                # colocar tipo e não o valor
                                atribuicao = tipo
                                if self.tipo_token[i + 1] == 'NRO':
                                    if self.valor_token[i + 1].__contains__('.'):
                                        atribuicao = 'real'
                                    else:
                                        atribuicao = 'int'
                                elif self.tipo_token[i + 1] == 'CAD':
                                    atribuicao = 'string'
                                elif self.valor_token[i + 1] in ['true', 'false']:
                                    atribuicao = 'boolean'
                                linha[2] = atribuicao
                                linha[4] = True
                        i += 1
                    elif self.valor_token[i] == '[':
                        i, novo_elm, tipo_elm = self.tabelaIndiceVetor(i)
                        if novo_elm != '':
                            tabela_indice_vetor.append([novo_elm, tipo_elm])
                    else:
                        tipo, nome = self.valor_token[i], self.valor_token[i + 1]
                        if tipo == 'int':
                            tabela_var.append(
                                [tipo, nome, 'int', self.numero_linha[i], False])
                        elif tipo == 'real':
                            tabela_var.append(
                                [tipo, nome, 'real', self.numero_linha[i], False])
                        elif tipo == 'string':
                            tabela_var.append(
                                [tipo, nome, 'string', self.numero_linha[i], False])
                        elif tipo == 'boolean':
                            tabela_var.append(
                                [tipo, nome, 'boolean', self.numero_linha[i], False])
                        else:
                            tabela_var.append([tipo, nome, tipo, self.numero_linha[i], False])
                        i += 1
                    i += 1
            indice_token += 1
        print('Tabela Var Global')
        for elm in tabela_var:
            print(elm)
        print('----------------------------')
        print('Tabela Indices de Vetor Var Global')
        for elm in tabela_indice_vetor:
            print(elm)
        self.tabela_var_global = tabela_var
        seman = AnalisadorSemantico.AnalisadorSemantico(self.texto_lexico)
        self.texto_lexico = seman.analisarVarGlobal(tabelaVar=tabela_var, tabelaStruct=self.tabela_struct, tabelaConst=self.tabela_const,
                                tabelaIndiceVetor=tabela_indice_vetor)
        print('**************************************************')
        seman = AnalisadorSemantico.AnalisadorSemantico(self.texto_lexico)
        self.texto_lexico = seman.analisarIndiceVetorStruct(tabelaVarStruct=self.tabela_var_struct, tabelaVarGlobal=self.tabela_var_global,
                                        tabelaConst=self.tabela_const, tabelaIndiceVetor=self.tabela_indice_vetor_struct,
                                        tabelaFunction=self.tabela_function)


    # procedure
    # OBS: ANALISAR INDICE VETOR EM PROCEDURE E EM FUNCTION
    def tabelasProcedure(self):
        tabela_procedure = []
        tabela_var_procedure = []
        tabela_parametros_procedure = []
        tabela_indice_vetor = []
        indice_token = 0
        while indice_token < len(self.valor_token):
            if self.valor_token[indice_token] == 'procedure':
                procedure_atual = self.valor_token[indice_token + 1]
                tabela_procedure.append(procedure_atual)
                while self.valor_token[indice_token] != '(':
                    indice_token += 1
                indice_token += 1
                tem_parametro = False
                # pra quando o procedimento tiver paramentros, criar uma tabela de parametros para os procedimentos
                if self.valor_token[indice_token] != ')':
                    tem_parametro = True
                    while True:
                        tipo, nome = self.valor_token[indice_token], self.valor_token[indice_token + 1]
                        tabela_parametros_procedure.append([tipo, nome, procedure_atual, self.numero_linha[indice_token]])
                        indice_token += 3
                        if self.valor_token[indice_token - 1] == ')':
                            break
                # print(self.valor_token[self.indice_token])
                if tem_parametro:
                    indice_token += 1
                else:
                    indice_token += 2
                if self.valor_token[indice_token] == 'var':
                    i = indice_token + 2
                    tipo = ''
                    while self.valor_token[i] != '}':
                        if self.valor_token[i] in [';', 'struct']:
                            pass
                        elif self.valor_token[i] == ',':
                            nome = self.valor_token[i + 1]
                            if tipo == 'int':
                                tabela_var_procedure.append([tipo, nome, 'int', procedure_atual, self.numero_linha[i], False])
                            elif tipo == 'real':
                                tabela_var_procedure.append([tipo, nome, 'real', procedure_atual, self.numero_linha[i], False])
                            elif tipo == 'string':
                                tabela_var_procedure.append([tipo, nome, 'string', procedure_atual, self.numero_linha[i], False])
                            elif tipo == 'boolean':
                                tabela_var_procedure.append([tipo, nome, 'boolean', procedure_atual, self.numero_linha[i], False])
                            else:
                                tabela_var_procedure.append([tipo, nome, tipo, procedure_atual, self.numero_linha[i], False])
                            i += 1
                        elif self.valor_token[i] == '=':
                            for linha in tabela_var_procedure:
                                if linha[4] == self.numero_linha[i] and linha[0] == tipo:
                                    # colocar tipo e não o valor
                                    atribuicao = tipo
                                    if self.tipo_token[i + 1] == 'NRO':
                                        if self.valor_token[i + 1].__contains__('.'):
                                            atribuicao = 'real'
                                        else:
                                            atribuicao = 'int'
                                    elif self.tipo_token[i + 1] == 'CAD':
                                        atribuicao = 'string'
                                    elif self.valor_token[i + 1] in ['true', 'false']:
                                        atribuicao = 'boolean'
                                    linha[2] = atribuicao
                                    linha[5] = True
                            i += 1
                        elif self.valor_token[i] == '[':
                            i, novo_elm, tipo_elm = self.tabelaIndiceVetor(i)
                            if novo_elm != '':
                                tabela_indice_vetor.append([novo_elm, tipo_elm, procedure_atual])
                        else:
                            tipo, nome = self.valor_token[i], self.valor_token[i + 1]
                            if tipo == 'int':
                                tabela_var_procedure.append(
                                    [tipo, nome, 'int', procedure_atual,
                                     self.numero_linha[i], False])
                            elif tipo == 'real':
                                tabela_var_procedure.append(
                                    [tipo, nome, 'real', procedure_atual,
                                     self.numero_linha[i], False])
                            elif tipo == 'string':
                                tabela_var_procedure.append(
                                    [tipo, nome, 'string', procedure_atual,
                                     self.numero_linha[i], False])
                            elif tipo == 'boolean':
                                tabela_var_procedure.append(
                                    [tipo, nome, 'boolean', procedure_atual,
                                     self.numero_linha[i], False])
                            else:
                                tabela_var_procedure.append(
                                    [tipo, nome, tipo, procedure_atual, self.numero_linha[i], False])
                            i += 1
                        i += 1
            indice_token += 1

        print('Tabela Procedure')
        for elm in tabela_procedure:
            print(elm)
        print('----------------------------')
        print('Tabela Parametros Procedure')
        for elm in tabela_parametros_procedure:
            print(elm)
        print('----------------------------')
        print('Tabela Var Procedure')
        for elm in tabela_var_procedure:
            print(elm)
        print('Tabela Indices de Vetor Procedures')
        for elm in tabela_indice_vetor:
            print(elm)
        print('**************************************************')
        self.tabela_procedure = tabela_procedure
        self.tabela_var_procedure = tabela_var_procedure
        seman = AnalisadorSemantico.AnalisadorSemantico(self.texto_lexico)
        self.texto_lexico = seman.analisarProcedure(tabelaProcedure=tabela_procedure, tabelaVarProcedure=tabela_var_procedure,
                                tabelaParametrosProcedure= tabela_parametros_procedure,
                                tabelaStruct=self.tabela_struct, tabelaVarStruct=self.tabela_var_struct,
                                tabelaVarGlobal=self.tabela_var_global, tabelaConst=self.tabela_const,
                                tabelaIndiceVetor=tabela_indice_vetor, tabelaFunction=self.tabela_function)

    # function
    def tabelasFunction(self):
        tabela_function = []
        tabela_var_function = []
        tabela_parametros_function = []
        tabela_indice_vetor = []
        indice_token = 0
        while indice_token < len(self.valor_token):
            if self.valor_token[indice_token] == 'function':
                tipo_function, function_atual = self.valor_token[indice_token + 1], self.valor_token[indice_token + 2]
                tabela_function.append([tipo_function, function_atual])
                while self.valor_token[indice_token] != '(':
                    indice_token += 1
                indice_token += 1
                tem_parametro = False
                # pra quando o procedimento tiver paramentros, criar uma tabela de parametros para os procedimentos
                if self.valor_token[indice_token] != ')':
                    tem_parametro = True
                    while True:
                        tipo, nome = self.valor_token[indice_token], self.valor_token[indice_token + 1]
                        tabela_parametros_function.append([tipo, nome, function_atual, self.numero_linha[indice_token]])
                        indice_token += 3
                        if self.valor_token[indice_token - 1] == ')':
                            break
                # print(self.valor_token[self.indice_token])
                if tem_parametro:
                    indice_token += 1
                else:
                    indice_token += 2
                if self.valor_token[indice_token] == 'var':
                    i = indice_token + 2
                    tipo = ''
                    while self.valor_token[i] != '}':
                        if self.valor_token[i] in [';', 'struct']:
                            pass
                        elif self.valor_token[i] == ',':
                            nome = self.valor_token[i + 1]
                            if tipo == 'int':
                                tabela_var_function.append([tipo, nome, 'int', function_atual, self.numero_linha[i], False])
                            elif tipo == 'real':
                                tabela_var_function.append([tipo, nome, 'real', function_atual, self.numero_linha[i], False])
                            elif tipo == 'string':
                                tabela_var_function.append([tipo, nome, 'string', function_atual, self.numero_linha[i], False])
                            elif tipo == 'boolean':
                                tabela_var_function.append([tipo, nome, 'boolean', function_atual, self.numero_linha[i], False])
                            else:
                                tabela_var_function.append([tipo, nome, tipo, function_atual, self.numero_linha[i], False])
                            i += 1
                        elif self.valor_token[i] == '=':
                            for linha in tabela_var_function:
                                if linha[4] == self.numero_linha[i] and linha[0] == tipo:
                                    # colocar tipo e não o valor
                                    atribuicao = tipo
                                    if self.tipo_token[i + 1] == 'NRO':
                                        if self.valor_token[i + 1].__contains__('.'):
                                            atribuicao = 'real'
                                        else:
                                            atribuicao = 'int'
                                    elif self.tipo_token[i + 1] == 'CAD':
                                        atribuicao = 'string'
                                    elif self.valor_token[i + 1] in ['true', 'false']:
                                        atribuicao = 'boolean'
                                    linha[2] = atribuicao
                                    linha[5] = True
                            i += 1
                        elif self.valor_token[i] == '[':
                            i, novo_elm, tipo_elm = self.tabelaIndiceVetor(i)
                            if novo_elm != '':
                                tabela_indice_vetor.append([novo_elm, tipo_elm, function_atual])
                        else:
                            tipo, nome = self.valor_token[i], self.valor_token[i + 1]
                            if tipo == 'int':
                                tabela_var_function.append(
                                    [tipo, nome, 'int', function_atual,
                                     self.numero_linha[i], False])
                            elif tipo == 'real':
                                tabela_var_function.append(
                                    [tipo, nome, 'real', function_atual,
                                     self.numero_linha[i], False])
                            elif tipo == 'string':
                                tabela_var_function.append(
                                    [tipo, nome, 'string', function_atual,
                                     self.numero_linha[i], False])
                            elif tipo == 'boolean':
                                tabela_var_function.append(
                                    [tipo, nome, 'boolean', function_atual,
                                     self.numero_linha[i], False])
                            else:
                                tabela_var_function.append(
                                    [tipo, nome, tipo, function_atual, self.numero_linha[i], False])
                            i += 1
                        i += 1
            indice_token += 1

        print('Tabela Function')
        for elm in tabela_function:
            print(elm)
        print('----------------------------')
        print('Tabela Parametros Function')
        for elm in tabela_parametros_function:
            print(elm)
        print('----------------------------')
        print('Tabela Var Function')
        for elm in tabela_var_function:
            print(elm)
        print('Tabela Indices de Vetor Function')
        for elm in tabela_indice_vetor:
            print(elm)
        print('**************************************************')
        self.tabela_function = tabela_function
        seman = AnalisadorSemantico.AnalisadorSemantico(self.texto_lexico)
        self.texto_lexico = seman.analisarFunction(tabelaFunction=tabela_function, tabelaVarFunction=tabela_var_function,
                                tabelaParametrosFunction=tabela_parametros_function,
                                tabelaStruct=self.tabela_struct, tabelaVarStruct=self.tabela_var_struct,
                               tabelaProcedure=self.tabela_procedure, tabelaVarGlobal=self.tabela_var_global,
                               tabelaConst=self.tabela_const, tabelaIndiceVetor=tabela_indice_vetor)

    # struct nome{
    # tipo nome;
    # }

    def tabelasStruct(self):
        tabela_struct = []
        tabela_var_struct = []
        tabela_indice_vetor = []
        indice_token = 0
        while indice_token < len(self.valor_token):
            if self.valor_token[indice_token] == 'struct':
                if self.valor_token[indice_token + 2] in ['{', 'extends']:
                    # print(valor_token[indice_escopo + 2])
                    if self.valor_token[indice_token + 2] == 'extends':
                        tabela_struct.append([self.valor_token[indice_token + 1], self.valor_token[indice_token + 3]])
                        indice_token += 2
                    else:
                        tabela_struct.append([self.valor_token[indice_token + 1], ''])
                i = indice_token + 3
                tipo = ''
                while self.valor_token[i] != '}':
                    if self.valor_token[i] in [';', 'struct']:
                        pass
                    elif self.valor_token[i] == ',':
                        nome = self.valor_token[i + 1]
                        if tipo == 'int':
                            tabela_var_struct.append(
                                [tipo, nome, 'int', self.valor_token[indice_token + 1],
                                 self.numero_linha[i], False])
                        elif tipo == 'real':
                            tabela_var_struct.append(
                                [tipo, nome, 'real', self.valor_token[indice_token + 1],
                                 self.numero_linha[i], False])
                        elif tipo == 'string':
                            tabela_var_struct.append(
                                [tipo, nome, 'string', self.valor_token[indice_token + 1],
                                 self.numero_linha[i], False])
                        elif tipo == 'boolean':
                            tabela_var_struct.append(
                                [tipo, nome, 'boolean', self.valor_token[indice_token + 1],
                                 self.numero_linha[i], False])
                        else:
                            tabela_var_struct.append(
                                [tipo, nome, tipo, self.valor_token[indice_token + 1], self.numero_linha[i], False])
                        i += 1
                    elif self.valor_token[i] == '=':
                        for linha in tabela_var_struct:
                            if linha[4] == self.numero_linha[i] and linha[0] == tipo:
                                # colocar tipo e não o valor
                                atribuicao = tipo
                                if self.tipo_token[i + 1] == 'NRO':
                                    if self.valor_token[i + 1].__contains__('.'):
                                        atribuicao = 'real'
                                    else:
                                        atribuicao = 'int'
                                elif self.tipo_token[i + 1] == 'CAD':
                                    atribuicao = 'string'
                                elif self.valor_token[i + 1] in ['true', 'false']:
                                    atribuicao = 'boolean'
                                linha[2] = atribuicao
                                linha[5] = True
                        i += 1
                    elif self.valor_token[i] == '[':
                        i, novo_elm, tipo_elm = self.tabelaIndiceVetor(i)
                        if novo_elm != '':
                            tabela_indice_vetor.append([novo_elm, tipo_elm,self.valor_token[indice_token + 1]])
                    else:
                        tipo, nome = self.valor_token[i], self.valor_token[i + 1]
                        if tipo == 'int':
                            tabela_var_struct.append(
                                [tipo, nome, 'int', self.valor_token[indice_token + 1],
                                 self.numero_linha[i], False])
                        elif tipo == 'real':
                            tabela_var_struct.append(
                                [tipo, nome, 'real', self.valor_token[indice_token + 1],
                                 self.numero_linha[i], False])
                        elif tipo == 'string':
                            tabela_var_struct.append(
                                [tipo, nome, 'string', self.valor_token[indice_token + 1],
                                 self.numero_linha[i], False])
                        elif tipo == 'boolean':
                            tabela_var_struct.append(
                                [tipo, nome, 'boolean', self.valor_token[indice_token + 1],
                                 self.numero_linha[i], False])
                        else:
                            tabela_var_struct.append(
                                [tipo, nome, tipo, self.valor_token[indice_token + 1], self.numero_linha[i], False])
                        i += 1
                    i += 1
            indice_token += 1

        print('Tabela Struct')
        for elm in tabela_struct:
            print(elm)
        print('----------------------------')
        print('Tabela Var Struct')
        for elm in tabela_var_struct:
            print(elm)
        print('Tabela Indices de Vetor Struct')
        for elm in tabela_indice_vetor:
            print(elm)
        self.tabela_struct = tabela_struct
        self.tabela_var_struct = tabela_var_struct
        self.tabela_indice_vetor_struct = tabela_indice_vetor
        seman = AnalisadorSemantico.AnalisadorSemantico(self.texto_lexico)
        self.texto_lexico = seman.analisarStruct(tabelaStruct=tabela_struct, tabelaVarStruct=tabela_var_struct)
        print('**************************************************')

    # start

    def tabelasStart(self):
        tabela_var_start = []
        tabela_indice_vetor = []
        indice_token = 0
        while indice_token < len(self.valor_token):
            if self.valor_token[indice_token] == 'start':
                indice_token += 4
                if self.valor_token[indice_token] == 'var':
                    indice_token += 2
                    i = indice_token
                    # print(self.valor_token[self.indice_token])
                    tipo = ''
                    while self.valor_token[i] != '}':
                        if self.valor_token[i] in [';', 'struct']:
                            pass
                        elif self.valor_token[i] == ',':
                            nome = self.valor_token[i + 1]
                            if tipo == 'int':
                                tabela_var_start.append([tipo, nome, 'int', self.numero_linha[i], False])
                            elif tipo == 'real':
                                tabela_var_start.append([tipo, nome, 'real', self.numero_linha[i], False])
                            elif tipo == 'string':
                                tabela_var_start.append([tipo, nome, 'string', self.numero_linha[i], False])
                            elif tipo == 'boolean':
                                tabela_var_start.append([tipo, nome, 'boolean', self.numero_linha[i], False])
                            else:
                                tabela_var_start.append([tipo, nome, tipo, self.numero_linha[i], False])
                            i += 1
                        elif self.valor_token[i] == '=':
                            for linha in tabela_var_start:
                                if linha[3] == self.numero_linha[i] and linha[0] == tipo:
                                    # colocar tipo e não o valor
                                    atribuicao = tipo
                                    if self.tipo_token[i + 1] == 'NRO':
                                        if self.valor_token[i + 1].__contains__('.'):
                                            atribuicao = 'real'
                                        else:
                                            atribuicao = 'int'
                                    elif self.tipo_token[i + 1] == 'CAD':
                                        atribuicao = 'string'
                                    elif self.valor_token[i + 1] in ['true', 'false']:
                                        atribuicao = 'boolean'
                                    linha[2] = atribuicao
                                    linha[4] = True
                            i += 1
                        elif self.valor_token[i] == '[':
                            i, novo_elm, tipo_elm = self.tabelaIndiceVetor(i)
                            if novo_elm != '':
                                tabela_indice_vetor.append([novo_elm, tipo_elm])
                        else:
                            tipo, nome = self.valor_token[i], self.valor_token[i + 1]
                            if tipo == 'int':
                                tabela_var_start.append(
                                    [tipo, nome, 'int',
                                     self.numero_linha[i], False])
                            elif tipo == 'real':
                                tabela_var_start.append([tipo, nome, 'real', self.numero_linha[i], False])
                            elif tipo == 'string':
                                tabela_var_start.append(
                                    [tipo, nome, 'string',
                                     self.numero_linha[i], False])
                            elif tipo == 'boolean':
                                tabela_var_start.append(
                                    [tipo, nome, 'boolean',
                                     self.numero_linha[i], False])
                            else:
                                tabela_var_start.append(
                                    [tipo, nome, tipo, self.numero_linha[i], False])
                            i += 1
                        i += 1
            indice_token += 1

        print('Tabela Var Start')
        for elm in tabela_var_start:
            print(elm)
        print('Tabela Indices Vetor Start')
        for elm in tabela_indice_vetor:
            print(elm)

        seman = AnalisadorSemantico.AnalisadorSemantico(self.texto_lexico)
        self.texto_lexico = seman.analisarStart(tabelaVarStart=tabela_var_start, tabelaStruct=self.tabela_struct,
                            tabelaVarStruct=self.tabela_var_struct, tabelaVarGlobal=self.tabela_var_global,
                            tabelaConst=self.tabela_const, tabelaIndiceVetor=tabela_indice_vetor, tabelaFunction=self.tabela_function)
        print('**************************************************')

    def tabelaIndiceVetor(self, indice_token):
        nome_indice_vetor = ''
        tipo_indice = ''
        if self.valor_token[indice_token] == '[':
            indice_token += 1
            if self.tipo_token[indice_token] == 'NRO':
                if self.valor_token[indice_token].__contains__('.') or self.valor_token[indice_token].__contains__('-')\
                        or self.valor_token[indice_token] == '0':
                    self.texto_lexico.append('Erro - Índice de vetor deve ser do tipo inteiro e positivo\n')
                    print(self.erro)
            elif self.tipo_token[indice_token] == 'IDE' and self.valor_token[indice_token + 1] == '(':
                nome_indice_vetor, tipo_indice = self.valor_token[indice_token], 'function'
                indice_token += 1
                while self.valor_token[indice_token] != ']':
                    indice_token += 1
                indice_token += 1
            elif self.tipo_token[indice_token] == 'IDE' and self.valor_token[indice_token + 1] == ']':
                nome_indice_vetor, tipo_indice = self.valor_token[indice_token], 'var'

        indice_token += 1
        return indice_token, nome_indice_vetor, tipo_indice
