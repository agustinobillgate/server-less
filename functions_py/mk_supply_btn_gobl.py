from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_lieferant, Gl_acct, Counters

t_l_lieferant_list, T_l_lieferant = create_model_like(L_lieferant)

def mk_supply_btn_gobl(pvilanguage:int, lname:str, zcode:str, t_l_lieferant_list:[T_l_lieferant]):
    msg_str = ""
    created = False
    lvcarea:str = "mk-supply"
    l_lieferant = gl_acct = counters = None

    t_l_lieferant = l_supp = None

    L_supp = create_buffer("L_supp",L_lieferant)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, created, lvcarea, l_lieferant, gl_acct, counters
        nonlocal pvilanguage, lname, zcode
        nonlocal l_supp


        nonlocal t_l_lieferant, l_supp
        nonlocal t_l_lieferant_list
        return {"msg_str": msg_str, "created": created}

    if lname == "":
        msg_str = msg_str + translateExtended ("Company Name not yet defined.", lvcarea, "") + chr(2)

        return generate_output()

    l_supp = db_session.query(L_supp).filter(
             (func.lower(L_supp.firma) == (lname).lower())).first()

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

    counters = db_session.query(Counters).filter(
             (Counters.counter_no == 14)).first()
    counters.counter = counters.counter + 1
    t_l_lieferant.lief_nr = counters.counter
    l_lieferant = L_lieferant()
    db_session.add(l_lieferant)

    buffer_copy(t_l_lieferant, l_lieferant)
    created = True

    return generate_output()