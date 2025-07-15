#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Waehrung, Arrangement

def prepare_rm_product_1bl():

    prepare_cache ([Htparam, Waehrung, Arrangement])

    price_decimal = 0
    foreign_nr = 0
    f_log = False
    t_argt_data = []
    htparam = waehrung = arrangement = None

    t_argt = None

    t_argt_data, T_argt = create_model("T_argt", {"code":string, "name":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, foreign_nr, f_log, t_argt_data, htparam, waehrung, arrangement


        nonlocal t_argt
        nonlocal t_argt_data

        return {"price_decimal": price_decimal, "foreign_nr": foreign_nr, "f_log": f_log, "t-argt": t_argt_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    if htparam.fchar != "":

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            foreign_nr = waehrung.waehrungsnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    f_log = htparam.flogical

    for arrangement in db_session.query(Arrangement).order_by(Arrangement._recid).all():
        t_argt = T_argt()
        t_argt_data.append(t_argt)

        t_argt.code = arrangement.arrangement
        t_argt.name = arrangement.argt_bez

    return generate_output()