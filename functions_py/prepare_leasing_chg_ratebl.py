# using conversion tools version: 1.0.0.119
"""_yusufwijasena_06/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
                    - only convert
"""
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy


def prepare_leasing_chg_ratebl(resnr: int, reslinnr: int):

    prepare_cache([Queasy])

    amount = to_decimal("0.0")
    tlist_data = []
    amount_ori = to_decimal("0.0")
    amount_new = to_decimal("0.0")
    queasy = None

    tlist = None

    tlist_data, Tlist = create_model(
        "Tlist",
        {
            "avail_chg_rate": bool
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount, tlist_data, amount_ori, amount_new, queasy
        nonlocal resnr, reslinnr
        nonlocal tlist
        nonlocal tlist_data

        return {
            "amount": amount,
            "tlist": tlist_data
        }

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 356) & (Queasy.number1 == resnr) & (Queasy.number2 == reslinnr)).order_by(Queasy.date1.desc()).all():
        amount_ori = to_decimal(amount_ori) + to_decimal(queasy.deci1)
        amount_new = to_decimal(amount_new) + to_decimal(queasy.deci2)

        break

    queasy = get_cache(
        Queasy, {"key": [(eq, 329)], "number1": [(eq, resnr)], "number2": [(eq, reslinnr)]})

    if queasy:
        amount = to_decimal(queasy.deci2 - amount_new)

    queasy = get_cache(
        Queasy, {"key": [(eq, 356)], "number1": [(eq, resnr)], "number2": [(eq, reslinnr)]})

    if queasy:
        tlist = query(tlist_data, first=True)

        if not tlist:
            tlist = Tlist()
            tlist_data.append(tlist)

        tlist.avail_chg_rate = True

    return generate_output()
