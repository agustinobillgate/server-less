#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Akthdr, Akt_code

def akt_rivaladmin_btn_delbl(pvilanguage:int, aktionscode:int, aktiongrup:int, bezeich:string):
    msg_str = ""
    success_flag = False
    lvcarea:string = "akt-rivaladmin"
    akthdr = akt_code = None

    db_session = local_storage.db_session
    bezzeich = bezeich.strip()
    

    def generate_output():
        nonlocal msg_str, success_flag, lvcarea, akthdr, akt_code
        nonlocal pvilanguage, aktionscode, aktiongrup, bezeich

        return {"msg_str": msg_str, "success_flag": success_flag}


    akthdr = db_session.query(Akthdr).filter(
             (Akthdr.mitbewerber[inc_value(0)] == aktionscode) | (Akthdr.mitbewerber[inc_value(1)] == aktionscode) | (Akthdr.mitbewerber[inc_value(2)] == aktionscode)).first()

    if akthdr:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Open sales action exists, deleting not possible.", lvcarea, "")
    else:

        # akt_code = get_cache (Akt_code, {"aktiongrup": [(eq, aktiongrup)],"aktionscode": [(eq, aktionscode)],"bezeich": [(eq, bezeich)]})

        akt_code = db_session.query(Akt_code).filter(
                 (Akt_code.aktiongrup == aktiongrup) &
                 (Akt_code.aktionscode == aktionscode) &
                 (Akt_code.bezeich == bezeich)).with_for_update().first()

        if akt_code:
            db_session.delete(akt_code)
            success_flag = True

    return generate_output()