class Sync:

    def __init__(self):
        self.sync_tokens = {
            'Decl': ['function', 'procedure'],

            'StructBlock': ['function', 'procedure', 'struct', 'start'],

            'ConstBlock': ['procedure', 'var', 'function', 'start', 'struct', '{', '}'],

            'Type': ['IDE'],

            'Typedef': ['}', 'int', 'real', 'IDE', 'string', 'typedef', 'boolean', 'struct'],

            'VarDecl': ['string', 'typedef', 'boolean', '}', 'int', 'struct', 'real', 'IDE'],

            'VarId': ['string', 'typedef', 'boolean', '}', 'int', 'struct', 'real', 'IDE'],

            'Var': [',', ';'],

            'ConstDecl': ['string', 'boolean', '}', 'int', 'real'],

            'ConstId': ['string', 'typedef', 'local', 'boolean', '}', 'int', 'struct', 'real', 'global', 'IDE'],

            'Const': ['=', ','],

            'ConstList': ['string', 'boolean', '}', ';', 'int', 'real', 'IDE'],

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

            'StartBlock': ['$', 'function', 'procedure', 'struct', 'typedef', '{', 'if', 'while', 'return', 'local', 'global', 'print', 'read', 'IDE'],

            'ProcDecl': ['$', 'function', 'procedure'],

            'ParamType': ['IDE'],

            'ParamMultArrays': [',', ')'],

            'ParamArrays': [',', ')'],

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

            'IdValue': [')', ';', '+', '>=', '&&', '-', '>', '!=', '||', ',', ']', '<=', '==', '*', '<', '/', '}'],

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
