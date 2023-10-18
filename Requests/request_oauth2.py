from requests_oauthlib import OAuth2Session
from Resources  import utils as Utils

class MyOauth2:
    def access_token_get(self, client_id, client_secret, scope, redirect_uri, token):
        if token:
            if self._can_refresh_token(token) is True:
                token = self.token_refresh(client_id, client_secret, token)
                return token
            else:
                return token
        else:
            client = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
            authorization_url, state=client.authorization_url('https://accounts.spotify.com/authorize')
            print(' \n \n Por favor, visite esta URL e obtenha a URL callback? \n' + authorization_url)
            redirect_response = input('\n \nCole a redirect URL: ')
            token = client.fetch_token('https://accounts.spotify.com/api/token', authorization_response=redirect_response, client_secret=client_secret)
            return token

    def token_refresh(self, client_id, client_secret, token):
        extra = {'client_id': client_id, 'client_secret': client_secret, 'refresh_token': token['refresh_token']}
        oauth_refresh = OAuth2Session(client_id, token=token)
        new_token = oauth_refresh.refresh_token('https://accounts.spotify.com/api/token', **extra)
        return new_token

    def _can_refresh_token(self, token):
        if Utils.check_timestamp_is_old(token['expires_at']) is True:
            return True
        else:
            return False

        return True
