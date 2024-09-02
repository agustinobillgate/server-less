from functions.additional_functions import *
import decimal
from models import Mathis

def fa_mkpo_check_mathisbl(art_nr:int, t_mathis:[T_mathis]):
    avail_mathis = False
    mathis = None

    t_mathis = None

    t_mathis_list, T_mathis = create_model_like(Mathis)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_mathis, mathis


        nonlocal t_mathis
        nonlocal t_mathis_list
        return {"avail_mathis": avail_mathis}

    mathis = db_session.query(Mathis).filter(
            (Mathis.nr == art_nr)).first()

    if not mathis:
        avail_mathis = False

    for mathis in db_session.query(Mathis).filter(
            (Mathis.nr == art_nr)).all():
        t_mathis = T_mathis()
        t_mathis_list.append(t_mathis)

        buffer_copy(mathis, t_mathis)

    return generate_output()