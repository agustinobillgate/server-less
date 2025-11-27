#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Katpreis, Arrangement

p_list_data, P_list = create_model("P_list", {"argtnr":int, "betriebsnr":int, "endperiode":date, "kindpreis":[Decimal, 2], "perspreis":[Decimal, 4], "startperiode":date, "zikatnr":int})


def rmcat_rate_btn_gobl(p_list_data:[P_list], case_type:int, curr_arg:int, rec_id:int):

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
        arr = get_cache (Arrangement, {"argtnr": [(eq, curr_arg)]})

        if arr:
            katpreis.argtnr = arr.argtnr

        katpreis.zikatnr = p_list.zikatnr
        katpreis.startperiode = p_list.startperiode
        katpreis.endperiode = p_list.endperiode
        katpreis.betriebsnr = p_list.betriebsnr

        if katpreis.perspreis[4] != 0:
            p_list.perspreis.append(katpreis.perspreis[4])
        else:
            p_list.perspreis.append(to_decimal(0))

        if katpreis.perspreis[5] != 0:
            p_list.perspreis.append(katpreis.perspreis[5])
        else:
            p_list.perspreis.append(to_decimal(0))

        katpreis.perspreis= p_list.perspreis
        katpreis.kindpreis = p_list.kindpreis


    p_list = query(p_list_data, first=True)

    for i, convert in enumerate(p_list.perspreis):
        p_list.perspreis[i] = to_decimal(convert)
    for i, convert in enumerate(p_list.kindpreis):
        p_list.kindpreis[i] = to_decimal(convert)

    if case_type == 1:
        katpreis = Katpreis()
        db_session.add(katpreis)

        fill_katpreis()

    elif case_type == 2:

        # katpreis = get_cache (Katpreis, {"_recid": [(eq, rec_id)]})
        katpreis = db_session.query(Katpreis).filter(
                 (Katpreis._recid == rec_id)).with_for_update().first()

        if katpreis:
            fill_katpreis()

    return generate_output()