# --- AST 類別 ---
class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Assignment(ASTNode):
    def __init__(self, targets, value):
        self.targets = targets
        self.value = value

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements


# --- Parser 類別 ---
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', '')

    def eat(self, token_type):
        if self.current_token()[0] == token_type:
            val = self.current_token()[1]
            self.pos += 1
            return val
        else:
            raise SyntaxError(f"Expected token {token_type}, got {self.current_token()}")

    def parse(self):
        statements = []
        while self.current_token()[0] != 'EOF':
            stmt = self.statement()
            statements.append(stmt)
        return Program(statements)

    def statement(self):
        if self.current_token()[0] == 'IDENTIFIER':
            return self.assignment()
        else:
            raise SyntaxError(f"Unknown statement starting with: {self.current_token()}")

    def assignment(self):
        # 支援 x = 3 + 5
        identifier = Identifier(self.eat('IDENTIFIER'))
        self.eat('OPERATOR')  # 應該是 '='
        expr = self.expression()
        return Assignment([identifier], expr)

    def expression(self):
        # 支援簡單的二元運算（左結合）
        left = self.term()
        while self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('+', '-'):
            op = self.eat('OPERATOR')
            right = self.term()
            left = BinaryExpression(left, op, right)
        return left

    def term(self):
        left = self.factor()
        while self.current_token()[0] == 'OPERATOR' and self.current_token()[1] in ('*', '/'):
            op = self.eat('OPERATOR')
            right = self.factor()
            left = BinaryExpression(left, op, right)
        return left

    def factor(self):
        tok_type, tok_val = self.current_token()
        if tok_type == 'NUMBER':
            self.eat('NUMBER')
            return Number(tok_val)
        elif tok_type == 'IDENTIFIER':
            return Identifier(self.eat('IDENTIFIER'))
        elif tok_type == 'DELIMITER' and tok_val == '(':
            self.eat('DELIMITER')  # (
            node = self.expression()
            self.eat('DELIMITER')  # )
            return node
        else:
            raise SyntaxError(f"Unexpected token in factor: {self.current_token()}")
