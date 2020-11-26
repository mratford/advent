from typing import Dict, List, Tuple, NamedTuple
from collections import defaultdict, deque
import math


class Ingredient(NamedTuple):
    required: int
    chemical: str

    
class Reaction(NamedTuple):
    produced: int
    ingredients: List[Ingredient]


def parse_data(s: str) -> Dict[str, Reaction]:
    'Create a dictionary of reactions'
    reactions = {}
    
    for line in s.splitlines():
        inout = line.split(' => ')
        inputs = inout[0].split(', ')
        split_inputs = [x.split(' ') for x in inputs]
        ingredients = [Ingredient(int(x[0]), x[1]) for x in split_inputs]
        num_output = inout[1].split(' ')
        n_of_chemical = int(num_output[0])
        chemical_name = num_output[1]
        
        reactions[chemical_name] = Reaction(n_of_chemical, ingredients)
        
    return reactions



def topological_sort(reactions: Dict[str, Reaction]) -> List[str]:
    graph = defaultdict(set)
    
    for chem in reactions:
        for _, dependency in reactions[chem].ingredients:
            graph[dependency].add(chem)
            
    search = ['ORE']
    seen = set()
    result = []
    
    while search:
        node = search.pop()
        if children := graph[node] - seen:
            print(children)
            search.append(node)
            c = children.pop()
            search.append(c)
            seen.add(c)
        else:
            result.append(node)
        
    return result
    
    
def minimum_ore(s: str) -> int:
    reactions = parse_data(s)
    
    to_produce = defaultdict(int)
    to_produce['FUEL'] = 1
    
    for chem in topological_sort(reactions):
        print(chem)
        if chem == 'ORE':
            return to_produce['ORE']
        
        required = to_produce[chem]
        produced_per_reaction = reactions[chem].produced
        reactions_required = math.ceil(required / produced_per_reaction)

        for n_ing_required, ingredient in reactions[chem].ingredients:
            to_produce[ingredient] += reactions_required * n_ing_required
            
            
test_data = '''10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL'''

        
if __name__ == '__main__':
    data = open('input', 'r').read()
    print(f'Part 1: {minimum_ore(data)}')
