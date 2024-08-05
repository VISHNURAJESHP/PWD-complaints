from random import randint

def generate_otp():
    """
    Generate a random OTP (One Time Password) consisting of 6 digits.
    """
    return ''.join([str(randint(0, 9)) for _ in range(6)])
