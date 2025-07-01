#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Kontplan, Htparam

def calc_servvat(depart:int, artnr:int, datum:date, service_code:int, mwst_code:int):

    prepare_cache ([Kontplan, Htparam])

    serv_htp = to_decimal("0.0")
    vat_htp = to_decimal("0.0")
    serv_vat:bool = False
    vat:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    kontplan = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal serv_htp, vat_htp, serv_vat, vat, service, kontplan, htparam
        nonlocal depart, artnr, datum, service_code, mwst_code

        return {"serv_htp": serv_htp, "vat_htp": vat_htp}


    kontplan = get_cache (Kontplan, {"betriebsnr": [(eq, depart)],"kontignr": [(eq, artnr)],"datum": [(eq, datum)]})

    if kontplan:

        if kontplan.anzkont >= 10000000:
            serv_htp =  to_decimal(kontplan.anzkont) / to_decimal("10000000")
            vat_htp =  to_decimal(kontplan.anzconf) / to_decimal("10000000")


        else:
            serv_htp =  to_decimal(kontplan.anzkont) / to_decimal("10000")
            vat_htp =  to_decimal(kontplan.anzconf) / to_decimal("10000")


    else:

        if service_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, service_code)]})

            if htparam and htparam.fdecimal != 0:
                serv_htp =  to_decimal(htparam.fdecimal) / to_decimal("100")

                htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
                serv_vat = htparam.flogical

        if mwst_code != 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, mwst_code)]})

            if htparam and htparam.fdecimal != 0:
                vat_htp =  to_decimal(htparam.fdecimal) / to_decimal("100")

            if vat_htp == 1:
                serv_htp =  to_decimal("0")

            elif serv_vat:
                vat_htp =  to_decimal(vat_htp) + to_decimal(vat_htp) * to_decimal(serv_htp)

    return generate_output()