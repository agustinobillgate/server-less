#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Arrangement, Waehrung, Katpreis

def mk_resline_leave_zipreisbl(from_date:date, to_date:date, r_arrangement:string, r_betriebsnr:int, local_nr:int, price_decimal:int, rmcat:int):

    prepare_cache ([Htparam, Arrangement, Waehrung])

    wrong_price = False
    exrate1 = 1
    exrate2 = 1
    t_list_list = []
    datum:date = None
    tol_value:Decimal = to_decimal("0.0")
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    htparam = arrangement = waehrung = katpreis = None

    t_list = htp1 = None

    t_list_list, T_list = create_model("T_list", {"datum":date, "avail_katpreis":bool})

    Htp1 = create_buffer("Htp1",Htparam)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal wrong_price, exrate1, exrate2, t_list_list, datum, tol_value, wd_array, htparam, arrangement, waehrung, katpreis
        nonlocal from_date, to_date, r_arrangement, r_betriebsnr, local_nr, price_decimal, rmcat
        nonlocal htp1


        nonlocal t_list, htp1
        nonlocal t_list_list

        return {"wrong_price": wrong_price, "exrate1": exrate1, "exrate2": exrate2, "t-list": t_list_list}

    arrangement = get_cache (Arrangement, {"arrangement": [(eq, r_arrangement)]})

    if not arrangement:
        wrong_price = True

        return generate_output()

    htp1 = get_cache (Htparam, {"paramnr": [(eq, 145)]})

    if r_betriebsnr == local_nr and (price_decimal == 0):
        tol_value =  to_decimal(htp1.finteger) * to_decimal("10")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exrate1 =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, r_betriebsnr)]})

    if waehrung:
        exrate2 =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    for datum in date_range(from_date,to_date) :

        katpreis = get_cache (Katpreis, {"zikatnr": [(eq, rmcat)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"betriebsnr": [(eq, wd_array[get_weekday(datum) - 1])]})

        if not katpreis:

            katpreis = get_cache (Katpreis, {"zikatnr": [(eq, rmcat)],"argtnr": [(eq, arrangement.argtnr)],"startperiode": [(le, datum)],"endperiode": [(ge, datum)],"betriebsnr": [(eq, 0)]})
        t_list = T_list()
        t_list_list.append(t_list)

        t_list.datum = datum
        t_list.avail_katpreis = None != katpreis

    return generate_output()