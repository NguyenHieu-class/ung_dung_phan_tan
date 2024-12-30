import requests

url = "http://localhost:5000/rpc"

def make_request(method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    response = requests.post(url, json=payload)
    return response.json()

print("Addition: ", make_request("add", [5, 7]))
print("Subtraction: ", make_request("subtract", [10, 4]))
print("Multiplication: ", make_request("multiply", [3, 6]))
print("Division: ", make_request("divide", [8, 2]))
print("Division by zero: ", make_request("divide", [8, 0]))