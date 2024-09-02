from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_main, Gl_fstype, Gl_department, Gl_acct, Bediener

def glacct_listbl(fibukonto:str, from_main:int, from_fstype:int, from_depart:int):
    b1_list_list = []
    gl_main = gl_fstype = gl_department = gl_acct = bediener = None

    b1_list = None

    b1_list_list, B1_list = create_model("B1_list", {"fibukonto":str, "glacct_bezeich":str, "glmain_bezeich":str, "acc_type":int, "glfstype_bezeich":str, "gldepartment_bezeich":str, "glsubdept":str, "bemerk":str, "nr":int, "code":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, gl_main, gl_fstype, gl_department, gl_acct, bediener


        nonlocal b1_list
        nonlocal b1_list_list
        return {"b1-list": b1_list_list}

    def display_it():

        nonlocal b1_list_list, gl_main, gl_fstype, gl_department, gl_acct, bediener
        nonlocal b1_list
        nonlocal b1_list_list

        if from_main == 0 and from_fstype == 0 and from_depart == 0:

            gl_acct_obj_list = []
            for gl_acct, gl_main, gl_fstype, gl_department in db_session.query(Gl_acct, Gl_main, Gl_fstype, Gl_department).\
                join(Gl_main,(Gl_main.nr == Gl_acct.main_nr)).\
                join(Gl_fstype,(Gl_fstype.nr == Gl_acct.fs_type)).\
                join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).\
                filter((Gl_acct.fibukonto >= fibukonto) &  (Gl_acct.activeflag)).all():
                if gl_acct._recid in gl_acct_obj_list:
                    continue
                else:
                    gl_acct_obj_list.append(gl_acct._recid)
                assign_it()

        elif from_main != 0:

            gl_acct_obj_list = []
            for gl_acct, gl_main, gl_fstype, gl_department in db_session.query(Gl_acct, Gl_main, Gl_fstype, Gl_department).\
                join(Gl_main,(Gl_main.nr == Gl_acct.main_nr) &  (Gl_main.code == from_main)).\
                join(Gl_fstype,(Gl_fstype.nr == Gl_acct.fs_type)).\
                join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).\
                filter((Gl_acct.fibukonto >= fibukonto) &  (Gl_acct.activeflag)).all():

                if gl_acct._recid in gl_acct_obj_list:
                    continue
                else:
                    gl_acct_obj_list.append(gl_acct._recid)
                assign_it()
        elif from_fstype != 0:

            gl_acct_obj_list = []
            for gl_acct, gl_main, gl_fstype, gl_department in db_session.query(Gl_acct, Gl_main, Gl_fstype, Gl_department).\
                join(Gl_main,(Gl_main.nr == Gl_acct.main_nr)).\
                join(Gl_fstype,(Gl_fstype.nr == Gl_acct.fs_type) &  (Gl_fstype.nr == from_fstype)).\
                join(Gl_department,(Gl_department.nr == Gl_acct.deptnr)).\
                filter((Gl_acct.fibukonto >= fibukonto) &  (Gl_acct.activeflag)).all():
                if gl_acct._recid in gl_acct_obj_list:
                    continue
                else:
                    gl_acct_obj_list.append(gl_acct._recid)
                assign_it()
        elif from_depart != 0:

            gl_acct_obj_list = []
            for gl_acct, gl_main, gl_fstype, gl_department in db_session.query(Gl_acct, Gl_main, Gl_fstype, Gl_department).\
                join(Gl_main,(Gl_main.nr == Gl_acct.main_nr)).\
                join(Gl_fstype,(Gl_fstype.nr == Gl_acct.fs_type)).\
                join(Gl_department,(Gl_department.nr == Gl_acct.deptnr) &  (Gl_department.nr == from_depart)).\
                filter((Gl_acct.fibukonto >= fibukonto) &  (Gl_acct.activeflag)).all():
                if gl_acct._recid in gl_acct_obj_list:
                    continue
                else:
                    gl_acct_obj_list.append(gl_acct._recid)
                assign_it()

    def assign_it():

        nonlocal b1_list_list, gl_main, gl_fstype, gl_department, gl_acct, bediener


        nonlocal b1_list
        nonlocal b1_list_list

        usrname:str = " "

        # if gl_acct.chginit != " ":

        #     bediener = db_session.query(Bediener).filter(
        #             (Bediener.userinit == gl_acct.chginit)).first()

        #     if bediener:
        #         usrname = bediener.username


        if bediener and bediener.userinit == gl_acct.chginit:
            usrname = bediener.username
        elif gl_acct.chginit.strip(" ") != "":
        # if gl_acct.chginit != " ":
            bediener = db_session.query(Bediener).filter(
                    (Bediener.userinit == gl_acct.chginit)).first()

            if bediener:
                usrname = bediener.username
                
        b1_list = B1_list()
        b1_list_list.append(b1_list)

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