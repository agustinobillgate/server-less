#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_duration

def prepare_sel_egdurbl():

    prepare_cache ([Eg_duration])

    q_list_data = []
    eg_duration = None

    sduration = q_list = None

    sduration_data, Sduration = create_model("Sduration", {"duration_nr":int, "time_str":string})
    q_list_data, Q_list = create_model("Q_list", {"duration_nr":int, "time_str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q_list_data, eg_duration


        nonlocal sduration, q_list
        nonlocal sduration_data, q_list_data

        return {"q-list": q_list_data}

    def create_duration():

        nonlocal q_list_data, eg_duration


        nonlocal sduration, q_list
        nonlocal sduration_data, q_list_data

        qbuff = None
        str:string = ""
        Qbuff =  create_buffer("Qbuff",Eg_duration)
        sduration_data.clear()

        for qbuff in db_session.query(Qbuff).order_by(Qbuff.duration_nr).all():

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
                    str = str + " hour "

            if qbuff.minute == 0:
                str = str
            else:
                str = str + to_string(qbuff.minute) + " min "
            sduration = Sduration()
            sduration_data.append(sduration)

            sduration.duration_nr = qbuff.Duration_nr
            sduration.time_str = str


    create_duration()

    eg_duration_obj_list = {}
    for eg_duration in db_session.query(Eg_duration).order_by(Eg_duration.duration_nr).all():
        sduration = query(sduration_data, (lambda sduration: sduration.Duration_nr == eg_duration.Duration_nr), first=True)
        if not sduration:
            continue

        if eg_duration_obj_list.get(eg_duration._recid):
            continue
        else:
            eg_duration_obj_list[eg_duration._recid] = True


        q_list = Q_list()
        q_list_data.append(q_list)

        q_list.duration_nr = eg_duration.Duration_nr
        q_list.time_str = sduration.time_str

    return generate_output()