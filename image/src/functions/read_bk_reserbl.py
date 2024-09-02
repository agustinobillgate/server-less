from functions.additional_functions import *
import decimal
from datetime import date
from models import Bk_reser

def read_bk_reserbl(case_type:int, veranno:int, datum:date, resstatus:int, zeit:int):
    t_bk_reser_list = []
    bk_reser = None

    t_bk_reser = None

    t_bk_reser_list, T_bk_reser = create_model_like(Bk_reser)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bk_reser_list, bk_reser


        nonlocal t_bk_reser
        nonlocal t_bk_reser_list
        return {"t-bk-reser": t_bk_reser_list}

    if case_type == 1:

        bk_reser = db_session.query(Bk_reser).filter(
                (Bk_reser.veran_nr == veranno) &  (Bk_reser.datum > datum) &  (Bk_reser.resstatus <= resstatus)).first()

        if bk_reser:
            t_bk_reser = T_bk_reser()
            t_bk_reser_list.append(t_bk_reser)

            buffer_copy(bk_reser, t_bk_reser)
    elif case_type == 2:

        t_bk_reser = query(t_bk_reser_list, filters=(lambda t_bk_reser :t_bk_reser.veran_nr == veranno and t_bk_reser.datum == datum and t_bk_reser.resstatus == resstatus and (t_bk_reser.bis_i * 1800) > zeit), first=True)

        if bk_reser:
            t_bk_reser = T_bk_reser()
            t_bk_reser_list.append(t_bk_reser)

            buffer_copy(bk_reser, t_bk_reser)
    elif case_type == 3:

        for bk_reser in db_session.query(Bk_reser).filter(
                (Bk_reser.veran_nr == veranno) &  (Bk_reser.resstatus == resstatus)).all():
            t_bk_reser = T_bk_reser()
            t_bk_reser_list.append(t_bk_reser)

            buffer_copy(bk_reser, t_bk_reser)
    elif case_type == 4:

        bk_reser = db_session.query(Bk_reser).filter(
                (Bk_reser.veran_nr == veranno) &  (Bk_reser.resstatus == resstatus)).first()

        if bk_reser:
            t_bk_reser = T_bk_reser()
            t_bk_reser_list.append(t_bk_reser)

            buffer_copy(bk_reser, t_bk_reser)
    elif case_type == 5:

        for bk_reser in db_session.query(Bk_reser).filter(
                (Bk_reser.veran_nr == veranno) &  (Bk_reser.resstatus != resstatus)).all():
            t_bk_reser = T_bk_reser()
            t_bk_reser_list.append(t_bk_reser)

            buffer_copy(bk_reser, t_bk_reser)

    return generate_output()