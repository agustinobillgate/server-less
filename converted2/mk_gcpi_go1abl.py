#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gc_pi, Gc_pitype

pbuff_data, Pbuff = create_model_like(Gc_pi)

def mk_gcpi_go1abl(pbuff_data:[Pbuff], pi_type:string, pay_type:string, pay_acctno:string, rcvname:string, bemerk:string, pi_number:string):

    prepare_cache ([Gc_pi, Gc_pitype])

    gc_pi = gc_pitype = None

    pbuff = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gc_pi, gc_pitype
        nonlocal pi_type, pay_type, pay_acctno, rcvname, bemerk, pi_number


        nonlocal pbuff

        return {}

    pbuff = query(pbuff_data, first=True)

    gc_pitype = get_cache (Gc_pitype, {"bezeich": [(eq, pi_type)]})

    gc_pi = get_cache (Gc_pi, {"docu_nr": [(eq, pi_number)]})

    if gc_pi:
        pass
        buffer_copy(pbuff, gc_pi)
        gc_pi.rcvname = rcvname
        gc_pi.bemerk = bemerk
        gc_pi.pay_type = to_int(substring(pay_type, 0, 1))
        gc_pi.credit_fibu = pay_acctno

        if gc_pitype:
            gc_pi.pi_type = gc_pitype.nr
        pass
        pass

    return generate_output()