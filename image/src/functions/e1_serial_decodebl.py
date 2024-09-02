from functions.additional_functions import *
import decimal
from datetime import date

def e1_serial_decodebl(serial_number:str):
    license_nr = 0
    valid_until = None
    case_id = 0
    parameter_int = 0
    valid_flag = False
    license_hex:str = ""
    valid_hex:str = ""
    case_hex:str = ""
    parameter_hex:str = ""
    valid_str:str = ""
    checksum:str = ""
    randomizer:str = ""
    the_serial:str = ""
    the_randomizer:str = ""
    the_checksum:str = ""
    i:int = 0


    db_session = local_storage.db_session

    def generate_output():
        nonlocal license_nr, valid_until, case_id, parameter_int, valid_flag, license_hex, valid_hex, case_hex, parameter_hex, valid_str, checksum, randomizer, the_serial, the_randomizer, the_checksum, i


        return {"license_nr": license_nr, "valid_until": valid_until, "case_id": case_id, "parameter_int": parameter_int, "valid_flag": valid_flag}

    def CharToInt(input_char:str):

        nonlocal license_nr, valid_until, case_id, parameter_int, valid_flag, license_hex, valid_hex, case_hex, parameter_hex, valid_str, checksum, randomizer, the_serial, the_randomizer, the_checksum, i


        return ord(input_char) - 65

    def IntToChar(input_int:int):

        nonlocal license_nr, valid_until, case_id, parameter_int, valid_flag, license_hex, valid_hex, case_hex, parameter_hex, valid_str, checksum, randomizer, the_serial, the_randomizer, the_checksum, i


        return chr(input_int % 26 + 65)

    def HexToDec(hexvalue:str):

        nonlocal license_nr, valid_until, case_id, parameter_int, valid_flag, license_hex, valid_hex, case_hex, parameter_hex, valid_str, checksum, randomizer, the_serial, the_randomizer, the_checksum, i

        decvalue:int = 0
        i:int = 0
        j:int = 0
        tmp_dec:int = 0
        for i in range(0,len(hexvalue) - 1 + 1) :
            tmp_dec = CharToInt (substring(hexvalue, len(hexvalue) - i - 1, 1))
            for j in range(1,i + 1) :
                tmp_dec = tmp_dec * 26
            decvalue = decvalue + tmp_dec
        return decvalue

    def Unrandomize(input_serial:str, input_rand:str, rand_pos:int):

        nonlocal license_nr, valid_until, case_id, parameter_int, valid_flag, license_hex, valid_hex, case_hex, parameter_hex, valid_str, checksum, randomizer, the_serial, the_randomizer, the_checksum, i

        j:int = 0
        i:int = 0
        k:int = 0
        jj:int = 0
        kk:int = 0
        numbers:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(1,15 + 1) :
            numbers[i - 1] = CharToInt (substring(input_serial, i - 1, 1))
        for i in range(5,15 + 1) :
            for k in range(1,4 + 1) :
                numbers[k - 1] = (numbers[k - 1] - numbers[i - 1] + 4 * k) % 26
        for j in range(1,15 + 1) :
            i = 15 + 1 - j
            for k in range(1,i - 1 + 1) :
                numbers[k - 1] = numbers[k - 1] - numbers[i - 1] + 2 * k
            for k in range(i + 1,15 + 1) :
                numbers[k - 1] = numbers[k - 1] - numbers[i - 1] + k
        input_serial = ""
        for i in range(1,15 + 1) :
            input_serial = input_serial + IntToChar (numbers[i - 1] - CharToInt (substring(input_rand, rand_pos - 1, 1)) - i * 11)
        return input_serial

    def CombineNumber(number:int):

        nonlocal license_nr, valid_until, case_id, parameter_int, valid_flag, license_hex, valid_hex, case_hex, parameter_hex, valid_str, checksum, randomizer, the_serial, the_randomizer, the_checksum, i

        if number > 9:
            number = number % 10 + number - 10
        return number

    def CalcChecksum(input_serial:str):

        nonlocal license_nr, valid_until, case_id, parameter_int, valid_flag, license_hex, valid_hex, case_hex, parameter_hex, valid_str, checksum, randomizer, the_serial, the_randomizer, the_checksum, i

        checksum:int = 0
        i:int = 0
        numbers:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(1,17 + 1) :
            numbers[i - 1] = CharToInt (substring(input_serial, i - 1, 1))
        for i in range(1,16 + 1) :
            checksum = (checksum + CombineNumber (numbers[i - 1] + numbers[i + 1 - 1])) % 26
        return IntToChar (checksum)

    the_serial = substring(serial_number, 0, 15)
    the_randomizer = substring(serial_number, 15, 2)
    the_checksum = substring(serial_number, 17, 1)
    checksum = calcChecksum (serial_number + the_randomizer)

    if checksum.lower()  != (the_checksum).lower() :
        valid_flag = False
    else:
        valid_flag = True
    the_serial = Unrandomize (the_serial, the_randomizer, 2)
    the_serial = Unrandomize (the_serial, the_randomizer, 1)
    license_hex = substring(the_serial, 0, 4)
    valid_hex = substring(the_serial, 4, 6)
    case_hex = substring(the_serial, 10, 2)
    parameter_hex = substring(the_serial, 12, 3)
    license_nr = HexToDec (license_hex)
    valid_str = to_string(HexToDec (valid_hex))
    while len(valid_str) < 8:
        valid_str = "0" + valid_str
    valid_until = date_mdy(to_int(substring(valid_str, 0, 2)) , to_int(substring(valid_str, 2, 2)) , to_int(substring(valid_str, 4, 4)))
    case_id = HexToDec (case_hex)
    parameter_int = HexToDec (parameter_hex)

    return generate_output()