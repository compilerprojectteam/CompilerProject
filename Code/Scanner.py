class CharType:
    @staticmethod
    def is_digit(c):
        return "9" >= c >= "0"

    @staticmethod
    def is_letter(c):
        return ("z" >= c >= "a") or ("Z" >= c >= "A")

    @staticmethod
    def is_symbol(c):
        return c in ":;,{}()[]+-*<="

    @staticmethod
    def is_white_space(c):
        return c in "\t\n\r\f\v "

    @staticmethod
    def everything(c):
        return True

    @staticmethod
    def match_except(f, c, c_list):
        res = f(c)
        for c_ in c_list:
            if c_ == c:
                return False
        return res


class Token:
    NUMBER = "NUM"
    ID = "ID"
    SYMBOL = "SYMBOL"
    KEYWORD = "KEYWORD"
    COMMENT = "COMMENT"
    EOF = "EOF"
    WHITE_SPACE = "WHITE_SPACE"
    ERROR = "ERROR"
    KEYWORDS_LIST = [
        "if",
        "else",
        "void",
        "int",
        "while",
        "break",
        "continue",
        "switch",
        "default",
        "case",
        "return",
    ]

    def __init__(self, ttype, value):
        self.value = value
        self.type = ttype
        if self.value in Token.KEYWORDS_LIST:
            self.type = Token.KEYWORD

    def to_str(self):
        if self.type == Token.ERROR:
            return "({}, invalid input) ".format(self.value)
        else:
            return "({}, {}) ".format(self.type, self.value)

    def translate_for_parser(self):
        if self.type in [self.NUMBER, self.ID, self.EOF]:
            return self.type
        return self.value


class State:
    def __init__(self, final=False, finished=False, stype=None):
        self.final = final
        self.finished = finished
        self.type = stype


class ScannerDFA:
    def __init__(self):
        self.current_state = self.start_state = State()

        self.number_state = State(final=True, stype=Token.NUMBER)
        self.id_state = State(final=True, stype=Token.ID)

        self.symbol_except_equal_state = State(final=True, finished=True, stype=Token.SYMBOL)
        self.equal_state = State(final=True, stype=Token.SYMBOL)
        self.equal_equal_state = State(final=True, finished=True, stype=Token.SYMBOL)

        self.slash_state = State()
        self.slash_star_state = State()
        self.slash_star_star_state = State()
        self.comment_type1_final_state = State(final=True, finished=True, stype=Token.COMMENT)
        self.comment_type2_final_state = State(final=True, stype=Token.COMMENT)

        self.white_space_state = State(final=True, finished=True, stype=Token.WHITE_SPACE)
        self.EOF_state = State(final=True, finished=True, stype=Token.EOF)

    def predict(self, c, state=None):

        if state is None:
            state = self.current_state

        if state == self.start_state:
            if c is None:
                return self.EOF_state
            elif CharType.is_digit(c):
                return self.number_state
            elif CharType.is_letter(c):
                return self.id_state
            elif CharType.match_except(CharType.is_symbol, c, ["="]):
                return self.symbol_except_equal_state
            elif c == "=":
                return self.equal_state
            elif c == "/":
                return self.slash_state
            elif CharType.is_white_space(c):
                return self.white_space_state

        elif state == self.number_state:
            if CharType.is_digit(c):
                return self.number_state

        elif state == self.id_state:
            if CharType.is_digit(c) or CharType.is_letter(c):
                return self.id_state

        elif state == self.symbol_except_equal_state:
            pass

        elif state == self.equal_state:
            if c == "=":
                return self.equal_equal_state

        elif state == self.equal_equal_state:
            pass

        elif state == self.slash_state:
            if c == "*":
                return self.slash_star_state
            elif c == "/":
                return self.comment_type2_final_state

        elif state == self.slash_star_state:
            if CharType.match_except(CharType.everything, c, ["*"]):
                return self.slash_star_state
            elif c == "*":
                return self.slash_star_star_state

        elif state == self.slash_star_star_state:
            if CharType.match_except(CharType.everything, c, ["/", "*"]):
                return self.slash_star_state
            if c == "*":
                return self.slash_star_star_state
            if c == "/":
                return self.comment_type1_final_state

        elif state == self.comment_type1_final_state:
            pass

        elif state == self.comment_type2_final_state:
            if CharType.match_except(CharType.everything, c, ["\n"]):
                return self.comment_type2_final_state

        elif state == self.white_space_state:
            pass

        elif state == self.EOF_state:
            pass

        return False

    def move(self, c):
        self.current_state = self.predict(c)

    def reset(self):
        self.current_state = self.start_state


class Scanner:
    def __init__(self):
        self.dfa = ScannerDFA()

    @staticmethod
    def read_file(file_name):
        with open(file_name) as f:
            code = "".join(f.readlines())
        return code

    def scan_file(self, file_name):
        code = Scanner.read_file(file_name)
        buffer = ""
        line_number = 1

        def get_code_char_by_char():
            for c in code:
                yield c
            yield None
            yield None

        for c in get_code_char_by_char():
            current_state = self.dfa.current_state
            if current_state.final:
                if self.dfa.predict(c):
                    buffer += c
                    self.dfa.move(c)
                else:
                    if self.dfa.predict(state=self.dfa.start_state, c=c):
                        self.dfa.reset()
                        yield Token(ttype=current_state.type, value=buffer), line_number
                        buffer = c
                        self.dfa.move(c)
                    else:
                        if self.dfa.current_state.finished:
                            self.dfa.reset()
                            yield Token(ttype=current_state.type, value=buffer), line_number
                            yield Token(ttype=Token.ERROR, value=c), line_number
                            buffer = ""
                        else:
                            self.dfa.reset()
                            buffer += c
                            yield Token(ttype=Token.ERROR, value=buffer), line_number
                            buffer = ""
            else:
                if self.dfa.predict(c):
                    buffer += c
                    self.dfa.move(c)
                else:
                    buffer += c
                    self.dfa.reset()
                    yield Token(ttype=Token.ERROR, value=buffer), line_number
                    buffer = ""
            if c == "\n":
                line_number += 1

    def scan_file_ignore_extra(self, file_name):
        for token, line_number in self.scan_file(file_name):
            if token.type == Token.WHITE_SPACE or token.type == Token.COMMENT or token.type == Token.ERROR:
                continue
            print("new Token: ", token.translate_for_parser())
            yield token, line_number


if __name__ == "__main__":
    scanner = Scanner()

    scanner_last_number = -1
    lexical_error_last_number = -1

    scanner_output = open("scanner.txt", "w")
    lexical_errors = open("lexical_errors.txt", "w")

    for token, last_line_number in scanner.scan_file("simple.nc"):
        if token.type == Token.WHITE_SPACE or token.type == Token.COMMENT:
            continue

        if token.type == Token.ERROR:
            if last_line_number != lexical_error_last_number:
                if lexical_error_last_number != -1:
                    lexical_errors.write("\n")
                lexical_error_last_number = last_line_number
                lexical_errors.write(str(last_line_number) + ". ")
            lexical_errors.write(token.to_str())
        else:
            if last_line_number != scanner_last_number:
                if scanner_last_number != -1:
                    scanner_output.write("\n")
                scanner_last_number = last_line_number
                scanner_output.write(str(last_line_number) + ". ")
            scanner_output.write(token.to_str())

    scanner_output.close()
    lexical_errors.close()
