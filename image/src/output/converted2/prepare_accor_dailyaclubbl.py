#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam

def prepare_accor_dailyaclubbl():

    prepare_cache ([Htparam])

    bill_date = None
    price_decimal = 0
    foreign_rate = False
    rm_vat = False
    rm_serv = False
    serv_taxable = False
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, price_decimal, foreign_rate, rm_vat, rm_serv, serv_taxable, htparam

        return {"bill_date": bill_date, "price_decimal": price_decimal, "foreign_rate": foreign_rate, "rm_vat": rm_vat, "rm_serv": rm_serv, "serv_taxable": serv_taxable}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
    rm_vat = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 128)]})
    rm_serv = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
    serv_taxable = htparam.flogical

    return generate_output()