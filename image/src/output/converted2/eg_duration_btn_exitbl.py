#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_duration

duration_list, Duration = create_model_like(Eg_duration)

def eg_duration_btn_exitbl(duration_list:[Duration], case_type:int, rec_id:int):

    prepare_cache ([Eg_duration])

    fl_code = 0
    sduration_list = []
    eg_duration = None

    sduration = duration = queasy1 = None

    sduration_list, Sduration = create_model("Sduration", {"duration_nr":int, "time_str":string})

    Queasy1 = create_buffer("Queasy1",Eg_duration)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, sduration_list, eg_duration
        nonlocal case_type, rec_id
        nonlocal queasy1


        nonlocal sduration, duration, queasy1
        nonlocal sduration_list

        return {"fl_code": fl_code, "sduration": sduration_list}

    def fill_new_queasy():

        nonlocal fl_code, sduration_list, eg_duration
        nonlocal case_type, rec_id
        nonlocal queasy1


        nonlocal sduration, duration, queasy1
        nonlocal sduration_list


        eg_duration.duration_nr = duration.duration_nr
        eg_duration.days = duration.days
        eg_duration.hour = duration.hour
        eg_duration.minute = duration.minute


    def create_duration():

        nonlocal fl_code, sduration_list, eg_duration
        nonlocal case_type, rec_id
        nonlocal queasy1


        nonlocal sduration, duration, queasy1
        nonlocal sduration_list

        qbuff = None
        str:string = ""
        tmp_days:int = 0
        Qbuff =  create_buffer("Qbuff",Eg_duration)
        sduration_list.clear()

        for qbuff in db_session.query(Qbuff).order_by(Qbuff.duration_nr).all():
            tmp_days = to_int(qbuff.days)

            if tmp_days == 0:
                str = ""
            else:
                str = to_string(tmp_days)

                if tmp_days > 1:
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

    duration = query(duration_list, first=True)

    if case_type == 1:

        queasy1 = get_cache (Eg_duration, {"duration_nr": [(eq, duration.duration_nr)]})

        if queasy1:
            fl_code = 1
        else:

            queasy1 = get_cache (Eg_duration, {"days": [(eq, duration.days)],"hour": [(eq, duration.hour)],"minute": [(eq, duration.minute)]})

            if queasy1:
                fl_code = 2
            else:
                eg_duration = Eg_duration()
                db_session.add(eg_duration)

                fill_new_queasy()
                pass
                fl_code = 3
                create_duration()

    elif case_type == 2:

        eg_duration = get_cache (Eg_duration, {"_recid": [(eq, rec_id)]})

        if eg_duration:

            queasy1 = get_cache (Eg_duration, {"duration_nr": [(eq, duration.duration_nr)],"_recid": [(ne, eg_duration._recid)]})

            if queasy1:
                fl_code = 1
            else:

                queasy1 = get_cache (Eg_duration, {"days": [(eq, duration.days)],"hour": [(eq, duration.hour)],"minute": [(eq, duration.minute)],"_recid": [(ne, eg_duration._recid)]})

                if queasy1:
                    fl_code = 2
                else:
                    pass
                    eg_duration.duration_nr = duration.Duration_nr
                    eg_duration.days = duration.days
                    eg_duration.hour = duration.hour
                    eg_duration.minute = duration.minute
                    pass
                    pass
                    fl_code = 3
                    create_duration()

    return generate_output()