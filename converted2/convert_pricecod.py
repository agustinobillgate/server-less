from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Guest_pr, Ratecode, Pricecod

def convert_pricecod():
    ci_date:date = None
    n:int = 0
    htparam = guest_pr = ratecode = pricecod = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, n, htparam, guest_pr, ratecode, pricecod

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()

    for guest_pr in db_session.query(Guest_pr).order_by(Guest_pr._recid).all():

        ratecode = db_session.query(Ratecode).filter(
                 (Ratecode.code == guest_pr.code)).first()

        if not ratecode:

            for pricecod in db_session.query(Pricecod).filter(
                     (Pricecod.code == guest_pr.code)).order_by(Pricecod._recid).all():
                for n in range(1,4 + 1) :

                    if pricecod.perspreis[n - 1] != 0:
                        ratecode = Ratecode()
                        db_session.add(ratecode)

                        ratecode.code = pricecod.code
                        ratecode.marknr = pricecod.marknr
                        ratecode.zikatnr = pricecod.zikatnr
                        ratecode.argtnr = pricecod.argtnr
                        ratecode.startperiode = pricecod.startperiode
                        ratecode.endperiode = pricecod.endperiode
                        ratecode.erwachs = n
                        ratecode.zipreis =  to_decimal(pricecod.perspreis[n - 1])
                        ratecode.ch1preis =  to_decimal(pricecod.kindpreis[0])
                        ratecode.ch2preis =  to_decimal(pricecod.kindpreis[1])


    return generate_output()