from functions.additional_functions import *
import decimal
from sqlalchemy import func
from functions.del_gcfbl import del_gcfbl
from models import Guest, Bediener, Akt_kont

def gcf_list_del_gcfbl(i_case:int, pvilanguage:int, gastno:int, user_init:str):
    msg_str = ""
    error_flag = True
    zugriff:bool = False
    error_code:int = 0
    lvcarea:str = "gcf-list"
    gname:str = ""
    guest = bediener = akt_kont = None

    guest1 = gbuff = None

    Guest1 = create_buffer("Guest1",Guest)
    Gbuff = create_buffer("Gbuff",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_flag, zugriff, error_code, lvcarea, gname, guest, bediener, akt_kont
        nonlocal i_case, pvilanguage, gastno, user_init
        nonlocal guest1, gbuff


        nonlocal guest1, gbuff
        return {"msg_str": msg_str, "error_flag": error_flag}


    guest = db_session.query(Guest).filter(
             (Guest.gastnr == gastno)).first()

    if not guest:
        msg_str = translateExtended ("The guest no longer available", lvcarea, "")

        return generate_output()

    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if i_case == 1:

        if guest.anlage_datum == get_current_date():
            zugriff = substring(bediener.permission, 1, 1) >= "2"
        else:
            zugriff = substring(bediener.permission, 1, 1) >= "3"

        if not zugriff:

            if guest.anlage_datum == get_current_date():
                msg_str = translateExtended ("No User Access Right [2,2]", lvcarea, "")
            else:
                msg_str = translateExtended ("No User Access Right [2,3]", lvcarea, "")

            return generate_output()
        msg_str = "&Q" + translateExtended ("Do you really want to delete the guestcard: ", lvcarea, "") + guest.name.upper() + " ?"
        error_flag = False

        return generate_output()
    error_code = get_output(del_gcfbl(guest.gastnr))

    if error_code == 0:
        msg_str = translateExtended ("Guestcard deleted.", lvcarea, "")
        error_flag = False

    elif error_code == 1:
        msg_str = translateExtended ("Reservation record exists, deletion not possible.", lvcarea, "")

    elif error_code == 2:
        msg_str = translateExtended ("Debt record exists, deletion not possible.", lvcarea, "")

    elif error_code == 3:

        guest1 = db_session.query(Guest1).filter(
                 (Guest1.master_gastnr == guest.gastnr)).first()
        msg_str = translateExtended ("The file is currently used as Master-file of the guest file ", lvcarea, "") + guest1.name.upper() + ", " + guest1.vorname1.upper() + " " + guest1.anredefirma.upper() + guest1.anrede1.upper() + chr(10) + translateExtended ("Deletion not possible.", lvcarea, "")

    elif error_code == 4:
        msg_str = translateExtended ("Sales customer record exists, deletion not possible.", lvcarea, "")

    elif error_code == 5:
        msg_str = translateExtended ("Bill record exists, deletion not possible.", lvcarea, "")

    elif error_code == 6:
        msg_str = translateExtended ("Allotment record exists, deletion not possible.", lvcarea, "")

    elif error_code == 7:
        msg_str = translateExtended ("Condo unit exists, deletion not possible.", lvcarea, "")

    elif error_code == 8:
        msg_str = translateExtended ("Banquet reservation exists, deletion not possible.", lvcarea, "")

    elif error_code == 9:
        msg_str = translateExtended ("Member Card exists, deletion not possible.", lvcarea, "")

    elif error_code == 10:
        msg_str = translateExtended ("Sport Club Member exists, deletion not possible.", lvcarea, "")

    elif error_code == 11:

        akt_kont = db_session.query(Akt_kont).filter(
                 (Akt_kont.betrieb_gast == guest.gastnr)).first()

        gbuff = db_session.query(Gbuff).filter(
                 (Gbuff.gastnr == akt_kont.gastnr)).first()

        if gbuff:
            gname = gbuff.name
        msg_str = translateExtended ("Name contact using guest's GcfNO exists, deletion not possible.", lvcarea, "") + chr(10) + translateExtended ("Please check names contact list under:", lvcarea, "") + " " + gname

    elif error_code == 12:
        msg_str = translateExtended ("Deleting Guest Card Not Possible", lvcarea, "")
        error_flag = True

    return generate_output()