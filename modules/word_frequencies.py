from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from flask import request
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://remote:BIw883k8@212.31.2.93/monitor",
                        connect_args={"charset": "utf8mb4"}, echo=False)
class WordFrequencies:

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
                flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes)
                creds = flow.run_local_server(port=0)


        #kullanıcıdan girilen verileri alır
        service = build('searchconsole', 'v1', credentials=creds)
        start_date=request.form.get("start_date")
        end_date=request.form.get("end_date")
        row_limit=request.form.get("row_limit")
        platform=request.form.get("platform")
        
        requests={
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": ["page"],
            "type": "discover",
            "rowLimit": row_limit
            }
        gsc_search_analytics = service.searchanalytics().query(siteUrl=f'sc-domain:{platform}',body=requests).execute()
        report = pd.DataFrame(data=gsc_search_analytics['rows'])

        report.to_sql('data',engine,if_exists="replace",index=False)

    def calculate_word_frequencies(n: int):
        data = pd.read_sql_table("data", engine) 
        dict_address = {}
        for address in data["keys"]:
            address = str(address).split("/")[-1].split("-") #Keşfetten çekilen adresin
            #son son kısmını alır.
            for word in address:
                if len(word)>=4 and not word.isdigit():
                    if word in dict_address:
                        dict_address[word]+=1
                    else:
                        dict_address[word]=1
        #Büyükten küçüğe en çok tekrar eden "n" kelime olan listeye dönüşür.
        sorted_list = sorted(dict_address.items(), key=lambda t: t[1], reverse=True)[:n]
        df_address = pd.DataFrame(data=sorted_list, columns=["Kelimeler", "Tekrar Sayilari"])
        df_address.to_sql("word_frequencies", engine, if_exists="replace", index=False)
        return df_address

if __name__=="__main__":
    WordFrequencies.gsc_auth(['https://www.googleapis.com/auth/webmasters'])