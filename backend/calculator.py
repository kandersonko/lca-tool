from sympy import symbols, sympify, simplify, lambdify
import pandas as pd
import logging

logger = logging.getLogger()


class Calculator(object):
    def __init__(self, equation, variables, csv_file):
        self.variables = variables
        self.equation = equation
        self.csv_file = csv_file

    def validate(self):
        error = None
        data = None
        self.variables = symbols(self.variables)
        self.equation = sympify(self.equation)
        logger.error("vars: %s", self.variables)

        try:
            data = pd.read_csv(self.csv_file, index_col=None)
        except FileNotFoundError:
            error = f"Error: The file '{self.csv_file.filename}' does not exist."
        except pd.errors.EmptyDataError:
            error = "Error: The uploaded file is empty."
        except pd.errors.ParserError:
            error = "Error: The uploaded file is not in CSV format."

        if data is not None:
            missing_variables = [
                str(var) for var in self.variables if str(var) not in data.columns
            ]
            if len(missing_variables) > 0:
                error = f"Error: Missing variables in the CSV file: {', '.join(missing_variables)}"
            elif error is None:
                self.data = data
                return True, data

        return False, error

    def evaluate(self):
        validated, outcome = self.validate()
        if not validated:
            return False, outcome
        else:
            data = self.data
            variables = self.variables
            equation = self.equation
            expr = simplify(equation)

            # Evaluate the equation using lambdify
            eval_func = lambdify(variables, expr, modules=["numpy"])

            # Evaluate the function for each row of the DataFrame
            results = []
            for index, row in data.iterrows():
                row_values = [row[str(var)] for var in variables]
                result = eval_func(*row_values)
                results.append(result)

            # Store and render the result
            data["result"] = results
            # Create a list of column names that should be displayed in the result table
            column_names = [str(v) for v in variables] + ["result"]
            # Filter the DataFrame to include only the selected columns
            data = data[column_names]
            return True, data
