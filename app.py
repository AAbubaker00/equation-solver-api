from flask import Flask, request
from selenium import webdriver

app = Flask(__name__)

# Create ChromeOptions object for headless mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode

# Create a webdriver with the specified options
driver = webdriver.Chrome(options=chrome_options)


@app.route('/api/v1/<latextformat>', methods=['GET'])
def book(latextformat):
    if request.method == 'GET':
        from methods_collection import sympy_method

        try:
            return sympy_method.sympy_solve(expression=latextformat)
        except Exception as error:
            return jsonify({'error': '{}'.format(error)})

if __name__ == '__main__':
    app.run(debug=True)
