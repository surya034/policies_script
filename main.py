import traceback
from netsuite_api import fetch_files_from_netsuite
from sharepoint_api import get_access_token, clear_sharepoint_folder, upload_files_to_sharepoint
from send_error_notification import send_error_notification
import config
import os

def run():

    log_file_path = None
    try:
        log_dir = config.SHAREPOINT["log_dir"]
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, "chatbot_log.txt") 

        with open(log_file_path, "a") as log_file:
            log_file.write("started the process \n")
        
        print("Authenticating to SharePoint...")
        token = get_access_token()

        print("Fetching files from NetSuite...")
        files = fetch_files_from_netsuite()
    
        print("Clearing old files...")
        clear_sharepoint_folder(token, log_file_path)

        print("Uploading new files...")
        upload_files_to_sharepoint(token, files,log_file_path)
    
        with open( log_file_path, "a") as log_file:
            log_file.write("finished uploading files\n")
        print("Upload complete. Check the log file for details.")


    except Exception as e:
        send_error_notification(config.SHAREPOINT["from_email"], config.SHAREPOINT["password"], config.SHAREPOINT["to_emails"], 'Error while running filesupload script.','Error details:\n' + str(e) + "\n" + traceback.format_exc() + "\n")
        with open(log_file_path, "a") as log_file:
            log_file.write(f"Error: {str(e)}\n")
            log_file.write(traceback.format_exc() + "\n")
if __name__ == "__main__":
    run()