from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

def make_token():
    # Your client credentials
    client_id = 'eec7d04e-621b-4bf8-8a92-10fb0dea8083'
    client_secret = '1fqBm3kP5hQhT57i2Sq4FRMJyxD0qU8G'

    # Create a session
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)

    # Get token for the session
    token = oauth.fetch_token(token_url='https://services.sentinel-hub.com/auth/realms/main/protocol/openid-connect/token',
                              client_secret=client_secret, include_client_id=True)

    # All requests using this session will have an access token automatically added
    resp = oauth.get("https://services.sentinel-hub.com/configuration/v1/wms/instances")
    print(resp.content)

    # eec7d04e-621b-4bf8-8a92-10fb0dea8083
    # 1fqBm3kP5hQhT57i2Sq4FRMJyxD0qU8G
    return token['access_token']

#print(make_token())