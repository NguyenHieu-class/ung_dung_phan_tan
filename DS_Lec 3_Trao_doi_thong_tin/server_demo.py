from jsonrpc import JSONRPCResponseManager, dispatcher
from flask import Flask, request

app = Flask(__name__)

@dispatcher.add_method
def add(a, b):
    return a + b

@dispatcher.add_method
def subtract(a, b):
    return a - b

@dispatcher.add_method
def multiply(a, b):
    return a * b

@dispatcher.add_method
def divide(a, b):
    if b == 0:
        return "Error: Division by zero"
    return a / b

@app.route("/rpc", methods=["POST"])
def handle_rpc():
    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return response.json

if __name__ == "__main__":
    app.run(port=5000)
    