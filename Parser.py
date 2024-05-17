class Parser:
    def __init__(self, tokens):
        # Инициализация парсера с токенами
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]

    def advance(self):
        # Переход к следующему токену
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def expect(self, token):
        # Ожидание определенного токена
        if self.current_token == token:
            self.advance()
        else:
            raise SyntaxError(f"Expected {token}, got {self.current_token}")

    def parse_program(self):
        # Парсинг программы
        self.expect('{')
        while self.current_token != 'end':
            if self.current_token == 'dim':
                self.parse_declaration()
            else:
                self.parse_statement()
            if self.current_token == ':':
                self.advance()
            elif self.current_token == '\n':
                self.advance()
        self.expect('}')
        self.expect('end')

    def parse_declaration(self):
        # Парсинг объявления переменной
        self.expect('dim')
        self.parse_identifier()
        while self.current_token == ',':
            self.advance()
            self.parse_identifier()
        self.parse_type()

    def parse_type(self):
        # Парсинг типа данных
        if self.current_token in type_of_data:
            self.advance()
        else:
            raise SyntaxError(f"Expected type, got {self.current_token}")

    def parse_statement(self):
        # Парсинг оператора
        if self.current_token in ['if', 'while', 'for', 'begin', 'readln', 'writeln']:
            if self.current_token == 'if':
                self.parse_if_statement()
            elif self.current_token == 'while':
                self.parse_while_statement()
            elif self.current_token == 'for':
                self.parse_for_statement()
            elif self.current_token == 'begin':
                self.parse_compound_statement()
            elif self.current_token == 'readln':
                self.parse_readln_statement()
            elif self.current_token == 'writeln':
                self.parse_writeln_statement()
        else:
            self.parse_assignment()

    def parse_if_statement(self):
        # Парсинг оператора if
        self.expect('if')
        self.parse_expression()
        self.expect('then')
        self.parse_statement()
        if self.current_token == 'else':
            self.advance()
            self.parse_statement()

    def parse_while_statement(self):
        # Парсинг оператора while
        self.expect('while')
        self.expect('(')
        self.parse_expression()
        self.expect(')')
        self.parse_statement()

    def parse_for_statement(self):
        # Парсинг оператора for
        self.expect('for')
        self.parse_assignment()
        self.expect('to')
        self.parse_expression()
        self.expect('do')
        self.parse_statement()

    def parse_compound_statement(self):
        # Парсинг составного оператора
        self.expect('begin')
        self.parse_statement()
        while self.current_token == ';':
            self.advance()
            self.parse_statement()
        self.expect('end')

    def parse_readln_statement(self):
        # Парсинг оператора readln
        self.expect('readln')
        self.parse_identifier()
        while self.current_token == ',':
            self.advance()
            self.parse_identifier()

    def parse_writeln_statement(self):
        # Парсинг оператора writeln
        self.expect('writeln')
        self.parse_expression()
        while self.current_token == ',':
            self.advance()
            self.parse_expression()

    def parse_assignment(self):
        # Парсинг оператора присваивания
        self.parse_identifier()
        self.expect('as')
        self.parse_expression()

    def parse_expression(self):
        # Парсинг выражения
        self.parse_operand()
        while self.current_token in operator:
            self.advance()
            self.parse_operand()

    def parse_operand(self):
        # Парсинг операнда
        self.parse_term()
        while self.current_token in arithmetic_operator:
            self.advance()
            self.parse_term()

    def parse_term(self):
        # Парсинг терма
        self.parse_factor()
        while self.current_token in arithmetic_operator:
            self.advance()
            self.parse_factor()

    def parse_factor(self):
        # Парсинг фактора
        if self.current_token.isidentifier():
            self.parse_identifier()
        elif self.current_token.isdigit():
            self.parse_number()
        elif self.current_token == '~':
            self.advance()
            self.parse_factor()
        elif self.current_token == '(':
            self.advance()
            self.parse_expression()
            self.expect(')')

    def parse_identifier(self):
        # Парсинг идентификатора
        if self.current_token.isidentifier():
            self.advance()
        else:
            raise SyntaxError(f"Expected identifier, got {self.current_token}")

    def parse_number(self):
        # Парсинг числа
        if self.current_token.isdigit():
            self.advance()
        else:
            raise SyntaxError(f"Expected number, got {self.current_token}")
