from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_lieferant

def po_list_return_lnamebl(case_type:int, lname:str, liefno:int):
    a_firma = ""
    l_supp_lief_nr = 0
    avail_l_supp = False
    l_lieferant = None

    l_supp = None

    L_supp = L_lieferant

    db_session = local_storage.db_session

    def generate_output():
        nonlocal a_firma, l_supp_lief_nr, avail_l_supp, l_lieferant
        nonlocal l_supp


        nonlocal l_supp
        return {"a_firma": a_firma, "l_supp_lief_nr": l_supp_lief_nr, "avail_l_supp": avail_l_supp}


    if case_type == 1:

        l_supp = db_session.query(L_supp).filter(
                (func.lower(L_supp.firma) == (lname).lower())).first()

    elif case_type == 2:

        l_supp = db_session.query(L_supp).filter(
                (L_supp.lief_nr == liefno)).first()

    if l_supp:
        a_firma = l_supp.firma
        avail_l_supp = True
        l_supp_lief_nr = l_supp.lief_nr

    return generate_output()