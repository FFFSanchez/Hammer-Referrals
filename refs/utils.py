import uuid
from random import randint


def generate_confirmation_code(amount_of_signs=4):
    code = ''.join(
        ["{}".format(randint(0, 9)) for _ in range(amount_of_signs)]
    )
    print(code)
    return code


def generate_ref_code(code_length=6):
    code = str(uuid.uuid4()).replace("-", "")[:code_length]
    print(code)

    return code
