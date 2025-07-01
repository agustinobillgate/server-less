#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.view_staycostbl import view_staycostbl
from models import Htparam, Waehrung

def mk_resline_view_staycostbl(pvilanguage:int, ankunft:date, abreise:date, contcode:string, currency:string, curr_rmcat:string, curr_argt:string, rate_zikat:string, zimmer_wunsch:string, inp_gastnr:int, inp_resnr:int, inp_reslinnr:int, marketnr:int, zimmeranz:int, pax:int, kind1:int, inp_rmrate:Decimal):

    prepare_cache ([Htparam])

    output_list_list = []
    new_contrate:bool = False
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    bonus_array:List[bool] = create_empty_list(999, False)
    ci_date:date = None
    lvcarea:string = "view-staycost"
    htparam = waehrung = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"flag":int, "str":string, "str1":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, new_contrate, wd_array, bonus_array, ci_date, lvcarea, htparam, waehrung
        nonlocal pvilanguage, ankunft, abreise, contcode, currency, curr_rmcat, curr_argt, rate_zikat, zimmer_wunsch, inp_gastnr, inp_resnr, inp_reslinnr, marketnr, zimmeranz, pax, kind1, inp_rmrate


        nonlocal output_list
        nonlocal output_list_list

        return {"output-list": output_list_list}

    def get_rackrate(erwachs:int, kind1:int, kind2:int):

        nonlocal output_list_list, new_contrate, wd_array, bonus_array, ci_date, lvcarea, htparam, waehrung
        nonlocal pvilanguage, ankunft, abreise, contcode, currency, curr_rmcat, curr_argt, rate_zikat, zimmer_wunsch, inp_gastnr, inp_resnr, inp_reslinnr, marketnr, zimmeranz, pax, inp_rmrate


        nonlocal output_list
        nonlocal output_list_list

        rate:Decimal = to_decimal("0.0")

        if erwachs >= 1 and erwachs <= 4:
            rate =  to_decimal(rate) + to_decimal(katpreis.perspreis[erwachs - 1])
        rate =  to_decimal(rate) + to_decimal(kind1) * to_decimal(katpreis.kindpreis[0] + kind2) * to_decimal(katpreis.kindpreis[1])
        return rate


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, currency)]})

    if not waehrung:

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, "1")]})
    output_list_list = get_output(view_staycostbl(pvilanguage, inp_resnr, inp_reslinnr, contcode))

    return generate_output()