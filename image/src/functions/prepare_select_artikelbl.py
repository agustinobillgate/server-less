from functions.additional_functions import *
import decimal
from datetime import date
from models import Bk_reser, Htparam, Waehrung, Artikel, Bk_rart

def prepare_select_artikelbl(veran_nr:int, veran_seite:int, sub_group:int):
    curr_date = None
    bill_date = None
    ba_dept = 0
    double_currency = False
    foreign_rate = False
    exchg_rate = 0
    art_list_list = []
    bk_reser = htparam = waehrung = artikel = bk_rart = None

    art_list = None

    art_list_list, Art_list = create_model("Art_list", {"artnr":int, "bezeich":str, "h_our":[int, 48], "astatus":[int, 48]})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_date, bill_date, ba_dept, double_currency, foreign_rate, exchg_rate, art_list_list, bk_reser, htparam, waehrung, artikel, bk_rart


        nonlocal art_list
        nonlocal art_list_list
        return {"curr_date": curr_date, "bill_date": bill_date, "ba_dept": ba_dept, "double_currency": double_currency, "foreign_rate": foreign_rate, "exchg_rate": exchg_rate, "art-list": art_list_list}

    def create_availability():

        nonlocal curr_date, bill_date, ba_dept, double_currency, foreign_rate, exchg_rate, art_list_list, bk_reser, htparam, waehrung, artikel, bk_rart


        nonlocal art_list
        nonlocal art_list_list

        i:int = 0
        from_i:int = 0
        to_i:int = 0
        art_list_list.clear()

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == ba_dept) &  (Artikel.zwkum == sub_group) &  (Artikel.activeflag)).all():
            art_list = Art_list()
            art_list_list.append(art_list)

            art_list.bezeich = artikel.bezeich
            art_list.artnr = artikel.artnr
            for i in range(1,48 + 1) :
                art_list.h_our[i - 1] = artikel.anzahl

            bk_rart_obj_list = []
            for bk_rart, bk_reser in db_session.query(Bk_rart, Bk_reser).join(Bk_reser,(Bk_reser.veran_nr == Bk_rart.veran_nr) &  (Bk_reser.veran_resnr == Bk_rart.veran_resnr) &  (Bk_reser.datum == curr_date)).filter(
                    (Bk_rart.veran_artnr == artikel.artnr)).all():
                if bk_rart._recid in bk_rart_obj_list:
                    continue
                else:
                    bk_rart_obj_list.append(bk_rart._recid)


                from_i = bk_reser.von_i
                to_i = bk_reser.bis_i
                for i in range(from_i,to_i + 1) :
                    art_list.h_our[i - 1] = art_list.h_our[i - 1] - bk_rart.anzahl
            for i in range(1,48 + 1) :

                if art_list.h_our[i - 1] == artikel.anzahl:
                    art_list.astatus[i - 1] = 15
                else:

                    if art_list.h_our[i - 1] > 0:
                        art_list.astatus[i - 1] = 10

                    elif art_list.h_our[i - 1] == 0:
                        art_list.astatus[i - 1] = 14

                    elif art_list.h_our[i - 1] < 0:
                        art_list.astatus[i - 1] = 12

    bk_reser = db_session.query(Bk_reser).filter(
            (Bk_reser.veran_nr == veran_nr) &  (Bk_reser.veran_resnr == veran_seite)).first()
    curr_date = bk_reser.datum

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 900)).first()
    ba_dept = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    if foreign_rate or double_currency:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate = waehrung.ankauf / waehrung.einheit
    create_availability()

    return generate_output()