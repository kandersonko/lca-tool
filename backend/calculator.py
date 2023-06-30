from sympy import symbols, sympify, simplify, lambdify
import pandas as pd
import numpy as np
import re
import logging

logger = logging.getLogger()


class Calculator(object):
    def _get_data(self, csvfile):
        data, error = None, None
        try:
            data = pd.read_csv(csvfile, index_col=None)
            data = data.apply(
                lambda col: pd.to_numeric(col, downcast="float", errors="coerce")
            )
        except FileNotFoundError:
            error = f"Error: The file '{csvfile.filename}' does not exist."
        except pd.errors.EmptyDataError:
            error = "Error: The uploaded file is empty."
        except pd.errors.ParserError:
            error = "Error: The uploaded file is not in CSV format."

        return data, error

    def _validate_equation(self, data, equation):
        error = None
        header = data.columns.to_list()
        header_variables = dict(zip(header, [f"var{x}" for x in range(len(header))]))

        subs = [(k, v) for k, v in header_variables.items()]
        substitutions = subs

        formula = equation
        for sub in subs:
            data[sub[1]] = data[sub[0]]
            formula = re.sub(f"[\"']{sub[0]}[\"']", sub[1], formula)

        equation = formula

        return equation, error

    def _validate(self, csv_file, input_equation):
        error = None
        data = None

        data, error = self._get_data(csv_file)
        if data is None:
            return False, error, data

        equation, error = self._validate_equation(data, input_equation)
        if error is None:
            return True, equation, data

        logger.debug("equation spec: %s", equation)

        return True, error, data

    def _evaluate_equation(self, input_data, equation):
        data = input_data.copy()
        expr = None
        error = None
        cols = dict()
        for k, v in data.to_dict().items():
            if any(isinstance(s, str) for s in list(v.values())):
                continue
            cols[k] = np.array(list(v.values()), dtype=np.float64)
        expr = sympify(equation, cols)

        expr = simplify(expr)
        logger.debug("=== Expr: %s", expr)

        results = np.array(expr, np.float64)

        return True, results

    def evaluate(self, csv_file, equation):
        result = None
        validated, outcome, data = self._validate(csv_file, equation)
        if not validated:
            return False, outcome
            # evaluated, result = self._evaluate_equation(data, equation, result=result)
        equation = outcome
        evaluated, result = self._evaluate_equation(data, equation)
        if evaluated:
            result = np.round(result.astype(np.float64), 3).tolist()

        return validated, result
