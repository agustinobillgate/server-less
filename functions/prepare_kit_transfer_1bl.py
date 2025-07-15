#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from functions.htpdate import htpdate
from models import Hoteldpt, Htparam, Waehrung, H_artikel, Artikel

def prepare_kit_transfer_1bl(curr_dept:int):

    prepare_cache ([Htparam, Waehrung, H_artikel, Artikel])

    price_decimal = 0
    curr_local = ""
    foreign_nr = 0
    curr_foreign = ""
    double_currency = False
    foreign_rate = False
    exchg_rate = 1
    deptname = ""
    b_title = ""
    p_852 = 0
    p_135 = False
    p_134 = False
    p_479 = False
    p_110 = None
    t_h_artikel_data = []
    t_artikel_data = []
    t_hoteldpt_data = []
    hoteldpt = htparam = waehrung = h_artikel = artikel = None

    t_hoteldpt = t_artikel = t_h_artikel = None

    t_hoteldpt_data, T_hoteldpt = create_model_like(Hoteldpt)
    t_artikel_data, T_artikel = create_model("T_artikel", {"artnr":int, "departement":int, "bezeich":string, "pricetab":bool})
    t_h_artikel_data, T_h_artikel = create_model("T_h_artikel", {"artnr":int, "departement":int, "artnrfront":int, "bezeich":string, "epreis1":Decimal, "epreis2":Decimal, "artart":int, "bezaendern":bool, "autosaldo":bool, "mwst_code":int, "service_code":int, "prozent":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, curr_local, foreign_nr, curr_foreign, double_currency, foreign_rate, exchg_rate, deptname, b_title, p_852, p_135, p_134, p_479, p_110, t_h_artikel_data, t_artikel_data, t_hoteldpt_data, hoteldpt, htparam, waehrung, h_artikel, artikel
        nonlocal curr_dept


        nonlocal t_hoteldpt, t_artikel, t_h_artikel
        nonlocal t_hoteldpt_data, t_artikel_data, t_h_artikel_data

        return {"price_decimal": price_decimal, "curr_local": curr_local, "foreign_nr": foreign_nr, "curr_foreign": curr_foreign, "double_currency": double_currency, "foreign_rate": foreign_rate, "exchg_rate": exchg_rate, "deptname": deptname, "b_title": b_title, "p_852": p_852, "p_135": p_135, "p_134": p_134, "p_479": p_479, "p_110": p_110, "t-h-artikel": t_h_artikel_data, "t-artikel": t_artikel_data, "t-hoteldpt": t_hoteldpt_data}


    p_135 = get_output(htplogic(135))
    p_134 = get_output(htplogic(134))
    p_479 = get_output(htplogic(479))
    p_110 = get_output(htpdate(110))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 852)]})
    p_852 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})
    curr_local = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    if htparam.fchar != "":

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            foreign_nr = waehrung.waehrungsnr
        curr_foreign = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    if foreign_rate or double_currency:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})
    deptname = hoteldpt.depart
    b_title = hoteldpt.depart

    for h_artikel in db_session.query(H_artikel).filter(
             (H_artikel.departement == curr_dept) & (H_artikel.activeflag == yes)).order_by(H_artikel._recid).all():
        t_h_artikel = T_h_artikel()
        t_h_artikel_data.append(t_h_artikel)

        t_h_artikel.artnr = h_artikel.artnr
        t_h_artikel.departement = h_artikel.departement
        t_h_artikel.artnrfront = h_artikel.artnrfront
        t_h_artikel.bezeich = h_artikel.bezeich
        t_h_artikel.epreis1 =  to_decimal(h_artikel.epreis1)
        t_h_artikel.epreis2 =  to_decimal(h_artikel.epreis2)
        t_h_artikel.artart = h_artikel.artart
        t_h_artikel.bezaendern = h_artikel.bezaendern
        t_h_artikel.autosaldo = h_artikel.autosaldo
        t_h_artikel.mwst_code = h_artikel.mwst_code
        t_h_artikel.service_code = h_artikel.service_code
        t_h_artikel.prozent =  to_decimal(h_artikel.prozent)

    for artikel in db_session.query(Artikel).order_by(Artikel._recid).all():
        t_artikel = T_artikel()
        t_artikel_data.append(t_artikel)

        t_artikel.artnr = artikel.artnr
        t_artikel.departement = artikel.departement
        t_artikel.bezeich = artikel.bezeich
        t_artikel.pricetab = artikel.pricetab

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_data.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()