import re


def stripe_error(e):
    return re.sub(r"Request [^:]+:", "", str(e)).strip()