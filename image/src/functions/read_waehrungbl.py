from functions.additional_functions import *
import decimal
from models import Waehrung

def read_waehrungbl(case_type:int, currencyno:int, currbez:str):
    t_waehrung_list = []
    waehrung = None

    t_waehrung = None

    t_waehrung_list, T_waehrung = create_model_like(Waehrung)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_waehrung_list, waehrung


        nonlocal t_waehrung
        nonlocal t_waehrung_list
        return {"t-waehrung": t_waehrung_list}

    if case_type == 1:

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == currencyno)).first()

        if waehrung:
            t_waehrung = T_waehrung()
            t_waehrung_list.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)
    elif case_type == 2:

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == currbez)).first()

        if waehrung:
            t_waehrung = T_waehrung()
            t_waehrung_list.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)
    elif case_type == 3:

        for waehrung in db_session.query(Waehrung).filter(
                (Waehrung.betriebsnr == 0)).all():
            t_waehrung = T_waehrung()
            t_waehrung_list.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)

    elif case_type == 4:

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.bezeich == currbez)).first()

        if waehrung:
            t_waehrung = T_waehrung()
            t_waehrung_list.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)
    elif case_type == 5:

        for waehrung in db_session.query(Waehrung).filter(
                (Waehrungsnr != currencyno) &  (Waehrung.betriebsnr == 0)).all():
            t_waehrung = T_waehrung()
            t_waehrung_list.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)
    elif case_type == 6:

        for waehrung in db_session.query(Waehrung).filter(
                (Waehrung.betriebsnr == 0) &  (Waehrung.ankauf > 0) &  (Waehrung.wabkurz != currbez)).all():
            t_waehrung = T_waehrung()
            t_waehrung_list.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)
    elif case_type == 7:

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == currencyno) &  (Waehrung.ankauf != 0)).first()

        if waehrung:
            t_waehrung = T_waehrung()
            t_waehrung_list.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)
    elif case_type == 8:

        for waehrung in db_session.query(Waehrung).all():
            t_waehrung = T_waehrung()
            t_waehrung_list.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)

    elif case_type == 9:

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr != currencyno) &  (Waehrung.wabkurz == currbez)).first()

        if waehrung:
            t_waehrung = T_waehrung()
            t_waehrung_list.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)

    return generate_output()