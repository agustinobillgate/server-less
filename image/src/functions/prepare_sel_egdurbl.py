from functions.additional_functions import *
import decimal
from models import Eg_duration

def prepare_sel_egdurbl():
    q_list_list = []
    eg_duration = None

    sduration = q_list = qbuff = None

    sduration_list, Sduration = create_model("Sduration", {"duration_nr":int, "time_str":str})
    q_list_list, Q_list = create_model("Q_list", {"duration_nr":int, "time_str":str})

    Qbuff = Eg_duration

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q_list_list, eg_duration
        nonlocal qbuff


        nonlocal sduration, q_list, qbuff
        nonlocal sduration_list, q_list_list
        return {"q-list": q_list_list}

    def create_duration():

        nonlocal q_list_list, eg_duration
        nonlocal qbuff


        nonlocal sduration, q_list, qbuff
        nonlocal sduration_list, q_list_list

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
                    str = str + " hour "

            if qbuff.minute == 0:
                str = str
            else:
                str = str + to_string(qbuff.minute) + " min "
            sduration = Sduration()
            sduration_list.append(sduration)

            sduration.Duration_nr = qbuff.Duration_nr
            sduration.time_str = str

    create_duration()

    eg_duration_obj_list = []
    for eg_duration, sduration in db_session.query(Eg_duration, Sduration).join(Sduration,(Sduration.Duration_nr == eg_Duration.Duration_nr)).all():
        if eg_duration._recid in eg_duration_obj_list:
            continue
        else:
            eg_duration_obj_list.append(eg_duration._recid)


        q_list = Q_list()
        q_list_list.append(q_list)

        q_list.Duration_nr = eg_Duration.Duration_nr
        q_list.time_str = sduration.time_str

    return generate_output()