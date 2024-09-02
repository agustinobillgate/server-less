from functions.additional_functions import *
import decimal
from models import Mathis, Fa_artikel

def fa_artlist_btn_delbl(mathis_nr:int):
    mathis = fa_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mathis, fa_artikel


        return {}


    mathis = db_session.query(Mathis).filter(
            (Mathis.nr == mathis_nr)).first()

    if mathis:

        mathis = db_session.query(Mathis).first()
        db_session.delete(mathis)


    fa_artikel = db_session.query(Fa_artikel).filter(
            (Fa_artikel.nr == mathis.nr)).first()

    if fa_artikel:

        fa_artikel = db_session.query(Fa_artikel).first()
        db_session.delete(fa_artikel)


    return generate_output()