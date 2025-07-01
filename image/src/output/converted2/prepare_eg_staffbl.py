#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_staff, Queasy, Htparam, Bediener

def prepare_eg_staffbl(user_init:string):

    prepare_cache ([Queasy, Htparam, Bediener])

    engid = 0
    groupid = 0
    dept_list = []
    userskill_list = []
    t_eg_staff_list = []
    queasy_19_list = []
    eg_staff = queasy = htparam = bediener = None

    queasy_19 = dept = userskill = t_eg_staff = None

    queasy_19_list, Queasy_19 = create_model("Queasy_19", {"number1":int, "char3":string})
    dept_list, Dept = create_model("Dept", {"dept_nr":int, "dept_nm":string})
    userskill_list, Userskill = create_model("Userskill", {"categ_nr":int, "categ_nm":string, "categ_sel":bool})
    t_eg_staff_list, T_eg_staff = create_model_like(Eg_staff, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, dept_list, userskill_list, t_eg_staff_list, queasy_19_list, eg_staff, queasy, htparam, bediener
        nonlocal user_init


        nonlocal queasy_19, dept, userskill, t_eg_staff
        nonlocal queasy_19_list, dept_list, userskill_list, t_eg_staff_list

        return {"engid": engid, "groupid": groupid, "Dept": dept_list, "UserSkill": userskill_list, "t-eg-staff": t_eg_staff_list, "queasy-19": queasy_19_list}

    def define_engineering():

        nonlocal engid, groupid, dept_list, userskill_list, t_eg_staff_list, queasy_19_list, eg_staff, queasy, htparam, bediener
        nonlocal user_init


        nonlocal queasy_19, dept, userskill, t_eg_staff
        nonlocal queasy_19_list, dept_list, userskill_list, t_eg_staff_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def define_group():

        nonlocal engid, groupid, dept_list, userskill_list, t_eg_staff_list, queasy_19_list, eg_staff, queasy, htparam, bediener
        nonlocal user_init


        nonlocal queasy_19, dept, userskill, t_eg_staff
        nonlocal queasy_19_list, dept_list, userskill_list, t_eg_staff_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def create_skill():

        nonlocal engid, groupid, dept_list, userskill_list, t_eg_staff_list, queasy_19_list, eg_staff, queasy, htparam, bediener
        nonlocal user_init


        nonlocal queasy_19, dept, userskill, t_eg_staff
        nonlocal queasy_19_list, dept_list, userskill_list, t_eg_staff_list


        userskill_list.clear()

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 132)).order_by(Queasy.number1).all():
            userskill = Userskill()
            userskill_list.append(userskill)

            userskill.categ_nr = queasy.number1
            userskill.categ_nm = queasy.char1
            userskill.categ_sel = False


    def create_dept():

        nonlocal engid, groupid, dept_list, userskill_list, t_eg_staff_list, queasy_19_list, eg_staff, queasy, htparam, bediener
        nonlocal user_init


        nonlocal queasy_19, dept, userskill, t_eg_staff
        nonlocal queasy_19_list, dept_list, userskill_list, t_eg_staff_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        dept_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 19)).order_by(Qbuff._recid).all():
            dept = Dept()
            dept_list.append(dept)

            dept.dept_nr = qbuff.number1
            dept.dept_nm = qbuff.char3


    define_group()
    define_engineering()
    create_dept()
    create_skill()

    for eg_staff in db_session.query(Eg_staff).order_by(Eg_staff._recid).all():
        t_eg_staff = T_eg_staff()
        t_eg_staff_list.append(t_eg_staff)

        buffer_copy(eg_staff, t_eg_staff)
        t_eg_staff.rec_id = eg_staff._recid

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 19)).order_by(Queasy._recid).all():
        queasy_19 = Queasy_19()
        queasy_19_list.append(queasy_19)

        queasy_19.number1 = queasy.number1
        queasy_19.char3 = queasy.char3

    return generate_output()