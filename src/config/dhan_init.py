from dhanhq import dhanhq

client_id = '1000700713'
client_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzMwNzMzMTY2LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTAwMDcwMDcxMyJ9.lwYD1BC_sadcqPZJgMXGVfwxhuG9jvz9buTn02RkK0dXxUUtbWeTDE2bMjpAeMtPIRSwi8P2jFpmbMas9GmpYw'

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