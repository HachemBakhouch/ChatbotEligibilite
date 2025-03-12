import os

class Config:
    # Configuration du serveur
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5004))
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Configuration de la base de données (pour usage futur)
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///decision_tree.db')