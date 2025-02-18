# !pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import os.path
import base64
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from bs4 import BeautifulSoup 

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
class Gmail:
    def __init__(self, user_id):
        self.user_id = user_id

    def authenticate_gmail(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('google_cloud_credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return build('gmail', 'v1', credentials=creds)

    def extract_email_body(self, payload):
        """Extracts and decodes the email body from the payload."""
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    body_data = part['body'].get('data', '')
                    body = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
                    break  # Take only the first plain-text part
                elif part['mimeType'] == 'text/html':
                    body_data = part['body'].get('data', '')
                    html_body = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
                    body = BeautifulSoup(html_body, 'html.parser').get_text()  # Convert HTML to plain text
        else:
            body_data = payload['body'].get('data', '')
            body = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')

        return body.strip()


    def search_job_applications(self):
        service = self.authenticate_gmail()

        query = """(subject:(application OR applied OR "job application" OR resume OR interview OR position OR recruiter OR "career opportunity") 
                    OR body:(application OR resume OR recruiter OR hiring OR interview OR opportunity OR "job offer"))"""
        
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])

        email_data = []

        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            headers = msg_data['payload']['headers']

            # Extract header values
            email_from = next((header['value'] for header in headers if header['name'] == 'From'), 'Unknown')
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')

            # Extract email body
            body = self.extract_email_body(msg_data['payload'])

            email_data.append({
                'user_id': self.user_id,  
                'from': email_from,
                'subject': subject,
                'body': body
            })

        return pd.DataFrame(email_data)