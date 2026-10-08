import os

from flask import Flask, jsonify, render_template, request

from app import calculator

APP_VERSION = os.getenv("APP_VERSION", "dev")
APP_ENV = os.getenv("APP_ENV", "local")

OPERATIONS = {
    "add": calculator.add,
    "subtract": calculator.subtract,
    "multiply": calculator.multiply,
    "divide": calculator.divide,
    # DEMO (missing dependency): uncomment together with power() in calculator.py
    "power": calculator.power,
}

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html", version=APP_VERSION, environment=APP_ENV)


@app.get("/api/info")
def info():
    return jsonify(
        message="Hello from the GitHub Actions CI/CD demo!",
        version=APP_VERSION,
        environment=APP_ENV,
    )


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/calc/<operation>")
def calc(operation: str):
    func = OPERATIONS.get(operation)
    if func is None:
        return jsonify(error=f"Unknown operation '{operation}'"), 404

    try:
        a = float(request.args["a"])
        b = float(request.args["b"])
        result = func(a, b)
    except KeyError:
        return jsonify(error="Query parameters 'a' and 'b' are required"), 400
    except ValueError as exc:
        return jsonify(error=str(exc)), 400

    return jsonify(operation=operation, a=a, b=b, result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
