"""
Purpose: Verify the Supabase-issued JWT on incoming requests and expose the
authenticated user's id to route handlers.
"""

import os
import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]

# Supabase signs access tokens with an asymmetric key pair (ES256/RS256) and
# publishes the matching public keys at the project's JWKS endpoint. PyJWKClient
# fetches and caches them, selecting the right key via the token's "kid" header.
_jwks_client = PyJWKClient(f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json")

# Parses the "Authorization: Bearer <token>" header; auto-401s if it's missing
bearer_scheme = HTTPBearer()
optional_bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
  credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
  """
  Validate the access token and return the Supabase user id (the 'sub' claim).
  Raises 401 if the token is missing, expired, or tampered with.
  """
  token = credentials.credentials

  try:
      signing_key = _jwks_client.get_signing_key_from_jwt(token)
      payload = jwt.decode(
          token,
          signing_key,
          algorithms=["ES256", "RS256"],  # Supabase asymmetric signing algorithms
          audience="authenticated",       # Supabase sets aud="authenticated" for logged-in users
      )
  except jwt.PyJWTError:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid or expired token",
      )

  user_id = payload.get("sub")
  if not user_id:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Token missing subject",
      )

  return user_id


def get_optional_current_user(
  credentials: HTTPAuthorizationCredentials | None = Depends(optional_bearer_scheme),
) -> str | None:
  """
  Validate an optional access token and return the Supabase user id when
  present. Returns None when the request is anonymous.
  """
  if credentials is None:
      return None

  return get_current_user(credentials)
