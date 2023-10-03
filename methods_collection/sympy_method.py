
def custom_latex(expr):
    latex_str = (expr)

    latex_str = latex_str.replace('(', '{').replace(')', '}')

    latex_str = latex_str.replace('sqrt', r'\sqrt')

    return latex_str


def sympy_solve(expression):
    latextformat = custom_latex(expr=expression)

    try:
        from latex2sympy2 import latex2sympy, latex2latex
        from sympy import solve

        result = solve(latex2sympy(latextformat))

        if isinstance(result, list):
            formatted_result = ', '.join(map(str, result))
        else:
            formatted_result = str(result)

        try:
            from flask import jsonify

            return jsonify({
                'standardFormat': latextformat,
                'sympy': "{}".format(latex2sympy(latextformat)),
                'solution': formatted_result,
                'solutionLaTex': custom_latex(formatted_result),
                'latextToLatex': latex2latex(latextformat)
            })
        except Exception as error:
            return jsonify({
                'location': 'Method 1',
                'error': '{}'.format(error)
            })
    except Exception as error:
        from . import math_solver

        return math_solver.math_solve(expression=expression)
