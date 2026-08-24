from functools import lru_cache

import firebase_admin
from firebase_admin import credentials, firestore

from app.config import get_settings

MEETINGS_COLLECTION = "meetings"


@lru_cache
def get_firestore_client():
    settings = get_settings()
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.firestore_service_account_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()
