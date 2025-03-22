from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from routes.jobs import jobs
from routes.users import users
from routes.resumes import resumes

# MAKE ENDPOINT FOR RESUME DOWNLOAD --> PDF
# MAKE ENDPOINT FOR REMOVING SAVEDJOB


# Initialize Flask app
app = Flask(__name__)
os.environ['TOKENIZERS_PARALLELISM'] = "false"
CORS(app, origins=["http://localhost:3000"])

# Register blueprints
app.register_blueprint(jobs, url_prefix="/jobs")
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(resumes, url_prefix="/resumes")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
