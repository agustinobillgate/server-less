#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_rart, Bk_func, Artikel, Bk_reser

def ba_availability_create_listbl(ba_dept:int, z_zknr:int, curr_date:date):

    prepare_cache ([Bk_func, Artikel, Bk_reser])

    art_list_data = []
    q3_list_data = []
    bk_rart = bk_func = artikel = bk_reser = None

    art_list = r_list = q3_list = None

    art_list_data, Art_list = create_model("Art_list", {"artnr":int, "bezeich":string, "h_our":[int,48], "astatus":[int,48]})
    r_list_data, R_list = create_model_like(Bk_rart)
    q3_list_data, Q3_list = create_model_like(R_list, {"uhrzeit":string, "raeume":string, "bestellt__durch":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal art_list_data, q3_list_data, bk_rart, bk_func, artikel, bk_reser
        nonlocal ba_dept, z_zknr, curr_date


        nonlocal art_list, r_list, q3_list
        nonlocal art_list_data, r_list_data, q3_list_data

        return {"art-list": art_list_data, "q3-list": q3_list_data}

    def create_list():

        nonlocal art_list_data, q3_list_data, bk_rart, bk_func, artikel, bk_reser
        nonlocal ba_dept, z_zknr, curr_date


        nonlocal art_list, r_list, q3_list
        nonlocal art_list_data, r_list_data, q3_list_data

        i:int = 0
        from_i:int = 0
        to_i:int = 0
        art_list_data.clear()
        r_list_data.clear()

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == ba_dept) & (Artikel.zwkum == z_zknr)).order_by(Artikel._recid).all():
            art_list = Art_list()
            art_list_data.append(art_list)

            art_list.bezeich = artikel.bezeich
            art_list.artnr = artikel.artnr
            for i in range(1,48 + 1) :
                art_list.h_our[i - 1] = artikel.anzahl

            bk_rart_obj_list = {}
            for bk_rart, bk_reser in db_session.query(Bk_rart, Bk_reser).join(Bk_reser,(Bk_reser.veran_nr == Bk_rart.veran_nr) & (Bk_reser.veran_resnr == Bk_rart.veran_resnr) & (Bk_reser.resstatus == 1) & (Bk_reser.datum == curr_date)).filter(
                     (Bk_rart.veran_artnr == artikel.artnr)).order_by(Bk_rart._recid).all():
                if bk_rart_obj_list.get(bk_rart._recid):
                    continue
                else:
                    bk_rart_obj_list[bk_rart._recid] = True

                r_list = query(r_list_data, filters=(lambda r_list: r_list.veran_artnr == bk_rart.veran_artnr and r_list.veran_nr == bk_rart.veran_nr and r_list.veran_resnr == bk_rart.veran_resnr), first=True)

                if not r_list:
                    r_list = R_list()
                    r_list_data.append(r_list)

                    buffer_copy(bk_rart, r_list)
                else:
                    r_list.anzahl = r_list.anzahl + bk_rart.anzahl
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

    create_list()

    for r_list in query(r_list_data, sort_by=[("raum",False)]):

        bk_func = get_cache (Bk_func, {"veran_nr": [(eq, r_list.veran_nr)],"veran_seite": [(eq, r_list.veran_seite)]})

        if bk_func:
            q3_list = Q3_list()
            q3_list_data.append(q3_list)

            q3_list.uhrzeit = bk_func.uhrzeit
            q3_list.raeume = bk_func.raeume[0]
            q3_list.bestellt__durch = bk_func.bestellt__durch

    return generate_output()