from functions.additional_functions import *
import decimal
from models import Calls

def calls_list_updatebl(i_case:int, s_recid:int, destination:str):
    calls = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal calls
        nonlocal i_case, s_recid, destination


        return {}


    calls = db_session.query(Calls).filter(
             (Calls._recid == s_recid)).first()

    if calls:

        if i_case == 1:
            calls.satz_id = destination

        elif i_case == 2:
            calls.betriebsnr = 0

    return generate_output()