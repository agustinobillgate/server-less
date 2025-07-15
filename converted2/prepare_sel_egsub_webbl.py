#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_subtask, Eg_duration

def prepare_sel_egsub_webbl(main_nr:int, dept_nr:int):

    prepare_cache ([Eg_subtask, Eg_duration])

    q_list_data = []
    eg_subtask = eg_duration = None

    duration = q_list = None

    duration_data, Duration = create_model("Duration", {"dur_nr":int, "dur_str":string})
    q_list_data, Q_list = create_model("Q_list", {"sub_code":string, "bezeich":string, "dur_str":string, "dur_nr":int, "days":string, "hours":string, "minutes":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q_list_data, eg_subtask, eg_duration
        nonlocal main_nr, dept_nr


        nonlocal duration, q_list
        nonlocal duration_data, q_list_data

        return {"q-list": q_list_data}

    def create_list():

        nonlocal q_list_data, eg_subtask, eg_duration
        nonlocal main_nr, dept_nr


        nonlocal duration, q_list
        nonlocal duration_data, q_list_data


        q_list = Q_list()
        q_list_data.append(q_list)

        q_list.sub_code = eg_subtask.sub_code
        q_list.bezeich = eg_subtask.bezeich
        q_list.dur_nr = eg_subtask.dur_nr

        if eg_subtask.dur_nr != 0:

            eg_duration = get_cache (Eg_duration, {"duration_nr": [(eq, eg_subtask.dur_nr)]})

            if eg_duration:
                q_list.days = to_string(eg_duration.DAY)
                q_list.hour = to_string(eg_duration.hour)
                q_list.minutes = to_string(eg_duration.minute)

        elif eg_subtask.reserve_char != "":
            q_list.days = entry(0, eg_subtask.reserve_char, ";")
            q_list.hour = entry(1, eg_subtask.reserve_char, ";")
            q_list.minutes = entry(2, eg_subtask.reserve_char, ";")

    if main_nr == 0 and dept_nr != 0:

        for eg_subtask in db_session.query(Eg_subtask).filter(
                 (Eg_subtask.dept_nr == dept_nr)).order_by(Eg_subtask.sub_code).all():
            create_list()


    elif main_nr == 0 and dept_nr == 0:

        for eg_subtask in db_session.query(Eg_subtask).order_by(Eg_subtask.sub_code).all():
            create_list()

    else:

        for eg_subtask in db_session.query(Eg_subtask).filter(
                 (Eg_subtask.dept_nr == dept_nr) & (Eg_subtask.main_nr == main_nr)).order_by(Eg_subtask.sub_code).all():
            create_list()


    return generate_output()