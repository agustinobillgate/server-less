from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Eg_staff, Queasy, Htparam, Bediener

def prepare_eg_staffbl(user_init:str):
    engid = 0
    groupid = 0
    dept_list = []
    userskill_list = []
    t_eg_staff_list = []
    queasy_19_list = []
    eg_staff = queasy = htparam = bediener = None

    queasy_19 = dept = userskill = t_eg_staff = qbuff = None

    queasy_19_list, Queasy_19 = create_model("Queasy_19", {"number1":int, "char3":str})
    dept_list, Dept = create_model("Dept", {"dept_nr":int, "dept_nm":str})
    userskill_list, Userskill = create_model("Userskill", {"categ_nr":int, "categ_nm":str, "categ_sel":bool})
    t_eg_staff_list, T_eg_staff = create_model_like(Eg_staff, {"rec_id":int})

    Qbuff = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, dept_list, userskill_list, t_eg_staff_list, queasy_19_list, eg_staff, queasy, htparam, bediener
        nonlocal qbuff


        nonlocal queasy_19, dept, userskill, t_eg_staff, qbuff
        nonlocal queasy_19_list, dept_list, userskill_list, t_eg_staff_list
        return {"engid": engid, "groupid": groupid, "Dept": dept_list, "UserSkill": userskill_list, "t-eg-staff": t_eg_staff_list, "queasy-19": queasy_19_list}

    def define_engineering():

        nonlocal engid, groupid, dept_list, userskill_list, t_eg_staff_list, queasy_19_list, eg_staff, queasy, htparam, bediener
        nonlocal qbuff


        nonlocal queasy_19, dept, userskill, t_eg_staff, qbuff
        nonlocal queasy_19_list, dept_list, userskill_list, t_eg_staff_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def define_group():

        nonlocal engid, groupid, dept_list, userskill_list, t_eg_staff_list, queasy_19_list, eg_staff, queasy, htparam, bediener
        nonlocal qbuff


        nonlocal queasy_19, dept, userskill, t_eg_staff, qbuff
        nonlocal queasy_19_list, dept_list, userskill_list, t_eg_staff_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def create_skill():

        nonlocal engid, groupid, dept_list, userskill_list, t_eg_staff_list, queasy_19_list, eg_staff, queasy, htparam, bediener
        nonlocal qbuff


        nonlocal queasy_19, dept, userskill, t_eg_staff, qbuff
        nonlocal queasy_19_list, dept_list, userskill_list, t_eg_staff_list


        UserSkill_list.clear()

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 132)).all():
            userskill = Userskill()
            userskill_list.append(userskill)

            UserSkill.Categ_nr = queasy.number1
            UserSkill.Categ_nm = queasy.char1
            UserSkill.Categ_sel = False

    def create_dept():

        nonlocal engid, groupid, dept_list, userskill_list, t_eg_staff_list, queasy_19_list, eg_staff, queasy, htparam, bediener
        nonlocal qbuff


        nonlocal queasy_19, dept, userskill, t_eg_staff, qbuff
        nonlocal queasy_19_list, dept_list, userskill_list, t_eg_staff_list


        Qbuff = Queasy
        dept_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 19)).all():
            dept = Dept()
            dept_list.append(dept)

            dept.dept_nr = qbuff.number1
            dept.dept_nm = qbuff.char3

    define_group()
    define_engineering()
    create_dept()
    create_skill()

    for eg_staff in db_session.query(Eg_staff).all():
        t_eg_staff = T_eg_staff()
        t_eg_staff_list.append(t_eg_staff)

        buffer_copy(eg_staff, t_eg_staff)
        t_eg_staff.rec_id = eg_staff._recid

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 19)).all():
        queasy_19 = Queasy_19()
        queasy_19_list.append(queasy_19)

        queasy_19.number1 = queasy.number1
        queasy_19.char3 = queasy.char3

    return generate_output()