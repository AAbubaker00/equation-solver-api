from bs4 import BeautifulSoup
from selenium import webdriver

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
    # print(url)


    # # Create ChromeOptions object for headless mode
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    # Create a webdriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    try:
        page_source = driver.page_source
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        script_tag = soup.find(
            'script', attrs={'id': '__NEXT_DATA__', 'type':  'application/json'})

        from flask import jsonify
        import json
        json_data =  json.loads(script_tag.string)

        final_json = json_data['props']['pageProps']['response']['mathSolverResult']

        action_list = []

        for action in final_json['actions']:
            action_dict = {
                "actionName": action.get("actionName", ""),
                "solution": action.get("solution", ""),
                'steps': action.get('templateSteps')
            }
            # Append the extracted data to the list
            action_list.append(action_dict)

        return jsonify({
            'standardFormat': final_json['problem'],
            'problemCategory':  final_json['problemCategory'],
            'solutions': action_list,
        })

    except Exception as error:
        return jsonify({
            'location': 'Method 2',
            'error': '{}'.format(error)})
    finally: 
        driver.quit()
