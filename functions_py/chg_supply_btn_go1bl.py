# using conversion tools version: 1.0.0.119
"""_yusufwijasena_15/12/2025

        _remark_:   - strip value lname & zcode
"""
from functions.additional_functions import *
from decimal import Decimal
from models import L_lieferant, Gl_acct, Bediener, Res_history

from functions import log_program

t_l_lieferant_data, T_l_lieferant = create_model_like(L_lieferant)


def chg_supply_btn_go1bl(pvilanguage: int, lname: string, zcode: string, supply_recid: int, user_init: string, t_l_lieferant_data: [T_l_lieferant]):

    prepare_cache([Bediener, Res_history])

    msg_str = ""
    lname = lname.strip()
    zcode = zcode.strip()
    lvcarea: string = "chg-supply"
    l_lieferant = gl_acct = bediener = res_history = None

    t_l_lieferant = l_supp = None

    L_supp = create_buffer("L_supp", L_lieferant)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, l_lieferant, gl_acct, bediener, res_history
        nonlocal pvilanguage, lname, zcode, supply_recid, user_init
        nonlocal l_supp
        nonlocal t_l_lieferant, l_supp

        return {"msg_str": msg_str}

    if lname == "":
        msg_str = msg_str + translateExtended(
            "Company Name not yet defined.", lvcarea, "") + chr_unicode(2)

        return generate_output()

    l_supp = db_session.query(L_supp).filter(
        (L_supp.firma == (lname).lower()) &
        (L_supp._recid != supply_recid)).first()

    if l_supp:
        msg_str = msg_str + translateExtended(
            "Other Supplier with the same company name exists.", lvcarea, "") + chr_unicode(2)

        return generate_output()

    if zcode != "":
        gl_acct = get_cache(Gl_acct, {"fibukonto": [(eq, zcode)]})

        if not gl_acct:
            msg_str = msg_str + translateExtended(
                "Account Number not found.", lvcarea, "") + chr_unicode(2)

            return generate_output()

    t_l_lieferant = query(t_l_lieferant_data, first=True)
    
    l_lieferant = db_session.query(L_lieferant).filter(
            L_lieferant._recid == supply_recid
        ).with_for_update().first()

    try:
        if l_lieferant:
            buffer_copy(t_l_lieferant, l_lieferant)
            
            l_lieferant.segment1 = (
                int(l_lieferant.segment1)
                if str(l_lieferant.segment1).strip() else 0
            )
            l_lieferant.telefon = l_lieferant.telefon.strip()
    except Exception as e:        
        log_program.write_log(
            'ERROR',
            f'failed create Supplier: {e}'
        )
    
    # log_program.write_log('LOG', f'l_lieferant: {l_lieferant.__dict__}')


    bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})

    if bediener:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Modify Supplier - Supplier No : " + \
            to_string(t_l_lieferant.lief_nr)
        res_history.action = "Modify"

    return generate_output()
