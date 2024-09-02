from functions.additional_functions import *
import decimal
from models import Briefzei

def write_briefzeibl(case_type:int, int1:int, int2:int, int3:int, char1:str, word_exist:bool):
    success_flag = False
    briefzei = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, briefzei


        return {"success_flag": success_flag}


    if case_type == 1:

        if not word_exist:
            briefzei = Briefzei()
            db_session.add(briefzei)

            briefzei.briefnr = int1
            briefzeilnr = int2

            briefzei = db_session.query(Briefzei).first()
        else:

            briefzei = db_session.query(Briefzei).filter(
                    (Briefzei.briefnr == int1)).first()
        briefzei.texte = char1

        success_flag = True

    return generate_output()