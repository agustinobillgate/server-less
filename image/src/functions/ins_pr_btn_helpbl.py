from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct, L_artikel

def ins_pr_btn_helpbl(pvilanguage:int, curr_select:str, acct:str, s_artnr:int):
    outputchar = ""
    l_traubensort = ""
    l_lief_einheit = 0
    msg_str = ""
    lvcarea:str = "ins_pr"
    gl_acct = l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal outputchar, l_traubensort, l_lief_einheit, msg_str, lvcarea, gl_acct, l_artikel


        return {"outputchar": outputchar, "l_traubensort": l_traubensort, "l_lief_einheit": l_lief_einheit, "msg_str": msg_str}


    if curr_select.lower()  == "cost_acct":

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (acct).lower())).first()

        if gl_acct:
            outputchar = acct

    elif curr_select.lower()  == "artnr":

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == s_artnr)).first()

        if l_artikel.betriebsnr != 0:
            msg_str = translateExtended ("This is a special article not for purchasing.", lvcarea, "")

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == s_artnr)).first()
        l_traubensort = l_artikel.traubensort
        l_lief_einheit = l_artikel.lief_einheit
        outputchar = trim(l_artikel.bezeich) + " - " +\
                to_string(l_artikel.inhalt) + " " +\
                to_string(l_artikel.masseinheit, "x(3)")

    return generate_output()