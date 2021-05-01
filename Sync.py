class Sync:

    def __init__(self):
        self.sync_tokens = {
            'Decl': ['function', 'procedure'],

            'StructBlock': ['function', 'procedure', 'struct', 'start'],

            'Type': ['IDE'],

            'Typedef': ['local', '}', 'int', 'real', 'IDE', 'string', 'typedef', 'boolean', 'struct', 'global'],

            'VarDecl': ['string', 'typedef', 'local', 'boolean', '}', 'int', 'struct', 'real', 'global', 'IDE'],

            'VarId': ['string', 'typedef', 'local', 'boolean', '}', 'int', 'struct', 'real', 'global', 'IDE'],

            'Var': [',', ';'],

            'ConstDecl': ['string', 'typedef', 'local', 'boolean', '}', 'int', 'struct', 'real', 'global', 'IDE'],

            'ConstId': ['string', 'typedef', 'local', 'boolean', '}', 'int', 'struct', 'real', 'global', 'IDE'],

            'Const': ['=', ','],

            'ConstList': ['string', 'typedef', 'local', 'boolean', '}', ';', 'int', 'struct', 'real', 'global', 'IDE'],

            'DeclAtribute': [';'],

            'ArrayDecl': [';'],

            'ArrayDef': ['}'],

            'Array': ['*', '=', '++', '[', '}', ']', '<', '-', '<=', '>', '.', '!=', '/', '&&', '||', '>=', ';', '--',
                      ')', '+', ',', '=='],

            'Assign': ['local', '}', 'int', 'real', 'else', 'return', 'id', 'while', 'string', 'typedef', 'read',
                       'boolean', ';', 'struct', 'global', 'print', '{', 'if'],

            'Access': ['*', '=', '++', '}', ']', '<', '-', '<=', '>', '.', '!=', '/', '&&', '||', '>=', ';', '--', ')',
                       '+', ',', '=='],

            'FuncDecl': ['$', 'function', 'procedure'],

            'StartBlock': ['$', 'function', 'procedure', 'struct', 'typedef', '{', 'if', 'while', 'return', 'local', 'global', 'print', 'read'],

            'ProcDecl': ['$', 'function', 'procedure'],

            'ParamType': ['IDE'],

            'Param': [',', ')'],

            'FuncBlock': ['$', 'function', 'procedure'],

            'FuncStm': ['local', '}', 'else', 'return', 'while', 'IDE', 'read', ';', 'global', 'print', '{', 'if'],

            'FuncNormalStm': ['local', '}', 'else', 'return', 'while', 'IDE', 'read', ';', 'global', 'print', '{',
                              'if'],

            'VarStm': ['local', '}', 'else', 'return', 'while', 'IDE', 'read', ';', 'global', 'print', '{',
                       'if'],

            'StmId': ['local', '}', 'int', 'real', 'else', 'return', 'IDE', 'while', 'string', 'typedef',
                      'read', 'boolean', ';', 'struct', 'global', 'print', '{', 'if'],

            'StmScope': ['local', '}', 'int', 'real', 'else', 'return', 'IDE', 'while', 'string', 'typedef', 'read',
                         'boolean', ';', 'struct', 'global', 'print', '{', 'if'],

            'StmCmd': ['local', '}', 'else', 'return', 'while', 'IDE', 'read', ';', 'global', 'print', '{', 'if'],

            'Expr': [')', '}', ',', ';', ']'],

            'Or': [')', '}', ',', ';', ']'],

            'And': ['}', '||', ';', ']', ')', ','],

            'Equate': ['&&', '||', '}', ';', ']', ')', ','],

            'Compare': ['!=', '&&', '||', '}', ';', ',', ')', ']', '=='],

            'Add': ['}', ',', '<', '<=', '>', '!=', '&&', '||', '>=', ';', ')', ']', '=='],

            'Mult': ['}', ',', '<', '-', '<=', '>', '!=', '&&', '||', '>=', ';', ')', '+', ']', '=='],

            'Unary': ['*', '}', ']', '<', '-', '<=', '>', '!=', '/', '&&', '||', '>=', ';', ')', '+', ',', '=='],

            'Value': ['*', '}', ']', '<', '-', '<=', '>', '!=', '/', '&&', '||', '>=', ';', ')', '+', ',', '=='],

            'LogExpr': [')'],

            'LogOr': [')'],

            'LogAnd': ['||', ')'],

            'LogEquate': [')', '&&', '||'],

            'LogCompare': ['!=', ')', '&&', '||', '=='],

            'LogUnary': ['!=', '&&', '||', '>=', '<', '<=', ')', '>', '=='],

            'LogValue': ['!=', '&&', '||', '>=', '<', '<=', ')', '>', '==']
        }

    def sync(self):
        return self.sync_tokens
