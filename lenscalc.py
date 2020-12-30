from sympy import symbols, Eq
from sympy.core.symbol import Symbol
from sympy.solvers import solve


class Lens:
    variables = "Φ_OS", "Φ_IS", "Φ", "n_OS", "n_L", "n_IS", "R_1", "R_2", "CT", "P", "P_2", "f_F", "f_R", "EFL", "FFL", "BFL", "NPS"

    for variable in variables:
        vars()[variable] = symbols(variable)

    equations = (
        Eq(Φ_OS, (n_L - n_OS) / R_1),
        Eq(Φ_IS, (n_IS - n_L) / R_2),
        Eq(Φ, Φ_OS + Φ_IS - Φ_OS * Φ_IS * (CT / n_L)),
        Eq(P, (Φ_IS / Φ) * (n_OS / n_L) * CT),
        Eq(P_2, -(Φ_OS / Φ) * (n_IS / n_L) * CT),
        Eq(EFL, 1 / Φ),
        Eq(f_F, -n_OS * EFL),
        Eq(f_R, n_IS * EFL),
        Eq(BFL, f_R + P_2),
        Eq(FFL, f_F + P),
        Eq(NPS, f_R + f_F),
    )

    def __init__(self, *, Φ_OS=None, Φ_IS=None, Φ=None, n_OS=None, n_L=None, n_IS=None, R_1=None, R_2=None, CT=None, P=None, P_2=None, f_F=None, f_R=None, EFL=None, FFL=None, BFL=None, NPS=None):
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
        solved_equations = solve(self.equations, missing_values)
        for variable, solved_equation in zip(missing_values, solved_equations[0]):
            setattr(self, variable, solved_equation.subs(self.replacements))
    
    def __str__(self):
        return "\n".join(f"{var}: {self.parameters[var]}" for var in self.variables)
    
    def __repr__(self):
        return self.__str__()
