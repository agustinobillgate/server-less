from functions.additional_functions import *
import decimal
from models import Wgrpdep

def rsubgrp_admin_btn_exitbl(wgrpdep_list:[Wgrpdep_list], case_type:int, dept:int):
    wgrpdep = None

    wgrpdep_list = None

    wgrpdep_list_list, Wgrpdep_list = create_model_like(Wgrpdep, {"bg_color":int, "kiosk_flag":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal wgrpdep


        nonlocal wgrpdep_list
        nonlocal wgrpdep_list_list
        return {}

    def fill_new_wgrpdep():

        nonlocal wgrpdep


        nonlocal wgrpdep_list
        nonlocal wgrpdep_list_list


        wgrpdep.departement = dept
        wgrpdep.zknr = wgrpdep_list.zknr
        wgrpdep.bezeich = wgrpdep_list.bezeich
        wgrpdep.betriebsnr = wgrpdep_list.betriebsnr
        wgrpdep.fibukonto = to_string(wgrpdep_list.bg_color) + ";" +\
                to_string(to_int(wgrpdep_list.kiosk_flag)) + ";"

    wgrpdep_list = query(wgrpdep_list_list, first=True)

    if case_type == 1:
        wgrpdep = Wgrpdep()
        db_session.add(wgrpdep)

        fill_new_wgrpdep()

    elif case_type == 2:

        wgrpdep = db_session.query(Wgrpdep).filter(
                (Wgrpdep.departement == wgrpdep_list.departement) &  (Wgrpdep.zknr == wgrpdep_list.zknr)).first()

        if wgrpdep:

            wgrpdep = db_session.query(Wgrpdep).first()
            wgrpdep.bezeich = wgrpdep_list.bezeich
            wgrpdep.betriebsnr = wgrpdep_list.betriebsnr
            wgrpdep.fibukonto = to_string(wgrpdep_list.bg_color) + ";" +\
                    to_string(to_int(wgrpdep_list.kiosk_flag)) + ";"


            pass

            wgrpdep = db_session.query(Wgrpdep).first()

    return generate_output()