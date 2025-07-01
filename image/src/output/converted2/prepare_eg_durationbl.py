#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_duration, Bediener, Htparam

def prepare_eg_durationbl(user_init:string):

    prepare_cache ([Bediener, Htparam])

    groupid = 0
    engid = 0
    sduration_list = []
    t_eg_duration_list = []
    eg_duration = bediener = htparam = None

    sduration = t_eg_duration = None

    sduration_list, Sduration = create_model("Sduration", {"duration_nr":int, "time_str":string})
    t_eg_duration_list, T_eg_duration = create_model_like(Eg_duration, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, sduration_list, t_eg_duration_list, eg_duration, bediener, htparam
        nonlocal user_init


        nonlocal sduration, t_eg_duration
        nonlocal sduration_list, t_eg_duration_list

        return {"groupid": groupid, "engid": engid, "sduration": sduration_list, "t-eg-Duration": t_eg_duration_list}

    def create_duration():

        nonlocal groupid, engid, sduration_list, t_eg_duration_list, eg_duration, bediener, htparam
        nonlocal user_init


        nonlocal sduration, t_eg_duration
        nonlocal sduration_list, t_eg_duration_list

        qbuff = None
        str:string = ""
        Qbuff =  create_buffer("Qbuff",Eg_duration)
        sduration_list.clear()

        for qbuff in db_session.query(Qbuff).order_by(Qbuff.duration_nr).all():

            if qbuff.days == 0:
                str = ""
            else:
                str = to_string(qbuff.days)

                if qbuff.days > 1:
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

            sduration.duration_nr = qbuff.duration_nr
            sduration.time_str = str


    def define_group():

        nonlocal groupid, engid, sduration_list, t_eg_duration_list, eg_duration, bediener, htparam
        nonlocal user_init


        nonlocal sduration, t_eg_duration
        nonlocal sduration_list, t_eg_duration_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def define_engineering():

        nonlocal groupid, engid, sduration_list, t_eg_duration_list, eg_duration, bediener, htparam
        nonlocal user_init


        nonlocal sduration, t_eg_duration
        nonlocal sduration_list, t_eg_duration_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    create_duration()
    define_group()
    define_engineering()

    for eg_duration in db_session.query(Eg_duration).order_by(Eg_duration._recid).all():
        t_eg_duration = T_eg_duration()
        t_eg_duration_list.append(t_eg_duration)

        buffer_copy(eg_duration, t_eg_duration)
        t_eg_duration.rec_id = eg_duration._recid

    return generate_output()