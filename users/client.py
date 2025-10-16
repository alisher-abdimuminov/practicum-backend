import requests


class HemisClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        authorize_url,
        access_token_url,
        resource_owner_url,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorize_url = authorize_url
        self.access_token_url = access_token_url
        self.resource_owner_url = resource_owner_url


    def get_access_token(self, auth_code):
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": auth_code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }
        response = requests.post(self.access_token_url, data=payload)

        try:
            return response.json()
        except Exception as e:
            print("access_token:", e)
            return {}

    def get_user_details(self, access_token):
        response = requests.get(
            self.resource_owner_url, headers={"Authorization": f"Bearer {access_token}"}
        )
        try:
            return response.json()
        except Exception as e:
            print("user_details:", e)
            return None
