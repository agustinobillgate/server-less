from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Hoteldpt, Artikel, Umsatz

def mn_del_old_outlet_umsatzbl():
    i = 0
    htparam = hoteldpt = artikel = umsatz = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, htparam, hoteldpt, artikel, umsatz


        return {"i": i}

    def del_old_outlet_umsatz():

        nonlocal i, htparam, hoteldpt, artikel, umsatz

        billdate:date = None

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        billdate = htparam.fdate

        for hoteldpt in db_session.query(Hoteldpt).all():

            for artikel in db_session.query(Artikel).filter(
                    (Artikel.departement == hoteldpt.num) &  (Artikel.artart == 1) &  (Artikel.activeflag)).all():

                umsatz = db_session.query(Umsatz).filter(
                        (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum <= (billdate - 14))).first()
                while None != umsatz:
                    i = i + 1

                    umsatz = db_session.query(Umsatz).first()
                    db_session.delete(umsatz)


                    umsatz = db_session.query(Umsatz).filter(
                            (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum <= (billdate - 14))).first()

    del_old_outlet_umsatz()

    return generate_output()