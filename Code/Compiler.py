from Code.Utils import *
from Code.Scanner import *
from anytree import Node, RenderTree

parser_errors = None
scanner_output = None


class TransitionDFA:
    def __init__(self, transitions):
        self.transitions = transitions


class SemanticActions:
    """
    Args:
         symbol_table (SymbolTable)
    """

    def __init__(self, symbol_table):
        self.st = symbol_table
        self.i = 0
        self.type = None
        self.stack = []
        self.stack_flags = []
        self.code_block = []

    def push(self, t, flag=""):
        self.stack.append(t)
        self.stack_flags.append(flag)

    def poop(self):
        s = self.stack.pop()
        f = self.stack_flags.pop()
        return s, f

    def add_code(self, code):
        self.i += 1
        self.code_block.append(code)

    def assign(self, ct):
        rhs, rhs_type = self.poop()
        lhs, lhs_type = self.poop()

        rhs_indirect = rhs_type == "indirect" or rhs_type == "direct array"
        lhs_indirect = lhs_type == "indirect" or lhs_type == "direct array"

        self.add_code("(ASSIhhhhhGN, {}{}, {}{})".format("@" if rhs_indirect else "",
                                                         rhs,
                                                         "@" if lhs_indirect else "",
                                                         lhs))
        self.push(lhs, lhs_type)

    def save_to_temp(self, ct):
        t = self.st.get_temp()
        self.add_code("(ASSIGN, #{}, {})".format(int(ct.value), t))
        self.push(t, "")

    def add_to_var(self, ct):
        exp, exp_type = self.poop()
        addr, addr_type = self.poop()
        self.add_code("(MULT, {}, #4, {})".format(exp, exp))
        t = self.st.get_temp()
        self.add_code("(ADD, {}, {}, {})".format(addr, exp, addr))
        self.push(addr, "indirect")

    def start(self, ct):
        self.st.start_new_scope("normal")

    def pid(self, ct):
        id_name = ct.value
        symbol = self.st.resolve_symbol(id_name)
        if not symbol:
            print_semantic_error("ID {} is not defined".format(id_name))
            return

        self.code_block.append(id_name)
        if symbol.is_function:
            self.push(symbol.address, "function")
        elif symbol.location == "heap":
            if symbol.is_array:
                t = self.st.get_temp()
                self.add_code("(ASSIGN, #{}, {})".format(symbol.address, t))
                self.push(t, "direct array")
            else:
                self.push(symbol.address, "direct int")
        else:
            if symbol.is_reference and symbol.is_array:
                pointer = SymbolTable.STACK_BASE
                t = self.st.get_temp()
                self.add_code("(ASSIGN, {}, {})".format(pointer, t))
                for i in range(len(self.st.symbol_table))[::-1]:
                    if id_name in self.st.symbol_table[i]:
                        tf = self.st.get_temp()
                        self.add_code("(ADD, {}, #{}, {})".format(t, symbol.address, tf))
                        self.add_code("(ASSIGN, @{}, {})".format(tf, tf))
                        self.push(tf, "indirect")
                        break
                    if self.st.scope_type == "function":
                        function_symbol = self.st.last_symbol[i - 1]
                        q_displacement = ((function_symbol.n_args + SymbolTable.N_STACK_VARS) * 4
                                          - SymbolTable.STACK_BLOCK_SIZE)
                        t2 = self.st.get_temp()
                        self.add_code("(ADD, {}, #{}, {})".format(t, q_displacement, t2))
                        self.add_code("(ASSIGN, @{}, {})".format(t2, t2))
                        t = t2
                        pass

                pass
            else:
                pointer = SymbolTable.STACK_BASE
                t = self.st.get_temp()
                self.add_code("(ASSIGN, {}, {})".format(pointer, t))
                for i in range(len(self.st.symbol_table))[::-1]:
                    if id_name in self.st.symbol_table[i]:
                        tf = self.st.get_temp()
                        self.add_code("(ADD, {}, #{}, {})".format(t, symbol.address, tf))
                        self.push(tf, "indirect")
                        break
                    if self.st.scope_type == "function":
                        function_symbol = self.st.last_symbol[i - 1]
                        q_displacement = ((function_symbol.n_args + SymbolTable.N_STACK_VARS) * 4
                                          - SymbolTable.STACK_BLOCK_SIZE)
                        t2 = self.st.get_temp()
                        self.add_code("(ADD, {}, #{}, {})".format(t, q_displacement, t2))
                        self.add_code("(ASSIGN, @{}, {})".format(t2, t2))
                        t = t2
                        pass

                pass

    def set_var_type_reference(self, ct):
        self.st.last_symbol[-1].is_reference = True
        self.st.last_symbol[-1].is_array = True

    def inc_n_args(self, ct):
        self.st.last_symbol[-2].args.append("array" if self.st.last_symbol[-1].is_reference else "int")
        self.st.last_symbol[-2].n_args += 1

    def save_stack(self, ct):
        i = self.st.get_last_function_scope()
        self.st.stack_pointer[i] += 4

    def void_type_error(self, ct):
        print_semantic_error("error")

    def start_normal_scope(self, ct):
        self.st.start_new_scope("normal")

    def start_function_scope(self, ct):
        self.st.start_new_scope("function")

    def close_scope(self, ct):
        self.st.remove_last_scope()

    def save_type(self, ct):
        self.type = ct.value

    def create_symbol(self, ct):
        self.st.add_symbol(ct.value, ttype=self.type)

    def set_fun_address(self, ct):
        last_symbol = self.st.get_last_symbol()
        last_symbol.address = self.i

    def set_var_address(self, ct):
        last_symbol = self.st.get_last_symbol()

        if self.st.get_current_memory_type() == "stack":
            i = self.st.get_last_function_scope()
            last_symbol.location = "stack"
            last_symbol.address = self.st.stack_pointer[i]

        else:
            last_symbol.address = self.st.heap_pointer

    def inc_var_pointer_default(self, ct):
        if self.st.get_current_memory_type() == "stack":
            i = self.st.get_last_function_scope()
            self.st.stack_pointer[i] += 4
        else:
            self.st.heap_pointer += 4

    def inc_var_pointer_array(self, ct):
        self.st.last_symbol[-1].is_array = True
        if self.st.get_current_memory_type() == "stack":
            i = self.st.get_last_function_scope()
            self.st.stack_pointer[i] += 4 * int(ct.value)
        else:
            self.st.heap_pointer += 4 * int(ct.value)


