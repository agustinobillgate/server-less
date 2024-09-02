from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Fa_grup, Fa_artikel, Gl_acct

def fa_subgrpadmin_btn_exitbl(l_list:[L_list], case_type:int, fibukonto:str, credit_fibu:str, debit_fibu:str, rec_id:int):
    err_no = 0
    fibuchg:bool = False
    fa_grup = fa_artikel = gl_acct = None

    l_list = fabuff = None

    l_list_list, L_list = create_model_like(Fa_grup)

    Fabuff = Fa_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_no, fibuchg, fa_grup, fa_artikel, gl_acct
        nonlocal fabuff


        nonlocal l_list, fabuff
        nonlocal l_list_list
        return {"err_no": err_no}

    def fill_new_fa_grup():

        nonlocal err_no, fibuchg, fa_grup, fa_artikel, gl_acct
        nonlocal fabuff


        nonlocal l_list, fabuff
        nonlocal l_list_list


        fa_grup.gnr = l_list.gnr
        fa_grup.bezeich = l_list.bezeich
        fa_grup.fibukonto = fibukonto
        fa_grup.credit_fibu = credit_fibu
        fa_grup.debit_fibu = debit_fibu
        fa_grup.flag = 1

    l_list = query(l_list_list, first=True)

    if case_type == 1:

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.(fibukonto).lower()) == (fibukonto).lower())).first()

        if not gl_acct:
            err_no = 1

            return generate_output()

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (credit_fibu).lower())).first()

        if not gl_acct:
            err_no = 2

            return generate_output()

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (debit_fibu).lower())).first()

        if not gl_acct:
            err_no = 3

            return generate_output()
        fa_grup = Fa_grup()
        db_session.add(fa_grup)

        fill_new_fa_grup()

        fa_grup = db_session.query(Fa_grup).first()

    elif case_type == 2:

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.(fibukonto).lower()) == (fibukonto).lower())).first()

        if not gl_acct:
            err_no = 1

            return generate_output()

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (credit_fibu).lower())).first()

        if not gl_acct:
            err_no = 2

            return generate_output()

        gl_acct = db_session.query(Gl_acct).filter(
                (func.lower(Gl_acct.fibukonto) == (debit_fibu).lower())).first()

        if not gl_acct:
            err_no = 3

            return generate_output()

        fa_grup = db_session.query(Fa_grup).filter(
                    (Fa_grup._recid == rec_id)).first()
        fibuchg = (fa_grup.fibukonto != fibukonto) or (fa_grup.credit_fibu != credit_fibu) or (fa_grup.debit_fibu != debit_fibu)

        fa_grup = db_session.query(Fa_grup).first()
        fa_grup.gnr = l_list.gnr
        fa_grup.bezeich = l_list.bezeich
        fa_grup.fibukonto = fibukonto
        fa_grup.credit_fibu = credit_fibu
        fa_grup.debit_fibu = debit_fibu

        if fibuchg:

            for fa_artikel in db_session.query(Fa_artikel).filter(
                        (Fa_artikel.subgrp == fa_grup.gnr)).all():

                if fa_artikel.(fibukonto).lower().lower()  != (fibukonto).lower()  or fa_artikel.(credit_fibu).lower().lower()  != (credit_fibu).lower()  or fa_artikel.(debit_fibu).lower().lower()  != (debit_fibu).lower() :

                    fabuff = db_session.query(Fabuff).filter(
                                (Fabuff._recid == fa_artikel._recid)).first()
                    fabuff.fibukonto = fibukonto
                    fabuff.credit_fibu = credit_fibu
                    fabuff.debit_fibu = debit_fibu

                    fabuff = db_session.query(Fabuff).first()


                fa_grup = db_session.query(Fa_grup).first()


    return generate_output()