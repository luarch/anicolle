class Config:
    DATABASE = "anicolle.db"
    AUTH_USER = "demo"
    AUTH_PASSWD = "password"
    DEBUG = True
    SERVER_HOST = "127.0.0.1"
    SERVER_PORT = "7777"

class ProductionConfig(Config):
    AUTH_USER = "YOUR_USER"
    AUTH_PASSWD = "YOUR_PASSWORD"
    DEBUG = False
    SERVER_HOST = "0.0.0.0"

config = {
    'default': Config,

    'production': ProductionConfig
}
