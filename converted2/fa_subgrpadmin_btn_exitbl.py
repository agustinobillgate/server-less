#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_grup, Fa_artikel, Gl_acct

l_list_data, L_list = create_model_like(Fa_grup)

def fa_subgrpadmin_btn_exitbl(l_list_data:[L_list], case_type:int, fibukonto:string, credit_fibu:string, debit_fibu:string, rec_id:int):

    prepare_cache ([Fa_grup, Fa_artikel])

    err_no = 0
    fibuchg:bool = False
    fa_grup = fa_artikel = gl_acct = None

    l_list = fabuff = None

    Fabuff = create_buffer("Fabuff",Fa_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_no, fibuchg, fa_grup, fa_artikel, gl_acct
        nonlocal case_type, fibukonto, credit_fibu, debit_fibu, rec_id
        nonlocal fabuff


        nonlocal l_list, fabuff

        return {"err_no": err_no}

    def fill_new_fa_grup():

        nonlocal err_no, fibuchg, fa_grup, fa_artikel, gl_acct
        nonlocal case_type, fibukonto, credit_fibu, debit_fibu, rec_id
        nonlocal fabuff


        nonlocal l_list, fabuff


        fa_grup.gnr = l_list.gnr
        fa_grup.bezeich = l_list.bezeich
        fa_grup.fibukonto = fibukonto
        fa_grup.credit_fibu = credit_fibu
        fa_grup.debit_fibu = debit_fibu
        fa_grup.flag = 1


    l_list = query(l_list_data, first=True)

    if case_type == 1:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibukonto)]})

        if not gl_acct:
            err_no = 1

            return generate_output()

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, credit_fibu)]})

        if not gl_acct:
            err_no = 2

            return generate_output()

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, debit_fibu)]})

        if not gl_acct:
            err_no = 3

            return generate_output()
        fa_grup = Fa_grup()
        db_session.add(fa_grup)

        fill_new_fa_grup()
        pass

    elif case_type == 2:

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, fibukonto)]})

        if not gl_acct:
            err_no = 1

            return generate_output()

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, credit_fibu)]})

        if not gl_acct:
            err_no = 2

            return generate_output()

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, debit_fibu)]})

        if not gl_acct:
            err_no = 3

            return generate_output()

        fa_grup = get_cache (Fa_grup, {"_recid": [(eq, rec_id)]})
        fibuchg = (fa_grup.fibukonto != fibukonto) or (fa_grup.credit_fibu != credit_fibu) or (fa_grup.debit_fibu != debit_fibu)
        pass
        fa_grup.gnr = l_list.gnr
        fa_grup.bezeich = l_list.bezeich
        fa_grup.fibukonto = fibukonto
        fa_grup.credit_fibu = credit_fibu
        fa_grup.debit_fibu = debit_fibu

        if fibuchg:

            for fa_artikel in db_session.query(Fa_artikel).filter(
                         (Fa_artikel.subgrp == fa_grup.gnr)).order_by(Fa_artikel._recid).all():

                if fa_artikel.fibukonto.lower()  != (fibukonto).lower()  or fa_artikel.credit_fibu.lower()  != (credit_fibu).lower()  or fa_artikel.debit_fibu.lower()  != (debit_fibu).lower() :

                    fabuff = get_cache (Fa_artikel, {"_recid": [(eq, fa_artikel._recid)]})
                    fabuff.fibukonto = fibukonto
                    fabuff.credit_fibu = credit_fibu
                    fabuff.debit_fibu = debit_fibu


                    pass
                    pass
                pass


    return generate_output()