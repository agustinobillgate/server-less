#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_artikel, Htparam, Fa_op

def fa_upgradelist_btn_cancelbl(mat_buff_nr:int, recid_fa_artikel:int, user_init:string):

    prepare_cache ([Fa_artikel, Htparam, Fa_op])

    err_no = 0
    last_depn:date = None
    fa_artikel = htparam = fa_op = None

    fa_buff = None

    Fa_buff = create_buffer("Fa_buff",Fa_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_no, last_depn, fa_artikel, htparam, fa_op
        nonlocal mat_buff_nr, recid_fa_artikel, user_init
        nonlocal fa_buff


        nonlocal fa_buff

        return {"err_no": err_no}

    def cancel_upgrade():

        nonlocal err_no, last_depn, fa_artikel, htparam, fa_op
        nonlocal mat_buff_nr, recid_fa_artikel, user_init
        nonlocal fa_buff


        nonlocal fa_buff


        pass
        fa_op.loeschflag = 1


        pass

        fa_buff = get_cache (Fa_artikel, {"nr": [(eq, fa_artikel.p_nr)]})
        fa_buff.warenwert =  to_decimal(fa_buff.warenwert) - to_decimal(fa_artikel.warenwert)
        fa_buff.book_wert =  to_decimal(fa_buff.book_wert) - to_decimal(fa_artikel.warenwert)


        pass
        pass
        fa_artikel.loeschflag = 0
        fa_artikel.deleted = None
        fa_artikel.did = user_init
        fa_artikel.p_nr = 0


        pass
        err_no = 2

    htparam = get_cache (Htparam, {"paramnr": [(eq, 881)]})
    last_depn = htparam.fdate

    fa_artikel = get_cache (Fa_artikel, {"_recid": [(eq, recid_fa_artikel)]})

    fa_op = get_cache (Fa_op, {"opart": [(eq, 4)],"nr": [(eq, mat_buff_nr)],"datum": [(eq, fa_artikel.deleted)]})

    if fa_op.datum < last_depn:
        err_no = 1

        return generate_output()
    cancel_upgrade()

    return generate_output()