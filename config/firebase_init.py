import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import secretmanager
import json

def init_firebase():
    client = secretmanager.SecretManagerServiceClient()
    secret_name = "projects/dhan-algo/secrets/firebase-credentials/versions/latest"
    response = client.access_secret_version(request={"name": secret_name})

    # Load the credentials from the secret
    credentials_data = response.payload.data.decode("UTF-8")
    cred_dict = json.loads(credentials_data)

    # Initialize Firebase Admin SDK
    cred = credentials.Certificate(cred_dict)

    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db
