#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel, Bk_veran, Htparam, Waehrung

def ba_depopaybl(veran_nr:int):

    prepare_cache ([Artikel, Htparam, Waehrung])

    currency = ""
    exchg_rate = to_decimal("0.0")
    bqt_dept = 0
    art_depo = 0
    err_msg = 0
    depoart = 0
    depobezeich = ""
    price_decimal = 0
    double_currency = False
    depobuff_list = []
    veran_list_list = []
    artikel = bk_veran = htparam = waehrung = None

    depobuff = veran_list = bartikel = None

    depobuff_list, Depobuff = create_model_like(Artikel)
    veran_list_list, Veran_list = create_model_like(Bk_veran)

    Bartikel = create_buffer("Bartikel",Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal currency, exchg_rate, bqt_dept, art_depo, err_msg, depoart, depobezeich, price_decimal, double_currency, depobuff_list, veran_list_list, artikel, bk_veran, htparam, waehrung
        nonlocal veran_nr
        nonlocal bartikel


        nonlocal depobuff, veran_list, bartikel
        nonlocal depobuff_list, veran_list_list

        return {"currency": currency, "exchg_rate": exchg_rate, "bqt_dept": bqt_dept, "art_depo": art_depo, "err_msg": err_msg, "depoart": depoart, "depobezeich": depobezeich, "price_decimal": price_decimal, "double_currency": double_currency, "depobuff": depobuff_list, "veran-list": veran_list_list}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    if htparam:
        currency = htparam.fchar

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})

    if htparam:
        bqt_dept = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 117)]})

    if htparam:
        art_depo = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})

    if htparam:
        price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})

    if htparam:
        double_currency = htparam.flogical

    artikel = get_cache (Artikel, {"artnr": [(eq, art_depo)],"departement": [(eq, bqt_dept)],"artart": [(eq, 5)]})

    if not artikel:

        bartikel = get_cache (Artikel, {"artnr": [(eq, art_depo)],"departement": [(eq, 0)],"artart": [(eq, 5)]})

        if not bartikel:
            err_msg = 1


        else:
            depoart = bartikel.artnr
            depobezeich = bartikel.bezeich


    else:
        depoart = artikel.artnr
        depobezeich = artikel.bezeich

    bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, veran_nr)]})

    if bk_veran:
        veran_list = Veran_list()
        veran_list_list.append(veran_list)

        buffer_copy(bk_veran, veran_list)

    for artikel in db_session.query(Artikel).order_by(Artikel._recid).all():
        depobuff = Depobuff()
        depobuff_list.append(depobuff)

        buffer_copy(artikel, depobuff)

    return generate_output()