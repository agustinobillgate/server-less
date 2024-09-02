from functions.additional_functions import *
import decimal
from models import Briefzei, Brief

def fo_wordadmin_btn_delbl(briefnr:int, int1:int):
    success_flag = False
    briefzei = brief = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, briefzei, brief


        return {"success_flag": success_flag}


    briefzei = db_session.query(Briefzei).filter(
            (Briefzei.briefnr == briefnr) &  (Briefzeilnr == 1)).first()

    if briefzei:
        db_session.delete(briefzei)

    brief = db_session.query(Brief).filter(
            (briefnr == int1)).first()

    if brief:
        db_session.delete(brief)
    success_flag = True

    return generate_output()