from functions.additional_functions import *
import decimal
from models import Argt_line, Arrangement

def delete_arrangementbl(case_type:int, int1:int, int2:int):
    success_flag = False
    argt_line = arrangement = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, argt_line, arrangement


        return {"success_flag": success_flag}


    if case_type == 1:

        for argt_line in db_session.query(Argt_line).filter(
                (Argt_line.argtnr == int1)).all():
            db_session.delete(argt_line)

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement.argtnr == int1)).first()

        if arrangement:
            db_session.delete(arrangement)
            success_flag = True
    elif case_type == 2:

        for argt_line in db_session.query(Argt_line).filter(
                (Argt_line.argtnr == int1)).all():
            db_session.delete(argt_line)

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement._recid == int2)).first()

        if arrangement:
            db_session.delete(arrangement)
            success_flag = True

    return generate_output()