import graphlib
from fractions import Fraction

dag = graphlib.TopologicalSorter()
values = {}

for line in open("input").read().strip().splitlines():
    a, bs = line.split(": ")
    bs = bs.split()
    if len(bs) == 1:
        values[a] = bs[0]
        dag.add(a)
    else:
        dag.add(a, bs[0], bs[2])
        values[a] = f"values['{bs[0]}'] {bs[1]} values['{bs[2]}']"

for x in dag.static_order():
    values[x] = eval(values[x])

values = {}
dag = graphlib.TopologicalSorter()

for line in open("input").read().strip().splitlines():
    a, bs = line.split(": ")
    if a != "humn":
        bs = bs.split()
        if len(bs) == 1:
            values[a] = bs[0]
            dag.add(a)
        else:
            dag.add(a, bs[0], bs[2])
            values[
                a
            ] = f"values['{bs[0]}'] {'=' if a =='root' else bs[1]} values['{bs[2]}']"

for n in dag.static_order():
    if n != "humn":
        xs = values[n].split()
        if len(xs) > 1:
            x, op, y = xs
            if "humn" not in x:
                x = str(eval(x))
            if "humn" not in y:
                y = str(eval(y))
            if "humn" not in x and "humn" not in y:
                values[n] = eval(f"{x} {op} {y}")
            else:
                values[n] = f"({x} {op} {y})"

eq, root = values["root"][1:-1].split(" = ")
print(values["root"].replace("values['humn']", "x").replace(".0", ""))
root = Fraction(root)
eq = eq.replace("values['humn']", "humn")
while eq.startswith("("):
    eq = eq[1:-1]
    root = Fraction(root)
    if eq.startswith("("):
        xs = eq.split(" ")
        x = Fraction(xs[-1])
        op = xs[-2]
        print(f"X {op} {x} = {root}")
        if op == "*":
            root = root / x
        elif op == "/":
            root = root * x
        elif op == "+":
            root = root - x
        elif op == "-":
            root = root + x
        eq = " ".join(xs[:-2])
    elif eq.endswith(")"):
        xs = eq.split(" ")
        x = Fraction(xs[0])
        op = xs[1]
        print(f"{x} {op} X = {root}")
        if op == "*":
            root = root / x
        elif op == "/":
            root = x / root
        elif op == "+":
            root = root - x
        elif op == "-":
            root = -root + x
        eq = " ".join(xs[2:])

print(root, "=", eq)
