from passlib.hash import pbkdf2_sha256

def encrypt(value):
    return pbkdf2_sha256.hash(value)

def verify(valueIn, valueCheck):
    return pbkdf2_sha256.verify(valueIn, valueCheck)