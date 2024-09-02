from functions.additional_functions import *
import decimal
from models import Eg_duration

def eg_duration_btn_exitbl(duration:[Duration], case_type:int, rec_id:int):
    fl_code = 0
    sduration_list = []
    eg_duration = None

    sduration = duration = queasy1 = qbuff = None

    sduration_list, Sduration = create_model("Sduration", {"duration_nr":int, "time_str":str})
    duration_list, Duration = create_model_like(Eg_duration)

    Queasy1 = Eg_duration
    Qbuff = Eg_duration

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, sduration_list, eg_duration
        nonlocal queasy1, qbuff


        nonlocal sduration, duration, queasy1, qbuff
        nonlocal sduration_list, duration_list
        return {"fl_code": fl_code, "sduration": sduration_list}

    def fill_new_queasy():

        nonlocal fl_code, sduration_list, eg_duration
        nonlocal queasy1, qbuff


        nonlocal sduration, duration, queasy1, qbuff
        nonlocal sduration_list, duration_list


        eg_Duration.Duration_nr = duration.Duration_nr
        eg_Duration.DAY = duration.DAY
        eg_Duration.hour = duration.hour
        eg_Duration.minute = duration.minute

    def create_duration():

        nonlocal fl_code, sduration_list, eg_duration
        nonlocal queasy1, qbuff


        nonlocal sduration, duration, queasy1, qbuff
        nonlocal sduration_list, duration_list

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


    duration = query(duration_list, first=True)

    if case_type == 1:

        queasy1 = db_session.query(Queasy1).filter(
                (Queasy1.Duration_nr == duration.Duration_nr)).first()

        if queasy1:
            fl_code = 1
        else:

            queasy1 = db_session.query(Queasy1).filter(
                    (Queasy1.DAY == duration.DAY) &  (Queasy1.hour == duration.hour) &  (Queasy1.minute == duration.minute)).first()

            if queasy1:
                fl_code = 2
            else:
                eg_duration = Eg_duration()
                db_session.add(eg_duration)

                fill_new_queasy()

                fl_code = 3
                create_duration()

    elif case_type == 2:

        eg_duration = db_session.query(Eg_duration).filter(
                (eg_Duration._recid == rec_id)).first()

        queasy1 = db_session.query(Queasy1).filter(
                (Queasy1.Duration_nr == duration.Duration_nr) &  (Queasy1._recid != eg_Duration._recid)).first()

        if queasy1:
            fl_code = 1
        else:

            queasy1 = db_session.query(Queasy1).filter(
                    (Queasy1.DAY == duration.DAY) &  (Queasy1.hour == duration.hour) &  (Queasy1.minute == duration.minute) &  (Queasy1._recid != eg_Duration._recid)).first()

            if queasy1:
                fl_code = 2
            else:

                eg_duration = db_session.query(Eg_duration).first()
                eg_Duration.Duration_nr = duration.Duration_nr
                eg_Duration.DAY = duration.DAY
                eg_Duration.hour = duration.hour
                eg_Duration.minute = duration.minute

                eg_duration = db_session.query(Eg_duration).first()

                fl_code = 3
                create_duration()

    return generate_output()