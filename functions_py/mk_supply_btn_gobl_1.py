# using conversion tools version: 1.0.0.119
"""_yusufwijasena_15/12/2025

        _remark_:   - fixed cannot save new supplier profile
                    - fixed position of db_session.add() & buffer_copy
                    - cast value l_lieferant.segment1 to int
                    - strip value l_lieferant.telepon
                    - added try & except while adding data l_lieferant
"""
from functions.additional_functions import *
from decimal import Decimal
from models import L_lieferant, Gl_acct, Counters, Bediener, Res_history
from functions.next_counter_for_update import next_counter_for_update

from functions import log_program


t_l_lieferant_data, T_l_lieferant = create_model_like(L_lieferant)


def mk_supply_btn_gobl_1(pvilanguage: int, lname: string, zcode: string, user_init: string, t_l_lieferant_data: [T_l_lieferant]):

    prepare_cache([Counters, Bediener, Res_history])

    msg_str = ""
    lname = lname.strip()
    zcode = zcode.strip()
    created = False
    lvcarea: string = "mk-supply"
    l_lieferant = gl_acct = counters = bediener = res_history = None

    t_l_lieferant = l_supp = None

    L_supp = create_buffer("L_supp", L_lieferant)

    db_session = local_storage.db_session
    last_count = 0
    error_lock: string = ""

    def generate_output():
        nonlocal msg_str, created, lvcarea, l_lieferant, gl_acct, counters, bediener, res_history
        nonlocal pvilanguage, lname, zcode, user_init
        nonlocal l_supp
        nonlocal t_l_lieferant, l_supp

        return {"msg_str": msg_str, "created": created}

    if lname == "":
        msg_str = msg_str + translateExtended(
            "Company Name not yet defined.", lvcarea, "") + chr_unicode(2)

        return generate_output()

    l_supp = db_session.query(L_supp).filter(
        (L_supp.firma == (lname).lower())).first()

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

    counters = db_session.query(Counters).filter(
        (Counters.counter_no == 14)
    ).with_for_update().first()

    counters.counter = counters.counter + 1
    t_l_lieferant.lief_nr = counters.counter

    # yusufwijasena, fix error cannot save new supplier profile
    l_lieferant = L_lieferant()
    buffer_copy(t_l_lieferant, l_lieferant)
    
    l_lieferant.segment1 = (
        int(l_lieferant.segment1)
        if str(l_lieferant.segment1).strip() else 0
    )
    
    l_lieferant.telefon = l_lieferant.telefon.strip()

    # log_program.write_log('LOG', f't_l_lieferant: {t_l_lieferant}')
    # log_program.write_log('LOG', f'l_lieferant: {l_lieferant.__dict__}')
    # log_program.write_log('LOG', f'l_lieferant.segemnt1: {l_lieferant.segment1} | l_lieferant.telefon: {l_lieferant.telefon}')
    try:
        db_session.add(l_lieferant)
        db_session.flush()
    except Exception as e:
        db_session.rollback()
        
        log_program.write_log(
            'ERROR',
            f'failed create Supplier: {e}'
        )
        
        msg_str = msg_str + translateExtended(
            "Failed create Supplier.", lvcarea, "") + chr_unicode(2)
    
    # end fix error cannot save new supplier profile

    created = True

    bediener = get_cache(Bediener, {"userinit": [(eq, user_init)]})
    
    if bediener:
        res_history = Res_history()

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = f"Create Supplier - Supplier No : {to_string(t_l_lieferant.lief_nr)}" 
            
        res_history.action = "Create"
        
        db_session.add(res_history)
            
    # supp_no = to_string(t_l_lieferant.lief_nr)
    # msg_str = msg_str + translateExtended(
    #         f"Successfully created Supplier - Supplier No : {supp_no}.", lvcarea, "") + chr_unicode(2)

    return generate_output()
