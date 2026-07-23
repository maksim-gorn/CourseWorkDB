import os

# путь к папке с проектом
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# путь к файлу sqlite базы данных
DB_PATH = os.path.join(os.path.dirname(BASE_DIR), 'shop_manager.db')


class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dev-secret-key'