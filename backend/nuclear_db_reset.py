from app import app, db
from sqlalchemy import text

def nuclear_reset():
    with app.app_context():
        print("⚠️  WARNING: Starting Nuclear Database Reset...")
        print("This will erase ALL data and structures in the 'public' schema.")
        
        try:
            # 1. Establish connection to the database
            with db.engine.connect() as connection:
                # 2. Force drop the public schema using CASCADE
                # This kills all tables (Users, Media, etc.) and their constraints.
                print("Dropping public schema (CASCADE)...")
                connection.execute(text("DROP SCHEMA public CASCADE;"))
                
                # 3. Recreate the schema to start fresh
                print("Recreating public schema...")
                connection.execute(text("CREATE SCHEMA public;"))
                
                # 4. Grant basic permissions (required in some environments like Railway)
                # Note: This ensures your database user owns the new schema.
                connection.execute(text("GRANT ALL ON SCHEMA public TO public;"))
                
                # 5. Commit these changes to the server
                connection.commit()
                print("✅ Database wiped clean.")

            # 6. Rebuild tables from your current models.py
            print("Building new tables from models.py...")
            db.create_all()
            print("✅ Success! Database structure has been recreated.")

        except Exception as e:
            print(f"❌ FAILED to reset database: {str(e)}")

if __name__ == "__main__":
    nuclear_reset()