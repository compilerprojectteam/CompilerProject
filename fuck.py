# dickt = {}
# with open(".csv", encoding='utf-8') as f:
#     for a in f.readlines():
#         key = a[:a.find("\t")]
#         value = a[a.find("\t") + 1:]
#         # value = value.replace(" ", "")
#         value = value.replace(",,", " virgol ")
#         value = value.replace(", ,", " virgol ")
#         value = value.replace(",", " ")
#         value = value.replace("virgol", ",")
#
#         values = value.split()
#         values = [a.replace("ε", "")
#                       .replace("id", "ID")
#                       .replace("voID", "void")
#                       .replace("num", "NUM")
#                       .replace("eof", "EOF") for a in values]
#
#         # print(values)
#         dickt[key] = values
#
# print(dickt)
#
# print(",\n".join(map(str, (['"' + str(x) + "\" : " + str(y) for x, y in zip(dickt.keys(), dickt.values())]))))

def f(x):
    print(x)


def g(x):
    print("sex", x)


a = [f, g, f, g, g, f]
[q(2) for q in a]
