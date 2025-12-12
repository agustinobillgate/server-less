#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 10-12-2025
# - Added with_for_update before delete query
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def read_gl_acct_1bl(case_type:int, fracctno:string, toacctno:string):
    t_gl_acct_data = []
    gl_acct = None

    t_gl_acct = None

    t_gl_acct_data, T_gl_acct = create_model_like(Gl_acct, {"map_acct":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_acct_data, gl_acct
        nonlocal case_type, fracctno, toacctno


        nonlocal t_gl_acct
        nonlocal t_gl_acct_data

        return {"t-gl-acct": t_gl_acct_data}

    if case_type == 1:

        # gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fracctno)]})
        gl_acct = db_session.query(Gl_acct).filter(
                 (Gl_acct.fibukonto == fracctno)).first()

        if gl_acct:
            t_gl_acct = T_gl_acct()
            t_gl_acct_data.append(t_gl_acct)

            buffer_copy(gl_acct, t_gl_acct)
            t_gl_acct.map_acct = entry(1, gl_acct.userinit, ";")


    elif case_type == 2:

        gl_acct = db_session.query(Gl_acct).filter(
                 (Gl_acct.fibukonto >= fracctno) & (Gl_acct.fibukonto <= toacctno) & ((Gl_acct.acc_type == 1) | (Gl_acct.acc_type == 2) | (Gl_acct.acc_type == 5))).first()

        if gl_acct:
            pass
            t_gl_acct = T_gl_acct()
            t_gl_acct_data.append(t_gl_acct)

            buffer_copy(gl_acct, t_gl_acct)
            t_gl_acct.map_acct = entry(1, gl_acct.userinit, ";")


    elif case_type == 3:

        # gl_acct = get_cache (Gl_acct, {"fibukonto": [(ge, fracctno),(le, toacctno)],"acc_type": [(eq, 3)]})
        gl_acct = db_session.query(Gl_acct).filter(
                 (Gl_acct.fibukonto >= fracctno) & (Gl_acct.fibukonto <= toacctno) & (Gl_acct.acc_type == 3)).first()

        if gl_acct:
            t_gl_acct = T_gl_acct()
            t_gl_acct_data.append(t_gl_acct)

            buffer_copy(gl_acct, t_gl_acct)
            t_gl_acct.map_acct = entry(1, gl_acct.userinit, ";")


    elif case_type == 4:

        # gl_acct = get_cache (Gl_acct, {"fibukonto": [(ge, fracctno),(le, toacctno)],"acc_type": [(eq, 4)]})
        gl_acct = db_session.query(Gl_acct).filter(
                 (Gl_acct.fibukonto >= fracctno) & (Gl_acct.fibukonto <= toacctno) & (Gl_acct.acc_type == 4)).first()

        if gl_acct:
            t_gl_acct = T_gl_acct()
            t_gl_acct_data.append(t_gl_acct)

            buffer_copy(gl_acct, t_gl_acct)
            t_gl_acct.map_acct = entry(1, gl_acct.userinit, ";")


    elif case_type == 5:

        # gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fracctno)],"activeflag": [(eq, True)]})
        gl_acct = db_session.query(Gl_acct).filter(
                 (Gl_acct.fibukonto == fracctno) & (Gl_acct.activeflag == True)).first()

        if gl_acct:
            t_gl_acct = T_gl_acct()
            t_gl_acct_data.append(t_gl_acct)

            buffer_copy(gl_acct, t_gl_acct)
            t_gl_acct.map_acct = entry(1, gl_acct.userinit, ";")


    elif case_type == 6:

        # gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fracctno)],"activeflag": [(eq, True)],"bezeich": [(ne, "")]})
        gl_acct = db_session.query(Gl_acct).filter(
                 (Gl_acct.fibukonto == fracctno) & (Gl_acct.activeflag == True) & (Gl_acct.bezeich != "")).first()

        if gl_acct:
            t_gl_acct = T_gl_acct()
            t_gl_acct_data.append(t_gl_acct)

            buffer_copy(gl_acct, t_gl_acct)
            t_gl_acct.map_acct = entry(1, gl_acct.userinit, ";")


    elif case_type == 7:

        # gl_acct = get_cache (Gl_acct, {"bezeich": [(eq, toacctno)],"fibukonto": [(ne, fracctno)]})
        gl_acct = db_session.query(Gl_acct).filter(
                 (Gl_acct.bezeich == toacctno) & (Gl_acct.fibukonto != fracctno)).first()

        if gl_acct:
            t_gl_acct = T_gl_acct()
            t_gl_acct_data.append(t_gl_acct)

            buffer_copy(gl_acct, t_gl_acct)
            t_gl_acct.map_acct = entry(1, gl_acct.userinit, ";")


    elif case_type == 8:

        gl_acct = db_session.query(Gl_acct).filter(
                 (to_int(Gl_acct.fibukonto) == 0) & (Gl_acct.bezeich == "") & (Gl_acct.main_nr == 0)).with_for_update().first()

        if gl_acct:
            db_session.delete(gl_acct)

    return generate_output()