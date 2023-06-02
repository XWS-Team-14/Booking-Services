import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("service_account_key.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://xws-booking-default-rtdb.europe-west1.firebasedatabase.app'
})
