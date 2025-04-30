from dotenv import load_dotenv
import os

load_dotenv()

NETSUITE = {
    "account": os.getenv("NETSUITE_ACCOUNT_ID"),
    "consumer_key": os.getenv("NETSUITE_CONSUMER_KEY"),
    "consumer_secret": os.getenv("NETSUITE_CONSUMER_SECRET"),
    "token_id": os.getenv("NETSUITE_TOKEN_ID"),
    "token_secret": os.getenv("NETSUITE_TOKEN_SECRET"),
    "restlet_url": os.getenv("NETSUITE_URL"),
    "signature_method": os.getenv("SIGNATURE_METHOD"),
    "base_url": os.getenv("BASE_URL"),
    "folder_names": [name.strip() for name in os.getenv("FOLDER_NAMES", "").split(",")],
    "file_names": [name.strip() for name in os.getenv("FILE_NAMES", "").split(",")],
    "token_url": os.getenv("TOKEN_URL"),
    "content_type": os.getenv("CONTENT_TYPE"),
}

SHAREPOINT = {
    "tenant_id": os.getenv("TENANT_ID"),
    "client_id": os.getenv("CLIENT_ID"),
    "client_secret": os.getenv("CLIENT_SECRET"),
    "authority_url": os.getenv("AUTHORITY_URL"),
    "log_dir": os.getenv("LOG_DIR"),
    "list_url": os.getenv("LIST_URL"),
    "del_url": os.getenv("DEL_URL"),
    "upload_url": os.getenv("UPLOAD_URL"),
    "from_email": os.getenv("FROM_EMAIL"),
    "password": os.getenv("EMAIL_PASSWORD"),
    "to_emails": [name.strip() for name in os.getenv("TO_EMAIL", "").split(",")],
}
