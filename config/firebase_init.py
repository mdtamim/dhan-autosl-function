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
    # When cloud function is invoked,in first call app is initialized.When in another call
    # main method is called,app should not be initialized if its already initialized in previous calls
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    return db
