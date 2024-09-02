from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Nation

def subnation_admin_checkbl(pvilanguage:int, kurzbez:str, natcode:int):
    msg_str = ""
    lvcarea:str = "subnation_admin_check"
    nation = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, nation


        return {"msg_str": msg_str}


    nation = db_session.query(Nation).filter(
            (func.lower(Nation.(kurzbez).lower()) == (kurzbez).lower()) &  (Nation.natcode == natcode)).first()

    if nation and kurzbez != "":
        msg_str = msg_str + chr(2) + translateExtended ("Region Code already exists, use other code.", lvcarea, "")

        return generate_output()

    nation = db_session.query(Nation).filter(
            (func.lower(Nation.(kurzbez).lower()) == (kurzbez).lower()) &  (Nation.natcode == 0)).first()

    if nation and kurzbez != "":
        msg_str = msg_str + chr(2) + translateExtended ("Region Code used for a Nation Code, use other code.", lvcarea, "")

        return generate_output()