
import requests
import config
import mimetypes
import traceback
from msal import ConfidentialClientApplication

def get_access_token():
    try:
        app = ConfidentialClientApplication(
            client_id=config.SHAREPOINT["client_id"],
            client_credential=config.SHAREPOINT["client_secret"],
            authority=config.SHAREPOINT["authority_url"]
        )
        token = app.acquire_token_for_client(scopes=[config.NETSUITE["token_url"]])
        
        return token["access_token"]
        
    except Exception as e:
        raise e

def clear_sharepoint_folder(token, log_file_path):
    try:
        # List items in the folder
        list_url = config.SHAREPOINT["list_url"]
        list_response = requests.get(list_url, headers={"Authorization": f"Bearer {token}"})

        items = list_response.json().get("value", [])
        for item in items:
            item_id = item["id"]
            del_url = f"{config.SHAREPOINT['del_url']}/{item_id}"
            del_response = requests.delete(del_url, headers={"Authorization": f"Bearer {token}"})

            if del_response.status_code != 204:
                with open(log_file_path, "a") as log_file:
                    log_file.write(f"Failed to delete item {item_id}:\n")
                    log_file.write(f"Status Code: {del_response.status_code}\n")
                    log_file.write(f"Response: {del_response.text}\n")
    except Exception as e:
        raise e

def upload_files_to_sharepoint(token, file_urls, log_file_path):
    try:
        for file_url, name in file_urls:
            try:
                print(f"Downloading: {name}")
                file_response = requests.get(file_url)

                if file_response.status_code != 200:
                    with open(log_file_path, "a") as log_file:
                        log_file.write(f"[DOWNLOAD ERROR] {file_url} — Status Code: {file_response.status_code}\n\n")
                    continue

                file_bytes = file_response.content

                # Detect content type based on file extension
                content_type, _ = mimetypes.guess_type(name)
                if not content_type:
                    content_type = "application/octet-stream"

                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": content_type
                }

                upload_url = (
                  config.SHAREPOINT["upload_url"].format(name=name)
                )

                print(f"Uploading to: {upload_url}")
                upload_response = requests.put(upload_url, headers=headers, data=file_bytes)

                if upload_response.status_code in [200, 201]:
                    print(f"Uploaded: {name}")
                else:
                    with open(log_file_path, "a") as log_file:
                        log_file.write(f"[UPLOAD ERROR] {name} — Status Code: {upload_response.status_code}\n")
                        log_file.write(f"Response: {upload_response.text}\n\n")

            except Exception as e:
                with open(log_file_path, "a") as log_file:
                    log_file.write(f"[EXCEPTION] while processing {file_url}:\n")
                    log_file.write(f"Error: {str(e)}\n")
                    log_file.write(traceback.format_exc() + "\n")
    except Exception as e:
        raise e