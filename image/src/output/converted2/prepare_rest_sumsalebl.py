#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Waehrung, Artikel, Hoteldpt

def prepare_rest_sumsalebl(curr_dept:int):

    prepare_cache ([Htparam, Waehrung, Artikel, Hoteldpt])

    ldry = 0
    dstore = 0
    clb = 0
    price_decimal = 0
    exchg_rate = to_decimal("0.0")
    curr_local = ""
    curr_foreign = ""
    anzahl = 0
    sep_line = ""
    dept_name = ""
    from_date = None
    tt_bezeich_list = []
    tt_artnr_list = []
    p_240 = False
    bezeich:List[string] = ["", "", "", "", ""]
    artnr_list:List[int] = [0, 0, 0, 0, 0]
    i:int = 0
    paramnr_list:List[int] = [489, 490, 492, 553, 554]
    htparam = waehrung = artikel = hoteldpt = None

    tt_artnr = tt_bezeich = None

    tt_artnr_list, Tt_artnr = create_model("Tt_artnr", {"curr_i":int, "artnr":int})
    tt_bezeich_list, Tt_bezeich = create_model("Tt_bezeich", {"curr_i":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ldry, dstore, clb, price_decimal, exchg_rate, curr_local, curr_foreign, anzahl, sep_line, dept_name, from_date, tt_bezeich_list, tt_artnr_list, p_240, bezeich, artnr_list, i, paramnr_list, htparam, waehrung, artikel, hoteldpt
        nonlocal curr_dept


        nonlocal tt_artnr, tt_bezeich
        nonlocal tt_artnr_list, tt_bezeich_list

        return {"ldry": ldry, "dstore": dstore, "clb": clb, "price_decimal": price_decimal, "exchg_rate": exchg_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "anzahl": anzahl, "sep_line": sep_line, "dept_name": dept_name, "from_date": from_date, "tt-bezeich": tt_bezeich_list, "tt-artnr": tt_artnr_list, "p_240": p_240}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    p_240 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})
    ldry = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1082)]})
    dstore = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1045)]})
    clb = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    else:
        exchg_rate =  to_decimal("1")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})
    curr_local = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})
    curr_foreign = htparam.fchar
    for i in range(1,5 + 1) :

        htparam = get_cache (Htparam, {"paramnr": [(eq, paramnr_list[i - 1])]})
        artnr_list[i - 1] = htparam.finteger

        if htparam.finteger != 0:
            anzahl = anzahl + 1

            artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 1)]})

            if artikel:
                bezeich[i - 1] = artikel.bezeich
        tt_artnr = Tt_artnr()
        tt_artnr_list.append(tt_artnr)

        tt_artnr.curr_i = i
        tt_artnr.artnr = artnr_list[i - 1]


        tt_bezeich = Tt_bezeich()
        tt_bezeich_list.append(tt_bezeich)

        tt_bezeich.curr_i = i
        tt_bezeich.bezeich = bezeich[i - 1]


    sep_line = ""
    for i in range(1,116 + 1) :
        sep_line = sep_line + "-"

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    from_date = htparam.fdate

    hoteldpt = get_cache (Hoteldpt, {"num": [(gt, 0),(eq, curr_dept)]})

    if hoteldpt:
        dept_name = hoteldpt.depart

    return generate_output()