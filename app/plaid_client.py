import os
import plaid
from plaid.api import plaid_api


PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")

environments = {
    "sandbox": plaid.Environment.Sandbox,
    "development": plaid.Environment.Development,
    "production": plaid.Environment.Production
}


host = environments.get(PLAID_ENV, plaid.Environment.Sandbox)

configuration = plaid.Configuration(
    host=host,
    api_key={
        "clientId": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET"),
        "plaidVersion": "2020-09-14"
    }
)

api_client = plaid.ApiClient(configuration)

client = plaid_api.PlaidApi(api_client)