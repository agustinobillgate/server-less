from functions.additional_functions import *
import decimal
from datetime import date
from models import Res_history, Htparam, Counters, L_kredit, Queasy

age_list_list, Age_list = create_model("Age_list", {"selected":bool, "ap_recid":int, "counter":int, "docu_nr":str, "rechnr":int, "lief_nr":int, "lscheinnr":str, "supplier":str, "rgdatum":date, "rabatt":decimal, "rabattbetrag":decimal, "ziel":date, "netto":decimal, "user_init":str, "debt":decimal, "credit":decimal, "bemerk":str, "tot_debt":decimal, "rec_id":int, "resname":str, "comments":str, "fibukonto":str, "t_bezeich":str, "debt2":decimal, "recv_date":date})

def ap_debtpay_get_voucherbl(age_list_list:[Age_list], pvilanguage:int):
    msg_str = ""
    lvcarea:str = "ap-debtpay"
    p_786:str = ""
    res_history = htparam = counters = l_kredit = queasy = None

    age_list = abuff = t_reshist = None

    Abuff = Age_list
    abuff_list = age_list_list

    T_reshist = create_buffer("T_reshist",Res_history)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, p_786, res_history, htparam, counters, l_kredit, queasy
        nonlocal pvilanguage
        nonlocal abuff, t_reshist


        nonlocal age_list, abuff, t_reshist
        nonlocal age_list_list
        return {"age-list": age_list_list, "msg_str": msg_str}

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 786)).first()

    if htparam:
        p_786 = htparam.fchar

    counters = db_session.query(Counters).filter(
             (Counters.counter_no == 40)).first()

    if not counters:
        counters = Counters()
        db_session.add(counters)

        counters.counter_no = 40
        counters.counter_bez = "Counter for AP Payment Voucher No."


    counters.counter = counters.counter + 1
    msg_str = msg_str + chr(2) + translateExtended ("DONE. A/P Payment Voucher Number", lvcarea, "") + " = " + to_string(counters.counter, "9999999")

    for abuff in query(abuff_list, filters=(lambda abuff: abuff.selected)):
        abuff.rechnr = counters.counter

        l_kredit = db_session.query(L_kredit).filter(
                 (L_kredit._recid == abuff.ap_recid)).first()
        l_kredit.rechnr = counters.counter

    if trim(p_786) != "":
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 173
        queasy.number1 = l_kredit.lief_nr
        queasy.number2 = counters.counter
        queasy.char1 = ""

    return generate_output()