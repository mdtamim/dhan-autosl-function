from dhanhq import dhanhq
from google.cloud import secretmanager


def get_client_token():
    # Create a Secret Manager client
    client = secretmanager.SecretManagerServiceClient()

    # Define the name of the secret
    secret_name = "projects/dhan-algo/secrets/dhan-client-token/versions/latest"

    # Access the secret version
    response = client.access_secret_version(request={"name": secret_name})

    # Get the token from the secret's payload
    token = response.payload.data.decode("UTF-8")

    return token

def get_client_id():
    # Create a Secret Manager client
    client = secretmanager.SecretManagerServiceClient()

    # Define the name of the secret
    secret_name = "projects/dhan-algo/secrets/dhan-client-id/versions/latest"

    # Access the secret version
    response = client.access_secret_version(request={"name": secret_name})

    # Get the token from the secret's payload
    client_id = response.payload.data.decode("UTF-8")

    return client_id

def init_dhan():
    # Initialize Dhan SDK
    return dhanhq(get_client_id,get_client_token())

url = "https://api.dhan.co/v2/marketfeed/ltp"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "access-token": get_client_token(),
    "client-id": get_client_id()
}