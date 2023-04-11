from flask import Flask, render_template, jsonify, request
from secrets import token_hex
import random

random.seed(token_hex(16))

app = Flask(__name__)

X = None
Y = None
B = None
B_public = None
A_public = None
secret_key = None

def get_random_number():
    return random.randint(1, 10) 


def get_6_digit_prime():
    primes = [101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197]
    a, b = random.choice(primes), random.choice(primes)
    if a == b:
        return get_6_digit_prime()
    return a, b


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/api/test')
def api_test():
    return jsonify({"test": "test"})


@app.route('/api/public_key_exchange', methods=['POST'])
def get_public_key():
    body = request.get_json()
    print("body: ", body)
    global A_public
    A_public = body['A_public_key']
    global secret_key
    secret_key = (A_public ** B) % Y
    print("SECRET KEY: ", secret_key)
    return jsonify({"B_public_key": B_public})

@app.route('/api/get_primes')
def get_primes():
    return jsonify({ "X": X, "Y": Y }), 200


if __name__ == '__main__':
    B = get_random_number()
    X, Y = get_6_digit_prime()
    B_public = (X ** B) % Y
    app.run(debug=True)