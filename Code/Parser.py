from Code.Scanner import *


class TransitionDFA:
    def __init__(self, transitions):
        self.transitions = transitions


def error(message):
    print(message)


class Parser:
    '''
    Args:
        file_name (str)
    '''

    def __init__(self, file_name):
        self.scanner = Scanner()
        self.init_dfas()
        self.first = {"Program": [], "Declaration-List": []}
        self.follow = {"Program": [], "Declaration-List": []}
        self.current_token = None
        self.scanner_tokens = self.scanner.scan_file_ignore_extra(file_name)

    def init_dfas(self):
        self.dfas = {
            "Program": TransitionDFA({
                1: {("Declaration-List", False): 2},
                2: {("EOF", True): -1}
            }),

            "Declaration-list": TransitionDFA({
                1: {("Declaration", False): 2},
                2: {("Declaration-list", False): -1}
            }),

            "Declaration": TransitionDFA({
                1: {("Declaration-initial", False): 2},
                2: {("Declaration-prime", False): -1}
            }),

            "Declaration-initial": TransitionDFA({
                1: {("Type-specifier", False): 2},
                2: {("ID", True): -1}
            }),

            "Declaration-prime": TransitionDFA({
                1: {("Fun-declaration-prime", False): -1,
                    ("Var-declaration-prime", False): -1},
            }),

            "Var-declaration-prime": TransitionDFA({
                1: {(";", True): -1,
                    ("[", True): 2},
                2: {("NUM", True): 3},
                3: {("]", True): 4},
                4: {(";", True): -1},
            }),

            "Fun-declaration-prime": TransitionDFA({
                1: {("(", True): 2},
                2: {("Params", False): 3},
                3: {(")", True): 4},
                4: {("Compound-stmt", False): -1},
            }),

            "Type-specifier": TransitionDFA({
                1: {("int", True): -1,
                    ("void", True): -1},
            }),

            "Params": TransitionDFA({
                1: {("int", True): 2,
                    ("void", True): 4},
                2: {("ID", True): 3},
                3: {("Param-list", False): -1},
                4: {("Param-list-void-abtar", False): -1}
            }),

            "Param-list-void-abtar": TransitionDFA({
                1: {("ID", True): 2},
                2: {("Param-list", False): -1},
            }),

            "Param-list": TransitionDFA({
                1: {(",", True): 2},
                2: {("Param", False): 3},
                3: {("Param-list", False): -1},
            }),

            "Param": TransitionDFA({
                1: {("Declaration-initial", False): 2},
                2: {("Param-prime", False): -1}
            }),

            "Param-prime": TransitionDFA({
                1: {("[", True): 2},
                2: {("]", True): -1}
            }),

            "Compound-stmt": TransitionDFA({
                1: {("{", True): 2},
                2: {("Declaration-list", False): 3},
                3: {("Statement-list", False): 4},
                4: {("}", True): -1}
            }),

            "Statement-list": TransitionDFA({
                1: {("Statement", False): 2},
                2: {("Statement-list", False): -1}
            }),

            "Statement": TransitionDFA({
                1: {("Expression-stmt", False): -1,
                    ("Compound-stmt", False): -1,
                    ("Selection-stmt", False): -1,
                    ("Iteration-stmt", False): -1,
                    ("Return-stmt", False): -1,
                    ("Switch-stmt", False): -1}
            }),

            "Expression-stmt": TransitionDFA({
                1: {("Expression", False): 2,
                    ("continue", True): 3,
                    ("break", True): 4,
                    (";", True): -1},
                2: {(";", True): -1},
                3: {(";", True): -1},
                4: {(";", True): -1}
            }),

            "Selection-stmt": TransitionDFA({
                1: {("if", True): 2},
                2: {("(", True): 3},
                3: {("Expression", False): 4},
                4: {(")", True): 5},
                5: {("Statement", False): 6},
                6: {("else", True): 7},
                7: {("Statement", False): -1},
            }),

            "Iteration-stmt": TransitionDFA({
                1: {("while", True): 2},
                2: {("(", True): 3},
                3: {("Expression", False): 4},
                4: {(")", True): 5},
                5: {("Statement", False): -1},
            }),

            "Return-stmt": TransitionDFA({
                1: {("return", True): 2},
                2: {("Return-stmt-prime", False): -1}
            }),

            "Return-stmt-prime": TransitionDFA({
                1: {(";", True): -1,
                    ("Expression", False): 2},
                2: {(";", True): -1}
            }),

            "Switch-stmt": TransitionDFA({
                1: {("switch", True): 2},
                2: {("(", True): 3},
                3: {("Expression", False): 4},
                4: {(")", True): 5},
                5: {("{", True): 6},
                6: {("Case-stmts", False): 7},
                7: {("Default-stmt", False): 8},
                8: {("}", True): -1},

            }),

            "Case-stmts": TransitionDFA({
                1: {("Case-stmt", False): 2},
                2: {("Case-stmts", False): -1}
            }),

            "Case-stmt": TransitionDFA({
                1: {("case", True): 2},
                2: {("NUM", True): 3},
                3: {(":", True): 4},
                4: {("Statement-list", False): -1},
            }),

            "Default-stmt": TransitionDFA({
                1: {("default", True): 2},
                2: {(":", True): 3},
                3: {("Statement-list", False): -1},
            }),

            "Expression": TransitionDFA({
                1: {("ID", True): 2,
                    ("Simple-expression-zegond", False): -1},
                2: {("B", False): -1}
            }),

            "B": TransitionDFA({
                1: {("=", True): 2,
                    ("Simple-expression-prime", False): -1},
                2: {("Expression", False): -1}
            }),

            "Simple-expression-zegond": TransitionDFA({
                1: {("Additive-expression-zegond", False): 2},
                2: {("C", False): -1}
            }),

            "Simple-expression-prime": TransitionDFA({
                1: {("Additive-expression-prime", False): 2},
                2: {("C", False): -1}
            }),

            "C": TransitionDFA({
                1: {("Relop", False): 2},
                2: {("Additive-expression", False): -1}
            }),

            "Relop": TransitionDFA({
                1: {("==", True): -1,
                    ("<", True): -1},
            }),

            "Addop": TransitionDFA({
                1: {("+", True): -1,
                    ("-", True): -1},
            }),

            "Additive-expression": TransitionDFA({
                1: {("Term", False): 2},
                2: {("D", False): -1}
            }),

            "Additive-expression-prime": TransitionDFA({
                1: {("Term-prime", False): 2},
                2: {("D", False): -1}
            }),

            "Additive-expression-zegond": TransitionDFA({
                1: {("Term-zegond", False): 2},
                2: {("D", False): -1}
            }),

            "D": TransitionDFA({
                1: {("Addop", False): 2},
                2: {("Term", False): 3},
                3: {("D", False): -1}
            }),

            "Term": TransitionDFA({
                1: {("Signed-factor", False): 2},
                2: {("G", False): -1}
            }),

            "Term-prime": TransitionDFA({
                1: {("Signed-factor-prime", False): 2},
                2: {("G", False): -1}
            }),

            "Term-zegond": TransitionDFA({
                1: {("Signed-factor-zegond", False): 2},
                2: {("G", False): -1}
            }),

            "G": TransitionDFA({
                1: {("*", True): 2},
                2: {("Signed-factor", False): 3},
                3: {("G", False): -1}
            }),

            "Signed-factor": TransitionDFA({
                1: {("+", True): 2,
                    ("-", True): 3,
                    ("Factor", False): -1},
                2: {("Factor", False): -1},
                3: {("Factor", False): -1}
            }),

            "Signed-factor-prime": TransitionDFA({
                1: {("Factor-prime", False): -1}
            }),

            "Signed-factor-zegond": TransitionDFA({
                1: {("+", True): 2,
                    ("-", True): 3,
                    ("Factor-zegond", False): -1},
                2: {("Factor", False): -1},
                3: {("Factor", False): -1}
            }),

            "Factor": TransitionDFA({
                1: {("(", True): 2,
                    ("NUM", True): -1,
                    ("ID", True): 3},
                2: {("Expression", False): 4},
                3: {("Var-call-prime", False): -1},
                4: {(")", True): -1},
            }),

            "Var-call-prime": TransitionDFA({
                1: {("Var-prime", False): -1,
                    ("(", True): 2},
                2: {("Args", False): 3},
                3: {(")", True): -1},
            }),

            "Var-prime": TransitionDFA({
                1: {("[", True): 2},
                2: {("Expression", False): 3},
                3: {("]", True): -1},
            }),

            "Factor-prime": TransitionDFA({
                1: {("Var-call-prime", False): -1},
            }),

            "Factor-zegond": TransitionDFA({
                1: {("(", True): 2,
                    ("NUM", True): -1},
                2: {("Expression", False): 3},
                3: {(")", True): -1},
            }),

            "Args": TransitionDFA({
                1: {("Arg-list", False): -1},
            }),

            "Arg-list": TransitionDFA({
                1: {("Expression", False): 2},
                2: {("Arg-list-prime", False): -1}
            }),

            "Arg-list-prime": TransitionDFA({
                1: {(",", True): 2},
                2: {("Expression", False): 3},
                3: {("Arg-list-prime", False): -1},
            }),

        }

    def is_nullable(self, V):
        return "" in self.first[V]

    def parse_from_non_terminal(self, V):
        current_dfa = self.dfas[V]
        current_state = 1
        transitions = current_dfa.transitions

        while current_state > 0:
            for var, is_terminal in transitions[current_state].keys():
                c = self.current_token.translate_for_parser()
                if is_terminal:
                    if c == var:
                        self.current_token, self.current_line_number = next(self.scanner_tokens)
                        current_state = transitions[(var, True)]
                        break
                    else:
                        if current_state != 1:
                            error("#{} : Syntax Error! Missing {}".format(self.current_line_number, var))
                            current_state = transitions[(var, True)]
                            break
                else:

                    if c in self.first[var]:
                        self.parse_from_non_terminal(var)
                        current_state = transitions[(var, False)]
                        break
                    else:
                        if self.is_nullable(var):
                            if c in self.follow[var]:
                                current_state = transitions[(var, False)]
                                break

                    if current_state != 1:
                        if c in self.follow[var] and not self.is_nullable(var):
                            current_state = transitions[(var, False)]
                            error("#{} : Syntax Error! Missing {}".format(self.current_line_number, var))
                        if c not in self.follow[var] and c not in self.first[var]:
                            error("#{} : Syntax Error! Unexpected {}".format(self.current_line_number, c))
                            self.current_token, self.current_line_number = next(self.scanner_tokens)

    def parse(self):
        self.current_token, self.current_line_number = next(self.scanner_tokens)
        self.parse_from_non_terminal("Program")


if __name__ == "__main__":
    pass
