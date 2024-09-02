from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Eg_duration, Bediener, Htparam

def prepare_eg_durationbl(user_init:str):
    groupid = 0
    engid = 0
    sduration_list = []
    t_eg_duration_list = []
    eg_duration = bediener = htparam = None

    sduration = t_eg_duration = qbuff = None

    sduration_list, Sduration = create_model("Sduration", {"duration_nr":int, "time_str":str})
    t_eg_duration_list, T_eg_duration = create_model_like(Eg_duration, {"rec_id":int})

    Qbuff = Eg_duration

    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, sduration_list, t_eg_duration_list, eg_duration, bediener, htparam
        nonlocal qbuff


        nonlocal sduration, t_eg_duration, qbuff
        nonlocal sduration_list, t_eg_duration_list
        return {"groupid": groupid, "engid": engid, "sduration": sduration_list, "t-eg-Duration": t_eg_duration_list}

    def create_duration():

        nonlocal groupid, engid, sduration_list, t_eg_duration_list, eg_duration, bediener, htparam
        nonlocal qbuff


        nonlocal sduration, t_eg_duration, qbuff
        nonlocal sduration_list, t_eg_duration_list

        str:str = ""
        Qbuff = Eg_duration
        sduration_list.clear()

        for qbuff in db_session.query(Qbuff).all():

            if qbuff.DAY == 0:
                str = ""
            else:
                str = to_string(qbuff.DAY)

                if qbuff.DAY > 1:
                    str = str + " days "
                else:
                    str = str + " day "

            if qbuff.hour == 0:
                str = str
            else:
                str = str + to_string(qbuff.hour)

                if qbuff.hour > 1:
                    str = str + " hrs "
                else:
                    str = str + " hr "

            if qbuff.minute == 0:
                str = str
            else:
                str = str + to_string(qbuff.minute) + " min "
            sduration = Sduration()
            sduration_list.append(sduration)

            sduration.Duration_nr = qbuff.Duration_nr
            sduration.time_str = str

    def define_group():

        nonlocal groupid, engid, sduration_list, t_eg_duration_list, eg_duration, bediener, htparam
        nonlocal qbuff


        nonlocal sduration, t_eg_duration, qbuff
        nonlocal sduration_list, t_eg_duration_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def define_engineering():

        nonlocal groupid, engid, sduration_list, t_eg_duration_list, eg_duration, bediener, htparam
        nonlocal qbuff


        nonlocal sduration, t_eg_duration, qbuff
        nonlocal sduration_list, t_eg_duration_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    create_duration()
    define_group()
    define_engineering()

    for eg_duration in db_session.query(Eg_duration).all():
        t_eg_duration = T_eg_duration()
        t_eg_duration_list.append(t_eg_duration)

        buffer_copy(eg_Duration, t_eg_duration)
        t_eg_Duration.rec_id = eg_Duration._recid

    return generate_output()