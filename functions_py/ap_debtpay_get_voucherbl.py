# using conversion tools version: 1.0.0.119
"""_yusufwijasena_28/11/2025
        issue:  - cannot generate AP Payment Voucher Number
                - changed counters.counter to last_count
                
    _yusufwijasena_18/12/2025
        issue:  - deactivate last_count, back using counters.counter
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_history, Htparam, Counters, L_kredit, Queasy
# from functions_py.next_counter_for_update import next_counter_for_update

from functions import log_program


age_list_data, Age_list = create_model(
    "Age_list",
    {
        "selected": bool,
        "ap_recid": int,
        "counter": int,
        "docu_nr": str,
        "rechnr": int,
        "lief_nr": int,
        "lscheinnr": str,
        "supplier": str,
        "rgdatum": date,
        "rabatt": Decimal,
        "rabattbetrag": Decimal,
        "ziel": date,
        "netto": Decimal,
        "user_init": str,
        "debt": Decimal,
        "credit": Decimal,
        "bemerk": str,
        "tot_debt": Decimal,
        "rec_id": int,
        "resname": str,
        "comments": str,
        "fibukonto": str,
        "t_bezeich": str,
        "debt2": Decimal,
        "recv_date": date
    })


def ap_debtpay_get_voucherbl(age_list_data: [Age_list], pvilanguage: int):

    prepare_cache([Htparam, Counters, L_kredit, Queasy])

    msg_str = ""
    lvcarea: str = "ap-debtpay"
    p_786 = ""
    voucher_num: int
    res_history = htparam = counters = l_kredit = queasy = None

    age_list = abuff = t_reshist = None

    Abuff = Age_list
    abuff_data = age_list_data

    T_reshist = create_buffer("T_reshist", Res_history)

    db_session = local_storage.db_session
    # last_count = 0
    # error_lock = ""

    def generate_output():
        nonlocal msg_str, lvcarea, p_786, res_history, htparam, counters, l_kredit, queasy
        nonlocal pvilanguage
        nonlocal abuff, t_reshist
        nonlocal age_list, abuff, t_reshist
        
        msg_str = f"{msg_str}{chr_unicode(2)}{translateExtended('DONE. A/P Payment Voucher Number', lvcarea, '')} = {to_string(voucher_num, '9999999')}"

        return {
            "age-list": age_list_data,
            "msg_str": msg_str
        }

    # htparam = get_cache(Htparam, {"paramnr": [(eq, 786)]})
    htparam = db_session.query(Htparam).filter(
        Htparam.paramnr == 786
    ).first()

    if htparam:
        p_786 = htparam.fchar

    # Rd, 24/11/2025, Update last counter dengan next_counter_for_update
    # counters = get_cache (Counters, {"counter_no": [(eq, 40)]})
    counters = db_session.query(Counters).filter(
        Counters.counter_no == 40
    ).with_for_update().first()
    if not counters:
        counters = Counters()
        db_session.add(counters)

        counters.counter_no = 40
        counters.counter_bez = "Counter for AP Payment Voucher No."

        # add db_session commit

    counters.counter = counters.counter + 1

    voucher_num = counters.counter

    # yusufwijasena: changed counters.counter to last_count

    selected_abuff = query(abuff_data, filters=(lambda abuff: abuff.selected))

    for abuff in selected_abuff:
        abuff.rechnr = voucher_num

        l_kredit = db_session.query(L_kredit).filter(
            L_kredit._recid == abuff.ap_recid
        ).with_for_update().first()

        if l_kredit:
            l_kredit.rechnr = voucher_num

    if trim(p_786) != "":
        queasy = Queasy()

        queasy.key = 173
        queasy.number1 = l_kredit.lief_nr
        # queasy.number2 = counters.counter
        queasy.number2 = voucher_num
        queasy.char1 = ""

        db_session.add(queasy)

    db_session.commit()
    return generate_output()
