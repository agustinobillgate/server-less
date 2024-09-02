from functions.additional_functions import *
import decimal
from sqlalchemy import func, and_
from models import Bediener, Queasy

def read_bedienerlist_cldbl(case_type:int, uname:str):
    print("read_bedienerlist_cldbl:", case_type, uname)
    t_bediener_list = []
    user_name:str = ""
    htlgrp_code:str = ""
    bediener = queasy = None

    t_bediener = None
    t_bediener, T_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bediener_list, user_name, htlgrp_code, bediener, queasy
        nonlocal case_type, uname

        nonlocal t_bediener
        nonlocal t_bediener_list
        return {"t-bediener": t_bediener_list}

    if case_type == 1:
        bediener = db_session.query(Bediener).filter(and_
                    (func.lower(Bediener.username) == uname.lower()),
                    (Bediener.flag == 0),
                    (Bediener.betriebsnr == 1)
                ).first()
        if bediener:
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)
            buffer_copy(bediener, t_bediener)
        elif uname.lower()  == "sindata":
            uname_chr3 = uname.lower() + chr(3)
            bediener = db_session.query(Bediener).filter(and_
                            (func.lower(Bediener.username) == uname_chr3.lower()),
                            (Bediener.flag == 1),
                            (Bediener.betriebsnr == 1)
                        ).first()
            if bediener:
                t_bediener = T_bediener()
                t_bediener_list.append(t_bediener)
                buffer_copy(bediener, t_bediener)
            else:
                print("ada 'sindata, tidak ada 1-1")

        return generate_output()
    elif case_type == 2:
        print("Case:2")
        for bediener in db_session.query(Bediener).filter(
                (func.lower(Bediener.username) == uname.lower()) &  (Bediener.flag == 0) &  (Bediener.betriebsnr == 1)).order_by(Bediener._recid).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

        if not t_bediener:
            t_bediener = query(t_bediener_list, first=True)

        if not t_bediener and uname.lower()  == ("sindata").lower() :

            if not bediener or not(bediener.username.lower()  == ((uname + chr(3)).lower()) and bediener.flag == 1 and bediener.betriebsnr == 1):
                bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.username) == ((uname + chr(3)).lower())) &  (Bediener.flag == 1) &  (Bediener.betriebsnr == 1)).first()

            if bediener:
                t_bediener = T_bediener()
                t_bediener_list.append(t_bediener)

                buffer_copy(bediener, t_bediener)
    elif case_type == 3:
        print("Case:3")
        for bediener in db_session.query(Bediener).filter(
                (Bediener.flag == 0)).order_by(Bediener.username).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)
    elif case_type == 4:
        print("Case:4")
        user_name = entry(0, uname, chr(2))
        htlgrp_code = entry(1, uname, chr(2))

        if user_name == "" or htlgrp_code == "":

            return generate_output()

        if not queasy or not(queasy.key == 187 and queasy.char1.lower()  == htlgrp_code.lower()):
            queasy = db_session.query(Queasy).filter(
                (Queasy.key == 187) &  (func.lower(Queasy.char1) == htlgrp_code.lower())).first()

        if not queasy:

            return generate_output()

        if not bediener or not(bediener.username.lower()  == user_name.lower()  and bediener.flag == 0 and bediener.betriebsnr == 1):
            bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.username) == user_name.lower()) &  (Bediener.flag == 0) &  (Bediener.betriebsnr == 1)).first()

        if bediener:
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)
    elif case_type == 5:
        print("Case:5")
        for bediener in db_session.query(Bediener).order_by(Bediener._recid).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

    elif case_type == 6:
        print("Case:6")
        if not bediener or not(re.match((".*" + chr(2) + ".*"),bediener.username, re.IGNORECASE)):
            bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.username).op("~")(("*" + chr(2) + "*").lower().replace("*",".*")))).first()

        if bediener:
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

    return generate_output()