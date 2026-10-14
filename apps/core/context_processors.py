import os

def firebase_config_context(request):
    """
    Injeta a configuração pública do Firebase em todos os templates.
    Valores provêm do arquivo .env ou variáveis de ambiente.
    """
    return {
        'FIREBASE_CONFIG': {
            'apiKey': os.getenv('FIREBASE_API_KEY', 'AIzaSyDyTc2EZztDP72Ssuzt_DHFjUDYzZmegas'),
            'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN', 'portal-igreja-e6a66.firebaseapp.com'),
            'projectId': os.getenv('FIREBASE_PROJECT_ID', 'portal-igreja-e6a66'),
            'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET', 'portal-igreja-e6a66.firebasestorage.app'),
            'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID', '1013927945766'),
            'appId': os.getenv('FIREBASE_APP_ID', '1:1013927945766:web:76879218b1e6ac3e2fa8e7'),
        },
        'FIREBASE_VAPID_KEY': os.getenv('FIREBASE_VAPID_KEY', ''),
    }
