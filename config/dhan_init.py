from dhanhq import dhanhq
import os

#TODO: Dont commit
client_id = 'XXX'
client_token = 'XXX'

def init_dhan():
    # Initialize Dhan SDK
    return dhanhq(client_id,client_token)

url = "https://api.dhan.co/v2/marketfeed/ltp"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "access-token": client_token,
    "client-id": client_id
}