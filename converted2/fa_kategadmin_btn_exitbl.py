#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_kateg

l_list_data, L_list = create_model_like(Fa_kateg)

def fa_kategadmin_btn_exitbl(l_list_data:[L_list], case_type:int, rec_id:int):

    prepare_cache ([Fa_kateg])

    fa_kateg = None

    l_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_kateg
        nonlocal case_type, rec_id


        nonlocal l_list

        return {}

    def fill_new_fa_kateg():

        nonlocal fa_kateg
        nonlocal case_type, rec_id


        nonlocal l_list


        fa_kateg.katnr = l_list.katnr
        fa_kateg.bezeich = l_list.bezeich
        fa_kateg.nutzjahr = l_list.nutzjahr
        fa_kateg.rate =  to_decimal(l_list.rate)


    l_list = query(l_list_data, first=True)

    if case_type == 1:
        fa_kateg = Fa_kateg()
        db_session.add(fa_kateg)

        fill_new_fa_kateg()
    else:

        fa_kateg = get_cache (Fa_kateg, {"_recid": [(eq, rec_id)]})
        pass
        fa_kateg.bezeich = l_list.bezeich
        fa_kateg.nutzjahr = l_list.nutzjahr
        fa_kateg.rate =  to_decimal(l_list.rate)
        pass

    return generate_output()