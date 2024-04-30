import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from urllib.parse import urlparse 
import tldextract

class SitemapAPI:
    def gsc_auth(scopes):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        file_path=os.path.join(os.path.dirname(__file__), ".." , "jsonFiles" , "token.json")
        if os.path.exists(file_path):
            creds = Credentials.from_authorized_user_file(file_path, scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', scopes)
                creds = flow.run_local_server(port=0)

        service = build('webmasters', 'v3', credentials=creds)

        return service
    
    def extract_domain_part(url):
        extracted = tldextract.extract(url)
        # Etki alanı adını ve üst seviye alan adını birleştir
        domain_part = "{}.{}".format(extracted.domain, extracted.suffix)
        print(domain_part)
        return domain_part
        
    def run_api(feedpath:str):
        scopes = ['https://www.googleapis.com/auth/webmasters']
        service = SitemapAPI.gsc_auth(scopes)
        site=f"sc-domain:{SitemapAPI.extract_domain_part(feedpath)}"

        service.sitemaps().submit(siteUrl=site, feedpath=feedpath).execute() 

if __name__=="__main__":
    SitemapAPI.run_api("https://secim.posta.com.tr/posta-sp/haber")