#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Wgrpgen

wgrpgen_list_list, Wgrpgen_list = create_model_like(Wgrpgen)

def rmaingrp_admin_btn_exitbl(wgrpgen_list_list:[Wgrpgen_list], case_type:int):

    prepare_cache ([Wgrpgen])

    wgrpgen = None

    wgrpgen_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal wgrpgen
        nonlocal case_type


        nonlocal wgrpgen_list

        return {}

    def fill_new_wgrpgen():

        nonlocal wgrpgen
        nonlocal case_type


        nonlocal wgrpgen_list


        wgrpgen.eknr = wgrpgen_list.eknr
        wgrpgen.bezeich = wgrpgen_list.bezeich


    wgrpgen_list = query(wgrpgen_list_list, first=True)

    if case_type == 1:
        wgrpgen = Wgrpgen()
        db_session.add(wgrpgen)

        fill_new_wgrpgen()

    elif case_type == 2:

        wgrpgen = get_cache (Wgrpgen, {"eknr": [(eq, wgrpgen_list.eknr)]})

        if wgrpgen:
            pass
            wgrpgen.bezeich = wgrpgen_list.bezeich

    return generate_output()