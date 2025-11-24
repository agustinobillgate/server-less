#using conversion tools version: 1.0.0.117

# ===================================================================
# Rulita, 16-10-2025 
# Tiket ID : 6526C2 | New compile program
# ===================================================================
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#--------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct, Gl_main, Gl_fstype, Gl_department

g_list_data, G_list = create_model_like(Gl_acct)

def glacct_admin_btn_exitbl(g_list_data:[G_list], case_type:int, comments:string, curr_mode:string, user_init:string, map_acct:string, prev_fibukonto:string, tax_code:string):

    prepare_cache ([Gl_main, Gl_fstype, Gl_department])

    from_acct = ""
    found = False
    success_flag = False
    b1_list_data = []
    gl_acct = gl_main = gl_fstype = gl_department = None

    b1_list = g_list = None

    b1_list_data, B1_list = create_model_like(Gl_acct, {"main_bezeich":string, "kurzbez":string, "dept_bezeich":string, "fstype_bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_acct, found, success_flag, b1_list_data, gl_acct, gl_main, gl_fstype, gl_department
        nonlocal case_type, comments, curr_mode, user_init, map_acct, prev_fibukonto, tax_code


        nonlocal b1_list, g_list
        nonlocal b1_list_data

        return {"from_acct": from_acct, "found": found, "success_flag": success_flag, "b1-list": b1_list_data}

    def fill_gl_acct():

        nonlocal from_acct, found, success_flag, b1_list_data, gl_acct, gl_main, gl_fstype, gl_department
        nonlocal case_type, comments, curr_mode, user_init, map_acct, prev_fibukonto, tax_code


        nonlocal b1_list, g_list
        nonlocal b1_list_data

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

        if curr_mode.lower()  == ("chg").lower() :
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

            if gl_acct.userinit == None:
                gl_acct.userinit = user_init + ";"


            gl_acct.chginit = user_init
            gl_acct.userinit = trim(entry(0, gl_acct.userinit, ";")) + ";" + map_acct
            gl_acct.m_date = get_current_date()

        elif curr_mode.lower()  == ("add").lower() :
            gl_acct.userinit = user_init + ";" + map_acct
            gl_acct.c_date = get_current_date()


        success_flag = True


    def create_b1_list():

        nonlocal from_acct, found, success_flag, b1_list_data, gl_acct, gl_main, gl_fstype, gl_department
        nonlocal case_type, comments, curr_mode, user_init, map_acct, prev_fibukonto, tax_code


        nonlocal b1_list, g_list
        nonlocal b1_list_data

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, g_list.fibukonto)]})

        gl_main = get_cache (Gl_main, {"nr": [(eq, gl_acct.main_nr)]})

        gl_fstype = get_cache (Gl_fstype, {"nr": [(eq, gl_acct.fs_type)]})

        gl_department = get_cache (Gl_department, {"nr": [(eq, gl_acct.deptnr)]})
        b1_list = B1_list()
        b1_list_data.append(b1_list)

        buffer_copy(gl_acct, b1_list)
        b1_list.main_bezeich = gl_main.bezeich
        b1_list.kurzbez = gl_fstype.kurzbez
        b1_list.dept_bezeich = gl_department.bezeich
        b1_list.fstype_bezeich = gl_fstype.bezeich

    g_list = query(g_list_data, first=True)

    if case_type == 1:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, g_list.fibukonto)]})

        if gl_acct:

            return generate_output()

    gl_main = get_cache (Gl_main, {"nr": [(eq, g_list.main_nr)]})

    if not gl_main:

        return generate_output()

    gl_fstype = get_cache (Gl_fstype, {"nr": [(eq, g_list.fs_type)]})

    if not gl_fstype:

        return generate_output()

    gl_department = get_cache (Gl_department, {"nr": [(eq, g_list.deptnr)]})

    if not gl_department:

        return generate_output()

    if case_type == 1:
        gl_acct = Gl_acct()
        db_session.add(gl_acct)

        fill_gl_acct()
        create_b1_list()
        from_acct = g_list.fibukonto

    elif case_type == 2:
        # Rd, 24/11/2025, get gl_acct dengan for update
        # gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, prev_fibukonto)]})
        gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == prev_fibukonto)).with_for_update().first()
        fill_gl_acct()
        create_b1_list()

    return generate_output()