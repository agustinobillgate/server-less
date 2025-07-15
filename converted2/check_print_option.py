from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def check_print_option(prog_name:str, sstr:str):
    print_it = True
    i:int = 0
    s:str = ""
    pflag:List[bool] = [False, True, True]
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal print_it, i, s, pflag, queasy
        nonlocal prog_name, sstr

        return {"print_it": print_it}


    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 140) & (func.lower(Queasy.char1) == (prog_name).lower())).first()

    if not queasy:

        return generate_output()
    for i in range(1,num_entries(queasy.char3, "\\")  + 1) :
        s = entry(i - 1, queasy.char3, "\\")

        if s != "":

            if entry(0, s, ";") == (sstr).lower() :
                print_it = pflag[to_int(entry(1, s, ";")) + 1 - 1]

                return generate_output()

    return generate_output()