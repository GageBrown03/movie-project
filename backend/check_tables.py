import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

load_dotenv()

# Manually grab the URL to be 100% sure
raw_uri = os.getenv('DATABASE_URL')
if raw_uri and raw_uri.startswith("postgres://"):
    raw_uri = raw_uri.replace("postgres://", "postgresql://", 1)

print(f"Checking Database at: {raw_uri}")

engine = create_engine(raw_uri)
inspector = inspect(engine)

tables = inspector.get_table_names()

if tables:
    print("✅ Tables found in database:")
    for table in tables:
        print(f" - {table}")
else:
    print("❌ No tables found! The database is empty.")