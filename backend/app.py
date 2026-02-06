from dotenv import load_dotenv
from flask import Flask, Response
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.config import Config
from src.models import db, bcrypt
from src.routes.movie_router import movie_router
from src.routes.auth_router import auth_router  # NEW: Import auth router
from sqlalchemy import text

# Load local environment variables before anything else
load_dotenv()

# Initialize flask WSGI app
app = Flask(__name__)

# Configure app using the Config class directly
app.config.from_object(Config)

# Initialize database with app
db.init_app(app)

# Initialize Bcrypt (for password hashing)
bcrypt.init_app(app)

# Apply CORS header middleware for cross-origin requests
CORS(
    app,
    # Revised CORS structure to allow resources
    resources={r"/*": {"origins": [
        "https://movie-project-six-eta.vercel.app"
    ]}},
    supports_credentials=True
)

# Initialize JWT (for authentication tokens)
jwt = JWTManager(app)

# Register routers
app.register_blueprint(movie_router)
app.register_blueprint(auth_router)  # NEW: Register auth routes


@app.get('/health')
def check_health():
    try:
        db.session.execute(text('SELECT 1')).all()
        return Response('OK', 200, mimetype='text/plain')
    except Exception as e:
        return Response(str(e), 500, mimetype='text/plain')


# Run the Flask development server
if __name__ == '__main__':
    app.run(debug=True)