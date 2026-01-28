from dotenv import load_dotenv
from flask import Flask, Response
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.config import Config
from src.models import db, bcrypt
from src.routes.movie_router import movie_router
from src.routes.auth_router import auth_router  # NEW: Import auth router

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

# Initialize JWT (for authentication tokens)
jwt = JWTManager(app)

# Apply CORS header middleware for cross-origin requests
CORS(app)

# Register routers
app.register_blueprint(movie_router)
app.register_blueprint(auth_router)  # NEW: Register auth routes


@app.get('/health')
def check_health():
    db.session.execute('SELECT 1').all()
    return Response('OK', 200, mimetype='text/plain')


# Run the Flask development server
if __name__ == '__main__':
    app.run(debug=True, port=5000)