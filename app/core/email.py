# app/core/email.py
import aiosmtplib
from email.mime.application import MIMEApplication # Pour les PDF
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import ssl
from typing import Optional, List, Tuple

async def send_email(
    to: str,
    subject: str,
    body: str, # Texte brut
    html_body: Optional[str] = None,
    attachments: Optional[List[Tuple[str, bytes, str]]] = None # (filename, data, mimetype)
):
    message = MIMEMultipart()
    message["From"] = settings.SMTP_FROM
    message["To"] = to
    message["Subject"] = subject

    # Attacher le corps en texte brut
    message.attach(MIMEText(body, "plain"))

    # Attacher le corps HTML s'il est fourni
    if html_body:
        message.attach(MIMEText(html_body, "html"))

    # Attacher les fichiers
    if attachments:
        for filename, file_data, mimetype in attachments:
            _, subtype = mimetype.split('/', 1)
            part = MIMEApplication(file_data, Name=filename, _subtype=subtype)
            part['Content-Disposition'] = f'attachment; filename="{filename}"'
            message.attach(part)

    tls_context = ssl.create_default_context()
    tls_context.check_hostname = False
    tls_context.verify_mode = ssl.CERT_NONE

    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        use_tls=True, # Souvent True pour le port 587, False pour 465 (SMTPS)
        # start_tls=True, # Si le serveur passe à TLS après la connexion (souvent pour le port 587)
        # Décommentez start_tls=True et commentez use_tls=True si votre serveur SMTP le requiert.
        # Si use_tls=True et le port est 465 (SMTPS), la connexion est TLS dès le début.
        # Si le port est 587, c'est souvent une connexion non chiffrée qui est mise à niveau vers TLS via STARTTLS.
        # aiosmtplib choisit souvent correctement, mais il est bon de le savoir.
        # La configuration actuelle avec use_tls=True est typique pour STARTTLS sur le port 587.
        # Si vous utilisez le port 465 (SSL/TLS direct), use_tls devrait être True et start_tls False.
        tls_context=tls_context,
    )