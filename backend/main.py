from flask import Flask  # type: ignore
from flask_cors import CORS  # type: ignore
import os
from routes.jobs import jobs
from routes.users import users
from routes.resumes import resumes
import nltk
nltk.data.path.append('/opt/venv/nltk_data')  # <- tell nltk where to find wordnet


os.environ['TOKENIZERS_PARALLELISM'] = "false"

# When one job is removed all the jobs are taken away from the display
# inhibiting removing any more jobs

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(jobs, url_prefix="/jobs")
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(resumes, url_prefix="/resumes")


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5001, debug=False)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # <- grab $PORT from Railway
    app.run(host="0.0.0.0", port=port, debug=False)
