import firebase_admin
from firebase_admin import credentials, firestore

def init_firebase():
    cred = credentials.Certificate('C:\\Users\\user\\Documents\\dhan-algo-firebase-adminsdk-qg1gu-eb29f3fc8a.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db
