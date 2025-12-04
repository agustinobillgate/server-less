#using conversion tools version: 1.0.0.119

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

    h_rezept = db_session.query(H_rezept).filter(H_rezept.artnrrezept == t_h_rezept_artnrrezept).first()

    if h_rezept:

        h_rezlin = db_session.query(H_rezlin).filter(H_rezlin.artnrrezept == t_h_rezept_artnrrezept).first()

        while None != h_rezlin:
            db_session.refresh(h_rezlin, with_for_update=True)

            db_session.delete(h_rezlin)

            db_session.flush()

            curr_recid = h_rezlin._recid
            h_rezlin = db_session.query(H_rezlin).filter(
                     (H_rezlin.artnrrezept == t_h_rezept_artnrrezept) & (H_rezlin._recid > curr_recid)).first()

        queasy = db_session.query(Queasy).filter((Queasy.key == 252) & (Queasy.number1 == t_h_rezept_artnrrezept)).first()

        if queasy:
            db_session.refresh(queasy, with_for_update=True)
            db_session.delete(queasy)
            db_session.flush()
        
        db_session.refresh(h_rezept, with_for_update=True)
        db_session.delete(h_rezept)
        db_session.flush()

    return generate_output()