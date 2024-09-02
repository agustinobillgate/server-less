from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_kredit, L_lieferant, Gl_jouhdr, Bediener, Res_history

def ap_edit_btn_ok_1bl(t_l_kredit:[T_l_kredit], recid_ap:int, orig_liefnr:int, lief_nr:int, firma:str, user_init:str):
    l_kredit = l_lieferant = gl_jouhdr = bediener = res_history = None

    t_l_kredit = supplier = subuff = None

    t_l_kredit_list, T_l_kredit = create_model_like(L_kredit)

    Supplier = L_lieferant
    Subuff = L_lieferant

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_kredit, l_lieferant, gl_jouhdr, bediener, res_history
        nonlocal supplier, subuff


        nonlocal t_l_kredit, supplier, subuff
        nonlocal t_l_kredit_list
        return {}

    l_kredit = db_session.query(L_kredit).filter(
            (L_kredit._recid == recid_ap)).first()

    subuff = db_session.query(Subuff).filter(
            (suBuff.lief_nr == l_kredit.lief_nr)).first()

    supplier = db_session.query(Supplier).filter(
            (Supplier.lief_nr == lief_nr)).first()

    t_l_kredit = query(t_l_kredit_list, first=True)

    l_kredit = db_session.query(L_kredit).filter(
            (L_kredit._recid == recid_ap)).first()
    l_kredit.lief_nr = t_l_kredit.lief_nr
    l_kredit.rabatt = t_l_kredit.rabatt
    l_kredit.rabattbetrag = t_l_kredit.rabattbetrag
    l_kredit.ziel = t_l_kredit.ziel
    l_kredit.netto = t_l_kredit.netto
    l_kredit.bediener_nr = t_l_kredit.bediener_nr
    l_kredit.bemerk = t_l_kredit.bemerk

    if orig_liefnr != lief_nr:

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                (Gl_jouhdr.refno == l_kredit.name)).first()

        if gl_jouhdr:
            gl_jouhdr.bezeich = firma

            gl_jouhdr = db_session.query(Gl_jouhdr).first()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener.nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.aenderung = "P/O " + l_kredit.name +\
            "; DeliveryNote " + l_kredit.lscheinnr +\
            "; Change Supplier " + suBuff.firma +\
            " -> " + supplier.firma


    res_history.action = "A/P"

    res_history = db_session.query(Res_history).first()


    return generate_output()