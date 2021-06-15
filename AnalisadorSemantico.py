class AnalisadorSemantico:

    def __init__(self, resposta):
        self.erro = ''
        self.resposta = resposta

    def analisarConst(self, tabelaConst, tabelaIndiceVetor):
        # analisar duplicidade de variaveis em uma mesma const
        lista_var = []
        for linha in tabelaConst:
            lista_var.append(linha[1])
        for item in lista_var:
            quantidade = lista_var.count(item)
            if quantidade > 1:
                self.resposta.append(f'Erro - Mais de uma constante com o mesmo nome - const {item}\n')
                break

        # analisar tipo da variavel em relação a sua atribuição
        for linha in tabelaConst:
            if linha[0] != linha[2]:
                self.resposta.append(f'Erro - Tipo de variável incompatível - type {linha[2]} deveria ser type {linha[0]}\n')
                break
        if len(tabelaIndiceVetor) > 0:
            achou_indice = False
            for ind in tabelaIndiceVetor:
                achou_indice = False
                if ind[1] == 'function':
                    self.resposta.append(f'Erro em indice de vetor. Função não declarada.\n')
                    break
                for const in tabelaConst:
                    if ind[0] == const[1] and const[0] == 'int' and const[2] == 'int':
                        achou_indice = True
                        break
                if achou_indice:
                    break
            if not achou_indice:
                self.resposta.append(f'Erro em indice de vetor. Verifique se a variável existe e é type int.\n')

        return self.resposta



    def analisarVarGlobal(self, tabelaVar, tabelaStruct, tabelaConst, tabelaIndiceVetor):
        # analisar duplicidade de variaveis em uma mesma var
        lista_var = []
        for linha in tabelaVar:
            lista_var.append(linha[1])
        for item in lista_var:
            quantidade = lista_var.count(item)
            if quantidade > 1:
                self.resposta.append(f'Erro - Mais de uma variável com o mesmo nome - var {item}\n')
                break

        # analisar duplicidade de variaveis em relacao as constantes
        tem_const_igual = False
        for var in tabelaVar:
            for const in tabelaConst:
                if var[1] == const[1]:
                    tem_const_igual = True
                    break
            if tem_const_igual:
                self.resposta.append(f'Erro - variável com o mesmo nome de constante - var {var[1]}\n')
                break

        # analisar tipo da variavel em relação a sua atribuição
        for linha in tabelaVar:
            if linha[0] != linha[2]:
                self.resposta.append(f'Erro - Tipo de variável incompatível - type {linha[2]} deveria ser type {linha[0]}\n')
                break

        # analisar tipo nao primitivo se existe na tabela de var global
        existe_struct_declarada = False
        for linha in tabelaVar:
            if linha[0] not in ['int', 'real', 'boolean', 'string']:
                for elm in tabelaStruct:
                    if elm[0] == linha[0]:
                        existe_struct_declarada = True
                        break
                if not existe_struct_declarada:
                    self.resposta.append(f'Erro - Tipo não primitivo desconhecido - type {linha[0]}\n')
                    break

        # analisar indices dos vetores em var global
        if len(tabelaIndiceVetor) > 0:
            achou_indice = False
            for ind in tabelaIndiceVetor:
                achou_indice = False
                if ind[1] == 'function':
                    self.resposta.append(f'Erro em indice de vetor. Função não declarada.')
                    break
                achou_indice = False
                for var in tabelaVar:
                    if ind[0] == var[1] and var[0] == 'int' and var[2] == 'int' and var[4] == True:
                        achou_indice = True
                        break
                if achou_indice:
                    break
                for const in tabelaConst:
                    if ind[0] == const[1] and const[0] == 'int' and const[2] == 'int':
                        achou_indice = True
                        break
                if achou_indice:
                    break
            if not achou_indice:
                self.resposta.append(f'Erro em indice de vetor. Verifique se a variável existe e é type int.\n')
        return self.resposta


    def analisarStruct(self, tabelaStruct, tabelaVarStruct):
        # analisar duplicidade de structs
        for elm in tabelaStruct:
            quantidade = tabelaStruct.count(elm)
            if quantidade > 1:
                self.resposta.append(f'Erro - Mais de uma struct com o mesmo nome - struct {elm}\n')
                break
        # analisar se a struct da herança existe
        lista_extends = []
        lista_structs_declaradas = []
        for linha in tabelaStruct:
            if linha[1] != '':
                lista_extends.append(linha[1])
            lista_structs_declaradas.append(linha[0])
        nao_existe_struct_heranca = False
        nome_struct_erro = ''
        for elm in lista_extends:
            if not lista_structs_declaradas.__contains__(elm):
                nao_existe_struct_heranca = True
                nome_struct_erro = elm
        if nao_existe_struct_heranca:
            self.resposta.append(f'Erro - Essa struct não existe, portanto não é possível usar o extends - struct {nome_struct_erro}\n')

        # analisar duplicidade de variaveis em uma mesma struct
        teve_duplicidade = False
        for elm in tabelaStruct:
            lista_var = []
            for linha in tabelaVarStruct:
                # verificando se as variáveis são da mesma struct pra poder fazer a verificação
                if linha[3] == elm:
                    lista_var.append(linha[1])
            for item in lista_var:
                quantidade = lista_var.count(item)
                if quantidade > 1:
                    teve_duplicidade = True
                    self.erro += f'Erro - Mais de uma variável com o mesmo nome - var {item} - na struct {elm}\n'
                    break
            if teve_duplicidade:
                break

        # analisar tipo da variavel em relação a sua atribuição
        for linha in tabelaVarStruct:
            if linha[0] != linha[2]:
                self.resposta.append(f'Erro - Tipo de variável incompatível - type {linha[2]} deveria ser type {linha[0]}\n')
                break

        # analisar tipo nao primitivo se existe na tabela de struct
        existe_struct_declarada = False
        for linha in tabelaVarStruct:
            if linha[0] not in ['int', 'real', 'boolean', 'string']:
                for elm in tabelaStruct:
                    if elm[0] == linha[0]:
                        existe_struct_declarada = True
                        break
                if not existe_struct_declarada:
                    self.resposta.append(f'Erro - Tipo não primitivo desconhecido - type {linha[0]}\n')
                    break
        return self.resposta



    def analisarIndiceVetorStruct(self, tabelaVarStruct, tabelaVarGlobal, tabelaConst, tabelaIndiceVetor, tabelaFunction):
        # analisar indices dos vetores em struct
        if len(tabelaIndiceVetor) > 0:
            achou_indice = False
            achou_function = False
            for ind in tabelaIndiceVetor:
                if ind[1] == 'var':
                    achou_indice = False
                    for varStruct in tabelaVarStruct:
                        if ind[2] == varStruct[3] and ind[0] == varStruct[1] and \
                                varStruct[0] == 'int' and varStruct[2] == 'int' and varStruct[5] == True:
                            achou_indice = True
                            break
                    if achou_indice:
                        break
                    for var in tabelaVarGlobal:
                        if ind[0] == var[1] and var[0] == 'int' and var[2] == 'int' and var[4] == True:
                            achou_indice = True
                            break
                    if achou_indice:
                        break
                    for const in tabelaConst:
                        if ind[0] == const[1] and const[0] == 'int' and const[2] == 'int':
                            achou_indice = True
                            break
                    if achou_indice:
                        break
                else:
                    achou_function = False
                    for func in tabelaFunction:
                        if ind[0] == func[1] and func[0] != 'int':
                            achou_function = True
                            self.resposta.append(f'Erro em indice de vetor. Função deve retornar int.\n')
                            break
                        elif ind[0] == func[1] and func[0] == 'int':
                            achou_function = True
                            break
                    if not achou_function:
                        self.resposta.append(f'Erro em indice de vetor. Função não declarada.\n')
            if not achou_indice and not achou_function:
                self.resposta.append(f'Erro em indice de vetor. Verifique se a variável existe, '
                             f'é type int e sua atribuição é type int.\n')
        return self.resposta


    def analisarProcedure(self, tabelaProcedure, tabelaVarProcedure, tabelaParametrosProcedure, tabelaStruct,
                          tabelaVarStruct, tabelaVarGlobal, tabelaConst, tabelaIndiceVetor, tabelaFunction):
        # analisar duplicidade de procedures
        for elm in tabelaProcedure:
            quantidade = tabelaProcedure.count(elm)
            if quantidade > 1:
                self.resposta.append(f'Erro - Mais de uma procedure com o mesmo nome - procedure {elm}\n')
                break

        # analisar se tem nome de variável igual a nome de parâmetro
        for parametro in tabelaParametrosProcedure:
            for variavel in tabelaVarProcedure:
                if parametro[1] == variavel[1] and parametro[2] == variavel[3]:
                    self.resposta.append(f'Erro - Mais de uma variável com o mesmo nome - var {parametro[1]} - na procedure {parametro[2]}\n')
                    break

        # analisar duplicidade de variaveis em uma mesma procedure
        teve_duplicidade = False
        for elm in tabelaProcedure:
            lista_var = []
            for linha in tabelaVarProcedure:
                # verificando se as variáveis são da mesma procedure pra poder fazer a verificação
                if linha[3] == elm:
                    lista_var.append(linha[1])
            for item in lista_var:
                quantidade = lista_var.count(item)
                if quantidade > 1:
                    teve_duplicidade = True
                    self.resposta.append(f'Erro - Mais de uma variável com o mesmo nome - var {item} - na procedure {elm}\n')
                    break
            if teve_duplicidade:
                break
        # analisar tipo da variavel em relação a sua atribuição
        for linha in tabelaVarProcedure:
            if linha[0] != linha[2]:
                self.resposta.append(f'Erro - Tipo de variável incompatível - type {linha[2]} deveria ser type {linha[0]}\n')
                break

        # analisar tipo nao primitivo se existe na tabela de struct para as variaveis
        existe_struct_declarada = False
        for linha in tabelaVarProcedure:
            if linha[0] not in ['int', 'real', 'boolean', 'string']:
                for elm in tabelaStruct:
                    if elm[0] == linha[0]:
                        existe_struct_declarada = True
                        break
                if not existe_struct_declarada:
                    self.resposta.append(f'Erro - Tipo não primitivo desconhecido - type {linha[0]}\n')
                    break

        # analisar tipo nao primitivo se existe na tabela de struct para os paramtros
        existe_struct_declarada = False
        for linha in tabelaParametrosProcedure:
            if linha[0] not in ['int', 'real', 'boolean', 'string']:
                for elm in tabelaStruct:
                    if elm[0] == linha[0]:
                        existe_struct_declarada = True
                        break
                if not existe_struct_declarada:
                    self.resposta.append(f'Erro - Tipo não primitivo desconhecido - type {linha[0]}\n')
                    break

        # analisar indices de vetor para procedure
        if len(tabelaIndiceVetor) > 0:
            achou_indice = False
            achou_function = False
            for ind in tabelaIndiceVetor:
                if ind[1] == 'var':
                    for varProc in tabelaVarProcedure:
                        if ind[2] == varProc[3] and ind[0] == varProc[1] and \
                                varProc[0] == 'int' and varProc[2] == 'int' and varProc[5] == True:
                            achou_indice = True
                            break
                    if achou_indice:
                        break
                    for param in tabelaParametrosProcedure:
                        if ind[2] == param[2] and ind[0] == param[1] and param[0] == 'int':
                            achou_indice = True
                            break
                    if achou_indice:
                        break
                    for var in tabelaVarGlobal:
                        if ind[0] == var[1] and var[0] == 'int' and var[2] == 'int' and var[4] == True:
                            achou_indice = True
                            break
                    if achou_indice:
                        break
                    for const in tabelaConst:
                        if ind[0] == const[1] and const[0] == 'int' and const[2] == 'int':
                            achou_indice = True
                            break
                    if achou_indice:
                        break
                else:
                    achou_function = False
                    for func in tabelaFunction:
                        if ind[0] == func[1] and func[0] != 'int':
                            achou_function = True
                            self.resposta.append(f'Erro em indice de vetor. Função deve retornar int.\n')
                            break
                        elif ind[0] == func[1] and func[0] == 'int':
                            achou_function = True
                            break
                    if not achou_function:
                        self.resposta.append(f'Erro em indice de vetor. Função não declarada.\n')

            if not achou_indice and not achou_function:
                self.resposta.append(f'Erro em indice de vetor. Verifique se a variável existe, '
                             f'é type int e sua atribuição é type int.\n')
        return self.resposta



    def analisarFunction(self, tabelaFunction, tabelaVarFunction, tabelaParametrosFunction, tabelaStruct,
                         tabelaVarStruct, tabelaProcedure, tabelaVarGlobal, tabelaConst, tabelaIndiceVetor):
        # analisar duplicidade de functions
        for elm in tabelaFunction:
            quantidade = tabelaFunction.count(elm)
            if quantidade > 1:
                self.resposta.append(f'Erro - Mais de uma function com o mesmo nome - function {elm}\n')
                break

        # analisar duplicidade function em relação a procedure
        tem_procedure_igual = False
        for func in tabelaFunction:
            for proc in tabelaProcedure:
                if func[1] == proc:
                    tem_procedure_igual = True
                    break
            if tem_procedure_igual:
                self.resposta.append(f'Erro - function com o mesmo nome de procedure - function {func[1]}\n')
                break

        # analisar se tem nome de variável igual a nome de parâmetro
        for parametro in tabelaParametrosFunction:
            for variavel in tabelaVarFunction:
                if parametro[1] == variavel[1] and parametro[2] == variavel[3]:
                    self.resposta.append(f'Erro - Mais de uma variável com o mesmo nome - var {parametro[1]} - na function {parametro[2]}\n')
                    break

        # analisar duplicidade de variaveis em uma mesma function
        teve_duplicidade = False
        for elm in tabelaFunction:
            lista_var = []
            for linha in tabelaVarFunction:
                # verificando se as variáveis são da mesma function pra poder fazer a verificação
                if linha[3] == elm:
                    lista_var.append(linha[1])
            for item in lista_var:
                quantidade = lista_var.count(item)
                if quantidade > 1:
                    teve_duplicidade = True
                    self.resposta.append(f'Erro - Mais de uma variável com o mesmo nome - var {item} - na function {elm}\n')
                    break
            if teve_duplicidade:
                break
        # analisar tipo da variavel em relação a sua atribuição
        for linha in tabelaVarFunction:
            if linha[0] != linha[2]:
                self.resposta.append(f'Erro - Tipo de variável incompatível - type {linha[2]} deveria ser type {linha[0]}\n')
                break

        # analisar tipo nao primitivo se existe na tabela de struct
        existe_struct_declarada = False
        for linha in tabelaVarFunction:
            if linha[0] not in ['int', 'real', 'boolean', 'string']:
                for elm in tabelaStruct:
                    if elm[0] == linha[0]:
                        existe_struct_declarada = True
                        break
                if not existe_struct_declarada:
                    self.resposta.append(f'Erro - Tipo não primitivo desconhecido - type {linha[0]}\n')
                    break

        # analisar tipo nao primitivo se existe na tabela de struct para o retorno da função
        existe_struct_declarada = False
        for linha in tabelaFunction:
            if linha[0] not in ['int', 'real', 'boolean', 'string']:
                for elm in tabelaStruct:
                    if elm[0] == linha[0]:
                        existe_struct_declarada = True
                        break
                if not existe_struct_declarada:
                    self.resposta.append(f'Erro - Tipo não primitivo desconhecido - type {linha[0]}\n')
                    break

        # analisar tipo nao primitivo se existe na tabela de struct para os parametros da função
        existe_struct_declarada = False
        for linha in tabelaParametrosFunction:
            if linha[0] not in ['int', 'real', 'boolean', 'string']:
                for elm in tabelaStruct:
                    if elm[0] == linha[0]:
                        existe_struct_declarada = True
                        break
                if not existe_struct_declarada:
                    self.resposta.append(f'Erro - Tipo não primitivo desconhecido - type {linha[0]}\n')
                    break

        # analisar indices de vetor para function
        if len(tabelaIndiceVetor) > 0:
            achou_indice = False
            achou_function = False
            for ind in tabelaIndiceVetor:
                if ind[1] == 'var':
                    achou_indice = False
                    for varFunc in tabelaVarFunction:
                        if ind[2] == varFunc[3] and ind[0] == varFunc[1] and \
                                varFunc[0] == 'int' and varFunc[2] == 'int' and varFunc[5] == True:
                            achou_indice = True
                            break
                    if achou_indice:
                        break
                    for param in tabelaParametrosFunction:
                        if ind[2] == param[2] and ind[0] == param[1] and param[0] == 'int':
                            achou_indice = True
                            break
                    if achou_indice:
                        break
                    for var in tabelaVarGlobal:
                        if ind[0] == var[1] and var[0] == 'int' and var[2] == 'int' and var[4] == True:
                            achou_indice = True
                            break
                    if achou_indice:
                        break
                    for const in tabelaConst:
                        if ind[0] == const[1] and const[0] == 'int' and const[2] == 'int':
                            achou_indice = True
                            break
                    if achou_indice:
                        break
                else:
                    achou_function = False
                    for func in tabelaFunction:
                        if ind[0] == func[1] and func[0] != 'int':
                            achou_function = True
                            self.resposta.append(f'Erro em indice de vetor. Função deve retornar int.\n')
                            break
                        elif ind[0] == func[1] and func[0] == 'int':
                            achou_function = True
                            break
                    if not achou_function:
                        self.resposta.append(f'Erro em indice de vetor. Função não declarada.\n')

            if not achou_indice and not achou_function:
                self.resposta.append(f'Erro em indice de vetor. Verifique se a variável existe, '
                             f'é type int e sua atribuição é type int.\n')
        return self.resposta



    def analisarStart(self, tabelaVarStart, tabelaStruct, tabelaVarStruct, tabelaVarGlobal, tabelaConst, tabelaIndiceVetor, tabelaFunction):
        # analisar duplicidade de variaveis no start
        lista_var = []
        for linha in tabelaVarStart:
            lista_var.append(linha[1])
        for item in lista_var:
            quantidade = lista_var.count(item)
            if quantidade > 1:
                self.resposta.append(f'Erro - Mais de uma variável com o mesmo nome - var {item} - no start\n')
                break

        # analisar tipo nao primitivo se existe na tabela de struct
        existe_struct_declarada = False
        for linha in tabelaVarStart:
            if linha[0] not in ['int', 'real', 'boolean', 'string']:
                for elm in tabelaStruct:
                    if elm[0] == linha[0]:
                        existe_struct_declarada = True
                        break
                if not existe_struct_declarada:
                    self.resposta.append(f'Erro - Tipo não primitivo desconhecido - type {linha[0]}\n')
                    break

        # analisar tipo da variavel em relação a sua atribuição
        for linha in tabelaVarStart:
            if linha[0] != linha[2]:
                self.resposta.append(f'Erro - Tipo de variável incompatível - type {linha[2]} deveria ser type {linha[0]}\n')
                break

        # analisar indices dos vetores em var start
        if len(tabelaIndiceVetor) > 0:
            achou_indice = False
            achou_function = False
            for ind in tabelaIndiceVetor:
                if ind[1] == 'var':
                    achou_indice = False
                    for varStart in tabelaVarStart:
                        if ind[0] == varStart[1] and varStart[0] == 'int' and varStart[2] == 'int' and varStart[4] == True:
                            achou_indice = True
                            break
                    if achou_indice:
                        break
                    for var in tabelaVarGlobal:
                        if ind[0] == var[1] and var[0] == 'int' and var[2] == 'int' and var[4] == True:
                            achou_indice = True
                            break
                    if achou_indice:
                        break
                    for const in tabelaConst:
                        if ind[0] == const[1] and const[0] == 'int' and const[2] == 'int':
                            achou_indice = True
                            break
                    if achou_indice:
                        break
                else:
                    achou_function = False
                    for func in tabelaFunction:
                        if ind[0] == func[1] and func[0] != 'int':
                            achou_function = True
                            self.resposta.append(f'Erro em indice de vetor. Função deve retornar int.\n')
                            break
                        elif ind[0] == func[1] and func[0] == 'int':
                            achou_function = True
                            break
                    if not achou_function:
                        self.resposta.append(f'Erro em indice de vetor. Função não declarada.\n')

            if not achou_indice and not achou_function:
                self.resposta.append(f'Erro em indice de vetor. Verifique se a variável existe, '
                             f'é type int e sua atribuição é type int.\n')
        return self.resposta
