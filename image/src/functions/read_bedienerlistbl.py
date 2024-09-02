from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Queasy

def read_bedienerlistbl(case_type:int, uname:str):
    t_bediener_list = []
    user_name:str = ""
    htlgrp_code:str = ""
    bediener = queasy = None

    t_bediener = None

    t_bediener_list, T_bediener = create_model_like(Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bediener_list, user_name, htlgrp_code, bediener, queasy


        nonlocal t_bediener
        nonlocal t_bediener_list
        return {"t-bediener": t_bediener_list}

    if case_type == 1:

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.username) == (uname).lower()) &  (Bediener.flag == 0) &  (Bediener.betriebsnr == 1)).first()

        if bediener:
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

        elif uname.lower()  == "sindata":

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.username) == (uname + chr(3))) &  (Bediener.flag == 1) &  (Bediener.betriebsnr == 1)).first()

            if bediener:
                t_bediener = T_bediener()
                t_bediener_list.append(t_bediener)

                buffer_copy(bediener, t_bediener)

        return generate_output()
    elif case_type == 2:

        for bediener in db_session.query(Bediener).filter(
                (func.lower(Bediener.username) == (uname).lower()) &  (Bediener.flag == 0) &  (Bediener.betriebsnr == 1)).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

        t_bediener = query(t_bediener_list, first=True)

        if not t_bediener and uname.lower()  == "sindata":

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.username) == (uname + chr(3))) &  (Bediener.flag == 1) &  (Bediener.betriebsnr == 1)).first()

            if bediener:
                t_bediener = T_bediener()
                t_bediener_list.append(t_bediener)

                buffer_copy(bediener, t_bediener)
    elif case_type == 3:

        for bediener in db_session.query(Bediener).filter(
                (Bediener.flag == 0)).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

    elif case_type == 4:
        user_name = entry(0, uname, chr(2))
        htlgrp_code = entry(1, uname, chr(2))

        if user_name == "" or htlgrp_code == "":

            return generate_output()

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 187) &  (func.lower(Queasy.char1) == (htlgrp_code).lower())).first()

        if not queasy:

            return generate_output()

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.username) == (user_name).lower()) &  (Bediener.flag == 0) &  (Bediener.betriebsnr == 1)).first()

        if bediener:
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)
    elif case_type == 5:

        for bediener in db_session.query(Bediener).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

    elif case_type == 6:

        bediener = db_session.query(Bediener).filter(
                (Bediener.username.op("~")(".*") + chr(2) + "*")).first()

        if bediener:
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

    return generate_output()