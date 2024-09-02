from functions.additional_functions import *
import decimal
from models import Artikel, Queasy

def write_artikel_1bl(case_type:int, t_artikel:[T_artikel]):
    success_flag = False
    artikel = queasy = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model_like(Artikel, {"rec_id":int, "minibar":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, artikel, queasy


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
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 266
        queasy.number1 = t_artikel.departement
        queasy.number2 = t_artikel.artnr
        queasy.logi1 = t_artikel.minibar


    elif case_type == 2:

        artikel = db_session.query(Artikel).filter(
                (Artikel._recid == t_Artikel.rec_id)).first()

        if artikel:
            buffer_copy(t_artikel, artikel)

            success_flag = True

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 266) &  (Queasy.number1 == t_artikel.departement) &  (Queasy.number2 == t_artikel.artnr)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 266
            queasy.number1 = t_artikel.departement
            queasy.number2 = t_artikel.artnr
            queasy.logi1 = t_artikel.minibar


        else:
            queasy.logi1 = t_artikel.minibar


    return generate_output()