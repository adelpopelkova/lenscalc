from math import isclose  # Due to the floating point inaccuracy
from decimal import Decimal

from sympy import Eq
from sympy.core.symbol import Symbol
from sympy.core.numbers import Float, Rational, Zero, Infinity
from sympy.core.expr import Expr
from sympy.solvers import solve


class Lens:
    numbers = int, float, Float, Rational, Decimal, Zero, Infinity  # Classes with numbers
    variables = "D1", "D2", "D", "n1", "nL", "n2", "r1", "r2", "CT", "P1", "P2", "f1", "f2", "EFL", "FFL", "BFL", "NPS"

    for variable in variables:
        vars()[variable] = Symbol(variable)

    equations = (
        Eq(D1, (nL - n1) / r1),
        Eq(D2, (n2 - nL) / r2),
        Eq(D, D1 + D2 - D1 * D2 * (CT / nL)),
        Eq(P1, (D2 / D) * (n1 / nL) * CT),
        Eq(P2, -(D1 / D) * (n2 / nL) * CT),
        Eq(EFL, 1 / D),
        Eq(f1, -n1 * EFL),
        Eq(f2, n2 * EFL),
        Eq(BFL, f2 + P2),
        Eq(FFL, f1 + P1),
        Eq(NPS, f2 + f1),
    )

    def __init__(self, *, D1=None, D2=None, D=None, n1=None, nL=None, n2=None, r1=None, r2=None, CT=None, P1=None, P2=None, f1=None, f2=None, EFL=None, FFL=None, BFL=None, NPS=None):
        for variable, value in locals().items():
            if variable in self.variables:
                setattr(self, variable, value)

    def __setattr__(self, name, value):
        if isinstance(value, str) and (name in self.variables):
            value = float(value)
        object.__setattr__(self, name, value)

    def _calculate_replacements(self):
        result = {}
        for variable in self.variables:
            if (value := getattr(self, variable)) is not None:
                result[variable] = value

        return result

    def calculate(self):
        self.replacements = self._calculate_replacements()
        # Calculation without any variables isn't supported
        # because `sympy.solve` gets into an infinite loop.
        if not self.replacements:
            raise ValueError("No variables were given!")

        missing_values = [Symbol(v) for v in self.variables if v not in self.replacements]
        if not missing_values:
            print("Nothing to compute. All variables have their values!")
            return

        # Copy the lens equations to later manipulate with them.
        equations = list(self.equations)

        equation_index = 0
        while missing_values and equation_index < len(equations):
            equation = equations[equation_index]
            common = set(missing_values) & equation.free_symbols

            if not common:
                equations.remove(equation)

            elif len(common) == 1:
                variable = common.pop()
                solved_equation = solve(equation, variable)

                if isinstance(solved_equation, list):
                    solved_equation = solved_equation[0]

                if isinstance(solved_equation, dict):
                    self.replacements[str(variable)] = solved_equation[variable].subs(self.replacements)

                if isinstance(solved_equation, Expr):
                    self.replacements[str(variable)] = solved_equation.subs(self.replacements)

                setattr(self, str(variable), self.replacements[str(variable)])
                missing_values.remove(variable)
                equations.remove(equation)
                equation_index = 0

            else:
                equation_index += 1

        # From the equations:
        # f1 = -n1 * EFL
        # f2 = n2 * EFL
        # NPS = f2 + f1
        # NPS = (n2 * EFL) + (-n1 * EFL)
        # NPS = EFL * (n2 - n1)
        # and if n1 == n2 -> n2 - n1 = 0
        # which means that NPS = EFL * 0
        # which means that NPS = 0
        if self.n1 and self.n2 and isclose(self.n1, self.n2):
            self.NPS = 0
            self.replacements["NPS"] = 0
            if Symbol("NPS") in missing_values:
                missing_values.remove(Symbol("NPS"))

        if not missing_values:
            return

        missing_values = [str(variable) for variable in missing_values]
        if len(equations) > len(missing_values):
            equations = equations[:len(missing_values)]
        solved_equations = solve(equations, missing_values)
        if isinstance(solved_equations, dict):
            if len(solved_equations) < len(missing_values):
                solved_equations[Symbol("NPS")] = Symbol("NPS")
            for variable in missing_values:
                setattr(self, variable, solved_equations[Symbol(variable)].subs(self.replacements))
            if isinstance(self.n1, Lens.numbers) and isinstance(self.n2, Lens.numbers) and isclose(self.n1, self.n2):
                self.NPS = 0
            return

        if not len(solved_equations):
            error_message = (
                "There has been a problem with the calculation.\n"
                "If you think, that this should return a propper result,"
                "don't hesitate to open an issue at "
                "https://github.com/adelpopelkova/lenscalc/"
            )
            raise ValueError(error_message)

        for variable, solved_equation in zip(missing_values, solved_equations[0]):
            value = solved_equation.subs(self.replacements)
            # The type of some values is sympy.core.add.Add
            # or sympy.core.mul.Mul, the value isn't a number.
            # This makes sure that we get the result as a number.
            if not isinstance(value, Float):
                value = value.n()
            setattr(self, variable, value)

    def __str__(self):
        return "\n".join(f"{var}: {getattr(self, var)}" for var in self.variables)

    def __repr__(self):
        return self.__str__()
