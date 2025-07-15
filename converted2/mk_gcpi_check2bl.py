#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gc_pi, Gc_piacct, Gl_acct

def mk_gcpi_check2bl(docu_nr:string, pbuff_returnamt:Decimal, pbuff_datum2:date, ret_acctno:string):

    prepare_cache ([Gc_pi, Gc_piacct])

    fl_err = 0
    gc_pi = gc_piacct = gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_err, gc_pi, gc_piacct, gl_acct
        nonlocal docu_nr, pbuff_returnamt, pbuff_datum2, ret_acctno

        return {"fl_err": fl_err}


    gc_pi = get_cache (Gc_pi, {"docu_nr": [(eq, docu_nr)]})
    gc_pi.returnamt =  to_decimal(pbuff_returnamt)
    gc_pi.datum2 = pbuff_datum2

    gc_piacct = get_cache (Gc_piacct, {"fibukonto": [(eq, ret_acctno)]})

    if gc_piacct:
        gc_pi.return_fibu = ret_acctno


    pass

    if pbuff_returnamt != 0:

        gc_piacct = get_cache (Gc_piacct, {"fibukonto": [(eq, ret_acctno)]})

        if not gc_piacct:
            fl_err = 1

            return generate_output()

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, ret_acctno)]})

        if not gl_acct:
            fl_err = 2

            return generate_output()

    return generate_output()