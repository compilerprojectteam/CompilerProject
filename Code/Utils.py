def print_symbol(symbol):
    d = symbol.__dict__
    for field in sorted(d.keys()):
        if field == 'parent_func':
            if d[field]:
                print("\t {}: {}".format(field, d[field].name))
            else:
                print("\t {}: {}".format(field, d[field]))
        else:
            print("\t {}: {}".format(field, d[field]))


def print_symbol_table(symbol_table):
    d = symbol_table.symbol_table[-1]
    for symbol_name in d.keys():
        print(symbol_name)
        print_symbol(d[symbol_name])


def print_semantic_error(error):
    print(error)
    exit()

if __name__ == "__main__":
    for i in range(5)[::-1]:
        print(i)