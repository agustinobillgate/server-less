#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, H_rezept

def prepare_export_recipebl():

    prepare_cache ([Htparam, H_rezept])

    price_type = 0
    from_artnr = 0
    to_artnr = 0
    from_kateg = 0
    to_kateg = 0
    htparam = h_rezept = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_type, from_artnr, to_artnr, from_kateg, to_kateg, htparam, h_rezept

        return {"price_type": price_type, "from_artnr": from_artnr, "to_artnr": to_artnr, "from_kateg": from_kateg, "to_kateg": to_kateg}

    def cal_nr():

        nonlocal price_type, from_artnr, to_artnr, from_kateg, to_kateg, htparam, h_rezept


        from_artnr = 999999
        to_artnr = 0
        from_kateg = 999999
        to_kateg = 0

        for h_rezept in db_session.query(H_rezept).order_by(H_rezept._recid).all():

            if h_rezept.artnrrezept > to_artnr:
                to_artnr = h_rezept.artnrrezept

            if h_rezept.artnrrezept < from_artnr:
                from_artnr = h_rezept.artnrrezept

            if h_rezept.kategorie > to_kateg:
                to_kateg = h_rezept.kategorie

            if h_rezept.kategorie < from_kateg:
                from_kateg = h_rezept.kategorie

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1024)]})
    price_type = htparam.finteger
    cal_nr()

    return generate_output()