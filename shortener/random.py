# shortener/utils.py

import secrets
import string

def generate_unique_code(length=6):
    """Generate a random alphanumeric string of fixed length."""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))
