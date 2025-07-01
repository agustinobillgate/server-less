#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.s_stockout_l_bestandbl import s_stockout_l_bestandbl
from models import L_artikel, Gl_acct

def s_stockout_btn_help2_webbl(s_artnr:int, curr_lager:int):

    prepare_cache ([L_artikel, Gl_acct])

    t_stock_oh = to_decimal("0.0")
    avail_l_bestand = False
    temp_l_artikel_list = []
    l_artikel = gl_acct = None

    temp_l_artikel = None

    temp_l_artikel_list, Temp_l_artikel = create_model("Temp_l_artikel", {"artnr":int, "bezeich":string, "betriebsnr":int, "endkum":int, "masseinheit":string, "vk_preis":Decimal, "inhalt":Decimal, "lief_einheit":Decimal, "traubensort":string, "fibukonto":string, "cost_alloc":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_stock_oh, avail_l_bestand, temp_l_artikel_list, l_artikel, gl_acct
        nonlocal s_artnr, curr_lager


        nonlocal temp_l_artikel
        nonlocal temp_l_artikel_list

        return {"t_stock_oh": t_stock_oh, "avail_l_bestand": avail_l_bestand, "temp-l-artikel": temp_l_artikel_list}

    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})
    temp_l_artikel = Temp_l_artikel()
    temp_l_artikel_list.append(temp_l_artikel)

    temp_l_artikel.artnr = l_artikel.artnr
    temp_l_artikel.bezeich = l_artikel.bezeich
    temp_l_artikel.betriebsnr = l_artikel.betriebsnr
    temp_l_artikel.endkum = l_artikel.endkum
    temp_l_artikel.masseinheit = l_artikel.masseinheit
    temp_l_artikel.vk_preis =  to_decimal(l_artikel.vk_preis)
    temp_l_artikel.inhalt =  to_decimal(l_artikel.inhalt)
    temp_l_artikel.lief_einheit =  to_decimal(l_artikel.lief_einheit)
    temp_l_artikel.traubensort = l_artikel.traubensorte
    temp_l_artikel.fibukonto = l_artikel.fibukonto

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_artikel.fibukonto)]})

    if gl_acct:
        temp_l_artikel.cost_alloc = gl_acct.bezeich
    t_stock_oh, avail_l_bestand = get_output(s_stockout_l_bestandbl(curr_lager, s_artnr))

    return generate_output()