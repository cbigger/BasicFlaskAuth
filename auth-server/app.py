from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from pymongo import MongoClient
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Setup API connection
api_server_url = f'http://localhost:9393/'

# Setup MongoDB connection
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/KerBI')
mongo_client = MongoClient(mongo_uri)
db = mongo_client.get_default_database()
clients_collection = db["accounts"]

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Change this to your secret key
jwt = JWTManager(app)

def get_user_data_from_database(api_key):
    print("\ngetting user data from database")
    return clients_collection.find_one({"api_key": api_key}, {"_id": 0})  # Exclude MongoDB ID from the payload

# client applications need to get a token first. They send an api_key here and get the token back after.
@app.route('/authenticate', methods=['POST'])
def authenticate():
    print("\nAuthenticating request: ")
    print("Headers:", request.headers)
    print("Body:", request.get_data(as_text=True))
    api_key = request.headers.get('Authorization')
    user_data = get_user_data_from_database(api_key)
    if user_data:
      # Create JWT token with user data embedded
        access_token = create_access_token(identity=user_data)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid API key"}), 401

# After getting a token, the client can send requests to the API through this endpoint
@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
def proxy_to_api():
  # Get JWT identity, which contains the user data
    current_user = get_jwt_identity()
    print("\nCurrent user data:", current_user)
    response = requests.request(
        method=request.method,
        url=api_server_url,
        headers={'Authorization': request.headers.get('Authorization')},
        data=request.get_data(),
        params=request.args,
        allow_redirects=False)

    return (response.content, response.status_code, response.headers.items())

@app.route('/api/data', methods=['GET'])
@jwt_required()
def get_data():
  # Get the identity of the current user from the JWT
    current_user_identity = get_jwt_identity()

  # Get the entire decoded token payload
    current_user_claims = get_jwt()

  # Access custom fields from the JWT payload, if any
    custom_field = current_user_claims.get('custom_field', 'default_value')

    return jsonify({
        "user_identity": current_user_identity,
        "custom_field": custom_field
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
