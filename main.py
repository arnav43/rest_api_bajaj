from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import re

app = FastAPI()

# Your details
FULL_NAME = "arnav_sinha"
DOB = "04012003"
USER_ID = f"{FULL_NAME}_{DOB}"
EMAIL = "arnavsinha4334@gmail.com"
ROLL_NUMBER = "22BCE1736"

class InputModel(BaseModel):
    data: List[str]

def is_integer(value: str) -> bool:
    """Check if the value is an integer (string or int)."""
    if isinstance(value, int):
        return True
    if isinstance(value, str):
        return re.fullmatch(r"[+-]?\d+", value) is not None
    return False

def alternate_caps(text: str) -> str:
    """Return the string with alternating caps."""
    result = []
    upper = True
    for ch in text:
        result.append(ch.upper() if upper else ch.lower())
        upper = not upper
    return "".join(result)

@app.post("/bfhl")
async def bfhl_api(input: InputModel):
    try:
        data = input.data
        even_numbers, odd_numbers, alphabets, specials = [], [], [], []
        sum_numbers = 0
        alpha_chars = []

        for item in data:
            if is_integer(item):
                num = int(item)
                sum_numbers += num
                if num % 2 == 0:
                    even_numbers.append(str(num))
                else:
                    odd_numbers.append(str(num))
            elif isinstance(item, str) and item.isalpha():
                alphabets.append(item.upper())
                alpha_chars.extend(item)
            else:
                specials.append(str(item))

        # Build concat string from reversed alphabets with alternating caps
        alpha_chars.reverse()
        concat_string = alternate_caps("".join(alpha_chars))

        return {
            "is_success": True,
            "user_id": USER_ID,
            "email": EMAIL,
            "roll_number": ROLL_NUMBER,
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": specials,
            "sum": str(sum_numbers),
            "concat_string": concat_string,
        }

    except Exception as e:
        return {"is_success": False, "error": str(e)}
