#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_fstype, Htparam, Gl_acct

def coa_budget_create_list1_webbl(disp_all:bool, case_type:int, fstype_nr:int):

    prepare_cache ([Htparam])

    max_row = 2
    month_closing = 0
    year_closing = 0
    curr_year = 0
    coa_list_list = []
    t_gl_fstype_list = []
    fs_number_group:int = -99
    is_first:bool = True
    gl_fstype = htparam = gl_acct = None

    coa_list = t_gl_fstype = None

    coa_list_list, Coa_list = create_model("Coa_list", {"fibukonto":string, "main_nr":int, "bezeich":string, "b_flag":bool, "acct_type":int, "actual":[Decimal,12], "bemerk":string, "fs_type":int, "last_yr":[Decimal,12], "budget":[Decimal,12], "deptnr":int, "userinit":string, "chginit":string, "c_date":date, "m_date":date, "modifiable":bool, "activeflag":bool, "ly_budget":[Decimal,12], "debit":[Decimal,12], "credit":[Decimal,12], "is_group":bool})
    t_gl_fstype_list, T_gl_fstype = create_model_like(Gl_fstype)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal max_row, month_closing, year_closing, curr_year, coa_list_list, t_gl_fstype_list, fs_number_group, is_first, gl_fstype, htparam, gl_acct
        nonlocal disp_all, case_type, fstype_nr


        nonlocal coa_list, t_gl_fstype
        nonlocal coa_list_list, t_gl_fstype_list

        return {"max_row": max_row, "month_closing": month_closing, "year_closing": year_closing, "curr_year": curr_year, "coa-list": coa_list_list, "t-gl-fstype": t_gl_fstype_list}

    def create_list1a():

        nonlocal max_row, month_closing, year_closing, curr_year, coa_list_list, t_gl_fstype_list, fs_number_group, is_first, gl_fstype, htparam, gl_acct
        nonlocal disp_all, case_type, fstype_nr


        nonlocal coa_list, t_gl_fstype
        nonlocal coa_list_list, t_gl_fstype_list

        gl_acct_obj_list = {}
        for gl_acct, gl_fstype in db_session.query(Gl_acct, Gl_fstype).join(Gl_fstype,(Gl_fstype.nr == Gl_acct.fs_type)).order_by(Gl_fstype.nr, Gl_acct.fibukonto).all():
            if gl_acct_obj_list.get(gl_acct._recid):
                continue
            else:
                gl_acct_obj_list[gl_acct._recid] = True


            create_coa_list()


    def create_list1b():

        nonlocal max_row, month_closing, year_closing, curr_year, coa_list_list, t_gl_fstype_list, fs_number_group, is_first, gl_fstype, htparam, gl_acct
        nonlocal disp_all, case_type, fstype_nr


        nonlocal coa_list, t_gl_fstype
        nonlocal coa_list_list, t_gl_fstype_list

        gl_acct_obj_list = {}
        for gl_acct, gl_fstype in db_session.query(Gl_acct, Gl_fstype).join(Gl_fstype,(Gl_fstype.nr == Gl_acct.fs_type)).filter(
                 (Gl_acct.acc_type != 3) & (Gl_acct.acc_type != 4)).order_by(Gl_fstype.nr, Gl_acct.fibukonto).all():
            if gl_acct_obj_list.get(gl_acct._recid):
                continue
            else:
                gl_acct_obj_list[gl_acct._recid] = True


            create_coa_list()


    def create_list2a():

        nonlocal max_row, month_closing, year_closing, curr_year, coa_list_list, t_gl_fstype_list, fs_number_group, is_first, gl_fstype, htparam, gl_acct
        nonlocal disp_all, case_type, fstype_nr


        nonlocal coa_list, t_gl_fstype
        nonlocal coa_list_list, t_gl_fstype_list

        gl_acct_obj_list = {}
        for gl_acct, gl_fstype in db_session.query(Gl_acct, Gl_fstype).join(Gl_fstype,(Gl_fstype.nr == Gl_acct.fs_type)).filter(
                 (Gl_acct.fs_type == fstype_nr)).order_by(Gl_fstype.nr, Gl_acct.fibukonto).all():
            if gl_acct_obj_list.get(gl_acct._recid):
                continue
            else:
                gl_acct_obj_list[gl_acct._recid] = True


            create_coa_list()


    def create_list2b():

        nonlocal max_row, month_closing, year_closing, curr_year, coa_list_list, t_gl_fstype_list, fs_number_group, is_first, gl_fstype, htparam, gl_acct
        nonlocal disp_all, case_type, fstype_nr


        nonlocal coa_list, t_gl_fstype
        nonlocal coa_list_list, t_gl_fstype_list

        gl_acct_obj_list = {}
        for gl_acct, gl_fstype in db_session.query(Gl_acct, Gl_fstype).join(Gl_fstype,(Gl_fstype.nr == Gl_acct.fs_type)).filter(
                 (Gl_acct.acc_type != 3) & (Gl_acct.acc_type != 4) & (Gl_acct.fs_type == fstype_nr)).order_by(Gl_fstype.nr, Gl_acct.fibukonto).all():
            if gl_acct_obj_list.get(gl_acct._recid):
                continue
            else:
                gl_acct_obj_list[gl_acct._recid] = True


            create_coa_list()


    def assign_it():

        nonlocal max_row, month_closing, year_closing, curr_year, coa_list_list, t_gl_fstype_list, fs_number_group, is_first, gl_fstype, htparam, gl_acct
        nonlocal disp_all, case_type, fstype_nr


        nonlocal coa_list, t_gl_fstype
        nonlocal coa_list_list, t_gl_fstype_list


        t_gl_fstype = T_gl_fstype()
        t_gl_fstype_list.append(t_gl_fstype)

        buffer_copy(gl_fstype, t_gl_fstype)


    def create_coa_list():

        nonlocal max_row, month_closing, year_closing, curr_year, coa_list_list, t_gl_fstype_list, fs_number_group, is_first, gl_fstype, htparam, gl_acct
        nonlocal disp_all, case_type, fstype_nr


        nonlocal coa_list, t_gl_fstype
        nonlocal coa_list_list, t_gl_fstype_list

        if fs_number_group != gl_fstype.nr:
            fs_number_group = gl_fstype.nr

            if is_first == False:
                coa_list = Coa_list()
                coa_list_list.append(coa_list)

                coa_list.fibukonto = ""
                coa_list.is_group = True


            else:
                is_first = False
            coa_list = Coa_list()
            coa_list_list.append(coa_list)

            coa_list.fibukonto = ""
            coa_list.main_nr = 0
            coa_list.bezeich = to_string(gl_fstype.nr) + " - " + to_string(gl_fstype.bezeich)
            coa_list.is_group = True


        coa_list = Coa_list()
        coa_list_list.append(coa_list)

        buffer_copy(gl_acct, coa_list)
        coa_list.is_group = False

    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    month_closing = get_month(htparam.fdate)
    year_closing = get_year(htparam.fdate)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    curr_year = get_year(htparam.fdate)
    coa_list_list.clear()
    t_gl_fstype_list.clear()

    if case_type == 1:
        t_gl_fstype = T_gl_fstype()
        t_gl_fstype_list.append(t_gl_fstype)

        t_gl_fstype.nr = 0
        t_gl_fstype.kurzbez = "ALL"
        t_gl_fstype.bezeich = "Select All"

        for gl_fstype in db_session.query(Gl_fstype).order_by(Gl_fstype.nr).all():
            assign_it()
    elif case_type == 2:

        if fstype_nr == 0:

            if disp_all:
                create_list1a()
            else:
                create_list1b()
        else:

            if disp_all:
                create_list2a()
            else:
                create_list2b()

        for gl_acct in db_session.query(Gl_acct).order_by(Gl_acct._recid).all():
            max_row = max_row + 1

    return generate_output()