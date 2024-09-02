from functions.additional_functions import *
import decimal
from models import Tisch

def read_tischbl(i_case:int, dept:int, tableno:int):
    t_tisch_list = []
    tisch = None

    t_tisch = None

    t_tisch_list, T_tisch = create_model_like(Tisch)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_tisch_list, tisch


        nonlocal t_tisch
        nonlocal t_tisch_list
        return {"t-tisch": t_tisch_list}

    if i_case == 1:

        if dept == 0:

            for tisch in db_session.query(Tisch).all():
                t_tisch = T_tisch()
                t_tisch_list.append(t_tisch)

                buffer_copy(tisch, t_tisch)

        else:

            for tisch in db_session.query(Tisch).filter(
                    (Tisch.departement == dept)).all():
                t_tisch = T_tisch()
                t_tisch_list.append(t_tisch)

                buffer_copy(tisch, t_tisch)

    elif i_case == 2:

        tisch = db_session.query(Tisch).filter(
                (Tisch.departement == dept) &  (Tischnr == tableno)).first()

        if tisch:
            t_tisch = T_tisch()
            t_tisch_list.append(t_tisch)

            buffer_copy(tisch, t_tisch)

    return generate_output()