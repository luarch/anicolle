class Config:
    DATABASE = "anicolle.db"
    AUTH_TOKEN = "test"
    DEBUG = True
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = "7777"


class ProductionConfig(Config):
    AUTH_TOKEN = "YOUR_TOKEN"
    DEBUG = False
    SERVER_HOST = "0.0.0.0"
    SERVER_PORT = "7777"


config = {
    'default': Config,
    'production': ProductionConfig
}
