from datetime import datetime, timedelta, timezone
import jwt
import os
import logging

logging.basicConfig(level=logging.DEBUG)

# Create a secret key constant variable
SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key'

def encode_token(customer_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': customer_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    logging.debug(f"Encoded token: {token}")
    return token

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        now = datetime.now(timezone.utc).timestamp()
        if payload.get('exp') < now:
            print('Token has expired')
            return None
        # return customer_id
        logging.debug(f"Decoded payload: {payload}")
        return payload.get('sub')
    except jwt.ExpiredSignatureError:
        print('Token has expired')
        return None
    except jwt.InvalidTokenError:
        print('Invalid token')
        return None
    except Exception as e:
        print(f"A error occurred: {e}")
        return None