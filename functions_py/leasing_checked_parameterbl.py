# using conversion tools version: 1.0.0.119
"""_yusufwijasena_05/11/2025

    Ticket ID: F6D79E
        _remark_:   - fix python indentation
"""
from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Artikel, Gl_acct, Queasy


def leasing_checked_parameterbl(curr_type: int, qrecid: int):

    prepare_cache([Htparam, Artikel, Queasy])

    error_msg = 0
    tlist_data = []
    ar_ledger: int = 0
    divered_rental: int = 0
    htparam = artikel = gl_acct = queasy = None
    tlist = None

    tlist_data, Tlist = create_model(
        "Tlist",
        {
            "ckey": string,
            "amount": Decimal
        })

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_msg, tlist_data, ar_ledger, divered_rental, htparam, artikel, gl_acct, queasy
        nonlocal curr_type, qrecid
        nonlocal tlist
        nonlocal tlist_data

        return {
            "error_msg": error_msg,
            "tlist": tlist_data
        }

    if curr_type == 1:
        htparam = get_cache(
            Htparam, {"paramnr": [(eq, 1051)]})

        if htparam:
            ar_ledger = htparam.finteger

        htparam = get_cache(
            Htparam, {"paramnr": [(eq, 1052)]})

        if htparam:
            divered_rental = htparam.finteger

        artikel = get_cache(
            Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

        if artikel:
            gl_acct = get_cache(
                Gl_acct, {"fibukonto": [(eq, artikel.fibukonto)]})

            if not gl_acct:
                error_msg = 1

                return generate_output()

        artikel = get_cache(
            Artikel, {"artnr": [(eq, divered_rental)], "departement": [(eq, 0)]})

        if artikel:
            gl_acct = get_cache(
                Gl_acct, {"fibukonto": [(eq, artikel.fibukonto)]})

            if not gl_acct:
                error_msg = 2

                return generate_output()

    elif curr_type == 2:
        htparam = get_cache(Htparam, {"paramnr": [(eq, 1051)]})

        if htparam:
            ar_ledger = htparam.finteger

        artikel = get_cache(
            Artikel, {"artnr": [(eq, ar_ledger)], "departement": [(eq, 0)]})

        if artikel:
            gl_acct = get_cache(
                Gl_acct, {"fibukonto": [(eq, artikel.fibukonto)]})

            if not gl_acct:
                error_msg = 1

                return generate_output()

        queasy = get_cache(
            Queasy, {"key": [(eq, 329)], "_recid": [(eq, qrecid)]})

        if queasy:
            tlist = Tlist()
            tlist_data.append(tlist)

            tlist.ckey = "payment deposit"
            tlist.amount = to_decimal(queasy.deci2)

    return generate_output()
