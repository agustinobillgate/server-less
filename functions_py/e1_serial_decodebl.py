#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 26/11/2025, with_for_update, skip, temp-table
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date

def e1_serial_decodebl(serial_number:string):
    license_nr = 0
    valid_until = None
    case_id = 0
    parameter_int = 0
    valid_flag = False
    license_hex:string = ""
    valid_hex:string = ""
    case_hex:string = ""
    parameter_hex:string = ""
    valid_str:string = ""
    checksum:string = ""
    randomizer:string = ""
    the_serial:string = ""
    the_randomizer:string = ""
    the_checksum:string = ""
    i:int = 0

    db_session = local_storage.db_session

    def generate_output():
        nonlocal license_nr, valid_until, case_id, parameter_int, valid_flag, license_hex, valid_hex, case_hex, parameter_hex, valid_str, checksum, randomizer, the_serial, the_randomizer, the_checksum, i
        nonlocal serial_number

        return {"license_nr": license_nr, "valid_until": valid_until, "case_id": case_id, "parameter_int": parameter_int, "valid_flag": valid_flag}

    def chartoint(input_char:string):

        nonlocal license_nr, valid_until, case_id, parameter_int, valid_flag, license_hex, valid_hex, case_hex, parameter_hex, valid_str, checksum, randomizer, the_serial, the_randomizer, the_checksum, i
        nonlocal serial_number


        return asc(input_char) - 65


    def inttochar(input_int:int):

        nonlocal license_nr, valid_until, case_id, parameter_int, valid_flag, license_hex, valid_hex, case_hex, parameter_hex, valid_str, checksum, randomizer, the_serial, the_randomizer, the_checksum, i
        nonlocal serial_number


        return chr_unicode(input_int % 26 + 65)


    def hextodec(hexvalue:string):

        nonlocal license_nr, valid_until, case_id, parameter_int, valid_flag, license_hex, valid_hex, case_hex, parameter_hex, valid_str, checksum, randomizer, the_serial, the_randomizer, the_checksum, serial_number

        decvalue:int = 0
        i:int = 0
        j:int = 0
        tmp_dec:int = 0
        for i in range(0,length(hexvalue) - 1 + 1) :
            tmp_dec = chartoint (substring(hexvalue, length(hexvalue) - i - 1, 1))
            for j in range(1,i + 1) :
                tmp_dec = tmp_dec * 26
            decvalue = decvalue + tmp_dec
        return decvalue


    def unrandomize(input_serial:string, input_rand:string, rand_pos:int):

        nonlocal license_nr, valid_until, case_id, parameter_int, valid_flag, license_hex, valid_hex, case_hex, parameter_hex, valid_str, checksum, randomizer, the_serial, the_randomizer, the_checksum, serial_number

        j:int = 0
        i:int = 0
        k:int = 0
        jj:int = 0
        kk:int = 0
        numbers:List[int] = create_empty_list(15,0)
        for i in range(1,15 + 1) :
            numbers[i - 1] = chartoint (substring(input_serial, i - 1, 1))
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
            input_serial = input_serial + inttochar (numbers[i - 1] - chartoint (substring(input_rand, rand_pos - 1, 1)) - i * 11)
        return input_serial


    def combinenumber(number:int):

        nonlocal license_nr, valid_until, case_id, parameter_int, valid_flag, license_hex, valid_hex, case_hex, parameter_hex, valid_str, checksum, randomizer, the_serial, the_randomizer, the_checksum, i
        nonlocal serial_number

        if number > 9:
            number = number % 10 + number - 10
        return number


    def calcchecksum(input_serial:string):

        nonlocal license_nr, valid_until, case_id, parameter_int, valid_flag, license_hex, valid_hex, case_hex, parameter_hex, valid_str, randomizer, the_serial, the_randomizer, the_checksum, serial_number

        checksum:int = 0
        i:int = 0
        numbers:List[int] = create_empty_list(17,0)
        for i in range(1,17 + 1) :
            numbers[i - 1] = chartoint (substring(input_serial, i - 1, 1))
        for i in range(1,16 + 1) :
            checksum = (checksum + combinenumber (numbers[i - 1] + numbers[i + 1 - 1])) % 26
        return inttochar (checksum)


    the_serial = substring(serial_number, 0, 15)
    the_randomizer = substring(serial_number, 15, 2)
    the_checksum = substring(serial_number, 17, 1)
    checksum = calcchecksum (serial_number + the_randomizer)

    if checksum.lower()  != (the_checksum).lower() :
        valid_flag = False
    else:
        valid_flag = True
    the_serial = unrandomize (the_serial, the_randomizer, 2)
    the_serial = unrandomize (the_serial, the_randomizer, 1)
    license_hex = substring(the_serial, 0, 4)
    valid_hex = substring(the_serial, 4, 6)
    case_hex = substring(the_serial, 10, 2)
    parameter_hex = substring(the_serial, 12, 3)
    license_nr = hextodec (license_hex)
    valid_str = to_string(hextodec (valid_hex))
    while length(valid_str) < 8:
        valid_str = "0" + valid_str
    valid_until = date_mdy(to_int(substring(valid_str, 0, 2)) , to_int(substring(valid_str, 2, 2)) , to_int(substring(valid_str, 4, 4)))
    case_id = hextodec (case_hex)
    parameter_int = hextodec (parameter_hex)

    return generate_output()