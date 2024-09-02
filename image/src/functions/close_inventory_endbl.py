from functions.additional_functions import *
import decimal
from models import Htparam

def close_inventory_endbl(user_init:str):
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam


        return {}


    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 232)).first()
    htparam.flogical = False
    htparam.lupdate = get_current_date()
    htparam.fdefault = user_init + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

    htparam = db_session.query(Htparam).first()


    return generate_output()