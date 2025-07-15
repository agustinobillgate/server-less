#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_lager

l_list_data, L_list = create_model_like(L_lager)

def storage_admin_btn_exitbl(case_type:int, l_list_data:[L_list]):

    prepare_cache ([L_lager])

    l_lager = None

    l_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_lager
        nonlocal case_type


        nonlocal l_list

        return {}

    def fill_new_l_lager():

        nonlocal l_lager
        nonlocal case_type


        nonlocal l_list


        l_lager.lager_nr = l_list.lager_nr
        l_lager.bezeich = l_list.bezeich
        l_lager.betriebsnr = l_list.betriebsnr


    l_list = query(l_list_data, first=True)

    if case_type == 1:
        l_lager = L_lager()
        db_session.add(l_lager)

        fill_new_l_lager()

    elif case_type == 2:

        l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_list.lager_nr)]})
        l_lager.bezeich = l_list.bezeich
        l_lager.betriebsnr = l_list.betriebsnr
        pass

    return generate_output()