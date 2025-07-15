#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Wgrpdep

wgrpdep_list_data, Wgrpdep_list = create_model_like(Wgrpdep, {"bg_color":int, "kiosk_flag":bool})

def rsubgrp_admin_btn_exitbl(wgrpdep_list_data:[Wgrpdep_list], case_type:int, dept:int):

    prepare_cache ([Wgrpdep])

    wgrpdep = None

    wgrpdep_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal wgrpdep
        nonlocal case_type, dept


        nonlocal wgrpdep_list

        return {}

    def fill_new_wgrpdep():

        nonlocal wgrpdep
        nonlocal case_type, dept


        nonlocal wgrpdep_list


        wgrpdep.departement = dept
        wgrpdep.zknr = wgrpdep_list.zknr
        wgrpdep.bezeich = wgrpdep_list.bezeich
        wgrpdep.betriebsnr = wgrpdep_list.betriebsnr
        wgrpdep.fibukonto = to_string(wgrpdep_list.bg_color) + ";" +\
                to_string(to_int(wgrpdep_list.kiosk_flag)) + ";"


    wgrpdep_list = query(wgrpdep_list_data, first=True)

    if case_type == 1:
        wgrpdep = Wgrpdep()
        db_session.add(wgrpdep)

        fill_new_wgrpdep()

    elif case_type == 2:

        wgrpdep = get_cache (Wgrpdep, {"departement": [(eq, wgrpdep_list.departement)],"zknr": [(eq, wgrpdep_list.zknr)]})

        if wgrpdep:
            pass
            wgrpdep.bezeich = wgrpdep_list.bezeich
            wgrpdep.betriebsnr = wgrpdep_list.betriebsnr
            wgrpdep.fibukonto = to_string(wgrpdep_list.bg_color) + ";" +\
                    to_string(to_int(wgrpdep_list.kiosk_flag)) + ";"

            pass

    return generate_output()