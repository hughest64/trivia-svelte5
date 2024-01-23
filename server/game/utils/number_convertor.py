# number_convertor.py
"""
A utiltiy class for converting strings to numbers.
"""


class NumberConversionException(Exception):
    default_msg = "An error occured during converstion"

    def __init__(self, message=None) -> None:
        self.message = message or self.default_msg

    def __str__(self):
        return self.message


class NumberConvertor:
    conversion_map = {
        "hundred": 100,
        "thousand": 1000,
        "million": 1000000,
        "billion": 1000000000,
        "trillion": 1000000000000,
    }

    @classmethod
    def convert_to_number(cls, answer: str) -> float:
        stripped = answer.replace(",", "").split(" ")

        # in the case of an actual number
        if len(stripped) == 1:
            return float(stripped[0])

        # too many split parts (spaces)
        if len(stripped) > 2:
            raise NumberConversionException(
                f"cannot convert {answer} to a number, too many parts"
            )

        number_string, suffix = stripped

        # a number that is not handled
        if not suffix.lower() in cls.conversion_map:
            raise NumberConversionException(f"could not convert suffix '{suffix}'")

        return float(number_string) * cls.conversion_map[suffix.lower()]
