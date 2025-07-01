#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.selforder_proc_sessionbl import selforder_proc_sessionbl
from models import Res_line, Guest

def selforder_verify_roombl(dept_number:int, room_number:string, inp_char:string):

    prepare_cache ([Res_line, Guest])

    sessionid = ""
    guest_name = ""
    guest_email = ""
    pax = 0
    mess_result = ""
    found_flag:bool = False
    checkout_date:date = None
    rsalt:bytes = None
    csalt:string = ""
    mmemptr:bytes = None
    encodedtext:string = ""
    encodedsession:string = ""
    res_line = guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sessionid, guest_name, guest_email, pax, mess_result, found_flag, checkout_date, rsalt, csalt, mmemptr, encodedtext, encodedsession, res_line, guest
        nonlocal dept_number, room_number, inp_char

        return {"sessionid": sessionid, "guest_name": guest_name, "guest_email": guest_email, "pax": pax, "mess_result": mess_result}

    def getsalt(saltlengthlimit:int):

        nonlocal sessionid, guest_name, guest_email, pax, mess_result, found_flag, checkout_date, rsalt, csalt, mmemptr, encodedtext, encodedsession, res_line, guest
        nonlocal dept_number, room_number, inp_char

        i:int = 0
        saltlengthlimit = saltlengthlimit / 8
        while i < saltlengthlimit:
            put_bytes (rsalt, length(rsalt) + 1) = GENERATE_PBE_SALT
            i = i + 1
        return (rsalt)

    if room_number == "" or room_number == None:
        mess_result = "1-Room Number must be filled in!"

        return generate_output()

    if inp_char == None or inp_char == "":
        mess_result = "2-Input Char must be filled in!"

        return generate_output()

    if dept_number == None or dept_number == 0:
        mess_result = "3-Department Number must be filled in!"

        return generate_output()
    checkout_date = date_mdy(inp_char)
    found_flag = False

    res_line = get_cache (Res_line, {"resstatus": [(eq, 6)],"zinr": [(eq, room_number)],"abreise": [(eq, checkout_date)]})

    if not res_line:
        found_flag = False

        res_line = get_cache (Res_line, {"resstatus": [(eq, 6)],"zinr": [(eq, room_number)]})

        if res_line:

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            if guest:

                if matches(guest.name,'"*' + inp_char + '*"'):
                    found_flag = True

                if not found_flag:

                    if matches(guest.vorname1,'"*' + inp_char + '*"'):
                        found_flag = True
            else:
                found_flag = False
        else:
            found_flag = False
    else:
        found_flag = True

    if found_flag:

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        guest_name = guest.name + " " + guest.vorname1 + "," + guest.anrede1
        guest_email = guest.email_adr
        pax = res_line.erwachs + res_line.kind1 + res_line.gratis
        csalt = to_string(GetSalt (32).hexdigest())
        encodedtext = substring(csalt, 0, 20).upper()
        sessionid = encodedtext
        mmemptr =  encodedtext
        encodedtext = base64_encode(mmemptr)
        encodedsession = to_string(encodedtext)
        sessionid = encodedsession
        get_output(selforder_proc_sessionbl(1, sessionid, dept_number, room_number, guest_name, pax, room_number, res_line.ankunft, res_line.abreise, "", guest_email))
        mess_result = "0-Verify Room Success!"

        return generate_output()
    else:
        mess_result = "3-No Reservation Found!"

    return generate_output()