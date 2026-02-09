from app import app, db
from sqlalchemy import text

with app.app_context():
    # connect to the database
    with db.engine.connect() as connection:
        # 1. Disable integrity checks (optional but safe)
        # 2. Drop the entire schema using CASCADE (The "Nuclear Option")
        connection.execute(text("DROP SCHEMA public CASCADE;"))
        connection.execute(text("CREATE SCHEMA public;"))
        
        # 3. Commit the destruction
        connection.commit()
        
        print("Existing database wiped clean.")

    # 4. Create new tables from your current models
    db.create_all()
    print("New database created successfully!")

exit()


#OLD reset_db.py:
#from app import app, db
#with app.app_context():
#    db.drop_all()  # Delete old tables
#    db.create_all()  # Create new tables with User
#    print("Database recreated!")
#exit()