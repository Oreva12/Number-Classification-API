from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
CORS(app)
executor = ThreadPoolExecutor(2)

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n):
    divisors = [i for i in range(1, n) if n % i == 0]
    return sum(divisors) == n

def is_armstrong(n):
    digits = [int(digit) for digit in str(n)]
    power = len(digits)
    return n == sum(digit**power for digit in digits)

def digit_sum(n):
    return sum(int(digit) for digit in str(n))

def get_fun_fact(number):
    response = requests.get(f"http://numbersapi.com/{number}?json")
    return response.json().get('text', 'No fun fact available.')

@app.route('/classify-number', methods=['GET'])
def classify_number():
    try:
        # Get the number from the query string
        number = request.args.get('number')

        # Handle case where number is missing or empty
        if not number:
            return jsonify({"error": True, "number": "", "message": "Number parameter is missing."}), 400

        # Handle case where number is not a valid integer
        if not number.lstrip('-').isdigit():
            return jsonify({"error": True, "number": number}), 400
        
        # Convert the number to an integer
        number = int(number)

        # Handle cases for negative numbers (optional based on your API logic)
        if number < 0:
            return jsonify({
                "error": True,
                "number": number,
                "message": "Negative numbers are not supported.",
                "is_prime": False,
                "is_perfect": False,
                "properties": [],
                "digit_sum": abs(number)
            }), 400

        # Fetch fun fact using asynchronous call
        fun_fact = executor.submit(get_fun_fact, number).result()

        # Prepare the result
        result = {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": [],
            "digit_sum": digit_sum(number),
            "fun_fact": fun_fact
        }

        # Additional number properties
        if is_armstrong(number):
            result["properties"].append("armstrong")
        if number % 2 == 1:
            result["properties"].append("odd")
        else:
            result["properties"].append("even")
        
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)