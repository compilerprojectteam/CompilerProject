from Code.Scanner import *
from anytree import Node, RenderTree

parser_errors = None
scanner_output = None


class TransitionDFA:
    def __init__(self, transitions):
        self.transitions = transitions


def error(message):
    parser_errors.write(message + "\n")


class Parser:
    '''
    Args:
        file_name (str)
    '''

    def __init__(self, file_name):
        self.scanner = Scanner()
        self.first = {}
        self.follow = {}
        self.init_dfas()
        self.current_token = None
        self.scanner_tokens = self.scanner.scan_file_ignore_extra(file_name)

    @staticmethod
    def load_dict(name):
        dictionary = {}

        with open(name + ".csv", encoding='utf-8') as f:
            for a in f.readlines():
                key = a[:a.find("\t")]
                value = a[a.find("\t") + 1:]

                value = value.replace(",,", " virgol ")
                value = value.replace(", ,", " virgol ")
                value = value.replace(",", " ")
                value = value.replace("virgol", ",")

                values = value.split()
                values = [a.replace("ε", "")
                              .replace("id", "ID")
                              .replace("voID", "void")
                              .replace("num", "NUM")
                              .replace("eof", "EOF") for a in values]

                dictionary[key] = values

            return dictionary

    def init_dfas(self):

        self.first = Parser.load_dict("first")

        self.follow = Parser.load_dict("follow")

        self.dfas = {
            "Program": TransitionDFA({
                1: {("Declaration-list", False): 2},
                2: {("EOF", True): -1}
            }),

            "Declaration-list": TransitionDFA({
                1: {("Declaration", False): 2,
                    ("Epsilon", True): -1},
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
                    ("void", True): 5},
                2: {("ID", True): 3},
                3: {("Param-prime", False): 4},
                4: {("Param-list", False): -1},
                5: {("Param-list-void-abtar", False): -1}
            }),

            "Param-list-void-abtar": TransitionDFA({
                1: {("ID", True): 2,
                    ("Epsilon", True): -1},
                2: {("Param-prime", False): 3},
                3: {("Param-list", False): -1},
            }),

            "Param-list": TransitionDFA({
                1: {(",", True): 2,
                    ("Epsilon", True): -1},
                2: {("Param", False): 3},
                3: {("Param-list", False): -1},
            }),

            "Param": TransitionDFA({
                1: {("Declaration-initial", False): 2},
                2: {("Param-prime", False): -1}
            }),

            "Param-prime": TransitionDFA({
                1: {("[", True): 2,
                    ("Epsilon", True): -1},
                2: {("]", True): -1}
            }),

            "Compound-stmt": TransitionDFA({
                1: {("{", True): 2},
                2: {("Declaration-list", False): 3},
                3: {("Statement-list", False): 4},
                4: {("}", True): -1}
            }),

            "Statement-list": TransitionDFA({
                1: {("Statement", False): 2,
                    ("Epsilon", True): -1},
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
                1: {("Case-stmt", False): 2,
                    ("Epsilon", True): -1},
                2: {("Case-stmts", False): -1}
            }),

            "Case-stmt": TransitionDFA({
                1: {("case", True): 2},
                2: {("NUM", True): 3},
                3: {(":", True): 4},
                4: {("Statement-list", False): -1},
            }),

            "Default-stmt": TransitionDFA({
                1: {("default", True): 2,
                    ("Epsilon", True): -1},
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
                    ("[", True): 3,
                    ("Simple-expression-prime", False): -1},
                2: {("Expression", False): -1},
                3: {("Expression", False): 4},
                4: {("]", True): 5},
                5: {("H", False): -1}
            }),

            "H": TransitionDFA({
                1: {("=", True): 2,
                    ("G", False): 3},
                2: {("Expression", False): -1},
                3: {("D", False): 4},
                4: {("C", False): -1},
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
                1: {("Relop", False): 2,
                    ("Epsilon", True): -1},
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
                1: {("Addop", False): 2,
                    ("Epsilon", True): -1},
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
                1: {("*", True): 2,
                    ("Epsilon", True): -1},
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
                1: {("[", True): 2,
                    ("Epsilon", True): -1},
                2: {("Expression", False): 3},
                3: {("]", True): -1},
            }),

            "Factor-prime": TransitionDFA({
                1: {("Epsilon", True): -1,
                    ("(", True): 2},
                2: {("Args", False): 3},
                3: {(")", True): -1},
            }),

            "Factor-zegond": TransitionDFA({
                1: {("(", True): 2,
                    ("NUM", True): -1},
                2: {("Expression", False): 3},
                3: {(")", True): -1},
            }),

            "Args": TransitionDFA({
                1: {("Arg-list", False): -1,
                    ("Epsilon", True): -1},
            }),

            "Arg-list": TransitionDFA({
                1: {("Expression", False): 2},
                2: {("Arg-list-prime", False): -1}
            }),

            "Arg-list-prime": TransitionDFA({
                1: {(",", True): 2,
                    ("Epsilon", True): -1},
                2: {("Expression", False): 3},
                3: {("Arg-list-prime", False): -1},
            }),
        }

    def is_nullable(self, V):
        return "" in self.first[V]

    def get_next_token(self):

        while True:
            self.current_token, self.current_line_number = next(self.scanner_tokens)
            if self.current_token.type != Token.ERROR:
                return
            else:
                error("Lexical Error in line #{} : invalid token {}".format(self.current_line_number, self.current_token.value))

    def parse_from_non_terminal(self, V):
        print("parsing from non terminal : ", V)
        me = Node(V, parent=None)

        current_dfa = self.dfas[V]
        current_state = 1
        transitions = current_dfa.transitions

        while current_state > 0:
            for var, is_terminal in transitions[current_state].keys():
                c = self.current_token.translate_for_parser()
                value = self.current_token.to_str()

                if var == "Epsilon":
                    if c in self.follow[V]:
                        current_state = -1
                        Node("epsilon", me)
                        break

                if is_terminal:
                    if c == var:
                        if c == Token.EOF:
                            current_state = transitions[current_state][(var, True)]
                            Node(c, parent=me)
                            break
                        else:
                            self.get_next_token()
                            current_state = transitions[current_state][(var, True)]
                            Node(value, parent=me)
                            break
                    else:
                        if current_state != 1:
                            if var == Token.EOF:
                                error("#{} : Syntax Error! Malformed Input".format(self.current_line_number))
                                return False, me
                            else:
                                error("#{} : Syntax Error! Missing {}".format(self.current_line_number, var))
                                current_state = transitions[current_state][(var, True)]
                                break
                else:

                    if c in self.first[var]:
                        result, node = self.parse_from_non_terminal(var)
                        node.parent = me
                        if not result:
                            return False, me
                        current_state = transitions[current_state][(var, False)]
                        break
                    else:
                        if self.is_nullable(var):
                            if c in self.follow[var]:
                                result, node = self.parse_from_non_terminal(var)
                                node.parent = me
                                if not result:
                                    return False, me
                                current_state = transitions[current_state][(var, False)]
                                break

                    if current_state != 1:
                        if c in self.follow[var] and not self.is_nullable(var):
                            current_state = transitions[current_state][(var, False)]
                            error("#{} : Syntax Error! Missing {}".format(self.current_line_number, var))
                        if c not in self.follow[var] and c not in self.first[var]:
                            if c == Token.EOF:
                                error("#{} : Syntax Error! Unexpected EndOfFile".format(self.current_line_number))
                                return False, me
                            else:
                                error("#{} : Syntax Error! Unexpected {}".format(self.current_line_number, c))
                                self.get_next_token()
        return True, me

    def parse(self):
        self.get_next_token()
        status, tree_root = self.parse_from_non_terminal("Program")
        for pre, fill, node in RenderTree(tree_root):
            parser_output.write("%s%s" % (pre, node.name))
            parser_output.write("\n")


if __name__ == "__main__":
    parser_errors = open("parser-error.txt", "w", encoding="utf-8")
    parser_output = open("parser-output.txt", "w", encoding="utf-8")
    p = Parser("doc_code.nc")

    dickt = Parser.load_dict("first")
    print(",\n".join(map(str, (['"' + str(x) + "\" : " + str(y) for x, y in zip(dickt.keys(), dickt.values())]))))

    p.parse()
    # scanner_output.close()
    # parser_output.close()
