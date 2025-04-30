import requests
from requests_oauthlib import OAuth1
import config
def fetch_files_from_netsuite():
    try:
        restletUrl = config.NETSUITE["restlet_url"] 
        
        auth = OAuth1(
            client_key=config.NETSUITE["consumer_key"],
            client_secret=config.NETSUITE["consumer_secret"],
            resource_owner_key=config.NETSUITE["token_id"],
            resource_owner_secret=config.NETSUITE["token_secret"],
            signature_method=config.NETSUITE["signature_method"],
            realm=config.NETSUITE["account"]
        )

        headers = {
            "Content-Type": config.NETSUITE["content_type"],
            "Accept": config.NETSUITE["content_type"],
        }

        response = requests.get(restletUrl, auth=auth, headers=headers)

        fileLinks = []
        baseUrl = config.NETSUITE["base_url"]
        fileDetails = response.json().get('data', []) 

        for fileDetail in fileDetails:
            folder_name = fileDetail.get('folder', '').lower()
            file_name = fileDetail.get('name', '').lower()
            if any(keyword in folder_name for keyword in config.NETSUITE["folder_names"]):
                continue
            if file_name in config.NETSUITE["file_names"]:
                continue
            fileUrl = fileDetail.get('url')
            if not fileUrl:
                continue
            fullUrl = baseUrl + fileUrl
            
            fileLinks.append([fullUrl, fileDetail.get('name')])

        return fileLinks

    except Exception as e:
        raise e    