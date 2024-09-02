from functions.additional_functions import *
import decimal
from models import Fa_grup, Gl_acct

def fa_artlist_subgrpbl(gnr:int):
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


        return {"avail_fibukonto": avail_fibukonto, "avail_credit": avail_credit, "avail_debit": avail_debit, "fibukonto": fibukonto, "credit_fibu": credit_fibu, "debit_fibu": debit_fibu, "sgrp_bez": sgrp_bez, "err_nr": err_nr}


    fa_grup = db_session.query(Fa_grup).filter(
            (Fa_grup.gnr == gnr) &  (Fa_grup.flag == 1)).first()

    if not fa_grup:
        err_nr = 1

        return generate_output()
    sgrp_bez = fa_grup.bezeich

    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == fa_grup.fibukonto)).first()

    if gl_acct:
        fibukonto = gl_acct.fibukonto
        avail_fibukonto = True

    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == fa_grup.credit_fibu)).first()

    if gl_acct:
        credit_fibu = gl_acct.fibukonto
        avail_credit = True

    gl_acct = db_session.query(Gl_acct).filter(
            (Gl_acct.fibukonto == fa_grup.debit_fibu)).first()

    if gl_acct:
        debit_fibu = gl_acct.fibukonto
        avail_debit = True

    return generate_output()