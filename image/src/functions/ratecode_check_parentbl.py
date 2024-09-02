from functions.additional_functions import *
import decimal
from models import Queasy

def ratecode_check_parentbl(intkey:int, inpchar1:str):
    check_parent = False
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal check_parent, queasy


        return {"check_parent": check_parent}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == intkey) &  (Queasy.char1 == inpchar1)).first()

    if not queasy:
        check_parent = True

    return generate_output()