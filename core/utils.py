import hashlib

from core.config import settings


def sign_verifier(data):
    if data.get('cryptocurrencyapi.net', 0) < 3:
        return False

    received_sign = data['sign']
    sorted_data = dict(sorted(data.items(), key=lambda x: x[0]))
    sorted_data = [str(value) for key, value in sorted_data.items() if key != 'sign']

    encoded_api_key = hashlib.md5(settings.CRYPTOCURRENCY_TOKEN.encode()).hexdigest()
    sorted_data.append(encoded_api_key)
    message = ':'.join(sorted_data)
    sign = hashlib.sha1(message.encode()).hexdigest()

    if sign == received_sign:
        return True
    else:
        return False


class SignVerificationException(Exception):
    pass
