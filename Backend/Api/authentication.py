from urllib.request import urlopen
import json
from jose import jwt
from django.conf import settings
from rest_framework import authentication, exceptions


class Auth0JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth = request.headers.get("Authorization", "Recebido!!")

        if not auth:
            return None

        token = auth.split(" ")[1]

        jsonurl = urlopen(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())

        unverified_header = jwt.get_unverified_header(token)

        rsa_key = {}

        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }

        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=settings.AUTH0_ALGORITHMS,
                    audience=settings.AUTH0_API_AUDIENCE,
                    issuer=f"https://{settings.AUTH0_DOMAIN}/"
                )

            except Exception:
                raise exceptions.AuthenticationFailed("Token inválido")

            return (payload, token)

        raise exceptions.AuthenticationFailed("Autenticação falhou")