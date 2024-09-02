from functions.additional_functions import *
import decimal
from models import L_hauptgrp

def smaingrp_admin_btn_exitbl(l_list:[L_list], case_type:int):
    l_hauptgrp = None

    l_list = None

    l_list_list, L_list = create_model_like(L_hauptgrp)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_hauptgrp


        nonlocal l_list
        nonlocal l_list_list
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

        l_hauptgrp = db_session.query(L_hauptgrp).filter(
                (L_hauptgrp.endkum == l_list.endkum)).first()
        l_hauptgrp.bezeich = l_list.bezeich

    return generate_output()