from functions.additional_functions import *
import decimal
from models import Ratecode, Pricecod

def check_del_prtablebl(pvilanguage:int, nr:int, bezeich:str):
    msg_str = ""
    rcode:str = ""
    lvcarea:str = "check-del-prtable"
    ratecode = pricecod = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, rcode, lvcarea, ratecode, pricecod
        nonlocal pvilanguage, nr, bezeich


        return {"msg_str": msg_str}


    ratecode = db_session.query(Ratecode).filter(
             (Ratecode.marknr == nr)).first()

    if ratecode:
        rcode = ratecode.code
    else:

        pricecod = db_session.query(Pricecod).filter(
                 (Pricecod.marknr == nr)).first()

        if pricecod:
            rcode = pricecod.code

    if rcode != "":
        msg_str = msg_str + chr(2) + translateExtended ("Rates exists, CODE = ", lvcarea, "") + rcode + "; " + translateExtended ("deleting not possibe", lvcarea, "")

        return generate_output()
    msg_str = msg_str + chr(2) + "&Q" + translateExtended ("Do you really want to REMOVE the Price Market Table", lvcarea, "") + chr(10) + to_string(nr) + " - " + bezeich + " ?"

    return generate_output()