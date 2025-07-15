#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Katpreis, Arrangement

p_list_data, P_list = create_model_like(Katpreis)

def rmcat_rate_btn_gobl(p_list_data:[P_list], case_type:int, curr_arg:string, rec_id:int):

    prepare_cache ([Katpreis, Arrangement])

    katpreis = arrangement = None

    p_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal katpreis, arrangement
        nonlocal case_type, curr_arg, rec_id


        nonlocal p_list

        return {}

    def fill_katpreis():

        nonlocal katpreis, arrangement
        nonlocal case_type, curr_arg, rec_id


        nonlocal p_list

        arr = None
        Arr =  create_buffer("Arr",Arrangement)

        arr = get_cache (Arrangement, {"arrangement": [(eq, curr_arg)]})

        if arr:
            katpreis.argtnr = arr.argtnr
        katpreis.zikatnr = p_list.zikatnr
        katpreis.startperiode = p_list.startperiode
        katpreis.endperiode = p_list.endperiode
        katpreis.betriebsnr = p_list.betriebsnr
        katpreis.perspreis[0] = p_list.perspreis[0]
        katpreis.perspreis[1] = p_list.perspreis[1]
        katpreis.perspreis[2] = p_list.perspreis[2]
        katpreis.perspreis[3] = p_list.perspreis[3]
        katpreis.kindpreis[0] = p_list.kindpreis[0]
        katpreis.kindpreis[1] = p_list.kindpreis[1]


    p_list = query(p_list_data, first=True)

    if case_type == 1:
        katpreis = Katpreis()
        db_session.add(katpreis)

        fill_katpreis()

    elif case_type == 2:

        katpreis = get_cache (Katpreis, {"_recid": [(eq, rec_id)]})

        if katpreis:
            pass
            fill_katpreis()
            pass
            pass

    return generate_output()