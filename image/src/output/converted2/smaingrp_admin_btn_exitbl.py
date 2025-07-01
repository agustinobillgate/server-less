#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_hauptgrp

l_list_list, L_list = create_model_like(L_hauptgrp)

def smaingrp_admin_btn_exitbl(l_list_list:[L_list], case_type:int):

    prepare_cache ([L_hauptgrp])

    l_hauptgrp = None

    l_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_hauptgrp
        nonlocal case_type


        nonlocal l_list

        return {}

    l_list = query(l_list_list, first=True)

    if not l_list:

        return generate_output()

    if case_type == 1:
        l_hauptgrp = L_hauptgrp()
        db_session.add(l_hauptgrp)

        l_hauptgrp.endkum = l_list.endkum
        l_hauptgrp.bezeich = l_list.bezeich

    elif case_type == 2:

        l_hauptgrp = get_cache (L_hauptgrp, {"endkum": [(eq, l_list.endkum)]})
        l_hauptgrp.bezeich = l_list.bezeich

    return generate_output()