from app import app, db

# Create all database tables
with app.app_context():
    db.create_all()
    print("✅ Database tables created successfully!")
    print(f"Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")