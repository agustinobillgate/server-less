from functions.additional_functions import *
import decimal
from models import Wgrpgen, Wgrpdep

def rmaingrp_admin_btn_exitbl(wgrpgen_list:[Wgrpgen_list], case_type:int):
    wgrpgen = wgrpdep = None

    wgrpgen_list = None

    wgrpgen_list_list, Wgrpgen_list = create_model_like(Wgrpgen)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal wgrpgen, wgrpdep


        nonlocal wgrpgen_list
        nonlocal wgrpgen_list_list
        return {}

    def fill_new_wgrpgen():

        nonlocal wgrpgen, wgrpdep


        nonlocal wgrpgen_list
        nonlocal wgrpgen_list_list


        wgrpgen.eknr = wgrpgen_list.eknr
        wgrpgen.bezeich = wgrpgen_list.bezeich

    wgrpgen_list = query(wgrpgen_list_list, first=True)

    if case_type == 1:
        wgrpgen = Wgrpgen()
        db_session.add(wgrpgen)

        fill_new_wgrpgen()

    elif case_type == 2:

        wgrpgen = db_session.query(Wgrpgen).filter(
                (Wgrpgen.eknr == wgrpgen_list.eknr)).first()

        if wgrpgen:

            wgrpdep = db_session.query(Wgrpdep).first()
            wgrpgen.bezeich = wgrpgen_list.bezeich

    return generate_output()