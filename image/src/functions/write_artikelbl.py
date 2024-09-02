from functions.additional_functions import *
import decimal
from models import Artikel

def write_artikelbl(case_type:int, t_artikel:[T_artikel]):
    success_flag = False
    artikel = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model_like(Artikel, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, artikel


        nonlocal t_artikel
        nonlocal t_artikel_list
        return {"success_flag": success_flag}

    t_artikel = query(t_artikel_list, first=True)

    if not t_artikel:

        return generate_output()

    if case_type == 1:
        artikel = Artikel()
        db_session.add(artikel)

        buffer_copy(t_artikel, artikel)

        success_flag = True
    elif case_type == 2:

        artikel = db_session.query(Artikel).filter(
                (Artikel._recid == t_Artikel.rec_id)).first()

        if artikel:
            buffer_copy(t_artikel, artikel)

            success_flag = True

    return generate_output()