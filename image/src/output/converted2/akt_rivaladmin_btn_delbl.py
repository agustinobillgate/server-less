from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Akthdr, Akt_code

def akt_rivaladmin_btn_delbl(pvilanguage:int, aktionscode:int, aktiongrup:int, bezeich:str):
    msg_str = ""
    success_flag = False
    lvcarea:str = "akt-rivaladmin"
    akthdr = akt_code = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, success_flag, lvcarea, akthdr, akt_code
        nonlocal pvilanguage, aktionscode, aktiongrup, bezeich


        return {"msg_str": msg_str, "success_flag": success_flag}


    akthdr = db_session.query(Akthdr).filter(
             (Akthdr.mitbewerber[inc_value(0)] == aktionscode) | (Akthdr.mitbewerber[inc_value(1)] == aktionscode) | (Akthdr.mitbewerber[inc_value(2)] == aktionscode)).first()

    if akthdr:
        msg_str = msg_str + chr(2) + translateExtended ("Open sales action exists, deleting not possible.", lvcarea, "")
    else:

        akt_code = db_session.query(Akt_code).filter(
                 (Akt_code.aktiongrup == aktiongrup) & (Akt_code.aktionscode == aktionscode) & (func.lower(Akt_code.bezeich) == (bezeich).lower())).first()

        if akt_code:
            db_session.delete(akt_code)
            success_flag = True

    return generate_output()