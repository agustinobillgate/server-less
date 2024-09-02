from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_artikel, Bediener, L_bestand, Gl_acct

def s_storerequest_create_op_listbl(op_list_artnr:int, op_list_fuellflag:int, op_list_stornogrund:str, curr_lager:int):
    s_bezeich = ""
    s_bez2 = ""
    s_username = ""
    s_onhand = 0
    l_artikel = bediener = l_bestand = gl_acct = None

    l_art = sys_user = None

    L_art = L_artikel
    Sys_user = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_bezeich, s_bez2, s_username, s_onhand, l_artikel, bediener, l_bestand, gl_acct
        nonlocal l_art, sys_user


        nonlocal l_art, sys_user
        return {"s_bezeich": s_bezeich, "s_bez2": s_bez2, "s_username": s_username, "s_onhand": s_onhand}


    l_art = db_session.query(L_art).filter(
            (L_art.artnr == op_list_artnr)).first()

    sys_user = db_session.query(Sys_user).filter(
            (Sys_user.nr == op_list_fuellflag)).first()

    l_bestand = db_session.query(L_bestand).filter(
            (L_bestand.artnr == op_list_artnr) &  (L_bestand.lager_nr == curr_lager)).first()
    s_bezeich = l_art.bezeich
    s_username = sys_user.username

    if l_bestand:
        s_onhand = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

    gl_acct = db_session.query(Gl_acct).filter(
            (func.lower(Gl_acct.fibukonto) == (op_list_stornogrund).lower())).first()

    if gl_acct:
        s_bez2 = gl_acct.bezeich

    return generate_output()