from functions.additional_functions import *
import decimal
from models import H_rezept, H_rezlin, Queasy

def recipe_list_btn_delbl(t_h_rezept_artnrrezept:int):
    h_rezept = h_rezlin = queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_rezept, h_rezlin, queasy


        return {}


    h_rezept = db_session.query(H_rezept).filter(
            (H_rezept.artnrrezept == t_h_rezept_artnrrezept)).first()

    h_rezlin = db_session.query(H_rezlin).filter(
            (H_rezlin.artnrrezept == t_h_rezept_artnrrezept)).first()
    while None != h_rezlin:

        h_rezlin = db_session.query(H_rezlin).first()
        db_session.delete(h_rezlin)

        h_rezlin = db_session.query(H_rezlin).filter(
                (H_rezlin.artnrrezept == t_h_rezept_artnrrezept)).first()

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 252) &  (Queasy.number1 == t_h_rezept_artnrrezept)).first()

    if queasy:

        queasy = db_session.query(Queasy).first()
        db_session.delete(queasy)


    h_rezept = db_session.query(H_rezept).first()
    db_session.delete(h_rezept)

    return generate_output()