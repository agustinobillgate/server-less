from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_lieferant, Gl_acct, Counters, Queasy, Bediener, Res_history

t_l_lieferant_list, T_l_lieferant = create_model_like(L_lieferant)
tax_supplier_list, Tax_supplier = create_model("Tax_supplier", {"rechnr":int, "taxcode":str, "vat1":decimal, "vat2":})

def mk_supply_btn_go_1bl(pvilanguage:int, lname:str, zcode:str, user_init:str, t_l_lieferant_list:[T_l_lieferant], tax_supplier_list:[Tax_supplier]):
    msg_str = ""
    created = False
    lvcarea:str = "mk-supply"
    l_lieferant = gl_acct = counters = queasy = bediener = res_history = None

    t_l_lieferant = tax_supplier = l_supp = None

    L_supp = create_buffer("L_supp",L_lieferant)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, created, lvcarea, l_lieferant, gl_acct, counters, queasy, bediener, res_history
        nonlocal pvilanguage, lname, zcode, user_init
        nonlocal l_supp


        nonlocal t_l_lieferant, tax_supplier, l_supp
        nonlocal t_l_lieferant_list, tax_supplier_list
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

    tax_supplier = query(tax_supplier_list, first=True)

    if tax_supplier:
        tax_supplier.rechnr = t_l_lieferant.lief_nr


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 219
        queasy.char1 = tax_supplier.taxcode
        queasy.number1 = tax_supplier.rechnr
        queasy.deci1 =  to_decimal(tax_supplier.vat1)
        queasy.deci2 =  to_decimal(tax_supplier.vat2)

    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if bediener:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Create Supplier - Supplier No : " + to_string(t_l_lieferant.lief_nr)
        res_history.action = "Create"


        pass

    return generate_output()