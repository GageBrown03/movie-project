# init_db.py
import os
from app import app, db

# Optional: Print to verify we are targeting the right DB
print(f"Creating tables in: {os.environ.get('DATABASE_URL')}")

with app.app_context():
    db.create_all()
    print("Tables created successfully!")