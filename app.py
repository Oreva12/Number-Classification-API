from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

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

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    try:
        number = request.args.get('number')
        
        if not number.isdigit():
            return jsonify({"error": True, "message": "Invalid number format"}), 400
        
        number = int(number)
        
        response = requests.get(f"http://numbersapi.com/{number}?json")
        if response.status_code != 200:
            return jsonify({"error": True, "message": "Error fetching fun fact"}), 500
        
        fun_fact = response.json().get('text', 'No fun fact available.')
        
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
        if number % 2 == 1:
            result["properties"].append("odd")
        else:
            result["properties"].append("even")
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
