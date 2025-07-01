#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Bediener, Queasy

def read_bedienerlistbl(case_type:int, uname:string):
    t_bediener_list = []
    user_name:string = ""
    htlgrp_code:string = ""
    bediener = queasy = None

    t_bediener = None

    t_bediener_list, T_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bediener_list, user_name, htlgrp_code, bediener, queasy
        nonlocal case_type, uname


        nonlocal t_bediener
        nonlocal t_bediener_list

        return {"t-bediener": t_bediener_list}

    if case_type == 1:

        bediener = get_cache (Bediener, {"username": [(eq, uname)],"flag": [(eq, 0)],"betriebsnr": [(eq, 1)]})

        if bediener:
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

        elif uname.lower()  == ("sindata").lower() :

            bediener = get_cache (Bediener, {"username": [(eq, (uname + chr_unicode(3)))],"flag": [(eq, 1)],"betriebsnr": [(eq, 1)]})

            if bediener:
                t_bediener = T_bediener()
                t_bediener_list.append(t_bediener)

                buffer_copy(bediener, t_bediener)

        return generate_output()
    elif case_type == 2:

        for bediener in db_session.query(Bediener).filter(
                 (Bediener.username == (uname).lower()) & (Bediener.flag == 0) & (Bediener.betriebsnr == 1)).order_by(Bediener._recid).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

        t_bediener = query(t_bediener_list, first=True)

        if not t_bediener and uname.lower()  == ("sindata").lower() :

            bediener = get_cache (Bediener, {"username": [(eq, (uname + chr_unicode(3)))],"flag": [(eq, 1)],"betriebsnr": [(eq, 1)]})

            if bediener:
                t_bediener = T_bediener()
                t_bediener_list.append(t_bediener)

                buffer_copy(bediener, t_bediener)
    elif case_type == 3:

        for bediener in db_session.query(Bediener).filter(
                 (Bediener.flag == 0)).order_by(Bediener.username).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

    elif case_type == 4:
        user_name = entry(0, uname, chr_unicode(2))
        htlgrp_code = entry(1, uname, chr_unicode(2))

        if user_name == "" or htlgrp_code == "":

            return generate_output()

        queasy = get_cache (Queasy, {"key": [(eq, 187)],"char1": [(eq, htlgrp_code)]})

        if not queasy:

            return generate_output()

        bediener = get_cache (Bediener, {"username": [(eq, user_name)],"flag": [(eq, 0)],"betriebsnr": [(eq, 1)]})

        if bediener:
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)
    elif case_type == 5:

        for bediener in db_session.query(Bediener).order_by(Bediener._recid).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

    elif case_type == 6:

        bediener = db_session.query(Bediener).filter(
                 (matches(Bediener.username,"*" + chr_unicode(2) + "*"))).first()

        if bediener:
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

    return generate_output()