#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezept, H_rezlin, Queasy

def recipe_list_btn_delbl(t_h_rezept_artnrrezept:int):
    h_rezept = h_rezlin = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_rezept, h_rezlin, queasy
        nonlocal t_h_rezept_artnrrezept

        return {}


    h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, t_h_rezept_artnrrezept)]})

    if h_rezept:

        h_rezlin = get_cache (H_rezlin, {"artnrrezept": [(eq, t_h_rezept_artnrrezept)]})
        while None != h_rezlin:
            pass
            db_session.delete(h_rezlin)

            curr_recid = h_rezlin._recid
            h_rezlin = db_session.query(H_rezlin).filter(
                     (H_rezlin.artnrrezept == t_h_rezept_artnrrezept) & (H_rezlin._recid > curr_recid)).first()

        queasy = get_cache (Queasy, {"key": [(eq, 252)],"number1": [(eq, t_h_rezept_artnrrezept)]})

        if queasy:
            pass
            db_session.delete(queasy)
            pass
        pass
        db_session.delete(h_rezept)
        pass

    return generate_output()