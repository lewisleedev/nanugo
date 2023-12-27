import random, string

__docformat__ = "google"


def get_hash(hash_len: int = 6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=hash_len))
