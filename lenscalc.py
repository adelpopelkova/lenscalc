from sympy import symbols, Eq
from sympy.core.symbol import Symbol
from sympy.sets.sets import Complement
from sympy.solvers.solveset import nonlinsolve


class Lens:
    variables = "D1", "D2", "D", "n1", "nL", "n2", "r1", "r2", "CT", "P1", "P2", "f1", "f2", "EFL", "FFL", "BFL", "NPS"

    for variable in variables:
        vars()[variable] = symbols(variable)

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
        self.parameters = locals()
        del self.parameters["self"]
    
    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)

        if isinstance(attr, Symbol):
            try:
                return self.parameters[name]
            except KeyError:
                raise AttributeError
        else:
            return attr

    def __setattr__(self, name, value):
        try:
            if name in self.parameters:
                self.parameters[name] = value
                return
        except AttributeError:
            object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)

    def _calculate_replacements(self):
        result = {}
        for variable in self.variables:
            if self.parameters[variable] is not None:
                result[variable] = self.parameters[variable]
        
        return result

    def calculate(self):
        self.replacements = self._calculate_replacements()
        missing_values = [v for v in self.variables if v not in self.replacements]
        if not missing_values:
            print("Nothing to compute. All variables have their values!")
            return
        solved_equations = nonlinsolve(self.equations, missing_values)
        # sympy.solvers.solveset.nonlinsolve returns a FiniteSet.
        # The problem with it is that it isn't subscriptable.
        # In the case of lenscalc, there is only one solution,
        # which can't be taken out using solved_equations[0].
        # FiniteSet has an args method which can be used to get out the result.
        # https://docs.sympy.org/latest/tutorial/manipulation.html#args
        solved_equations = solved_equations.args
        for variable, solved_equation in zip(missing_values, solved_equations[0]):
            if isinstance(solved_equation, Complement):
                # This variable assignment below is used,
                # so that all variables are of the same type.
                # The first args[0] gets the equation from the Complement.
                # The result is a FiniteSet, that's why args[0] is used again.
                solved_equation = solved_equation.args[0].args[0]
            setattr(self, variable, solved_equation.subs(self.replacements))

    def __str__(self):
        return "\n".join(f"{var}: {self.parameters[var]}" for var in self.variables)
    
    def __repr__(self):
        return self.__str__()
