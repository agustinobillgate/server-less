#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import L_lieferant, Gl_acct, Counters, Bediener, Res_history
from functions.next_counter_for_update import next_counter_for_update


t_l_lieferant_data, T_l_lieferant = create_model_like(L_lieferant)

def mk_supply_btn_gobl_1(pvilanguage:int, lname:string, zcode:string, user_init:string, t_l_lieferant_data:[T_l_lieferant]):

    prepare_cache ([Counters, Bediener, Res_history])

    msg_str = ""
    created = False
    lvcarea:string = "mk-supply"
    l_lieferant = gl_acct = counters = bediener = res_history = None

    t_l_lieferant = l_supp = None

    L_supp = create_buffer("L_supp",L_lieferant)

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    lname = lname.strip()
    zcode = zcode.strip()


    def generate_output():
        nonlocal msg_str, created, lvcarea, l_lieferant, gl_acct, counters, bediener, res_history
        nonlocal pvilanguage, lname, zcode, user_init
        nonlocal l_supp


        nonlocal t_l_lieferant, l_supp

        return {"msg_str": msg_str, "created": created}

    if lname == "":
        msg_str = msg_str + translateExtended ("Company Name not yet defined.", lvcarea, "") + chr_unicode(2)

        return generate_output()

    l_supp = db_session.query(L_supp).filter(
             (L_supp.firma == (lname).lower())).first()

    if l_supp:
        msg_str = msg_str + translateExtended ("Other Supplier with the same company name exists.", lvcarea, "") + chr_unicode(2)

        return generate_output()

    if zcode != "":

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, zcode)]})

        if not gl_acct:
            msg_str = msg_str + translateExtended ("Account Number not found.", lvcarea, "") + chr_unicode(2)

            return generate_output()

    t_l_lieferant = query(t_l_lieferant_data, first=True)

    # counters = get_cache (Counters, {"counter_no": [(eq, 14)]})
    counters = db_session.query(Counters).with_for_update().filter(
             (Counters.counter_no == 14)).first()
    
    counters.counter = counters.counter + 1
    t_l_lieferant.lief_nr = counters.counter
    pass
    pass
    l_lieferant = L_lieferant()
    db_session.add(l_lieferant)

    buffer_copy(t_l_lieferant, l_lieferant)
    created = True

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Create Supplier - Supplier No : " + to_string(t_l_lieferant.lief_nr)
        res_history.action = "Create"


        pass
        pass

    return generate_output()