from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import H_bill_line, Bediener, Res_history

def ts_closeinv_create_logfilebl(user_init:str, art_recid:int):
    h_bill_line = bediener = res_history = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill_line, bediener, res_history
        nonlocal user_init, art_recid


        return {}


    h_bill_line = db_session.query(H_bill_line).filter(
             (H_bill_line._recid == art_recid)).first()

    if h_bill_line:

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (user_init).lower())).first()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Void Sales Article: " +\
                to_string(h_bill_line.artnr) +\
                "|" + h_bill_line.bezeich +\
                "|" + "Qty=" + to_string(h_bill_line.anzahl) +\
                "|" + "Amount=" + trim(to_string(h_bill_line.betrag, "->>>,>>>,>>9.99"))
        res_history.action = "POS Close Bill"


        pass

    return generate_output()