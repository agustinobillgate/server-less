#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_main, Gl_fstype, Gl_department, Gl_acct, Bediener

def glacct_listbl(fibukonto:string, from_main:int, from_fstype:int, from_depart:int):

    prepare_cache ([Gl_main, Gl_fstype, Gl_department, Gl_acct, Bediener])

    b1_list_data = []
    gl_main = gl_fstype = gl_department = gl_acct = bediener = None

    b1_list = None

    b1_list_data, B1_list = create_model("B1_list", {"fibukonto":string, "glacct_bezeich":string, "glmain_bezeich":string, "acc_type":int, "glfstype_bezeich":string, "gldepartment_bezeich":string, "glsubdept":string, "bemerk":string, "nr":int, "code":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_data, gl_main, gl_fstype, gl_department, gl_acct, bediener
        nonlocal fibukonto, from_main, from_fstype, from_depart


        nonlocal b1_list
        nonlocal b1_list_data

        return {"b1-list": b1_list_data}

    def display_it():

        nonlocal b1_list_data, gl_main, gl_fstype, gl_department, gl_acct, bediener
        nonlocal fibukonto, from_main, from_fstype, from_depart


        nonlocal b1_list
        nonlocal b1_list_data

        if from_main == 0 and from_fstype == 0 and from_depart == 0:

            gl_acct_obj_list = {}
            gl_acct = Gl_acct()
            gl_main = Gl_main()
            gl_fstype = Gl_fstype()
            gl_department = Gl_department()
            for gl_acct.chginit, gl_acct.fibukonto, gl_acct.bezeich, gl_acct.acc_type, gl_acct.bemerk, gl_acct._recid, gl_main.bezeich, gl_main.nr, gl_main.code, gl_main._recid, gl_fstype.bezeich, gl_fstype._recid, gl_department.bezeich, gl_department._recid in db_session.query(Gl_acct.chginit, Gl_acct.fibukonto, Gl_acct.bezeich, Gl_acct.acc_type, Gl_acct.bemerk, Gl_acct._recid, Gl_main.bezeich, Gl_main.nr, Gl_main.code, Gl_main._recid, Gl_fstype.bezeich, Gl_fstype._recid, Gl_department.bezeich, Gl_department._recid).join(Gl_main,(Gl_main.nr == Gl_acct.main_nr)).join(Gl_fstype,(Gl_fstype.nr == Gl_acct.fs_type)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).filter(
                     (Gl_acct.fibukonto >= (fibukonto).lower()) & (Gl_acct.activeflag)).order_by(Gl_acct.fibukonto).all():
                if gl_acct_obj_list.get(gl_acct._recid):
                    continue
                else:
                    gl_acct_obj_list[gl_acct._recid] = True


                assign_it()


        elif from_main != 0:

            gl_acct_obj_list = {}
            gl_acct = Gl_acct()
            gl_main = Gl_main()
            gl_fstype = Gl_fstype()
            gl_department = Gl_department()
            for gl_acct.chginit, gl_acct.fibukonto, gl_acct.bezeich, gl_acct.acc_type, gl_acct.bemerk, gl_acct._recid, gl_main.bezeich, gl_main.nr, gl_main.code, gl_main._recid, gl_fstype.bezeich, gl_fstype._recid, gl_department.bezeich, gl_department._recid in db_session.query(Gl_acct.chginit, Gl_acct.fibukonto, Gl_acct.bezeich, Gl_acct.acc_type, Gl_acct.bemerk, Gl_acct._recid, Gl_main.bezeich, Gl_main.nr, Gl_main.code, Gl_main._recid, Gl_fstype.bezeich, Gl_fstype._recid, Gl_department.bezeich, Gl_department._recid).join(Gl_main,(Gl_main.nr == Gl_acct.main_nr) & (Gl_main.code == from_main)).join(Gl_fstype,(Gl_fstype.nr == Gl_acct.fs_type)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).filter(
                     (Gl_acct.fibukonto >= (fibukonto).lower()) & (Gl_acct.activeflag)).order_by(Gl_acct.fibukonto).all():
                if gl_acct_obj_list.get(gl_acct._recid):
                    continue
                else:
                    gl_acct_obj_list[gl_acct._recid] = True


                assign_it()


        elif from_fstype != 0:

            gl_acct_obj_list = {}
            gl_acct = Gl_acct()
            gl_main = Gl_main()
            gl_fstype = Gl_fstype()
            gl_department = Gl_department()
            for gl_acct.chginit, gl_acct.fibukonto, gl_acct.bezeich, gl_acct.acc_type, gl_acct.bemerk, gl_acct._recid, gl_main.bezeich, gl_main.nr, gl_main.code, gl_main._recid, gl_fstype.bezeich, gl_fstype._recid, gl_department.bezeich, gl_department._recid in db_session.query(Gl_acct.chginit, Gl_acct.fibukonto, Gl_acct.bezeich, Gl_acct.acc_type, Gl_acct.bemerk, Gl_acct._recid, Gl_main.bezeich, Gl_main.nr, Gl_main.code, Gl_main._recid, Gl_fstype.bezeich, Gl_fstype._recid, Gl_department.bezeich, Gl_department._recid).join(Gl_main,(Gl_main.nr == Gl_acct.main_nr)).join(Gl_fstype,(Gl_fstype.nr == Gl_acct.fs_type) & (Gl_fstype.nr == from_fstype)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).filter(
                     (Gl_acct.fibukonto >= (fibukonto).lower()) & (Gl_acct.activeflag)).order_by(Gl_acct.fibukonto).all():
                if gl_acct_obj_list.get(gl_acct._recid):
                    continue
                else:
                    gl_acct_obj_list[gl_acct._recid] = True


                assign_it()


        elif from_depart != 0:

            gl_acct_obj_list = {}
            gl_acct = Gl_acct()
            gl_main = Gl_main()
            gl_fstype = Gl_fstype()
            gl_department = Gl_department()
            for gl_acct.chginit, gl_acct.fibukonto, gl_acct.bezeich, gl_acct.acc_type, gl_acct.bemerk, gl_acct._recid, gl_main.bezeich, gl_main.nr, gl_main.code, gl_main._recid, gl_fstype.bezeich, gl_fstype._recid, gl_department.bezeich, gl_department._recid in db_session.query(Gl_acct.chginit, Gl_acct.fibukonto, Gl_acct.bezeich, Gl_acct.acc_type, Gl_acct.bemerk, Gl_acct._recid, Gl_main.bezeich, Gl_main.nr, Gl_main.code, Gl_main._recid, Gl_fstype.bezeich, Gl_fstype._recid, Gl_department.bezeich, Gl_department._recid).join(Gl_main,(Gl_main.nr == Gl_acct.main_nr)).join(Gl_fstype,(Gl_fstype.nr == Gl_acct.fs_type)).join(Gl_department,(Gl_department.nr == Gl_acct.deptnr) & (Gl_department.nr == from_depart)).filter(
                     (Gl_acct.fibukonto >= (fibukonto).lower()) & (Gl_acct.activeflag)).order_by(Gl_acct.fibukonto).all():
                if gl_acct_obj_list.get(gl_acct._recid):
                    continue
                else:
                    gl_acct_obj_list[gl_acct._recid] = True


                assign_it()

    def assign_it():

        nonlocal b1_list_data, gl_main, gl_fstype, gl_department, gl_acct, bediener
        nonlocal fibukonto, from_main, from_fstype, from_depart


        nonlocal b1_list
        nonlocal b1_list_data

        usrname:string = " "

        if trim(gl_acct.chginit) != "":

            bediener = get_cache (Bediener, {"userinit": [(eq, gl_acct.chginit)]})

            if bediener:
                usrname = bediener.username


        b1_list = B1_list()
        b1_list_data.append(b1_list)

        b1_list.fibukonto = gl_acct.fibukonto
        b1_list.glacct_bezeich = gl_acct.bezeich
        b1_list.glmain_bezeich = gl_main.bezeich
        b1_list.acc_type = gl_acct.acc_type
        b1_list.glfstype_bezeich = gl_fstype.bezeich
        b1_list.gldepartment_bezeich = gl_department.bezeich
        b1_list.nr = gl_main.nr
        b1_list.code = gl_main.code

        if num_entries(gl_acct.bemerk, ";") > 1:
            b1_list.bemerk = entry(0, gl_acct.bemerk, ";") + ";" + usrname


        else:
            b1_list.bemerk = gl_acct.bemerk + ";" + usrname

    display_it()

    return generate_output()