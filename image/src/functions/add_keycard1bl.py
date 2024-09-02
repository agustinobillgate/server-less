from functions.additional_functions import *
import decimal
from models import Res_line

def add_keycard1bl(resno:int, reslinno:int):
    card_type = ""
    res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal card_type, res_line


        return {"card_type": card_type}


    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

    res_line = db_session.query(Res_line).first()
    res_line.betrieb_gast = res_line.betrieb_gast + 1

    res_line = db_session.query(Res_line).first()
    card_type = "cardtype == 2"


    return generate_output()