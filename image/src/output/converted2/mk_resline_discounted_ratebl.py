#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Katpreis, Arrangement, Htparam, Waehrung

def mk_resline_discounted_ratebl(res_mode:string, r_arrangement:string, r_betriebsnr:int, r_ankunft:date, r_zikatnr:int, r_erwachs:int, r_kind1:int, r_kind2:int, ci_date:date):

    prepare_cache ([Arrangement, Htparam, Waehrung])

    exrate1 = 1
    exrate2 = 1
    t_katpreis_list = []
    datum:date = None
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    katpreis = arrangement = htparam = waehrung = None

    t_katpreis = None

    t_katpreis_list, T_katpreis = create_model_like(Katpreis)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal exrate1, exrate2, t_katpreis_list, datum, wd_array, katpreis, arrangement, htparam, waehrung
        nonlocal res_mode, r_arrangement, r_betriebsnr, r_ankunft, r_zikatnr, r_erwachs, r_kind1, r_kind2, ci_date


        nonlocal t_katpreis
        nonlocal t_katpreis_list

        return {"exrate1": exrate1, "exrate2": exrate2, "t-katpreis": t_katpreis_list}

    arrangement = get_cache (Arrangement, {"arrangement": [(eq, r_arrangement)]})

    if not arrangement:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exrate1 =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, r_betriebsnr)]})

    if waehrung:
        exrate2 =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    datum = r_ankunft

    if res_mode.lower()  == ("inhouse").lower() :
        datum = ci_date

    katpreis = get_cache (Katpreis, {"zikatnr": [(eq, r_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"betriebsnr": [(eq, wd_array[get_weekday(datum) - 1])]})

    if not katpreis:

        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, r_zikatnr)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"betriebsnr": [(eq, 0)]})

    if not katpreis:

        return generate_output()
    else:
        t_katpreis = T_katpreis()
        t_katpreis_list.append(t_katpreis)

        buffer_copy(katpreis, t_katpreis)

    return generate_output()