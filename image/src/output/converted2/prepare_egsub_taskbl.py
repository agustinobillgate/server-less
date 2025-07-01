#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_subtask, Queasy, Eg_request, Htparam, Bediener, Eg_duration

def prepare_egsub_taskbl(user_init:string):

    prepare_cache ([Queasy, Htparam, Bediener])

    engid = 0
    groupid = 0
    department_list = []
    maintask_list = []
    sduration_list = []
    dept_link_list = []
    t_eg_subtask_list = []
    t_eg_request_list = []
    queasy_133_list = []
    eg_subtask = queasy = eg_request = htparam = bediener = eg_duration = None

    t_eg_subtask = department = maintask = sduration = dept_link = queasy_133 = t_eg_request = None

    t_eg_subtask_list, T_eg_subtask = create_model_like(Eg_subtask, {"rec_id":int})
    department_list, Department = create_model("Department", {"dept_nr":int, "department":string})
    maintask_list, Maintask = create_model("Maintask", {"main_nr":int, "maintask":string, "main_grp":string})
    sduration_list, Sduration = create_model("Sduration", {"duration_nr":int, "time_str":string})
    dept_link_list, Dept_link = create_model("Dept_link", {"dept_nr":int, "dept_nm":string})
    queasy_133_list, Queasy_133 = create_model_like(Queasy)
    t_eg_request_list, T_eg_request = create_model_like(Eg_request)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, department_list, maintask_list, sduration_list, dept_link_list, t_eg_subtask_list, t_eg_request_list, queasy_133_list, eg_subtask, queasy, eg_request, htparam, bediener, eg_duration
        nonlocal user_init


        nonlocal t_eg_subtask, department, maintask, sduration, dept_link, queasy_133, t_eg_request
        nonlocal t_eg_subtask_list, department_list, maintask_list, sduration_list, dept_link_list, queasy_133_list, t_eg_request_list

        return {"engid": engid, "groupid": groupid, "department": department_list, "maintask": maintask_list, "sduration": sduration_list, "dept-link": dept_link_list, "t-eg-subtask": t_eg_subtask_list, "t-eg-request": t_eg_request_list, "queasy-133": queasy_133_list}

    def define_engineering():

        nonlocal engid, groupid, department_list, maintask_list, sduration_list, dept_link_list, t_eg_subtask_list, t_eg_request_list, queasy_133_list, eg_subtask, queasy, eg_request, htparam, bediener, eg_duration
        nonlocal user_init


        nonlocal t_eg_subtask, department, maintask, sduration, dept_link, queasy_133, t_eg_request
        nonlocal t_eg_subtask_list, department_list, maintask_list, sduration_list, dept_link_list, queasy_133_list, t_eg_request_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            pass


    def define_group():

        nonlocal engid, groupid, department_list, maintask_list, sduration_list, dept_link_list, t_eg_subtask_list, t_eg_request_list, queasy_133_list, eg_subtask, queasy, eg_request, htparam, bediener, eg_duration
        nonlocal user_init


        nonlocal t_eg_subtask, department, maintask, sduration, dept_link, queasy_133, t_eg_request
        nonlocal t_eg_subtask_list, department_list, maintask_list, sduration_list, dept_link_list, queasy_133_list, t_eg_request_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def create_related_dept():

        nonlocal engid, groupid, department_list, maintask_list, sduration_list, dept_link_list, t_eg_subtask_list, t_eg_request_list, queasy_133_list, eg_subtask, queasy, eg_request, htparam, bediener, eg_duration
        nonlocal user_init


        nonlocal t_eg_subtask, department, maintask, sduration, dept_link, queasy_133, t_eg_request
        nonlocal t_eg_subtask_list, department_list, maintask_list, sduration_list, dept_link_list, queasy_133_list, t_eg_request_list

        i:int = 0
        c:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        dept_link_list.clear()

        queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, engid)]})

        if queasy:
            dept_link = Dept_link()
            dept_link_list.append(dept_link)

            dept_link.dept_nr = engid
            dept_link.dept_nm = queasy.char3


            for i in range(1,num_entries(queasy.char2, ";")  + 1) :
                c = to_int(entry(i - 1, queasy.char2, ";"))

                qbuff = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, to_int(entry(i - 1, queasy.char2, ";")))]})

                if qbuff:
                    dept_link = Dept_link()
                    dept_link_list.append(dept_link)

                    dept_link.dept_nr = c
                    dept_link.dept_nm = qbuff.char3


    def create_duration():

        nonlocal engid, groupid, department_list, maintask_list, sduration_list, dept_link_list, t_eg_subtask_list, t_eg_request_list, queasy_133_list, eg_subtask, queasy, eg_request, htparam, bediener, eg_duration
        nonlocal user_init


        nonlocal t_eg_subtask, department, maintask, sduration, dept_link, queasy_133, t_eg_request
        nonlocal t_eg_subtask_list, department_list, maintask_list, sduration_list, dept_link_list, queasy_133_list, t_eg_request_list

        qbuff = None
        str:string = ""
        Qbuff =  create_buffer("Qbuff",Eg_duration)
        sduration_list.clear()
        sduration = Sduration()
        sduration_list.append(sduration)

        sduration.duration_nr = 0
        sduration.time_str = "User Defineable"

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


    def create_main():

        nonlocal engid, groupid, department_list, maintask_list, sduration_list, dept_link_list, t_eg_subtask_list, t_eg_request_list, queasy_133_list, eg_subtask, queasy, eg_request, htparam, bediener, eg_duration
        nonlocal user_init


        nonlocal t_eg_subtask, department, maintask, sduration, dept_link, queasy_133, t_eg_request
        nonlocal t_eg_subtask_list, department_list, maintask_list, sduration_list, dept_link_list, queasy_133_list, t_eg_request_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        maintask_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 133)).order_by(Qbuff._recid).all():
            maintask = Maintask()
            maintask_list.append(maintask)

            maintask.main_nr = qbuff.number1
            maintask.maintask = qbuff.char1

            queasy = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, qbuff.number2)]})

            if queasy:
                maintask.main_grp = queasy.char1


    def create_dept():

        nonlocal engid, groupid, department_list, maintask_list, sduration_list, dept_link_list, t_eg_subtask_list, t_eg_request_list, queasy_133_list, eg_subtask, queasy, eg_request, htparam, bediener, eg_duration
        nonlocal user_init


        nonlocal t_eg_subtask, department, maintask, sduration, dept_link, queasy_133, t_eg_request
        nonlocal t_eg_subtask_list, department_list, maintask_list, sduration_list, dept_link_list, queasy_133_list, t_eg_request_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        department_list.clear()
        department = Department()
        department_list.append(department)

        department.dept_nr = 0
        department.department = "All Related Department"

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 19)).order_by(Qbuff._recid).all():
            department = Department()
            department_list.append(department)

            department.dept_nr = qbuff.number1
            department.department = qbuff.char3

    define_group()
    define_engineering()
    create_related_dept()
    create_duration()
    create_main()
    create_dept()

    for eg_request in db_session.query(Eg_request).order_by(Eg_request._recid).all():
        t_eg_request = T_eg_request()
        t_eg_request_list.append(t_eg_request)

        buffer_copy(eg_request, t_eg_request)

    for eg_subtask in db_session.query(Eg_subtask).order_by(Eg_subtask._recid).all():
        t_eg_subtask = T_eg_subtask()
        t_eg_subtask_list.append(t_eg_subtask)

        buffer_copy(eg_subtask, t_eg_subtask)
        t_eg_subtask.rec_id = eg_subtask._recid

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 133)).order_by(Queasy._recid).all():
        queasy_133 = Queasy_133()
        queasy_133_list.append(queasy_133)

        buffer_copy(queasy, queasy_133)

    return generate_output()