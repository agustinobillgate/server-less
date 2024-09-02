from functions.additional_functions import *
import decimal
from datetime import date
from models import Kontline, Queasy

def write_kontlinebl(case_type:int, t_kontline:[T_kontline]):
    success_flag = False
    curr_date:date = None
    kontline = queasy = None

    t_kontline = qsy = None

    t_kontline_list, T_kontline = create_model_like(Kontline)

    Qsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, curr_date, kontline, queasy
        nonlocal qsy


        nonlocal t_kontline, qsy
        nonlocal t_kontline_list
        return {"success_flag": success_flag}

    t_kontline = query(t_kontline_list, first=True)

    if not t_kontline:

        return generate_output()

    if case_type == 1:
        for curr_date in range(t_kontline.ankunft,t_kontline.abreise + 1) :

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 171) &  (Queasy.date1 == curr_date) &  (Queasy.number1 == t_kontline.zikatnr) &  (Queasy.char1 == "")).first()

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                qsy = db_session.query(Qsy).filter(
                        (Qsy._recid == queasy._recid)).first()

                if qsy:
                    qsy.logi2 = True

                    qsy = db_session.query(Qsy).first()


        kontline = db_session.query(Kontline).filter(
                (Kontline.kontignr == t_Kontline.kontignr)).first()

        if kontline:
            buffer_copy(t_kontline, kontline)

            kontline = db_session.query(Kontline).first()
            success_flag = True
    elif case_type == 2:
        for curr_date in range(t_kontline.ankunft,t_kontline.abreise + 1) :

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 171) &  (Queasy.date1 == curr_date) &  (Queasy.number1 == t_kontline.zikatnr) &  (Queasy.char1 == "")).first()

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                qsy = db_session.query(Qsy).filter(
                        (Qsy._recid == queasy._recid)).first()

                if qsy:
                    qsy.logi2 = True

                    qsy = db_session.query(Qsy).first()

        kontline = Kontline()
        db_session.add(kontline)

        buffer_copy(t_kontline, kontline)
        success_flag = True

        kontline = db_session.query(Kontline).first()

    return generate_output()