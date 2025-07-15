#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_journal

def rest_journal_btn_sviewbl(h_recid:int):

    prepare_cache ([H_journal])

    t_rechnr = 0
    t_departement = 0
    t_bill_datum = None
    h_journal = None

    h_jou = None

    H_jou = create_buffer("H_jou",H_journal)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_rechnr, t_departement, t_bill_datum, h_journal
        nonlocal h_recid
        nonlocal h_jou


        nonlocal h_jou

        return {"t_rechnr": t_rechnr, "t_departement": t_departement, "t_bill_datum": t_bill_datum}


    h_jou = get_cache (H_journal, {"_recid": [(eq, h_recid)]})
    t_rechnr = h_jou.rechnr
    t_departement = h_jou.departement
    t_bill_datum = h_jou.bill_datum

    return generate_output()