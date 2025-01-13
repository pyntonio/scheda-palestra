# mail_config.py
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

class EmailConfig:
    MAIL_USERNAME = "tuo-email@example.com"
    MAIL_PASSWORD = "tuo-password-email"
    MAIL_FROM = "tuo-email@example.com"
    MAIL_PORT = 587
    MAIL_SERVER = "smtp.example.com"
    MAIL_USE_TLS = True

# Configurazione aggiornata per Pydantic v2
conf = ConnectionConfig(
    MAIL_USERNAME=EmailConfig.MAIL_USERNAME,
    MAIL_PASSWORD=EmailConfig.MAIL_PASSWORD,
    MAIL_FROM=EmailConfig.MAIL_FROM,
    MAIL_PORT=EmailConfig.MAIL_PORT,
    MAIL_SERVER=EmailConfig.MAIL_SERVER,
    USE_TLS=EmailConfig.MAIL_USE_TLS,  # Usa il parametro 'USE_TLS' al posto di 'STARTTLS'
    SSL_TLS=None  # Se non usi SSL, lascialo come None
)

fm = FastMail(conf)
