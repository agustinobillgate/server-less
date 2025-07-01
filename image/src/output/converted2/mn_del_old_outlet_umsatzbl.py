#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Hoteldpt, Artikel, Umsatz

def mn_del_old_outlet_umsatzbl():

    prepare_cache ([Htparam, Hoteldpt, Artikel])

    i = 0
    htparam = hoteldpt = artikel = umsatz = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, htparam, hoteldpt, artikel, umsatz

        return {"i": i}

    def del_old_outlet_umsatz():

        nonlocal i, htparam, hoteldpt, artikel, umsatz

        billdate:date = None

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        billdate = htparam.fdate

        for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():

            for artikel in db_session.query(Artikel).filter(
                     (Artikel.departement == hoteldpt.num) & (Artikel.artart == 1) & (Artikel.activeflag)).order_by(Artikel._recid).all():

                umsatz = get_cache (Umsatz, {"artnr": [(eq, artikel.artnr)],"departement": [(eq, artikel.departement)],"datum": [(le, (billdate - 14))]})
                while None != umsatz:
                    i = i + 1
                    pass
                    db_session.delete(umsatz)

                    curr_recid = umsatz._recid
                    umsatz = db_session.query(Umsatz).filter(
                             (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement) & (Umsatz.datum <= (billdate - timedelta(days=14))) & (Umsatz._recid > curr_recid)).first()


    del_old_outlet_umsatz()

    return generate_output()