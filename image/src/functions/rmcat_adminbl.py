from functions.additional_functions import *
import decimal
from models import Zimmer, Zimkateg

def rmcat_adminbl(pvilanguage:int, zikatnr:int):
    msg_str = ""
    lvcarea:str = "rmcat_admin"
    zimmer = zimkateg = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, zimmer, zimkateg


        return {"msg_str": msg_str}


    zimmer = db_session.query(Zimmer).filter(
            (Zimmer.zikatnr == zikatnr)).first()

    if zimmer:
        msg_str = msg_str + chr(2) + translateExtended ("Room under this category exists, deleting not possible.", lvcarea, "")
    else:

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == zikatnr)).first()

        if zimkateg:
            db_session.delete(zimkateg)

    return generate_output()