from functions.additional_functions import *
import decimal
from functions.prepare_main0 import prepare_main0
from models import Queasy

def check_licnrbl(input_lic_nr:str):
    ok_flag = False
    lstopped:bool = False
    lic_nr:str = ""
    htl_name:str = ""
    h_name:str = ""
    htl_city:str = ""
    h_city:str = ""
    htl_adr:str = ""
    htl_tel:str = ""
    vhp_multi:bool = False
    vhp_lite:bool = False
    rest_lic:bool = False
    eng_dept:int = 0
    i_param111:int = 0
    i_param297:int = 0
    p_decimal:int = 0
    d_currency:bool = False
    msg_str:str = ""
    queasy = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ok_flag, lstopped, lic_nr, htl_name, h_name, htl_city, h_city, htl_adr, htl_tel, vhp_multi, vhp_lite, rest_lic, eng_dept, i_param111, i_param297, p_decimal, d_currency, msg_str, queasy
        nonlocal input_lic_nr


        nonlocal t_queasy
        nonlocal t_queasy_list

        return {"ok_flag": ok_flag}


    lstopped, lic_nr, htl_name, h_name, htl_city, h_city, htl_adr, htl_tel, vhp_multi, vhp_lite, rest_lic, eng_dept, i_param111, i_param297, p_decimal, d_currency, msg_str, t_queasy_list = get_output(prepare_main0(0))
    lic_nr = entry(2, lic_nr, " ")

    if lic_nr.lower()  != (input_lic_nr).lower() :
        ok_flag = False
    else:
        ok_flag = True

    return generate_output()