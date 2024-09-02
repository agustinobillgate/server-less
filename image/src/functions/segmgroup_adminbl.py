from functions.additional_functions import *
import decimal
from models import Bediener

def segmgroup_adminbl(pvilanguage:int, int1:int, char3:str):
    msg_str = ""
    lvcarea:str = "segmgroup_admin"
    bediener = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, bediener


        return {"msg_str": msg_str}


    bediener = db_session.query(Bediener).filter(
            (Bediener.user_group == int1) &  (Bediener.flag == 0)).first()

    if bediener:
    else:
        msg_str = msg_str + chr(2) + "&Q" + translateExtended ("REMOVE the Department", lvcarea, "") + chr(10) + to_string(int1) + " - " + char3 + " ?"

    return generate_output()