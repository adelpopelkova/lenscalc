from itertools import combinations, chain

from lenscalc import Lens

# Create iterables for parametrized tests
single_variables = combinations(Lens.variables, 1)
pairs = combinations(Lens.variables, 2)
triplets = combinations(Lens.variables, 3)
combinations_of_4 = combinations(Lens.variables, 4)
combinations_of_5 = combinations(Lens.variables, 5)

combinations_failing = [
    ('nL', 'r1', 'r2', 'CT'),
    ('D1', 'nL', 'r1', 'r2', 'CT'),
    ('D1', 'nL', 'r2', 'P1', 'FFL'),
    ('D2', 'nL', 'r1', 'r2', 'CT'),
    ('D2', 'nL', 'r1', 'P2', 'BFL'),
    ('D', 'n1', 'nL', 'n2', 'EFL'),
    ('D', 'nL', 'r1', 'r2', 'CT'),
    ('n1', 'nL', 'r1', 'r2', 'CT'),
    ('nL', 'n2', 'r1', 'r2', 'CT'),
    ('nL', 'r1', 'r2', 'CT', 'P1'),
    ('nL', 'r1', 'r2', 'CT', 'P2'),
    ('nL', 'r1', 'r2', 'CT', 'f1'),
    ('nL', 'r1', 'r2', 'CT', 'f2'),
    ('nL', 'r1', 'r2', 'CT', 'EFL'),
    ('nL', 'r1', 'r2', 'CT', 'FFL'),
    ('nL', 'r1', 'r2', 'CT', 'BFL'),
    ('nL', 'r1', 'r2', 'CT', 'NPS'),
    ('D1', 'D2', 'nL', 'P1', 'FFL'),
    ('D1', 'D2', 'nL', 'P2', 'BFL')
]

combinations_of_4_passing = [c for c in combinations_of_4 if c not in combinations_failing]
combinations_of_5_passing = [c for c in combinations_of_5 if c not in combinations_failing]

combinations_passing = chain(
    single_variables,
    pairs,
    triplets,
    combinations_of_4_passing,
    combinations_of_5_passing
)
