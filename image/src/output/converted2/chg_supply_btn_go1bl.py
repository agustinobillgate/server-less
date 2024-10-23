from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_lieferant, Gl_acct, Bediener, Res_history

t_l_lieferant_list, T_l_lieferant = create_model_like(L_lieferant)

def chg_supply_btn_go1bl(pvilanguage:int, lname:str, zcode:str, supply_recid:int, user_init:str, t_l_lieferant_list:[T_l_lieferant]):
    msg_str = ""
    lvcarea:str = "chg-supply"
    l_lieferant = gl_acct = bediener = res_history = None

    t_l_lieferant = l_supp = None

    L_supp = create_buffer("L_supp",L_lieferant)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, l_lieferant, gl_acct, bediener, res_history
        nonlocal pvilanguage, lname, zcode, supply_recid, user_init
        nonlocal l_supp


        nonlocal t_l_lieferant, l_supp
        nonlocal t_l_lieferant_list
        return {"msg_str": msg_str}

    if lname == "":
        msg_str = msg_str + translateExtended ("Company Name not yet defined.", lvcarea, "") + chr(2)

        return generate_output()

    l_supp = db_session.query(L_supp).filter(
             (func.lower(L_supp.firma) == (lname).lower()) & (L_supp._recid != supply_recid)).first()

    if l_supp:
        msg_str = msg_str + translateExtended ("Other Supplier with the same company name exists.", lvcarea, "") + chr(2)

        return generate_output()

    if zcode != "":

        gl_acct = db_session.query(Gl_acct).filter(
                 (func.lower(Gl_acct.fibukonto) == (zcode).lower())).first()

        if not gl_acct:
            msg_str = msg_str + translateExtended ("Account Number not found.", lvcarea, "") + chr(2)

            return generate_output()

    t_l_lieferant = query(t_l_lieferant_list, first=True)

    l_lieferant = db_session.query(L_lieferant).filter(
             (L_lieferant._recid == supply_recid)).first()

    if l_lieferant:
        buffer_copy(t_l_lieferant, l_lieferant)

    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if bediener:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Modify Supplier - Supplier No : " + to_string(t_l_lieferant.lief_nr)
        res_history.action = "Modify"


        pass

    return generate_output()