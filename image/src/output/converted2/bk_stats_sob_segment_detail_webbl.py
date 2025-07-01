#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_veran, Bk_func, Artikel, Bk_rart

input_payload_list, Input_payload = create_model("Input_payload", {"disp_flag":int, "code":int, "to_date":string})

def bk_stats_sob_segment_detail_webbl(input_payload_list:[Input_payload]):

    prepare_cache ([Bk_veran, Bk_func, Artikel, Bk_rart])

    t_list_list = []
    from_date:date = None
    fb_rev:Decimal = to_decimal("0.0")
    other_rev:Decimal = to_decimal("0.0")
    tot_dgroom:int = 0
    tot_mgroom:int = 0
    tot_ygroom:int = 0
    tot_drev:Decimal = to_decimal("0.0")
    tot_mrev:Decimal = to_decimal("0.0")
    tot_yrev:Decimal = to_decimal("0.0")
    tot_d_fbrev:Decimal = to_decimal("0.0")
    tot_m_fbrev:Decimal = to_decimal("0.0")
    tot_y_fbrev:Decimal = to_decimal("0.0")
    tot_dorev:Decimal = to_decimal("0.0")
    tot_morev:Decimal = to_decimal("0.0")
    tot_yorev:Decimal = to_decimal("0.0")
    bk_veran = bk_func = artikel = bk_rart = None

    t_list = input_payload = None

    t_list_list, T_list = create_model("T_list", {"code":int, "veran_nr":int, "gastnr":int, "bestellt__durch":string, "dgroom":int, "mgroom":int, "ygroom":int, "drev":Decimal, "mrev":Decimal, "yrev":Decimal, "d_fbrev":Decimal, "m_fbrev":Decimal, "y_fbrev":Decimal, "dorev":Decimal, "morev":Decimal, "yorev":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_list, from_date, fb_rev, other_rev, tot_dgroom, tot_mgroom, tot_ygroom, tot_drev, tot_mrev, tot_yrev, tot_d_fbrev, tot_m_fbrev, tot_y_fbrev, tot_dorev, tot_morev, tot_yorev, bk_veran, bk_func, artikel, bk_rart


        nonlocal t_list, input_payload
        nonlocal t_list_list

        return {"t-list": t_list_list}

    def create_list():

        nonlocal t_list_list, from_date, fb_rev, other_rev, tot_dgroom, tot_mgroom, tot_ygroom, tot_drev, tot_mrev, tot_yrev, tot_d_fbrev, tot_m_fbrev, tot_y_fbrev, tot_dorev, tot_morev, tot_yorev, bk_veran, bk_func, artikel, bk_rart


        nonlocal t_list, input_payload
        nonlocal t_list_list


        t_list_list.clear()
        from_date = date_mdy(1, 1, get_year(date_mdy(input_payload.to_date)))

        bk_func_obj_list = {}
        bk_func = Bk_func()
        bk_veran = Bk_veran()
        for bk_func.bestellt__durch, bk_func.veran_nr, bk_func.veran_seite, bk_func.rpreis, bk_func.rpersonen, bk_func.technik, bk_func.datum, bk_func._recid, bk_veran.veran_nr, bk_veran.segmentcode, bk_veran.gastnr, bk_veran._recid in db_session.query(Bk_func.bestellt__durch, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.rpreis, Bk_func.rpersonen, Bk_func.technik, Bk_func.datum, Bk_func._recid, Bk_veran.veran_nr, Bk_veran.segmentcode, Bk_veran.gastnr, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr) & (Bk_veran.segmentcode == input_payload.code)).filter(
                 (Bk_func.datum >= from_date) & (Bk_func.datum <= date_mdy(input_payload.to_date))).order_by(Bk_func._recid).all():
            if bk_func_obj_list.get(bk_func._recid):
                continue
            else:
                bk_func_obj_list[bk_func._recid] = True

            t_list = query(t_list_list, filters=(lambda t_list: t_list.veran_nr == bk_veran.veran_nr), first=True)

            if not t_list:
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.code = bk_veran.segmentcode
                t_list.veran_nr = bk_veran.veran_nr
                t_list.bestellt__durch = bk_func.bestellt__durch
                t_list.gastnr = bk_veran.gastnr


                fb_rev =  to_decimal("0")
                other_rev =  to_decimal("0")

            bk_rart_obj_list = {}
            bk_rart = Bk_rart()
            artikel = Artikel()
            for bk_rart.preis, bk_rart.anzahl, bk_rart._recid, artikel.umsatzart, artikel._recid in db_session.query(Bk_rart.preis, Bk_rart.anzahl, Bk_rart._recid, Artikel.umsatzart, Artikel._recid).join(Artikel,(Artikel.artnr == Bk_rart.veran_artnr) & (Artikel.departement == Bk_rart.departement)).filter(
                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                if bk_rart_obj_list.get(bk_rart._recid):
                    continue
                else:
                    bk_rart_obj_list[bk_rart._recid] = True

                if artikel.umsatzart == 5 or artikel.umsatzart == 3 or artikel.umsatzart == 6:
                    fb_rev =  to_decimal(fb_rev) + to_decimal((bk_rart.preis) * to_decimal(bk_rart.anzahl))

                elif artikel.umsatzart == 4:
                    other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(bk_rart.anzahl))

            if bk_func.datum == date_mdy(input_payload.to_date):
                t_list.dgroom = t_list.dgroom + 1
                t_list.drev =  to_decimal(t_list.drev) + to_decimal(bk_func.rpreis[0])
                t_list.d_fbrev =  to_decimal(t_list.d_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                t_list.dorev =  to_decimal(t_list.dorev) + to_decimal(other_rev)
                tot_dgroom = tot_dgroom + 1
                tot_drev =  to_decimal(tot_drev) + to_decimal(bk_func.rpreis[0])
                tot_d_fbrev =  to_decimal(tot_d_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                tot_dorev =  to_decimal(tot_dorev) + to_decimal(other_rev)

            elif get_month(bk_func.datum) == get_month(date_mdy(input_payload.to_date)):
                t_list.mgroom = t_list.mgroom + 1
                t_list.mrev =  to_decimal(t_list.mrev) + to_decimal(bk_func.rpreis[0])
                t_list.m_fbrev =  to_decimal(t_list.m_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                t_list.morev =  to_decimal(t_list.morev) + to_decimal(other_rev)
                tot_mgroom = tot_mgroom + 1
                tot_mrev =  to_decimal(tot_mrev) + to_decimal(bk_func.rpreis[0])
                tot_m_fbrev =  to_decimal(tot_m_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                tot_morev =  to_decimal(tot_morev) + to_decimal(other_rev)


            t_list.ygroom = t_list.ygroom + 1
            t_list.yrev =  to_decimal(t_list.yrev) + to_decimal(bk_func.rpreis[0])
            t_list.y_fbrev =  to_decimal(t_list.y_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
            t_list.yorev =  to_decimal(t_list.yorev) + to_decimal(other_rev)
            tot_ygroom = tot_ygroom + 1
            tot_yrev =  to_decimal(tot_yrev) + to_decimal(bk_func.rpreis[0])
            tot_y_fbrev =  to_decimal(tot_y_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
            tot_yorev =  to_decimal(tot_yorev) + to_decimal(other_rev)


        t_list = T_list()
        t_list_list.append(t_list)

        t_list.bestellt__durch = "T O T A L"
        t_list.dgroom = tot_dgroom
        t_list.mgroom = tot_mgroom
        t_list.ygroom = tot_ygroom
        t_list.drev =  to_decimal(tot_drev)
        t_list.mrev =  to_decimal(tot_mrev)
        t_list.yrev =  to_decimal(tot_yrev)
        t_list.d_fbrev =  to_decimal(tot_d_fbrev)
        t_list.m_fbrev =  to_decimal(tot_m_fbrev)
        t_list.y_fbrev =  to_decimal(tot_y_fbrev)
        t_list.dorev =  to_decimal(tot_dorev)
        t_list.morev =  to_decimal(tot_morev)
        t_list.yorev =  to_decimal(tot_yorev)


    def create_list1():

        nonlocal t_list_list, from_date, fb_rev, other_rev, tot_dgroom, tot_mgroom, tot_ygroom, tot_drev, tot_mrev, tot_yrev, tot_d_fbrev, tot_m_fbrev, tot_y_fbrev, tot_dorev, tot_morev, tot_yorev, bk_veran, bk_func, artikel, bk_rart


        nonlocal t_list, input_payload
        nonlocal t_list_list


        t_list_list.clear()
        from_date = date_mdy(1, 1, get_year(date_mdy(input_payload.to_date)))

        for bk_func in db_session.query(Bk_func).filter(
                 (Bk_func.datum >= from_date) & (Bk_func.datum <= date_mdy(input_payload.to_date)) & (Bk_func.technik[inc_value(1)] == to_string(input_payload.code))).order_by(Bk_func.datum).all():

            t_list = query(t_list_list, filters=(lambda t_list: t_list.veran_nr == bk_func.veran_nr), first=True)

            if not t_list:
                t_list = T_list()
                t_list_list.append(t_list)

                t_list.code = to_int(bk_func.technik[1])
                t_list.veran = bk_func.veran_nr
                t_list.bestellt__durch = bk_func.bestellt__durch

                bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, bk_func.veran_nr)]})

                if bk_veran:
                    t_list.gastnr = bk_veran.gastnr


                fb_rev =  to_decimal("0")
                other_rev =  to_decimal("0")

            bk_rart_obj_list = {}
            bk_rart = Bk_rart()
            artikel = Artikel()
            for bk_rart.preis, bk_rart.anzahl, bk_rart._recid, artikel.umsatzart, artikel._recid in db_session.query(Bk_rart.preis, Bk_rart.anzahl, Bk_rart._recid, Artikel.umsatzart, Artikel._recid).join(Artikel,(Artikel.artnr == Bk_rart.veran_artnr) & (Artikel.departement == Bk_rart.departement)).filter(
                     (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                if bk_rart_obj_list.get(bk_rart._recid):
                    continue
                else:
                    bk_rart_obj_list[bk_rart._recid] = True

                if artikel.umsatzart == 5 or artikel.umsatzart == 3 or artikel.umsatzart == 6:
                    fb_rev =  to_decimal(fb_rev) + to_decimal((bk_rart.preis) * to_decimal(bk_rart.anzahl))

                elif artikel.umsatzart == 4:
                    other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(bk_rart.anzahl))

            if bk_func.datum == date_mdy(input_payload.to_date):
                t_list.dgroom = t_list.dgroom + 1
                t_list.drev =  to_decimal(t_list.drev) + to_decimal(bk_func.rpreis[0])
                t_list.d_fbrev =  to_decimal(t_list.d_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                t_list.dorev =  to_decimal(t_list.dorev) + to_decimal(other_rev)
                tot_dgroom = tot_dgroom + 1
                tot_drev =  to_decimal(tot_drev) + to_decimal(bk_func.rpreis[0])
                tot_d_fbrev =  to_decimal(tot_d_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                tot_dorev =  to_decimal(tot_dorev) + to_decimal(other_rev)

            elif get_month(bk_func.datum) == get_month(date_mdy(input_payload.to_date)):
                t_list.mgroom = t_list.mgroom + 1
                t_list.mrev =  to_decimal(t_list.mrev) + to_decimal(bk_func.rpreis[0])
                t_list.m_fbrev =  to_decimal(t_list.m_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                t_list.morev =  to_decimal(t_list.morev) + to_decimal(other_rev)
                tot_mgroom = tot_mgroom + 1
                tot_mrev =  to_decimal(tot_mrev) + to_decimal(bk_func.rpreis[0])
                tot_m_fbrev =  to_decimal(tot_m_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                tot_morev =  to_decimal(tot_morev) + to_decimal(other_rev)


            t_list.ygroom = t_list.ygroom + 1
            t_list.yrev =  to_decimal(t_list.yrev) + to_decimal(bk_func.rpreis[0])
            t_list.y_fbrev =  to_decimal(t_list.y_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
            t_list.yorev =  to_decimal(t_list.yorev) + to_decimal(other_rev)
            tot_ygroom = tot_ygroom + 1
            tot_yrev =  to_decimal(tot_yrev) + to_decimal(bk_func.rpreis[0])
            tot_y_fbrev =  to_decimal(tot_y_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
            tot_yorev =  to_decimal(tot_yorev) + to_decimal(other_rev)


        t_list = T_list()
        t_list_list.append(t_list)

        t_list.bestellt__durch = "T O T A L"
        t_list.dgroom = tot_dgroom
        t_list.mgroom = tot_mgroom
        t_list.ygroom = tot_ygroom
        t_list.drev =  to_decimal(tot_drev)
        t_list.mrev =  to_decimal(tot_mrev)
        t_list.yrev =  to_decimal(tot_yrev)
        t_list.d_fbrev =  to_decimal(tot_d_fbrev)
        t_list.m_fbrev =  to_decimal(tot_m_fbrev)
        t_list.y_fbrev =  to_decimal(tot_y_fbrev)
        t_list.dorev =  to_decimal(tot_dorev)
        t_list.morev =  to_decimal(tot_morev)
        t_list.yorev =  to_decimal(tot_yorev)

    input_payload = query(input_payload_list, first=True)

    if input_payload.disp_flag == 0:
        create_list()
    else:
        create_list1()

    return generate_output()