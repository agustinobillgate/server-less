from functions.additional_functions import *
import decimal
from models import L_artikel, Htparam

def ins_storerequest_return_qtybl(s_artnr:int, qty:decimal, stock_oh:decimal):
    err_flag = 0
    l_artikel = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_flag, l_artikel, htparam


        return {"err_flag": err_flag}


    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()

    if qty > stock_oh and l_artikel.betriebsnr == 0:
        err_flag = 1

        return generate_output()
    else:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 232)).first()

        if htparam.flogical:
            err_flag = 2

            return generate_output()
        else:
            err_flag = 99

    return generate_output()