import random


def generate_otp():
    digits = "0123456789"
    otp_length = 4
    otp = "".join(random.choice(digits) for _ in range(otp_length))
    return otp
