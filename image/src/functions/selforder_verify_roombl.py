from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.selforder_proc_sessionbl import selforder_proc_sessionbl
from models import Res_line, Guest

def selforder_verify_roombl(dept_number:int, room_number:str, inp_char:str):
    sessionid = ""
    guest_name = ""
    guest_email = ""
    pax = 0
    mess_result = ""
    found_flag:bool = False
    checkout_date:date = None
    rsalt:bytes = None
    csalt:str = ""
    mmemptr:bytes = None
    encodedtext:str = ""
    encodedsession:str = ""
    res_line = guest = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sessionid, guest_name, guest_email, pax, mess_result, found_flag, checkout_date, rsalt, csalt, mmemptr, encodedtext, encodedsession, res_line, guest


        return {"sessionid": sessionid, "guest_name": guest_name, "guest_email": guest_email, "pax": pax, "mess_result": mess_result}

    def GetSalt(saltlengthlimit:int):

        nonlocal sessionid, guest_name, guest_email, pax, mess_result, found_flag, checkout_date, rsalt, csalt, mmemptr, encodedtext, encodedsession, res_line, guest

        i:int = 0
        saltlengthlimit = saltlengthlimit / 8
        while i < saltlengthlimit:
            PUT_BYTES (rsalt, len(rsalt) + 1) = GENERATE_PBE_SALT
            i = i + 1
        return (rsalt)


    if room_number == "" or room_number == None:
        mess_result = "1_Room Number must be filled in!"

        return generate_output()

    if inp_char == None or inp_char == "":
        mess_result = "2_Input Char must be filled in!"

        return generate_output()

    if dept_number == None or dept_number == 0:
        mess_result = "3_Department Number must be filled in!"

        return generate_output()
    checkout_date = date_mdy(inp_char)
    found_flag = False

    res_line = db_session.query(Res_line).filter(
            (Res_line.resstatus == 6) &  (func.lower(Res_line.zinr) == (room_number).lower()) &  (Res_line.abreise == checkout_date)).first()

    if not res_line:
        found_flag = False

        res_line = db_session.query(Res_line).filter(
                (Res_line.resstatus == 6) &  (func.lower(Res_line.zinr) == (room_number).lower())).first()

        if res_line:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrmember)).first()

            if guest:

                if guest.name MATCHES '"*' + inp_char + '*"':
                    found_flag = True

                if not found_flag:

                    if guest.vorname1 MATCHES '"*' + inp_char + '*"':
                        found_flag = True
            else:
                found_flag = False
        else:
            found_flag = False
    else:
        found_flag = True

    if found_flag:

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()
        guest_name = guest.name + " " + guest.vorname1 + "," + guest.anrede1
        guest_email = guest.email_adr
        pax = res_line.erwachs + res_line.kind1 + res_line.gratis
        csalt = to_string(GetSalt (32).hexdigest())
        encodedtext = substring(csalt, 0, 20).upper()
        sessionid = encodedtext
        mmemptr = FROM encodedtext        encodedtext = BASE64_ENCODE (mmemptr)
        encodedsession = to_string(encodedtext)
        sessionid = encodedsession
        get_output(selforder_proc_sessionbl(1, sessionid, dept_number, room_number, guest_name, pax, room_number, res_line.ankunft, res_line.abreise, "", guest_email))
        mess_result = "0_Verify Room Success!"

        return generate_output()
    else:
        mess_result = "3_No Reservation Found!"

    return generate_output()