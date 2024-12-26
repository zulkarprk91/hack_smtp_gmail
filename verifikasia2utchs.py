import os
import base64
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import smtplib

# Definisikan cakupan untuk Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate():
    """Autentikasi OAuth2 dan dapatkan token akses."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)  # Ganti dengan file JSON Anda
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def send_email():
    """Kirim email menggunakan SMTP dan token OAuth2."""
    creds = authenticate()
    access_token = creds.token
    email_from = "your-email@gmail.com"
    email_to = "target-email@gmail.com"
    subject = "Test Email with OAuth2"
    body = "This is a test email sent using Gmail OAuth2."

    # Buat header dan isi pesan
    message = f"Subject: {subject}\n\n{body}"
    encoded_message = base64.urlsafe_b64encode(message.encode('utf-8')).decode('utf-8')

    # Kirim email menggunakan SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.ehlo()
            server.login(email_from, access_token)
            server.sendmail(email_from, email_to, message)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_email()
