from sympy import symbols, sympify, simplify, lambdify
import pandas as pd
import re
import logging

logger = logging.getLogger()


class Calculator(object):
    def __init__(self, equations, csv_file):

        self.input_equations = equations
        self.equations = []

        self.csv_file = csv_file
        self.substitutions = []

    def _get_data(self, csvfile):
        data, error = None, None
        try:
            data = pd.read_csv(csvfile, index_col=None)
        except FileNotFoundError:
            error = f"Error: The file '{csvfile.filename}' does not exist."
        except pd.errors.EmptyDataError:
            error = "Error: The uploaded file is empty."
        except pd.errors.ParserError:
            error = "Error: The uploaded file is not in CSV format."
        return data, error

    def _validate_equation(self, data, input_equation):
        error = None
        header = data.columns.to_list()
        header_variables = dict(zip(header, [f"var{x}" for x in range(len(header))]))

        subs = [(k, v) for k, v in header_variables.items()]
        self.substitutions = subs

        formula = input_equation
        for sub in subs:
            data[sub[1]] = data[sub[0]]
            formula = re.sub(f"[\"']{sub[0]}[\"']", sub[1], formula)

        equation = formula

        return equation, error

    def validate(self):
        error = None
        data = None

        data, error = self._get_data(self.csv_file)
        if data is None:
            return False, error

        self.data = data

        for input_equation in self.input_equations:
            equation, error = self._validate_equation(data, input_equation)
            self.equations.append(equation)

        logger.debug("equation spec: %s", self.equations)

        return True, error

    def _evaluate_equation(self, input_data, equation, result=[]):
        data = input_data.copy()
        expr = sympify(equation, dict(result=result))
        results = []
        column_names = []
        # expr = simplify(formula)
        if not hasattr(expr, "free_symbols"):
            results = expr
            return True, results

        variables = expr.free_symbols
        missing_variables = [
            str(var) for var in variables if str(var) not in data.columns
        ]
        if len(missing_variables) > 0:
            error = f"Error: Missing variables in the CSV file: {', '.join(missing_variables)}"

        # TODO lambdify uses `eval`, sanitize the expr to avoid remote code execution
        # Evaluate the equation using lambdify
        eval_func = lambdify(variables, expr, modules=["numpy"])

        # Evaluate the function for each row of the DataFrame
        for index, row in data.iterrows():
            row_values = [row[str(var)] for var in variables]
            result = eval_func(*row_values)
            results.append(result)

        # for sub in self.substitutions:
        #     if sub[1] in data.columns:
        #         data[sub[0]] = data[sub[1]]
        #         data.drop(columns=[sub[1]], axis=1)
        #         column_names.append(sub[0])

        # Store and render the result
        # column_names += ["result"]
        # Create a list of column names that should be displayed in the result table
        # Filter the DataFrame to include only the selected columns
        # data = data[column_names]
        return True, results

    def evaluate(self):
        validated, outcome = self.validate()
        if not validated:
            return False, outcome
        data = self.data
        evaluated, result = self._evaluate_equation(data, self.equations[0], result=[])
        if not evaluated:
            return False, None
        for equation in self.equations[1:]:
            evaluated, result = self._evaluate_equation(data, equation, result=result)
            if not evaluated:
                return False, None
        return evaluated, result
