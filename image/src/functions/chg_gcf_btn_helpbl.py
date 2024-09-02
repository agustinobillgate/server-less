from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Guest, Artikel

def chg_gcf_btn_helpbl(curr_select:str, int1:int, char1:str):
    char2 = ""
    bediener = guest = artikel = None

    usr = guest0 = None

    Usr = Bediener
    Guest0 = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal char2, bediener, guest, artikel
        nonlocal usr, guest0


        nonlocal usr, guest0
        return {"char2": char2}


    if curr_select.lower()  == "sales_id":

        if int1 > 0:

            usr = db_session.query(Usr).filter(
                    (func.lower(Usr.userinit) == (char1).lower())).first()
            char2 = usr.username

    elif curr_select.lower()  == "master":

        guest0 = db_session.query(Guest0).filter(
                (Guest0.gastnr == int1)).first()
        char2 = guest0.name + ", " + guest0.vorname1 + guest0.anredefirma + " " + guest0.anrede1

    if curr_select.lower()  == "payment":

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == int1) &  (Artikel.departement == 0)).first()
        char2 = artikel.bezeich

    return generate_output()