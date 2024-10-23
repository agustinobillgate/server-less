from functions.additional_functions import *
import decimal
from models import Paramtext, Zimmer

def delete_paramtextbl(case_type:int, int1:int, int2:int, int3:int):
    success_flag = False
    counter:int = 0
    paramtext = zimmer = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, counter, paramtext, zimmer
        nonlocal case_type, int1, int2, int3


        return {"success_flag": success_flag}


    if case_type == 1:

        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == int1) & (Paramtext.number == int2) & (Paramtext.sprachcode == int3)).first()

        if paramtext:
            db_session.delete(paramtext)
            pass
            success_flag = True
    elif case_type == 2:

        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == int1) & (Paramtext.number == int2) & (Paramtext.sprachcode == int3)).first()

        if paramtext:

            zimmer = db_session.query(Zimmer).filter(
                     (Zimmer.setup == paramtext.txtnr - 9200)).first()

            if not zimmer and paramtext.txtnr == 230:

                zimmer = db_session.query(Zimmer).filter(
                         (Zimmer.typ == paramtext.sprachcode)).first()

            if not zimmer:
                db_session.delete(paramtext)
                pass
                success_flag = True

    return generate_output()