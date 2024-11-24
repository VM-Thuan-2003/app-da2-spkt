import sys
import json
import requests
from pathlib import Path
from config import FIREBASE_API_URL, API_KEY

# Get the directory of the current script
script_dir = Path(__file__).parent

# Path to the Firebase Admin SDK credentials file
path_cred = Path.cwd() / "socket-io-db-firebase-adminsdk.json"

# Path to the firebase.json configuration file
path_firebase = Path.cwd() / "firebase.json"

# Load database URL from the firebase.json file
database_url = None
try:
    with open(path_firebase, "r") as f:
        firebase_config = json.load(f)
        database_url = firebase_config.get("databaseURL")
except FileNotFoundError:
    print("Warning: firebase.json file not found.")
    print("Please make sure to copy the firebase.json file from the Firebase console")
    print("into the root directory of the extracted zip file.")
    print(
        "If you are using the source code, you can find the file in the root directory."
    )
    print("If you are using the Docker image, you can mount the file as a volume.")
    print("For example: docker run -v /path/to/firebase.json:/app/firebase.json ...")
    sys.exit(1)

if not database_url:
    raise ValueError("databaseURL not found in firebase.json.")

# Initialize Firebase Admin SDK only if not already initialized
try:
    import firebase_admin
    from firebase_admin import credentials, auth, db

    if not firebase_admin._apps:
        cred = credentials.Certificate(path_cred)
        firebase_admin.initialize_app(
            cred, {"databaseURL": database_url}  # Loaded from firebase.json
        )
    else:
        print("Firebase app is already initialized.")
except ImportError:
    print("Error: Firebase Admin SDK not installed.")
    sys.exit(1)


# Firebase Manager Class
class FirebaseManager:
    """Class to manage user authentication and registration with Firebase."""

    @staticmethod
    def register_user(email, password):
        """Register a new user with email and password."""
        try:
            user = auth.create_user(email=email, password=password)
            print(f"Successfully created user: {user.uid}")
            return True
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return False

    @staticmethod
    def login_user(email, password):
        """Login a user with email and password using Firebase REST API."""
        try:
            # Request payload
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True,  # Request Firebase to return an ID Token
            }

            # Send POST request to Firebase Authentication REST API
            response = requests.post(
                FIREBASE_API_URL, params={"key": API_KEY}, json=payload
            )

            # Check for successful authentication
            if response.status_code == 200:
                user_data = response.json()
                id_token = user_data["idToken"]
                local_id = user_data["localId"]
                print(
                    f"Successfully authenticated user. ID Token: {id_token} - Local ID: {local_id}"
                )
                return True
            else:
                error_data = response.json()
                print(
                    f"Error during authentication: {error_data.get('error', {}).get('message')}"
                )
                return False
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False
