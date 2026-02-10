# backend/app.py - COMPLETE FIX
from dotenv import load_dotenv
from flask import Flask, Response
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from src.config import Config
from src.models import db, bcrypt
from sqlalchemy import text

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure app
app.config.from_object(Config)

# ==========================================
# CRITICAL: CORS Configuration FIRST
# ==========================================
# Must be configured BEFORE blueprint registration
# This handles OPTIONS preflight requests automatically

CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "https://movie-project-six-eta.vercel.app",
                "http://localhost:8080",
                "http://localhost:3000"
            ],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "expose_headers": ["Content-Type", "Authorization"],
            "max_age": 0  # Disable preflight caching temporarily
        }
    }
)

# Explicitly handle OPTIONS for all routes
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://movie-project-six-eta.vercel.app')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Initialize database
db.init_app(app)

# Initialize Migration
migrate = Migrate(app, db)

# Initialize Bcrypt
bcrypt.init_app(app)

# Initialize JWT
jwt = JWTManager(app)

# ==========================================
# Import and Register Blueprints
# ==========================================
from src.routes.media_router import media_router
from src.routes.auth_router import auth_router
from src.routes.tmdb_router import tmdb_router

# Week 2 routes
from src.routes.friends import friends
from src.routes.privacy import privacy
from src.routes.compare import compare

app.register_blueprint(auth_router)
app.register_blueprint(media_router)
app.register_blueprint(tmdb_router)
app.register_blueprint(friends)
app.register_blueprint(privacy)
app.register_blueprint(compare)

print("✅ Blueprints registered:")
print("  - auth_router")
print("  - media_router")
print("  - tmdb_router")
print("  - friends (/api/friends)")
print("  - privacy (/api/privacy)")
print("  - compare (/api/compare)")


# ==========================================
# Health Check
# ==========================================
@app.get('/health')
def check_health():
    try:
        db.session.execute(text('SELECT 1')).all()
        return Response('OK', 200, mimetype='text/plain')
    except Exception as e:
        return Response(str(e), 500, mimetype='text/plain')


# ==========================================
# Error Handlers
# ==========================================
@app.errorhandler(404)
def not_found(e):
    return {"error": "Not found"}, 404


@app.errorhandler(500)
def internal_error(e):
    print(f"500 Error: {str(e)}")
    return {"error": "Internal server error", "message": str(e)}, 500


# Run Flask development server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)