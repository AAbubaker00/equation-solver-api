from bs4 import BeautifulSoup

def format_equation(equation):
    equation = equation.replace('(', '{').replace(')', '}')
    equation = equation.replace("\\\\", "`")
    equation = equation.replace('sqrt', r'\sqrt')
    equation = equation.replace(' ', '')

    return equation


def math_solve(expression):
    equation = format_equation(equation=expression)
    # print(equation)

    url = 'https://mathsolver.microsoft.com/en/solve-problem/{}'.format(equation)
    print(url)
    
    from app import driver
    driver.get(url)

    try:
        page_source = driver.page_source
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        script_tag = soup.find(
            'script', attrs={'id': '__NEXT_DATA__', 'type':  'application/json'})

        from flask import jsonify
        import json

        json_data = json.loads(script_tag.string)

        final_json = json_data['props']['pageProps']['response']['mathSolverResult']

        return jsonify(final_json)
    except Exception as error:
        return jsonify({'error': '{}'.format(error)})
