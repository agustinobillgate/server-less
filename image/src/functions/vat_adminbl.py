from functions.additional_functions import *
import decimal
from models import Htparam

def vat_adminbl(paramno:int, bezeich:str, fdecimal:decimal, fchar:str):
    success_flag = False
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, htparam


        return {"success_flag": success_flag}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == paramno)).first()

    if htparam:
        htparam.bezeich = bezeich
        htparam.fdecimal = fdecimal
        htparam.fchar = fchar


        success_flag = True


    return generate_output()