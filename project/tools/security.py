import base64
import calendar
import datetime
import hashlib

import jwt
from flask import current_app, request, abort

from project.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(password)).decode('utf-8')


def get_hash(password):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),  # Convert the password to bytes
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    ).decode("utf-8", "ignore")


def get_data_from_token():
    try:
        token = jwt.decode(request.headers['Authorization'].split('Bearer ')[-1], key=current_app.config['SECRET_KEY'], algorithms=current_app.config['ALGORITHM'])
    except Exception as e:
        abort(401)
    return token


def auth_required(func):
    def wrapped(*args, **kwargs):
        get_data_from_token()
        return func(*args, **kwargs)

    return wrapped


def create_acc_token(data):
    sec30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data['exp'] = calendar.timegm(sec30.timetuple())
    access_token = jwt.encode(data, key=current_app.config['SECRET_KEY'], algorithm=current_app.config['ALGORITHM'])
    return access_token


def create_refr_token(data):
    d130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data['exp'] = calendar.timegm(d130.timetuple())
    refresh_token = jwt.encode(data, key=current_app.config['SECRET_KEY'], algorithm=current_app.config['ALGORITHM'])
    return refresh_token


# TODO: [security] Описать функцию compose_passwords(password_hash: Union[str, bytes], password: str)
