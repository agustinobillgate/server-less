import sqlalchemy as sa
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import aliased, load_only, make_transient
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import BinaryExpression, Cast
from sqlalchemy import not_, func, text, Function, and_
from sqlalchemy.dialects.postgresql import CITEXT
import datetime
import re
import string
from time import gmtime, strftime

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

def num_to_string(value, fmt=""):
    fmt = (fmt or "").strip().strip("-")
    if fmt == "":
        return "" if value is None else str(value)

    if set(fmt) <= {">", "-"} and "9" not in fmt and "." not in fmt and "," not in fmt:
        width = len(fmt)
        s = str(value)
        if fmt.startswith("-"):
            sign = "-" if (isinstance(value, (int, float, Decimal)) and Decimal(str(value)) < 0) or (isinstance(value, str) and value.startswith("-")) else " "
            magnitude = s[1:] if str(s).startswith("-") else s
            rest = width - 1
            return sign + magnitude.rjust(rest)
        else:
            return str(value).rjust(width)

    is_numeric_pattern = any(ch in fmt for ch in "9>.,-")
    if not is_numeric_pattern:
        return str(value).rjust(len(fmt))

    if "." in fmt:
        int_pat, frac_pat = fmt.split(".", 1)
    else:
        int_pat, frac_pat = fmt, ""

    sign_slot = int_pat.startswith("-")
    if sign_slot:
        int_pat_body = int_pat[1:]
    else:
        int_pat_body = int_pat

    try:
        dec = Decimal(str(value))
    except (InvalidOperation, ValueError):
        total_width = len(fmt.replace(",", ""))
        return str(value).rjust(total_width)

    negative = dec < 0
    dec = -dec if negative else dec

    frac_places = sum(1 for ch in frac_pat if ch in ("9", ">"))
    q = Decimal(1).scaleb(-frac_places)
    if frac_places > 0:
        dec = dec.quantize(q, rounding=ROUND_HALF_UP)
    else:
        dec = dec.quantize(Decimal(1), rounding=ROUND_HALF_UP)

    int_digits = f"{int(dec):d}"
    frac_digits = ""
    if frac_places > 0:
        frac_val = (dec - int(dec)).scaleb(frac_places)
        frac_val = abs(frac_val)
        frac_digits = f"{int(frac_val):0{frac_places}d}"

    pat_chars = list(int_pat_body)
    out_int_chars = []
    src = list(int_digits)
    src_i = len(src) - 1

    for i in range(len(pat_chars) - 1, -1, -1):
        ch = pat_chars[i]
        if ch == ",":
            if src_i >= 0:
                out_int_chars.append(",")
            else:
                out_int_chars.append(" ")
            continue

        if src_i >= 0:
            d = src[src_i]
            src_i -= 1
            out_int_chars.append(d)
        else:
            if ch == "9":
                out_int_chars.append("0")
            elif ch == ">":
                out_int_chars.append(" ")
            else:
                out_int_chars.append(ch)

    out_int = "".join(reversed(out_int_chars))

    if src_i >= 0:
        overflow = "".join(src[:src_i + 1])
        out_int = overflow + out_int

    out_frac = "." + frac_digits if frac_places > 0 else ""

    if sign_slot:
        sign_char = "-" if negative else " "
        out = sign_char + out_int + out_frac
    else:
        out = out_int + out_frac
        if negative:
            first_digit_idx = None
            for i, c in enumerate(out_int):
                if c.isdigit():
                    first_digit_idx = i
                    break
            if first_digit_idx is None:
                out = "-" + out
            else:
                place = None
                for i in range(first_digit_idx - 1, -1, -1):
                    if out_int[i] == " ":
                        place = i
                        break
                if place is not None:
                    out_int = out_int[:place] + "-" + out_int[place + 1:]
                    out = out_int + out_frac
                else:
                    out = "-" + out

    return out

def is_sqlalchemy_data(input_data):
    return (isinstance(input_data, InstrumentedAttribute) or 
            isinstance(input_data, BinaryExpression) or 
            isinstance(input_data, Cast) or 
            isinstance(input_data, Function))

def to_string(input_value, format_spec=""):
    if is_sqlalchemy_data(input_value):    
        return sa.cast(input_value, sa.String)

    if type(input_value) == datetime.timedelta:
        input_value = input_value.days

    if format_spec == "":
        if type(input_value) == datetime.date:
            date_format = "%m/%d/%y"
            formatted = input_value.strftime(date_format)
            return formatted
        
        return string(input_value)

    clean_format_spec = format_spec.strip(" ")

    if clean_format_spec.startswith("x("):
        width = int(clean_format_spec[2:-1])
        formatted = f"{input_value:<{width}}"
    elif (any(char.isdigit() for char in format_spec)):
        return num_to_string(input_value, clean_format_spec)
        
    elif type(input_value) == bool:
        if input_value:
            formatted = clean_format_spec.split("/")[0]
        else:
            formatted = clean_format_spec.split("/")[1]
    elif '/' in clean_format_spec:
        date_format = clean_format_spec.replace("99/99/9999","%m/%d/%Y")
        date_format = date_format.replace("99/99/99","%m/%d/%y")
        if isinstance(input_value, datetime.datetime) or isinstance(input_value, datetime.date):
            formatted = input_value.strftime(date_format)
        else:
            formatted = input_value
    elif type(input_value) == int and re.match(".*[HMS].*",format_spec,re.IGNORECASE):
        clean_format_spec = clean_format_spec.replace("HH","H").replace("MM","M").replace("SS","S")
        clean_format_spec = clean_format_spec.replace("H","%H").replace("M","%M").replace("S","%S")
        formatted = strftime(clean_format_spec, gmtime(input_value))
    else:
        formatted = string(input_value)

    if " " in format_spec:
        formatted = format_spec.replace(format_spec.strip(" "),formatted)

    return formatted


def format_fixed_length(text: str, length: int, direction: str="left") -> str:
    """
    Docstring for format_fixed_length
    by: Oscar

    :param text: for input text to be formatted
    :type text: str
    :param length: for the desired fixed length of the output string
    :type length: int
    :param direction: for the direction of padding, either 'left' or 'right'
    :type direction: str (default to 'left')
    :return: formatted string with fixed length (either truncated or left padded with spaces)
    :rtype: str
    
    """
    if len(text) > length:
        return text[:length]
    else:
        if direction == "left":
            return text.ljust(length)
        elif direction == "right":
            return text.rjust(length)

def handling_negative(value, format):
    """
    Docstring for handling_negative
    by: Oscar
    
    :param value: for input integer value to be formatted considering negative handling
    :type value: int
    :param format: for the format string used in formatting the value
    :type format: str
    :return: formatted string considering negative handling
    :rtype: str
    """
    charNr  = len(format)
    if value < 0:
        return format_fixed_length(to_string(value, format).strip(), charNr, "right")
    else:
        format = format.replace("-", "")
        return format_fixed_length(to_string(value, format).strip(), charNr, "right")