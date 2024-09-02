from functions.additional_functions import *
import decimal
from models import Artikel, Bk_veran, Htparam, Waehrung

def ba_deporefundbl(veran_nr:int):
    currency = ""
    exchg_rate = 0
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

    Bartikel = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal currency, exchg_rate, bqt_dept, art_depo, err_msg, depoart, depobezeich, price_decimal, double_currency, depobuff_list, veran_list_list, artikel, bk_veran, htparam, waehrung
        nonlocal bartikel


        nonlocal depobuff, veran_list, bartikel
        nonlocal depobuff_list, veran_list_list
        return {"currency": currency, "exchg_rate": exchg_rate, "bqt_dept": bqt_dept, "art_depo": art_depo, "err_msg": err_msg, "depoart": depoart, "depobezeich": depobezeich, "price_decimal": price_decimal, "double_currency": double_currency, "depobuff": depobuff_list, "veran-list": veran_list_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    if htparam:
        currency = htparam.fchar

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate = waehrung.ankauf / waehrung.einheit

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 900)).first()

    if htparam:
        bqt_dept = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 117)).first()

    if htparam:
        art_depo = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()

    if htparam:
        price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()

    if htparam:
        double_currency = htparam.flogical

    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == art_depo) &  (Artikel.departement == bqt_dept) &  (Artikel.artart == 5)).first()

    if not artikel:

        bartikel = db_session.query(Bartikel).filter(
                (Bartikel.artnr == art_depo) &  (Bartikel.departement == 0) &  (Bartikel.artart == 5)).first()

        if not bartikel:
            err_msg = 1


        else:
            depoart = bartikel.artnr
            depobezeich = bartikel.bezeich


    else:
        depoart = artikel.artnr
        depobezeich = artikel.bezeich

    bk_veran = db_session.query(Bk_veran).filter(
            (Bk_veran.veran_nr == veran_nr)).first()

    if bk_veran:
        veran_list = Veran_list()
        veran_list_list.append(veran_list)

        buffer_copy(bk_veran, veran_list)

    for artikel in db_session.query(Artikel).all():
        depobuff = Depobuff()
        depobuff_list.append(depobuff)

        buffer_copy(artikel, depobuff)

    return generate_output()