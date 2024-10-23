from functions.additional_functions import *
import decimal
from models import Hoteldpt

def delete_hoteldptbl(case_type:int, int1:int, int2:int, char1:str):
    success_flag = False
    hoteldpt = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, hoteldpt
        nonlocal case_type, int1, int2, char1


        return {"success_flag": success_flag}


    if case_type == 1:

        hoteldpt = db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num == int1)).first()

        if hoteldpt:
            db_session.delete(hoteldpt)
            pass
            success_flag = True

    return generate_output()