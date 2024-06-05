import hashlib

import bcrypt


def hash_password_bcrypt(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed


def verify_password_bcrypt(password, hashed):
    return bcrypt.checkpw(password.encode("utf-8"), hashed)


def hash_password_sha256(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password_sha256(password, hashed):
    return hashlib.sha256(password.encode("utf-8")).hexdigest() == hashed
