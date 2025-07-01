#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Paramtext

def check_htl_name_adminbl():

    prepare_cache ([Paramtext])

    flag = False
    t_list_list = []
    htparam = paramtext = None

    t_list = None

    t_list_list, T_list = create_model("T_list", {"htl_name":string, "htl_adr1":string, "htl_adr2":string, "htl_adr3":string, "htl_tel":string, "htl_fax":string, "htl_email":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, t_list_list, htparam, paramtext


        nonlocal t_list
        nonlocal t_list_list

        return {"flag": flag, "t-list": t_list_list}

    def fill_list():

        nonlocal flag, t_list_list, htparam, paramtext


        nonlocal t_list
        nonlocal t_list_list

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
        t_list.htl_name = paramtext.ptexte

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})
        t_list.htl_adr1 = paramtext.ptexte

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 202)]})
        t_list.htl_adr2 = paramtext.ptexte

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 203)]})
        t_list.htl_adr3 = paramtext.ptexte

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})
        t_list.htl_tel = paramtext.ptexte

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 205)]})
        t_list.htl_fax = paramtext.ptexte

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 206)]})
        t_list.htl_email = paramtext.ptexte


    htparam = get_cache (Htparam, {"paramnr": [(eq, 996)]})

    if not htparam.flogical:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1015)]})

        if not htparam.flogical:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 990)]})

            if htparam.flogical:
                flag = True
    t_list = T_list()
    t_list_list.append(t_list)

    fill_list()

    return generate_output()