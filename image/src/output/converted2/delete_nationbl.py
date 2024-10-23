from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Nation

def delete_nationbl(case_type:int, int1:int, char1:str):
    success_flag = False
    nation = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, nation
        nonlocal case_type, int1, char1


        return {"success_flag": success_flag}


    if case_type == 1:

        nation = db_session.query(Nation).filter(
                 (Nation.nationnr == int1) & (func.lower(Nation.kurzbez) == (char1).lower())).first()

        if nation:
            db_session.delete(nation)
            pass
            success_flag = True
    elif case_type == 2:

        nation = db_session.query(Nation).filter(
                 (Nation._recid == int1)).first()

        if nation:
            db_session.delete(nation)
            pass
            success_flag = True

    return generate_output()