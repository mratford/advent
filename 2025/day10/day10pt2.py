from pyrsistent import PVector, pset, pvector


def parse_data(input_data: str) -> PVector[PVector[PVector[int]]]:
    """Create sets of linear equations, each expressed as a matrix."""
    for line in input_data.strip().splitlines():
        fields = line.strip().split()
        buttons = [
            pset(eval(field.replace(")", ",)"))) for field in fields[1:-1]
        ]
        joltages = eval(fields[-1].replace("{", "[").replace("}", "]"))
        eqs  
