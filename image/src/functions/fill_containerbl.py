from functions.additional_functions import *
import decimal
from models import L_artikel

def fill_containerbl(ss_artnr1:int, ss_artnr2:int, ss_artnr3:int):
    ss_bezeich1 = ""
    ss_bezeich2 = ""
    ss_bezeich3 = ""
    ss_preis1 = 0
    ss_preis2 = 0
    ss_preis3 = 0
    l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ss_bezeich1, ss_bezeich2, ss_bezeich3, ss_preis1, ss_preis2, ss_preis3, l_artikel


        return {"ss_bezeich1": ss_bezeich1, "ss_bezeich2": ss_bezeich2, "ss_bezeich3": ss_bezeich3, "ss_preis1": ss_preis1, "ss_preis2": ss_preis2, "ss_preis3": ss_preis3}


    if ss_artnr1 != 0:

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == ss_artnr1)).first()

        if l_artikel:
            ss_bezeich1 = l_artikel.bezeich
            ss_preis1 = l_artikel.ek_aktuell

    if ss_artnr2 != 0:

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == ss_artnr2)).first()

        if l_artikel:
            ss_bezeich2 = l_artikel.bezeich
            ss_preis2 = l_artikel.ek_aktuell

    if ss_artnr3 != 0:

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == ss_artnr3)).first()

        if l_artikel:
            ss_bezeich3 = l_artikel.bezeich
            ss_preis3 = l_artikel.ek_aktuell

    return generate_output()