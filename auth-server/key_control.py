import sys
import pymongo
from bson.objectid import ObjectId
from pymongo.errors import DuplicateKeyError
import uuid

# MongoDB connection parameters
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'KerBI'
COLLECTION_NAME = 'accounts'

def connect_db():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db

def check_or_create_collection():
    db = connect_db()
    if COLLECTION_NAME in db.list_collection_names():
        print(f"Collection '{COLLECTION_NAME}' exists.")
    else:
        db.create_collection(COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' created.")
        db[COLLECTION_NAME].create_index([('name', pymongo.ASCENDING)], unique=True)

def generate_api_key(name):
    db = connect_db()
    api_key = str(uuid.uuid4())
    try:
        result = db[COLLECTION_NAME].insert_one({'name': name, 'api_key': api_key})
        print(api_key)
    except DuplicateKeyError:
        print("Error: Name must be unique. API key generation failed.")

def delete_user(name):
    db = connect_db()
    result = db[COLLECTION_NAME].delete_one({'name': name})
    if result.deleted_count > 0:
        print(f"User '{name}' and associated API key successfully deleted.")
    else:
        print(f"User '{name}' not found.")

def main():
    if len(sys.argv) == 1:
        # No arguments, check or create collection
        check_or_create_collection()
    elif len(sys.argv) == 3:
        if sys.argv[1] == '--generate':
            # Generate API key for the name
            name = sys.argv[2]
            generate_api_key(name)
        elif sys.argv[1] == '--delete':
            # Delete user and their API key
            name = sys.argv[2]
            delete_user(name)
        else:
            print("Invalid option. Use --generate to create a key or --delete to remove a user.")
    else:
        print("Usage:")
        print(f"  {sys.argv[0]}                      # Check for or create the 'accounts' collection")
        print(f"  {sys.argv[0]} --generate <name>    # Generate an API key for <name> and store in the collection")
        print(f"  {sys.argv[0]} --delete <name>      # Delete a user and their API key from the collection")

if __name__ == "__main__":
    main()
