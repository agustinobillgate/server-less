#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_history, Htparam, Counters, L_kredit, Queasy
from functions.next_counter_for_update import next_counter_for_update



age_list_data, Age_list = create_model("Age_list", {"selected":bool, "ap_recid":int, "counter":int, "docu_nr":string, "rechnr":int, "lief_nr":int, "lscheinnr":string, "supplier":string, "rgdatum":date, "rabatt":Decimal, "rabattbetrag":Decimal, "ziel":date, "netto":Decimal, "user_init":string, "debt":Decimal, "credit":Decimal, "bemerk":string, "tot_debt":Decimal, "rec_id":int, "resname":string, "comments":string, "fibukonto":string, "t_bezeich":string, "debt2":Decimal, "recv_date":date})

def ap_debtpay_get_voucherbl(age_list_data:[Age_list], pvilanguage:int):

    prepare_cache ([Htparam, Counters, L_kredit, Queasy])

    msg_str = ""
    lvcarea:string = "ap-debtpay"
    p_786:string = ""
    res_history = htparam = counters = l_kredit = queasy = None

    age_list = abuff = t_reshist = None

    Abuff = Age_list
    abuff_data = age_list_data

    T_reshist = create_buffer("T_reshist",Res_history)


    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""

    def generate_output():
        nonlocal msg_str, lvcarea, p_786, res_history, htparam, counters, l_kredit, queasy
        nonlocal pvilanguage
        nonlocal abuff, t_reshist


        nonlocal age_list, abuff, t_reshist

        return {"age-list": age_list_data, "msg_str": msg_str}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 786)]})

    if htparam:
        p_786 = htparam.fchar

    # Rd, 24/11/2025, Update last counter dengan next_counter_for_update
    # counters = get_cache (Counters, {"counter_no": [(eq, 40)]})
    # if not counters:
    #     counters = Counters()
    #     db_session.add(counters)

    #     counters.counter_no = 40
    #     counters.counter_bez = "Counter for AP Payment Voucher No."


    # counters.counter = counters.counter + 1

    last_count, error_lock = get_output(next_counter_for_update(40))

    pass
    msg_str = msg_str + chr_unicode(2) + translateExtended ("DONE. A/P Payment Voucher Number", lvcarea, "") + " = " + to_string(counters.counter, "9999999")

    for abuff in query(abuff_data, filters=(lambda abuff: abuff.selected)):
        # abuff.rechnr = counters.counter
        abuff.rechnr = last_count

        l_kredit = db_session.query(L_kredit).filter(L_kredit._recid == abuff.ap_recid).with_for_update().first()
        if l_kredit:
            # l_kredit.rechnr = counters.counter
            l_kredit.rechnr = last_count

    if trim(p_786) != "":
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 173
        queasy.number1 = l_kredit.lief_nr
        # queasy.number2 = counters.counter
        queasy.number2 = last_count
        queasy.char1 = ""

    return generate_output()