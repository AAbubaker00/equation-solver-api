from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/v1/<latextformat>', methods=['GET'])
def book(latextformat):
    if request.method == 'GET':
        from methods_collection import sympy_method

        try:
            return sympy_method.sympy_solve(expression=latextformat)
        except Exception as error:
            return jsonify({
                'location': 'Method 0',
                'error': '{}'.format(error)})

if __name__ == '__main__':
    app.run(debug=False)
