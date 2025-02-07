from flask import Flask, jsonify
from flask_cors import CORS

# Initializes FastAPI app.
# Loads routes from the routes/ directory.
# Runs the application.

# Initialize Flask app
app = Flask(__name__)

# Add CORS middleware
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route("/", methods=["GET"])
def read_root():
    return jsonify({"message": "Backend is running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
