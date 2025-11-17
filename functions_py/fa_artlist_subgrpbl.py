#using conversion tools version: 1.0.0.119

# ===============================
# Rulita, 17-11-2025 | D3684B
# - New Compile Program
# ===============================

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_grup, Gl_acct

def fa_artlist_subgrpbl(gnr:int):

    prepare_cache ([Fa_grup, Gl_acct])

    avail_fibukonto = False
    avail_credit = False
    avail_debit = False
    fibukonto = ""
    credit_fibu = ""
    debit_fibu = ""
    sgrp_bez = ""
    err_nr = 0
    fa_grup = gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_fibukonto, avail_credit, avail_debit, fibukonto, credit_fibu, debit_fibu, sgrp_bez, err_nr, fa_grup, gl_acct
        nonlocal gnr

        return {"avail_fibukonto": avail_fibukonto, "avail_credit": avail_credit, "avail_debit": avail_debit, "fibukonto": fibukonto, "credit_fibu": credit_fibu, "debit_fibu": debit_fibu, "sgrp_bez": sgrp_bez, "err_nr": err_nr}


    fa_grup = get_cache (Fa_grup, {"gnr": [(eq, gnr)],"flag": [(eq, 1)]})

    if not fa_grup:
        err_nr = 1

        return generate_output()
    sgrp_bez = fa_grup.bezeich

    if num_entries(fa_grup.fibukonto, ".") > 1:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, entry(0, fa_grup.fibukonto, "."))]})

        if gl_acct:
            fibukonto = gl_acct.fibukonto
            avail_fibukonto = True


    else:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_grup.fibukonto)]})

        if gl_acct:
            fibukonto = gl_acct.fibukonto
            avail_fibukonto = True

    if num_entries(fa_grup.credit_fibu, ".") > 1:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, entry(0, fa_grup.credit_fibu, "."))]})

        if gl_acct:
            credit_fibu = gl_acct.fibukonto
            avail_credit = True


    else:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_grup.credit_fibu)]})

        if gl_acct:
            credit_fibu = gl_acct.fibukonto
            avail_credit = True

    if num_entries(fa_grup.debit_fibu, ".") > 1:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, entry(0, fa_grup.debit_fibu, "."))]})

        if gl_acct:
            debit_fibu = gl_acct.fibukonto
            avail_debit = True


    else:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fa_grup.debit_fibu)]})

        if gl_acct:
            debit_fibu = gl_acct.fibukonto
            avail_debit = True

    return generate_output()