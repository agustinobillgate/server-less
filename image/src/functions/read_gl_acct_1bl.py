from functions.additional_functions import *
import decimal
from models import Gl_acct

def read_gl_acct_1bl(case_type:int, fracctno:str, toacctno:str):
    t_gl_acct_list = []
    gl_acct = None

    t_gl_acct = None

    t_gl_acct_list, T_gl_acct = create_model_like(Gl_acct, {"map_acct":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_acct_list, gl_acct


        nonlocal t_gl_acct
        nonlocal t_gl_acct_list
        return {"t-gl-acct": t_gl_acct_list}

    if case_type == 1:

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == fracctno)).first()

        if gl_acct:
            t_gl_acct = T_gl_acct()
            t_gl_acct_list.append(t_gl_acct)

            buffer_copy(gl_acct, t_gl_acct)
            t_gl_acct.map_acct = entry(1, gl_acct.userinit, ";")


    elif case_type == 2:

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto >= fracctno) &  (Gl_acct.fibukonto <= toacctno) &  ((Gl_acct.acc_type == 1) |  (Gl_acct.acc_type == 2) |  (Gl_acct.acc_type == 5))).first()

        if gl_acct:
            t_gl_acct = T_gl_acct()
            t_gl_acct_list.append(t_gl_acct)

            buffer_copy(gl_acct, t_gl_acct)
            t_gl_acct.map_acct = entry(1, gl_acct.userinit, ";")


    elif case_type == 3:

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto >= fracctno) &  (Gl_acct.fibukonto <= toacctno) &  (Gl_acct.acc_type == 3)).first()

        if gl_acct:
            t_gl_acct = T_gl_acct()
            t_gl_acct_list.append(t_gl_acct)

            buffer_copy(gl_acct, t_gl_acct)
            t_gl_acct.map_acct = entry(1, gl_acct.userinit, ";")


    elif case_type == 4:

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto >= fracctno) &  (Gl_acct.fibukonto <= toacctno) &  (Gl_acct.acc_type == 4)).first()

        if gl_acct:
            t_gl_acct = T_gl_acct()
            t_gl_acct_list.append(t_gl_acct)

            buffer_copy(gl_acct, t_gl_acct)
            t_gl_acct.map_acct = entry(1, gl_acct.userinit, ";")


    elif case_type == 5:

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == fracctno) &  (Gl_acct.activeflag)).first()

        if gl_acct:
            t_gl_acct = T_gl_acct()
            t_gl_acct_list.append(t_gl_acct)

            buffer_copy(gl_acct, t_gl_acct)
            t_gl_acct.map_acct = entry(1, gl_acct.userinit, ";")


    elif case_type == 6:

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == fracctno) &  (Gl_acct.activeflag) &  (Gl_acct.bezeich != "")).first()

        if gl_acct:
            t_gl_acct = T_gl_acct()
            t_gl_acct_list.append(t_gl_acct)

            buffer_copy(gl_acct, t_gl_acct)
            t_gl_acct.map_acct = entry(1, gl_acct.userinit, ";")


    elif case_type == 7:

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.bezeich == toacctno) &  (Gl_acct.fibukonto != fracctno)).first()

        if gl_acct:
            t_gl_acct = T_gl_acct()
            t_gl_acct_list.append(t_gl_acct)

            buffer_copy(gl_acct, t_gl_acct)
            t_gl_acct.map_acct = entry(1, gl_acct.userinit, ";")


    elif case_type == 8:

        gl_acct = db_session.query(Gl_acct).filter(
                (to_int(Gl_acct.fibukonto) == 0) &  (Gl_acct.bezeich == "") &  (Gl_acct.main_nr == 0)).first()

        if gl_acct:
            db_session.delete(gl_acct)

    return generate_output()