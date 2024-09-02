from functions.additional_functions import *
import decimal
from models import Hoteldpt

def delete_hoteldptbl(case_type:int, int1:int, int2:int, char1:str):
    success_flag = False
    hoteldpt = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, hoteldpt


        return {"success_flag": success_flag}


    if case_type == 1:

        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.num == int1)).first()

        if hoteldpt:
            db_session.delete(hoteldpt)

            success_flag = True

    return generate_output()