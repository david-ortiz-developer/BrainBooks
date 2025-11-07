import jwt
from datetime import datetime, timedelta
from flask import current_app

class JWTAuthenticator:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.secret_key = app.config.get('JWT_SECRET_KEY')
        if not self.secret_key:
            raise RuntimeError('JWT_SECRET_KEY must be set in the application configuration')
        self.algorithm = app.config.get('JWT_ALGORITHM', 'HS256')
        self.expiration_time = app.config.get('JWT_EXPIRATION_TIME', 3600)  # 1 hour in seconds

    def encode_token(self, payload):
        """Generate a JWT token with the given payload."""
        payload.update({
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=self.expiration_time)
        })
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def decode_token(self, token):
        """Verify and decode the JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return 'Token has expired'
        except jwt.InvalidTokenError:
            return 'Invalid token'