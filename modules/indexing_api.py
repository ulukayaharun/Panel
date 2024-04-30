from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import os
from urllib.parse import urlparse 

class IndexAPI:

    def get_domain(url): 
        #https://www.example.com.tr/blabla ---> www.example.com.tr --> example dönüştürücü
        parsed_url = urlparse(url)
        domain =parsed_url.netloc
        domain=domain.split(".")
        return domain[1]

    def run_api(api_url):
        requests = {
            api_url:'URL_UPDATED',

        }
        JSON_KEY_FILE =os.path.join(os.path.dirname(__file__), ".." , "jsonFiles" , 
                                    f"{IndexAPI.get_domain(api_url)}.json")
        

        SCOPES = [ "https://www.googleapis.com/auth/indexing" ]
        ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

        # Authorize credentials
        credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)

        # Build service
        service = build('indexing', 'v3', credentials=credentials)

        def insert_event(_, response, exception):
            if exception is not None:
                print(exception)
            else:
                print(response)

        batch = service.new_batch_http_request(callback=insert_event)

        for url, api_type in requests.items():
            batch.add(service.urlNotifications().publish(
                body={"url": url, "type": api_type}))

        batch.execute()

if __name__=="__main__":
    #örnek link
    IndexAPI.run_api("https://www.hurriyet.com.tr/ekonomi/bakan-simsekten-siki-para-politikasi-mesaji-42438992")
