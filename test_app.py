from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>SQL Injection Scanner Test App</h1>
    <form action="/search" method="GET">
        <input type="text" name="q" placeholder="Enter test input">
        <button type="submit">Search</button>
    </form>
    """


@app.route("/search")
def search():
    query = request.args.get("q", "")

    if "'" in query:
        return (
            "Simulated SQL syntax error: "
            "You have an error in your SQL syntax."
        ), 400

    return f"Search completed for: {query}", 200


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )