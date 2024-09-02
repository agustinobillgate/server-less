from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_acct, Gl_main, Gl_fstype, Gl_department

b1_list_list, B1_list = create_model_like(Gl_acct, {"main_bezeich":str, "kurzbez":str, "dept_bezeich":str, "fstype_bezeich":str})
g_list_list, G_list = create_model_like(Gl_acct)

def glacct_admin_btn_exitbl(g_list:[G_list], case_type:int, comments:str, curr_mode:str, user_init:str, map_acct:str, prev_fibukonto:str, tax_code:str):
    from_acct = ""
    found = False
    success_flag = False
    
    gl_acct = gl_main = gl_fstype = gl_department = None

    b1_list = g_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_acct, found, success_flag, gl_acct, gl_main, gl_fstype, gl_department

        nonlocal b1_list, g_list
        global b1_list_list, g_list_list
        return {"from_acct": from_acct, "found": found, "success_flag": success_flag, "b1-list": b1_list_list}

    def fill_gl_acct():

        nonlocal from_acct, found, success_flag, gl_acct, gl_main, gl_fstype, gl_department


        nonlocal b1_list, g_list
        global b1_list_list, g_list_list

        i:int = 0
        answer:bool = True

        if tax_code != " ":
            comments = comments + ";" + tax_code
        gl_acct.fibukonto = g_list.fibukonto
        gl_acct.bezeich = g_list.bezeich
        gl_acct.main_nr = g_list.main_nr
        gl_acct.acc_type = g_list.acc_type
        gl_acct.fs_type = g_list.fs_type
        gl_acct.deptnr = g_list.deptnr
        gl_acct.activeflag = g_list.activeflag
        gl_acct.bemerk = comments

        if curr_mode.lower()  == "chg":
            for i in range(1,12 + 1) :
                gl_acct.budget[i - 1] = g_list.budget[i - 1]
                gl_acct.ly_budget[i - 1] = g_list.ly_budget[i - 1]
                gl_acct.debit[i - 1] = g_list.debit[i - 1]
                gl_acct.actual[i - 1] = g_list.actual[i - 1]
                gl_acct.last_yr[i - 1] = g_list.last_yr[i - 1]


            answer = True

            if gl_acct.acc_type == 1:
                for i in range(1,12 + 1) :

                    if gl_acct.budget[i - 1] > 0:
                        found = True

                    if gl_acct.ly_budget[i - 1] > 0:
                        found = True

                    if gl_acct.debit[i - 1] > 0:
                        found = True
            gl_acct.chginit = user_init
            gl_acct.userinit = trim(entry(0, gl_acct.userinit, ";")) + ";" + map_acct
            gl_acct.m_date = get_current_date()

        elif curr_mode.lower()  == "add":
            gl_acct.userinit = user_init + ";" + map_acct
            gl_acct.c_date = get_current_date()


        success_flag = True

    def create_b1_list():

        nonlocal from_acct, found, success_flag, gl_acct, gl_main, gl_fstype, gl_department


        nonlocal b1_list, g_list
        global  b1_list_list, g_list_list

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == g_list.fibukonto)).first()

        gl_main = db_session.query(Gl_main).filter(
                (Gl_main.nr == gl_acct.main_nr)).first()

        gl_fstype = db_session.query(Gl_fstype).filter(
                (Gl_fstype.nr == gl_acct.fs_type)).first()

        gl_department = db_session.query(Gl_department).filter(
                (Gl_department.nr == gl_acct.deptnr)).first()
        b1_list = B1_list()
        b1_list_list.append(b1_list)

        buffer_copy(gl_acct, b1_list)
        b1_list.main_bezeich = gl_main.bezeich
        b1_list.kurzbez = gl_fstype.kurzbez
        b1_list.dept_bezeich = gl_department.bezeich
        b1_list.fstype_bezeich = gl_fstype.bezeich


    g_list = query(g_list_list, first=True)

    if case_type == 1:

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == g_list.fibukonto)).first()

        if gl_acct:

            return generate_output()

    if g_list is not None:
        gl_main = db_session.query(Gl_main).filter(
                (Gl_main.nr == g_list.main_nr)).first()

        if not gl_main:

            return generate_output()

        gl_fstype = db_session.query(Gl_fstype).filter(
                (Gl_fstype.nr == g_list.fs_type)).first()

        if not gl_fstype:

            return generate_output()

        gl_department = db_session.query(Gl_department).filter(
                (Gl_department.nr == g_list.deptnr)).first()

        if not gl_department:

            return generate_output()

    if case_type == 1:
        gl_acct = Gl_acct()
        db_session.add(gl_acct)

        fill_gl_acct()
        create_b1_list()
        from_acct = g_list.fibukonto

    elif case_type == 2:

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (prev_fibukonto).lower())).first()
        fill_gl_acct()
        create_b1_list()

    return generate_output()