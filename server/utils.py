import hashlib
from os import getenv


def sign_verificator(data):
    if data.get('cryptocurrencyapi.net') < 3:
        raise SignVerificationException('CryptoCurrencyAPI version is outdated.')

    received_sign = data['sign']
    del data['sign']
    sorted_data = dict(sorted(data.items(), key=lambda x: x[0]))
    sorted_data = [str(value) for value in sorted_data.values()]

    encoded_api_key = hashlib.md5(getenv("CRYPTOCURRENCY_TOKEN").encode()).hexdigest()
    sorted_data.append(encoded_api_key)
    message = ':'.join(sorted_data)
    sign = hashlib.sha1(message.encode()).hexdigest()

    if sign == received_sign:
        return True
    else:
        return False


class SignVerificationException(Exception):
    pass
