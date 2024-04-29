import hashlib


def calculate_md5_hash(string):
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    hexadecimal_hash = md5_hash.hexdigest()
    return hexadecimal_hash
