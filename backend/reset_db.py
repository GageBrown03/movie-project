from app import app, db
with app.app_context():
    db.drop_all()  # Delete old tables
    db.create_all()  # Create new tables with User
    print("Database recreated!")
exit()