class Symbol:
    def __init__(self, ttype="int", address=-1):
        self.address = address
        self.location = "heap"
        self.type = ttype
        self.is_function = False
        self.is_reference = False
        self.is_array = False
        self.length = 4

        self.block_size = 0
        self.n_args = 0
        self.args = []


class SymbolTable:
    N_STACK_VARS = 1
    STACK_BASE = 1500
    STACK_BLOCK_SIZE = 100

    def __init__(self):
        self.symbol_table = []

        self.last_symbol = []
        self.scope_type = []
        self.stack_pointer = []

        self.heap_pointer = 1000
        self.temp_pointer = 496

    def get_temp(self):
        self.temp_pointer += 4
        return self.temp_pointer

    def start_new_scope(self, stype):
        self.last_symbol.append(None)
        self.symbol_table.append({})
        self.scope_type.append(stype)
        self.stack_pointer.append(-SymbolTable.STACK_BLOCK_SIZE)

        if stype == "function":
            self.last_symbol[-2].is_function = True

    def remove_last_scope(self):
        print_symbol_table(self)
        print("_" * 100)
        self.symbol_table.pop()
        self.last_symbol.pop()
        self.stack_pointer.pop()
        self.scope_type.pop()

    def get_last_function_scope(self):
        i = len(self.scope_type) - 1
        while True:
            if self.scope_type[i] == "function":
                return i
            i -= 1

    def resolve_symbol(self, name):
        for scope_symbol_table in self.symbol_table[::-1]:
            if name in scope_symbol_table:
                return scope_symbol_table[name]
        return False

    def add_symbol(self, name, ttype):
        symbol = Symbol(ttype=ttype)
        self.last_symbol[-1] = symbol
        self.symbol_table[-1][name] = symbol

    def get_last_symbol(self):
        """
        :returns last_symbol[-1]
        :rtype Symbol
        """
        return self.last_symbol[-1]

    def get_current_memory_type(self):
        return "stack" if len(self.symbol_table) > 1 else "heap"


