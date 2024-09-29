import jwt
from jwt import PyJWKClient
from typing import Dict, Any
from logging import getLogger

logger = getLogger(__name__)


class Auth:
    def __init__(self, issuer: str, audience: str, algorithm: str = "RS256"):
        self.issuer = issuer
        self.audience = audience
        self.algorithm = algorithm
        self.jwks_client = PyJWKClient(f"{self.issuer}.well-known/jwks.json")

    def _get_signing_key(self, token: str) -> str:
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token).key
        except jwt.exceptions.PyJWKClientError as e:
            logger.error(f"JWK Client Error: {e}")
            raise ValueError("Token verification failed")
        except jwt.exceptions.DecodeError as e:
            logger.error(f"Decode Error: {e}")
            raise ValueError("Invalid token")
        return signing_key

    def decode_jwt(self, token: str) -> Dict[str, Any]:
        try:
            signing_key = self._get_signing_key(token)
            verified_payload = jwt.decode(
                token,
                signing_key,
                algorithms=[self.algorithm],
                audience=self.audience,
                issuer=self.issuer,
            )
            return verified_payload
        except jwt.ExpiredSignatureError:
            logger.error("Token has expired")
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid Token: {e}")
            raise ValueError("Invalid token")
        except Exception as e:
            logger.error(f"Token decoding error: {e}")
            raise ValueError(f"Token decoding error: {e}")
