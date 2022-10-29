"""
blocklist.py

This file just contains the blocklist of the JWT tokens. It is used by the JWTManager to check if a token is in the
blocklist or not. If it is, the token is invalid and the user is not allowed to access the protected routes.
"""

BLOCKLIST = set()