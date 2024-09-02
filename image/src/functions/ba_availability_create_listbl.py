from functions.additional_functions import *
import decimal
from datetime import date
from models import Bk_rart, Bk_func, Artikel, Bk_reser

def ba_availability_create_listbl(ba_dept:int, z_zknr:int, curr_date:date):
    art_list_list = []
    q3_list_list = []
    bk_rart = bk_func = artikel = bk_reser = None

    art_list = r_list = q3_list = None

    art_list_list, Art_list = create_model("Art_list", {"artnr":int, "bezeich":str, "h_our":[int, 48], "astatus":[int, 48]})
    r_list_list, R_list = create_model_like(Bk_rart)
    q3_list_list, Q3_list = create_model_like(R_list, {"uhrzeit":str, "raeume":str, "bestellt__durch":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal art_list_list, q3_list_list, bk_rart, bk_func, artikel, bk_reser


        nonlocal art_list, r_list, q3_list
        nonlocal art_list_list, r_list_list, q3_list_list
        return {"art-list": art_list_list, "q3-list": q3_list_list}

    def create_list():

        nonlocal art_list_list, q3_list_list, bk_rart, bk_func, artikel, bk_reser


        nonlocal art_list, r_list, q3_list
        nonlocal art_list_list, r_list_list, q3_list_list

        i:int = 0
        from_i:int = 0
        to_i:int = 0
        art_list_list.clear()
        r_list_list.clear()

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == ba_dept) &  (Artikel.zwkum == z_zknr)).all():
            art_list = Art_list()
            art_list_list.append(art_list)

            art_list.bezeich = artikel.bezeich
            art_list.artnr = artikel.artnr
            for i in range(1,48 + 1) :
                art_list.h_our[i - 1] = artikel.anzahl

            bk_rart_obj_list = []
            for bk_rart, bk_reser in db_session.query(Bk_rart, Bk_reser).join(Bk_reser,(Bk_reser.veran_nr == Bk_rart.veran_nr) &  (Bk_reser.veran_resnr == Bk_rart.veran_resnr) &  (bk_rese.resstatus == 1) &  (Bk_reser.datum == curr_date)).filter(
                    (Bk_rart.veran_artnr == artikel.artnr)).all():
                if bk_rart._recid in bk_rart_obj_list:
                    continue
                else:
                    bk_rart_obj_list.append(bk_rart._recid)

                r_list = query(r_list_list, filters=(lambda r_list :r_list.veran_artnr == bk_rart.veran_artnr and r_list.veran_nr == bk_rart.veran_nr and r_list.veran_resnr == bk_rart.veran_resnr), first=True)

                if not r_list:
                    r_list = R_list()
                    r_list_list.append(r_list)

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

    for r_list in query(r_list_list):
        bk_func = db_session.query(Bk_func).filter((Bk_func.veran_nr == r_list.veran_nr) &  (Bk_func.veran_seite == r_list.veran_seite)).first()
        if not bk_func:
            continue

        q3_list = Q3_list()
        q3_list_list.append(q3_list)

        q3_list.uhrzeit = bk_func.uhrzeit
        q3_list.raeume = bk_func.raeume[0]
        q3_list.bestellt__durch = bk_func.bestellt__durch

    return generate_output()