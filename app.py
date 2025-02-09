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
    digits = [int(digit) for digit in str(abs(n))]  # Consider absolute value for armstrong check
    power = len(digits)
    return abs(n) == sum(digit**power for digit in digits)

def digit_sum(n):
    return sum(int(digit) for digit in str(abs(n)))  # Ensure absolute value is used

def get_fun_fact(number):
    response = requests.get(f"http://numbersapi.com/{number}?json")
    return response.json().get('text', 'No fun fact available.')

@app.route('/classify-number', methods=['GET'])
def classify_number():
    try:
        number = request.args.get('number')

        if not number:
            return jsonify({"error": True, "number": "", "message": "Number parameter is missing."}), 400

        if not number.lstrip('-').isdigit():
            return jsonify({"error": True, "number": number}), 400
        
        number = int(number)

        fun_fact = executor.submit(get_fun_fact, number).result()

        result = {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": [],
            "digit_sum": digit_sum(number),
            "fun_fact": fun_fact
        }

        if is_armstrong(number):
            result["properties"].append("armstrong")
        if abs(number) % 2 == 1:  
            result["properties"].append("odd")
        else:
            result["properties"].append("even")

        if number < 0:
            result["properties"].append("negative")  

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)