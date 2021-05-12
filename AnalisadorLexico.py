import Regex


class AnalisadorLexico:

    def __init__(self):
        self.texto = ""
        self.delimitadores_exceto_ponto = [';', ',', '(', ')', '{', '}', '[', ']']
        self.opRelacionais = ['==', '!=', '>', '>=', '<', '<=', '=']
        self.palavrasReservadas = ['var', 'const', 'typedef', 'struct', 'extends', 'procedure',
                                   'function', 'start', 'return', 'if', 'else', 'then', 'while',
                                   'read', 'print', 'int', 'real', 'boolean', 'string', 'true',
                                   'false', 'global', 'local']
        self.buffer = ""
        self.buffer_comentario_bloco = ""
        self.teve_erro = False

    def analisar(self, texto):
        self.teve_erro = False
        resposta = []
        regex = Regex.Regex()
        self.texto = texto
        buffer_fixo = ""
        posicao_inicio_comentario_bloco = 1
        posicao_linha = 1
        acumulando_comentario_bloco = False
        for linha in texto:
            pular_proximo_caractere = False
            posicao_caractere = 0
            removendo_comentario_linha = False
            acumulando_cadeia_caracteres = False
            for caractere in linha:
                if not pular_proximo_caractere:
                    # ------------------------------------------------------------------------------
                    if removendo_comentario_linha:
                        if caractere == '\n':
                            removendo_comentario_linha = False
                    # ------------------------------------------------------------------------------
                    elif acumulando_comentario_bloco:
                        if caractere == '*' and linha[posicao_caractere + 1] == '/':
                            self.buffer_comentario_bloco += '*/'
                            classificacao = self.classificarBufferComentarioBloco(posicao_inicio_comentario_bloco,
                                                                                  self.buffer_comentario_bloco)
                            # print(classificacao)
                            if classificacao != "":
                                resposta.append(classificacao)
                            acumulando_comentario_bloco = False
                            pular_proximo_caractere = True
                        elif caractere == '\n':
                            self.buffer_comentario_bloco += " "
                        else:
                            self.buffer_comentario_bloco += caractere
                    # ------------------------------------------------------------------------------
                    elif acumulando_cadeia_caracteres:
                        if caractere == '\\' and linha[posicao_caractere + 1] == '"':
                            self.buffer += linha[posicao_caractere + 1]
                            pular_proximo_caractere = True
                        elif caractere == '"':
                            self.buffer += caractere
                            acumulando_cadeia_caracteres = False
                            classificacao = self.classificarBuffer(self.buffer, posicao_linha)
                            print(classificacao)
                            resposta.append(classificacao)
                        elif caractere == '\n':
                            acumulando_cadeia_caracteres = False
                            classificacao = self.classificarBuffer(self.buffer, posicao_linha)
                            print(classificacao)
                            resposta.append(classificacao)
                        else:
                            self.buffer += caractere
                    # ------------------------------------------------------------------------------
                    # print(self.buffer)
                    elif caractere in self.delimitadores_exceto_ponto:
                        if len(self.buffer) != 0:
                            # classificar buffer
                            classificacao = self.classificarBuffer(self.buffer, posicao_linha)
                            print(classificacao)
                            resposta.append(classificacao)
                        print(posicao_linha, "DEL", caractere)
                        resposta.append(f"{posicao_linha} DEL {caractere}")
                    # ------------------------------------------------------------------------------
                    elif caractere == " ":
                        if len(self.buffer) != 0:
                            # classificar buffer
                            classificacao = self.classificarBuffer(self.buffer, posicao_linha)
                            print(classificacao)
                            resposta.append(classificacao)
                    # ------------------------------------------------------------------------------
                    elif caractere == '"':
                        if len(self.buffer) != 0:
                            # classificar buffer
                            classificacao = self.classificarBuffer(self.buffer, posicao_linha)
                            print(classificacao)
                            resposta.append(classificacao)
                        self.buffer += caractere
                        # procurar próxima aspas duplas não seguida de barra invertida (\)
                        acumulando_cadeia_caracteres = True
                    # ------------------------------------------------------------------------------
                    elif caractere == '/':
                        if len(self.buffer) != 0:
                            # classificar buffer
                            classificacao = self.classificarBuffer(self.buffer, posicao_linha)
                            print(classificacao)
                            resposta.append(classificacao)
                        if linha[posicao_caractere + 1] == '/':
                            removendo_comentario_linha = True
                            pular_proximo_caractere = True
                            pass
                        elif linha[posicao_caractere + 1] == '*':
                            # comentario de bloco
                            self.buffer_comentario_bloco = "/*"
                            pular_proximo_caractere = True
                            acumulando_comentario_bloco = True
                            posicao_inicio_comentario_bloco = posicao_linha
                            pass
                        else:
                            print(posicao_linha, "ART", caractere)
                            resposta.append(f"{posicao_linha} ART {caractere}")
                        pass
                    # ------------------------------------------------------------------------------
                    elif caractere == '&':
                        if len(self.buffer) != 0:
                            # classificar buffer
                            classificacao = self.classificarBuffer(self.buffer, posicao_linha)
                            print(classificacao)
                            resposta.append(classificacao)
                        if linha[posicao_caractere + 1] == '&':
                            print(posicao_linha, "LOG", caractere + linha[posicao_caractere + 1])
                            resposta.append(f"{posicao_linha} LOG {caractere + linha[posicao_caractere + 1]}")
                            pular_proximo_caractere = True
                        else:
                            print(posicao_linha, "SIB", caractere)
                            resposta.append(f"{posicao_linha} SIB {caractere}")
                            self.teve_erro = True
                    # ------------------------------------------------------------------------------
                    elif caractere == '|':
                        if len(self.buffer) != 0:
                            # classificar buffer
                            classificacao = self.classificarBuffer(self.buffer, posicao_linha)
                            print(classificacao)
                            resposta.append(classificacao)
                        if linha[posicao_caractere + 1] == '|':
                            print(posicao_linha, "LOG", caractere + linha[posicao_caractere + 1])
                            resposta.append(f"{posicao_linha} LOG {caractere + linha[posicao_caractere + 1]}")
                            pular_proximo_caractere = True
                        else:
                            print(posicao_linha, "SIB", caractere)
                            resposta.append(f"{posicao_linha} SIB {caractere}")
                            self.teve_erro = True
                    # ------------------------------------------------------------------------------
                    elif caractere == '=' or caractere == '>' or caractere == '<':
                        if len(self.buffer) != 0:
                            # classificar buffer
                            classificacao = self.classificarBuffer(self.buffer, posicao_linha)
                            print(classificacao)
                            resposta.append(classificacao)
                        if linha[posicao_caractere + 1] == '=':
                            print(posicao_linha, "REL", caractere + linha[posicao_caractere + 1])
                            resposta.append(f"{posicao_linha} REL {caractere + linha[posicao_caractere + 1]}")
                            pular_proximo_caractere = True
                        else:
                            print(posicao_linha, "REL", caractere)
                            resposta.append(f"{posicao_linha} REL {caractere}")
                    # ------------------------------------------------------------------------------
                    elif caractere == '!':
                        if len(self.buffer) != 0:
                            # classificar buffer
                            classificacao = self.classificarBuffer(self.buffer, posicao_linha)
                            print(classificacao)
                            resposta.append(classificacao)
                        if linha[posicao_caractere + 1] == '=':
                            print(posicao_linha, "REL", caractere + linha[posicao_caractere + 1])
                            resposta.append(f"{posicao_linha} REL {caractere + linha[posicao_caractere + 1]}")
                            pular_proximo_caractere = True
                        else:
                            print(posicao_linha, "LOG", caractere)
                            resposta.append(f"{posicao_linha} LOG {caractere}")
                    # ------------------------------------------------------------------------------
                    elif caractere == '+':
                        if len(self.buffer) != 0:
                            # classificar buffer
                            classificacao = self.classificarBuffer(self.buffer, posicao_linha)
                            print(classificacao)
                            resposta.append(classificacao)
                        if linha[posicao_caractere + 1] == '+':
                            print(posicao_linha, "ART", caractere + linha[posicao_caractere + 1])
                            resposta.append(f"{posicao_linha} ART {caractere + linha[posicao_caractere + 1]}")
                            pular_proximo_caractere = True
                        else:
                            print(posicao_linha, "ART", caractere)
                            resposta.append(f"{posicao_linha} ART {caractere}")
                    # ------------------------------------------------------------------------------
                    elif caractere == '-':
                        # print(buffer_fixo)
                        if len(self.buffer) != 0:
                            # classificar buffer
                            classificacao = self.classificarBuffer(self.buffer, posicao_linha)
                            print(classificacao)
                            resposta.append(classificacao)
                            if linha[posicao_caractere + 1] == '-' \
                                    and not linha[posicao_caractere + 2].isdigit() \
                                    and linha[posicao_caractere + 2] != '-':
                                print(posicao_linha, "ART", caractere + linha[posicao_caractere + 1])
                                resposta.append(f"{posicao_linha} ART {caractere + linha[posicao_caractere + 1]}")
                                pular_proximo_caractere = True
                            else:
                                print(posicao_linha, "ART", caractere)
                                resposta.append(f"{posicao_linha} ART {caractere}")
                        elif linha[posicao_caractere + 1].isdigit() and not buffer_fixo[len(buffer_fixo) - 1].isdigit():
                            self.buffer += caractere
                        elif linha[posicao_caractere + 1] == '-' and linha[posicao_caractere + 2] != '-' and \
                                buffer_fixo[len(buffer_fixo) - 1] != '-':
                            print(posicao_linha, "ART", caractere + linha[posicao_caractere + 1])
                            resposta.append(f"{posicao_linha} ART {caractere + linha[posicao_caractere + 1]}")
                            pular_proximo_caractere = True
                        else:
                            print(posicao_linha, "ART", caractere)
                            resposta.append(f"{posicao_linha} ART {caractere}")

                    # ------------------------------------------------------------------------------
                    elif caractere == '*':
                        if len(self.buffer) != 0:
                            # classificar buffer
                            classificacao = self.classificarBuffer(self.buffer, posicao_linha)
                            print(classificacao)
                            resposta.append(classificacao)
                        print(posicao_linha, "ART", caractere)
                    # ------------------------------------------------------------------------------
                    elif caractere == '.':
                        if linha[posicao_caractere - 1].isdigit():
                            self.buffer += caractere
                        else:
                            if len(self.buffer) != 0:
                                # classificar buffer
                                classificacao = self.classificarBuffer(self.buffer, posicao_linha)
                                print(classificacao)
                                resposta.append(classificacao)
                            print(posicao_linha, "DEL", caractere)
                            resposta.append(f"{posicao_linha} DEL {caractere}")
                    # ------------------------------------------------------------------------------
                    elif caractere == '\t' or caractere == '\n':
                        if len(self.buffer) != 0:
                            # classificar buffer
                            classificacao = self.classificarBuffer(self.buffer, posicao_linha)
                            print(classificacao)
                            resposta.append(classificacao)
                    # ------------------------------------------------------------------------------
                    else:
                        self.buffer += caractere
                    if caractere != ' ' and caractere != '\n' and caractere != '\t':
                        buffer_fixo += caractere
                else:
                    pular_proximo_caractere = False

                posicao_caractere += 1
            posicao_linha += 1
        if acumulando_comentario_bloco:
            print(f"{posicao_inicio_comentario_bloco} CoMF {self.buffer_comentario_bloco}")
            resposta.append(f"{posicao_linha} CoMF {self.buffer_comentario_bloco}")
            self.teve_erro = True
        '''if not self.teve_erro:
            resposta.append("Sucesso - Arquivo sem erros")
        '''
        return resposta, self.teve_erro

    def classificarBuffer(self, buffer, numero_linha):
        self.buffer = ""
        regex = Regex.Regex()
        #print(buffer, '-----', buffer[0])
        if buffer in self.palavrasReservadas:
            resultado = f"{numero_linha} PRE {buffer}"
            return resultado
        elif buffer[0].isdigit():
            # colocar regex para validar números
            resultado = regex.identificadorNumero(buffer)
            if resultado:
                return f"{numero_linha} NRO {buffer}"
            else:
                self.teve_erro = True
                return f"{numero_linha} NMF {buffer}"
        elif buffer[0].isalpha():
            # colocar regex para validar identificadores
            resultado = regex.identificaIdentificador(buffer)
            if resultado:
                return f"{numero_linha} IDE {buffer}"
            else:
                self.teve_erro = True
                return f"{numero_linha} IMF {buffer}"
            pass
        elif buffer[0] == '"':
            # regex para cadeia de caracteres
            resultado = regex.identificadorCadeiaCaracteres(buffer)
            if resultado:
                return f"{numero_linha} CAD {buffer}"
            else:
                self.teve_erro = True
                return f"{numero_linha} CMF {buffer}"
        elif buffer[0] == '-':
            resultado = regex.identificadorNumeroNegativo(buffer)
            if resultado:
                return f"{numero_linha} NRO {buffer}"
            else:
                self.teve_erro = True
                return f"{numero_linha} NMF {buffer}"
        else:
            self.teve_erro = True
            return f"{numero_linha} SIB {buffer}"

    def classificarBufferComentarioBloco(self, numero_linha, buffer):
        self.buffer_comentario_bloco = ""
        regex = Regex.Regex()
        resultado = regex.identificaComentarioBloco(buffer)
        # print(buffer)
        # print(resultado)
        if not resultado:
            self.teve_erro = True
            return f"{numero_linha} CoMF {buffer}"
        return ""
