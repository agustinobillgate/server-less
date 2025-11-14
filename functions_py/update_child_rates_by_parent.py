# using conversion tools version: 1.0.0.119
"""_yusufwijasena_13/11/2025

    Ticket ID: 62BADE
        _remark_:   - fix python indentation
                    - only convert to py
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions_py.link_ratecodebl import link_ratecodebl
from models import Ratecode, Htparam, Queasy


def update_child_rates_by_parent(parent_code: str):

    prepare_cache([Htparam, Queasy])

    ci_date: date = None
    round_betrag: int = 0
    round_method: int = 0
    length_round: int = 0
    in_percent: bool = True
    adjust_value: Decimal = to_decimal("0.0")
    ratecode = htparam = queasy = None

    child_list = child_ratecode = rbuff = tb3buff = None

    child_list_data, Child_list = create_model(
        "Child_list",
        {
            "child_code": string,
            "true_child": bool
        },
        {
            "true_child": True
        })
    child_ratecode_data, Child_ratecode = create_model_like(Ratecode)

    Rbuff = create_buffer("Rbuff", Ratecode)
    Tb3buff = create_buffer("Tb3buff", Ratecode)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, round_betrag, round_method, length_round, in_percent, adjust_value, ratecode, htparam, queasy
        nonlocal parent_code
        nonlocal rbuff, tb3buff
        nonlocal child_list, child_ratecode, rbuff, tb3buff
        nonlocal child_list_data, child_ratecode_data

        return {}

    def create_child_list():
        nonlocal ci_date, round_betrag, round_method, length_round, in_percent, adjust_value, ratecode, htparam, queasy
        nonlocal parent_code
        nonlocal rbuff, tb3buff
        nonlocal child_list, child_ratecode, rbuff, tb3buff
        nonlocal child_list_data, child_ratecode_data

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 2) & not_(Queasy.logi2) & (num_entries(Queasy.char3, ";") > 2) & (entry(1, Queasy.char3, ";") == (parent_code).lower())).order_by(Queasy._recid).all():
            child_list = Child_list()
            child_list_data.append(child_list)

            child_list.child_code = queasy.char1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache(Htparam, {"paramnr": [(eq, 1013)]})

    if htparam.feldtyp == 1:
        round_betrag = htparam.finteger
        length_round = length(to_string(round_betrag))

    elif htparam.feldtyp == 5 and num_entries(htparam.fchar, ";") > 1:
        round_betrag = to_int(entry(0, htparam.fchar, ";"))
        length_round = length(to_string(round_betrag))
        round_method = to_int(entry(1, htparam.fchar, ";"))

    create_child_list()

    child_list = query(child_list_data, first=True)

    if not child_list:
        return generate_output()

    for child_list in query(child_list_data):
        queasy = get_cache(
            Queasy, {"key": [(eq, 2)], "char1": [(eq, child_list.child_code)]})
        in_percent = substring(entry(2, queasy.char3, ";"), 0, 1) == "%"
        adjust_value = to_decimal(
            substring(entry(2, queasy.char3, ";"), 1)) / 100

        get_output(link_ratecodebl(child_list.child_code, parent_code, queasy.char3, in_percent, adjust_value))

    return generate_output()
