from functions.additional_functions import *
import decimal
from models import L_lager

def storage_admin_btn_exitbl(case_type:int, l_list:[L_list]):
    l_lager = None

    l_list = None

    l_list_list, L_list = create_model_like(L_lager)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_lager


        nonlocal l_list
        nonlocal l_list_list
        return {}

    def fill_new_l_lager():

        nonlocal l_lager


        nonlocal l_list
        nonlocal l_list_list


        l_lager.lager_nr = l_list.lager_nr
        l_lager.bezeich = l_list.bezeich
        l_lager.betriebsnr = l_list.betriebsnr

    l_list = query(l_list_list, first=True)

    if case_type == 1:
        l_lager = L_lager()
        db_session.add(l_lager)

        fill_new_l_lager()

    elif case_type == 2:

        l_lager = db_session.query(L_lager).filter(
                (L_lager.lager_nr == l_list.lager_nr)).first()
        l_lager.bezeich = l_list.bezeich
        l_lager.betriebsnr = l_list.betriebsnr

        l_lager = db_session.query(L_lager).first()

    return generate_output()