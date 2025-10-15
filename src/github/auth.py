import base64
import time

import jwt
import requests
from cryptography.hazmat.primitives import serialization

from settings import Settings


class GithubAuthProvider:
    def __init__(self, app_id=None, private_key=None, install_id=None):
        if not app_id:
            app_id = Settings().app_id
        if not private_key:
            private_key = Settings().private_key
        if not install_id:
            install_id = Settings().install_id

        private_key_bytes = base64.b64decode(private_key)

        private_key = serialization.load_pem_private_key(
            private_key_bytes,
            password=None,
        )

        # generate JWT (max 10 min validity)
        now = int(time.time())
        payload = {
            "iat": now - 60,  # issued at (backdate 1 min for clock skew)
            "exp": now + (9 * 60),  # expires after 9 minutes
            "iss": app_id,  # GitHub App ID
        }

        jwt_token = jwt.encode(payload, private_key, algorithm="RS256")

        # exchange JWT for installation access token
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github+json",
        }
        url = f"https://api.github.com/app/installations/{install_id}/access_tokens"
        resp = requests.post(url, headers=headers)
        resp.raise_for_status()
        self.token = resp.json()["token"]

    def get_token(self):
        return self.token
