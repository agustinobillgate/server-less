from functions.additional_functions import *
import decimal
from datetime import date
from models import Kontplan, Htparam

def calc_servvat(depart:int, artnr:int, datum:date, service_code:int, mwst_code:int):
    serv_htp = 0
    vat_htp = 0
    serv_vat:bool = False
    vat:decimal = 0
    service:decimal = 0
    kontplan = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal serv_htp, vat_htp, serv_vat, vat, service, kontplan, htparam


        return {"serv_htp": serv_htp, "vat_htp": vat_htp}


    kontplan = db_session.query(Kontplan).filter(
            (Kontplan.betriebsnr == depart) &  (Kontplan.kontignr == artnr) &  (Kontplan.datum == datum)).first()

    if kontplan:

        if kontplan.anzkont >= 10000000:
            serv_htp = kontplan.anzkont / 10000000
            vat_htp = kontplan.anzconf / 10000000


        else:
            serv_htp = kontplan.anzkont / 10000
            vat_htp = kontplan.anzconf / 10000


    else:

        if service_code != 0:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == service_code)).first()

            if htparam and htparam.fdecimal != 0:
                serv_htp = htparam.fdecimal / 100

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 479)).first()
                serv_vat = htparam.flogical

        if mwst_code != 0:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == mwst_code)).first()

            if htparam and htparam.fdecimal != 0:
                vat_htp = htparam.fdecimal / 100

            if vat_htp == 1:
                serv_htp = 0

            elif serv_vat:
                vat_htp = vat_htp + vat_htp * serv_htp

    return generate_output()