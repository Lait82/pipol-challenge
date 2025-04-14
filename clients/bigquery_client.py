import os
from google.cloud import bigquery
from google.oauth2 import service_account

def get_client() -> bigquery.Client:

    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    return client