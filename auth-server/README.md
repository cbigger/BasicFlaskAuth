# KerBI's Auth Server

Basically, if you know how auth works, this should be a piece of cake, and if you don't, here's a nice & simple Flask auth from which you may learn!

This Flask application demonstrates JWT authentication using `flask_jwt_extended` and MongoDB for user management. It provides a simple API that authenticates users via an API key, issues JWT tokens, and proxies requests to another API with JWT validation.

## Features
- **User Authentication**: Validates users based on API keys and issues JWT access tokens.
- **JWT Token Management**: Uses `flask_jwt_extended` for handling JWT tokens, including token creation and protected route access.
- **MongoDB Integration**: Utilizes MongoDB to store and validate user account details.
- **API Proxy**: Proxies authenticated requests to another API, demonstrating how to use JWT tokens for accessing protected routes.
- **Environment Variables**: Configures sensitive information, such as database connection URI and JWT secret key, through environment variables for enhanced security.

## Setup

### Prerequisites
- Python 3
- Flask
- MongoDB
- `python-dotenv` for environment variable management
- `flask_jwt_extended` for JWT operations
- `pymongo` for MongoDB integration
- `requests` for making HTTP requests

### Installation
1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-folder>
```

2. Install the required Python packages:
```bash
pip install flask flask_jwt_extended python-dotenv pymongo requests
```

3. Set up your `.env` file with the necessary environment variables:
```env
MONGO_URI=mongodb://localhost:27017/KerBI
JWT_SECRET_KEY=your_secret_key_here
```

### Running the Application
1. Start your MongoDB server (ensure it's running on the URI specified in your `.env` file which is the default mongo port).

2. Run the Flask application:
```bash
python3 app.py
```

The Flask server will start, and you can begin making requests to authenticate and access the API.

## Usage

### Authenticating
Send a POST request to `/` with an `Authorization` header containing your API key to receive a JWT token.
This token can be used to pass client data around the KerBI API backend without the need to query databases.

### Accessing Protected Routes
Use the obtained JWT token as a Bearer token in the `Authorization` header to make requests to protected endpoints, such as `/api/` and `/api/data`.
GETs to `/api/data` with a valid JWT will return the parsed user data.
