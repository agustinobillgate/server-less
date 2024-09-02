from functions.additional_functions import *
import decimal
from models import L_lager

def po_stockin_curr_lagerbl(curr_lager:int):
    avail_l_lager = False
    l_lager_bezeich = ""
    l_lager = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_lager, l_lager_bezeich, l_lager


        return {"avail_l_lager": avail_l_lager, "l_lager_bezeich": l_lager_bezeich}


    l_lager = db_session.query(L_lager).filter(
            (L_lager.lager_nr == curr_lager)).first()

    if l_lager:
        l_lager_bezeich = l_lager.bezeich
        avail_l_lager = True

    return generate_output()