def error(message):
    parser_errors.write(message + "\n")


class Parser:
    '''
    Args:
        file_name (str)
    '''

    def __init__(self, file_name):
        self.scanner = Scanner()
        self.st = SymbolTable()
        self.sa = SemanticActions(self.st)
        self.scanner_tokens = self.scanner.scan_file_ignore_extra(file_name)

        self.current_token = None

        self.first = {}
        self.follow = {}
        self.init_dfas()

    @staticmethod
    def load_dict(name):
        dictionary = {}

        with open("../resources/" + name + ".csv", encoding='utf-8') as f:
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
                1: {("Declaration-list", False): (2, [self.sa.start], [])},
                2: {("EOF", True): (-1, [self.sa.close_scope], [])}
            }),

            "Declaration-list": TransitionDFA({
                1: {("Declaration", False): (2, [], []),
                    ("Epsilon", True): (-1, [], [])},
                2: {("Declaration-list", False): (-1, [], [])}
            }),

            "Declaration": TransitionDFA({
                1: {("Declaration-initial", False): (2, [], [])},
                2: {("Declaration-prime", False): (-1, [], [])}
            }),

            "Declaration-initial": TransitionDFA({
                1: {("Type-specifier", False): (2, [self.sa.save_type], [])},
                2: {("ID", True): (-1, [self.sa.create_symbol], [])}
            }),

            "Declaration-prime": TransitionDFA({
                1: {("Fun-declaration-prime", False): (-1, [self.sa.set_fun_address], []),
                    ("Var-declaration-prime", False): (-1, [self.sa.set_var_address], [])},
            }),

            "Var-declaration-prime": TransitionDFA({
                1: {(";", True): (-1, [self.sa.inc_var_pointer_default], []),
                    ("[", True): (2, [], [])},
                2: {("NUM", True): (3, [self.sa.inc_var_pointer_array], [])},
                3: {("]", True): (4, [], [])},
                4: {(";", True): (-1, [], [])},
            }),

            "Fun-declaration-prime": TransitionDFA({
                1: {("(", True): (2, [self.sa.start_function_scope], [])},
                2: {("Params", False): (3, [], [])},
                3: {(")", True): (4, [], [])},
                4: {("Compound-stmt", False): (-1, [self.sa.save_stack, self.sa.save_stack], [])},
            }),

            "Type-specifier": TransitionDFA({
                1: {("int", True): (-1, [], []),
                    ("void", True): (-1, [], [])},
            }),

            "Params": TransitionDFA({
                1: {("int", True): (2, [self.sa.save_type], []),
                    ("void", True): (5, [], [])},
                2: {("ID", True): (3, [self.sa.create_symbol], [])},
                3: {("Param-prime", False): (4, [self.sa.set_var_address, self.sa.inc_var_pointer_default], [])},
                4: {("Param-list", False): (-1, [], [])},
                5: {("Param-list-void-abtar", False): (-1, [], [])}
            }),

            "Param-list-void-abtar": TransitionDFA({
                1: {("ID", True): (2, [self.sa.void_type_error], []),
                    ("Epsilon", True): (-1, [], [])},
                2: {("Param-prime", False): (3, [], [])},
                3: {("Param-list", False): (-1, [], [])},
            }),

            "Param-list": TransitionDFA({
                1: {(",", True): (2, [self.sa.inc_n_args], []),
                    ("Epsilon", True): (-1, [self.sa.inc_n_args], [])},
                2: {("Param", False): (3, [], [])},
                3: {("Param-list", False): (-1, [], [])},
            }),

            "Param": TransitionDFA({
                1: {("Declaration-initial", False): (2, [], [])},
                2: {("Param-prime", False): (-1, [self.sa.set_var_address, self.sa.inc_var_pointer_default], [])}
            }),

            "Param-prime": TransitionDFA({
                1: {("[", True): (2, [self.sa.set_var_type_reference], []),
                    ("Epsilon", True): (-1, [], [])},
                2: {("]", True): (-1, [], [])}
            }),

            "Compound-stmt": TransitionDFA({
                1: {("{", True): (2, [], [])},
                2: {("Declaration-list", False): (3, [], [])},
                3: {("Statement-list", False): (4, [], [])},
                4: {("}", True): (-1, [], [self.sa.close_scope])}
            }),

            "Statement-list": TransitionDFA({
                1: {("Statement", False): (2, [], []),
                    ("Epsilon", True): (-1, [], [])},
                2: {("Statement-list", False): (-1, [], [])}
            }),

            "Statement": TransitionDFA({
                1: {("Expression-stmt", False): (-1, [], []),
                    ("Compound-stmt", False): (-1, [self.sa.start_normal_scope], []),
                    ("Selection-stmt", False): (-1, [], []),
                    ("Iteration-stmt", False): (-1, [], []),
                    ("Return-stmt", False): (-1, [], []),
                    ("Switch-stmt", False): (-1, [], [])}
            }),

            "Expression-stmt": TransitionDFA({
                1: {("Expression", False): (2, [], []),
                    ("continue", True): (3, [], []),
                    ("break", True): (4, [], []),
                    (";", True): (-1, [], [])},
                2: {(";", True): (-1, [], [])},
                3: {(";", True): (-1, [], [])},
                4: {(";", True): (-1, [], [])}
            }),

            "Selection-stmt": TransitionDFA({
                1: {("if", True): (2, [], [])},
                2: {("(", True): (3, [], [])},
                3: {("Expression", False): (4, [], [])},
                4: {(")", True): (5, [], [])},
                5: {("Statement", False): (6, [], [])},
                6: {("else", True): (7, [], [])},
                7: {("Statement", False): (-1, [], [])},
            }),

            "Iteration-stmt": TransitionDFA({
                1: {("while", True): (2, [], [])},
                2: {("(", True): (3, [], [])},
                3: {("Expression", False): (4, [], [])},
                4: {(")", True): (5, [], [])},
                5: {("Statement", False): (-1, [], [])},
            }),

            "Return-stmt": TransitionDFA({
                1: {("return", True): (2, [], [])},
                2: {("Return-stmt-prime", False): (-1, [], [])}
            }),

            "Return-stmt-prime": TransitionDFA({
                1: {(";", True): (-1, [], []),
                    ("Expression", False): (2, [], [])},
                2: {(";", True): (-1, [], [])}
            }),

            "Switch-stmt": TransitionDFA({
                1: {("switch", True): (2, [], [])},
                2: {("(", True): (3, [], [])},
                3: {("Expression", False): (4, [], [])},
                4: {(")", True): (5, [], [])},
                5: {("{", True): (6, [], [])},
                6: {("Case-stmts", False): (7, [], [])},
                7: {("Default-stmt", False): (8, [], [])},
                8: {("}", True): (-1, [], [])},

            }),

            "Case-stmts": TransitionDFA({
                1: {("Case-stmt", False): (2, [], []),
                    ("Epsilon", True): (-1, [], [])},
                2: {("Case-stmts", False): (-1, [], [])}
            }),

            "Case-stmt": TransitionDFA({
                1: {("case", True): (2, [], [])},
                2: {("NUM", True): (3, [], [])},
                3: {(":", True): (4, [], [])},
                4: {("Statement-list", False): (-1, [], [])},
            }),

            "Default-stmt": TransitionDFA({
                1: {("default", True): (2, [], []),
                    ("Epsilon", True): (-1, [], [])},
                2: {(":", True): (3, [], [])},
                3: {("Statement-list", False): (-1, [], [])},
            }),

            "Expression": TransitionDFA({
                1: {("ID", True): (2, [self.sa.pid], []),
                    ("Simple-expression-zegond", False): (-1, [], [])},
                2: {("B", False): (-1, [], [])}
            }),

            "B": TransitionDFA({
                1: {("=", True): (2, [], []),
                    ("[", True): (3, [], []),
                    ("Simple-expression-prime", False): (-1, [], [])},
                2: {("Expression", False): (-1, [], [self.sa.assign])},
                3: {("Expression", False): (4, [], [])},
                4: {("]", True): (5, [self.sa.add_to_var], [])},
                5: {("H", False): (-1, [], [])}
            }),

            "H": TransitionDFA({
                1: {("=", True): (2, [], []),
                    ("G", False): (3, [], [])},
                2: {("Expression", False): (-1, [], [self.sa.assign])},
                3: {("D", False): (4, [], [])},
                4: {("C", False): (-1, [], [])},
            }),

            "Simple-expression-zegond": TransitionDFA({
                1: {("Additive-expression-zegond", False): (2, [], [])},
                2: {("C", False): (-1, [], [])}
            }),

            "Simple-expression-prime": TransitionDFA({
                1: {("Additive-expression-prime", False): (2, [], [])},
                2: {("C", False): (-1, [], [])}
            }),

            "C": TransitionDFA({
                1: {("Relop", False): (2, [], []),
                    ("Epsilon", True): (-1, [], [])},
                2: {("Additive-expression", False): (-1, [], [])}
            }),

            "Relop": TransitionDFA({
                1: {("==", True): (-1, [], []),
                    ("<", True): (-1, [], [])},
            }),

            "Addop": TransitionDFA({
                1: {("+", True): (-1, [], []),
                    ("-", True): (-1, [], [])},
            }),

            "Additive-expression": TransitionDFA({
                1: {("Term", False): (2, [], [])},
                2: {("D", False): (-1, [], [])}
            }),

            "Additive-expression-prime": TransitionDFA({
                1: {("Term-prime", False): (2, [], [])},
                2: {("D", False): (-1, [], [])}
            }),

            "Additive-expression-zegond": TransitionDFA({
                1: {("Term-zegond", False): (2, [], [])},
                2: {("D", False): (-1, [], [])}
            }),

            "D": TransitionDFA({
                1: {("Addop", False): (2, [], []),
                    ("Epsilon", True): (-1, [], [])},
                2: {("Term", False): (3, [], [])},
                3: {("D", False): (-1, [], [])}
            }),

            "Term": TransitionDFA({
                1: {("Signed-factor", False): (2, [], [])},
                2: {("G", False): (-1, [], [])}
            }),

            "Term-prime": TransitionDFA({
                1: {("Signed-factor-prime", False): (2, [], [])},
                2: {("G", False): (-1, [], [])}
            }),

            "Term-zegond": TransitionDFA({
                1: {("Signed-factor-zegond", False): (2, [], [])},
                2: {("G", False): (-1, [], [])}
            }),

            "G": TransitionDFA({
                1: {("*", True): (2, [], []),
                    ("Epsilon", True): (-1, [], [])},
                2: {("Signed-factor", False): (3, [], [])},
                3: {("G", False): (-1, [], [])}
            }),

            "Signed-factor": TransitionDFA({
                1: {("+", True): (2, [], []),
                    ("-", True): (3, [], []),
                    ("Factor", False): (-1, [], [])},
                2: {("Factor", False): (-1, [], [])},
                3: {("Factor", False): (-1, [], [])}
            }),

            "Signed-factor-prime": TransitionDFA({
                1: {("Factor-prime", False): (-1, [], [])}
            }),

            "Signed-factor-zegond": TransitionDFA({
                1: {("+", True): (2, [], []),
                    ("-", True): (3, [], []),
                    ("Factor-zegond", False): (-1, [], [])},
                2: {("Factor", False): (-1, [], [])},
                3: {("Factor", False): (-1, [], [])}
            }),

            "Factor": TransitionDFA({
                1: {("(", True): (2, [], []),
                    ("NUM", True): (-1, [], []),
                    ("ID", True): (3, [self.sa.pid], [])},
                2: {("Expression", False): (4, [], [])},
                3: {("Var-call-prime", False): (-1, [], [])},
                4: {(")", True): (-1, [], [])},
            }),

            "Var-call-prime": TransitionDFA({
                1: {("Var-prime", False): (-1, [], []),
                    ("(", True): (2, [], [])},
                2: {("Args", False): (3, [], [])},
                3: {(")", True): (-1, [], [])},
            }),

            "Var-prime": TransitionDFA({
                1: {("[", True): (2, [], []),
                    ("Epsilon", True): (-1, [], [])},
                2: {("Expression", False): (3, [], [])},
                3: {("]", True): (-1, [self.sa.add_to_var], [])},
            }),

            "Factor-prime": TransitionDFA({
                1: {("Epsilon", True): (-1, [], []),
                    ("(", True): (2, [], [])},
                2: {("Args", False): (3, [], [])},
                3: {(")", True): (-1, [], [])},
            }),

            "Factor-zegond": TransitionDFA({
                1: {("(", True): (2, [], []),
                    ("NUM", True): (-1, [self.sa.save_to_temp], [])},
                2: {("Expression", False): (3, [], [])},
                3: {(")", True): (-1, [], [])},
            }),

            "Args": TransitionDFA({
                1: {("Arg-list", False): (-1, [], []),
                    ("Epsilon", True): (-1, [], [])},
            }),

            "Arg-list": TransitionDFA({
                1: {("Expression", False): (2, [], [])},
                2: {("Arg-list-prime", False): (-1, [], [])}
            }),

            "Arg-list-prime": TransitionDFA({
                1: {(",", True): (2, [], []),
                    ("Epsilon", True): (-1, [], [])},
                2: {("Expression", False): (3, [], [])},
                3: {("Arg-list-prime", False): (-1, [], [])},
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
                error("Lexical Error in line #{} : invalid token {}".format(self.current_line_number,
                                                                            self.current_token.value))

    def parse_from_non_terminal(self, V):
        # print("parsing from non terminal : ", V)
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
                        current_state, fs_before, fs_after = transitions[current_state][(var, True)]
                        [f(self.current_token) for f in fs_before]
                        [f(self.current_token) for f in fs_after]

                        current_state = -1
                        Node("epsilon", me)
                        break

                if is_terminal:
                    if c == var:
                        if c == Token.EOF:
                            current_state, fs_before, fs_after = transitions[current_state][(var, True)]
                            [f(self.current_token) for f in fs_before]
                            [f(self.current_token) for f in fs_after]
                            Node(c, parent=me)
                            break
                        else:
                            current_state, fs_before, fs_after = transitions[current_state][(var, True)]
                            [f(self.current_token) for f in fs_before]
                            self.get_next_token()
                            [f(self.current_token) for f in fs_after]

                            Node(value, parent=me)
                            break
                    else:
                        if current_state != 1:
                            if var == Token.EOF:
                                error("#{} : Syntax Error! Malformed Input".format(self.current_line_number))
                                return False, me
                            else:
                                error("#{} : Syntax Error! Missing {}".format(self.current_line_number, var))
                                current_state, _, _ = transitions[current_state][(var, True)]
                                break
                else:

                    if c in self.first[var]:
                        _, fs_before, fs_after = transitions[current_state][(var, False)]
                        [f(self.current_token) for f in fs_before]

                        result, node = self.parse_from_non_terminal(var)
                        [f(self.current_token) for f in fs_after]

                        node.parent = me
                        if not result:
                            return False, me
                        current_state, _, _ = transitions[current_state][(var, False)]
                        break
                    else:
                        if self.is_nullable(var):
                            if c in self.follow[var]:
                                _, fs_before, fs_after = transitions[current_state][(var, False)]
                                [f(self.current_token) for f in fs_before]

                                result, node = self.parse_from_non_terminal(var)
                                [f(self.current_token) for f in fs_after]

                                node.parent = me
                                if not result:
                                    return False, me
                                current_state, _, _ = transitions[current_state][(var, False)]
                                break

                    if current_state != 1:
                        if c in self.follow[var] and not self.is_nullable(var):
                            current_state, _, _ = transitions[current_state][(var, False)]
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
    parser_errors = open("../out/parser-error.txt", "w", encoding="utf-8")
    parser_output = open("../out/parser-output.txt", "w", encoding="utf-8")
    p = Parser("../input/test.nc")

    p.parse()
    print(p.st.symbol_table)
    print("\n".join(p.sa.code_block))
    # scanner_output.close()
    # parser_output.close()