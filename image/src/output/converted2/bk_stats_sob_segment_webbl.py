#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_veran, Bk_func, Queasy, Artikel, Bk_rart

input_payload_list, Input_payload = create_model("Input_payload", {"disp_flag":int, "to_date":string})

def bk_stats_sob_segment_webbl(input_payload_list:[Input_payload]):

    prepare_cache ([Bk_veran, Bk_func, Queasy, Artikel, Bk_rart])

    bk_statistic_list_list = []
    from_date:date = None
    fb_rev:Decimal = to_decimal("0.0")
    other_rev:Decimal = to_decimal("0.0")
    tot_dgroom:int = 0
    tot_mgroom:int = 0
    tot_ygroom:int = 0
    tot_dpax:int = 0
    tot_mpax:int = 0
    tot_ypax:int = 0
    tot_drev:Decimal = to_decimal("0.0")
    tot_mrev:Decimal = to_decimal("0.0")
    tot_yrev:Decimal = to_decimal("0.0")
    tot_d_fbrev:Decimal = to_decimal("0.0")
    tot_m_fbrev:Decimal = to_decimal("0.0")
    tot_y_fbrev:Decimal = to_decimal("0.0")
    tot_dorev:Decimal = to_decimal("0.0")
    tot_morev:Decimal = to_decimal("0.0")
    tot_yorev:Decimal = to_decimal("0.0")
    bk_veran = bk_func = queasy = artikel = bk_rart = None

    bk_statistic_list = input_payload = None

    bk_statistic_list_list, Bk_statistic_list = create_model("Bk_statistic_list", {"code":int, "bezeich":string, "dgroom":int, "proz1":Decimal, "mgroom":int, "proz2":Decimal, "ygroom":int, "proz3":Decimal, "dpax":int, "mpax":int, "ypax":int, "drev":Decimal, "mrev":Decimal, "yrev":Decimal, "d_fbrev":Decimal, "m_fbrev":Decimal, "y_fbrev":Decimal, "dorev":Decimal, "morev":Decimal, "yorev":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_statistic_list_list, from_date, fb_rev, other_rev, tot_dgroom, tot_mgroom, tot_ygroom, tot_dpax, tot_mpax, tot_ypax, tot_drev, tot_mrev, tot_yrev, tot_d_fbrev, tot_m_fbrev, tot_y_fbrev, tot_dorev, tot_morev, tot_yorev, bk_veran, bk_func, queasy, artikel, bk_rart


        nonlocal bk_statistic_list, input_payload
        nonlocal bk_statistic_list_list

        return {"bk-statistic-list": bk_statistic_list_list}

    def create_list():

        nonlocal bk_statistic_list_list, from_date, fb_rev, other_rev, tot_dgroom, tot_mgroom, tot_ygroom, tot_dpax, tot_mpax, tot_ypax, tot_drev, tot_mrev, tot_yrev, tot_d_fbrev, tot_m_fbrev, tot_y_fbrev, tot_dorev, tot_morev, tot_yorev, bk_veran, bk_func, queasy, artikel, bk_rart


        nonlocal bk_statistic_list, input_payload
        nonlocal bk_statistic_list_list


        bk_statistic_list_list.clear()
        from_date = date_mdy(1, 1, get_year(date_mdy(input_payload.to_date)))

        bk_func_obj_list = {}
        bk_func = Bk_func()
        bk_veran = Bk_veran()
        for bk_func.veran_nr, bk_func.veran_seite, bk_func.rpersonen, bk_func.rpreis, bk_func.technik, bk_func.datum, bk_func._recid, bk_veran.segmentcode, bk_veran._recid in db_session.query(Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.rpersonen, Bk_func.rpreis, Bk_func.technik, Bk_func.datum, Bk_func._recid, Bk_veran.segmentcode, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                 (Bk_func.datum >= from_date) & (Bk_func.datum <= date_mdy(input_payload.to_date))).order_by(Bk_veran.segmentcode).all():
            if bk_func_obj_list.get(bk_func._recid):
                continue
            else:
                bk_func_obj_list[bk_func._recid] = True

            bk_statistic_list = query(bk_statistic_list_list, filters=(lambda bk_statistic_list: bk_statistic_list.code == bk_veran.segmentcode), first=True)

            if not bk_statistic_list:
                bk_statistic_list = Bk_statistic_list()
                bk_statistic_list_list.append(bk_statistic_list)

                bk_statistic_list.code = bk_veran.segmentcode

                queasy = get_cache (Queasy, {"key": [(eq, 146)],"char1": [(eq, to_string(bk_veran.segmentcode))]})

                if queasy:
                    bk_statistic_list.bezeich = queasy.char3


                else:
                    bk_statistic_list.bezeich = "Unknown"


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
                bk_statistic_list.dgroom = bk_statistic_list.dgroom + 1
                bk_statistic_list.dpax = bk_statistic_list.dpax + bk_func.rpersonen[0]
                bk_statistic_list.drev =  to_decimal(bk_statistic_list.drev) + to_decimal(bk_func.rpreis[0])
                bk_statistic_list.d_fbrev =  to_decimal(bk_statistic_list.d_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                bk_statistic_list.dorev =  to_decimal(bk_statistic_list.dorev) + to_decimal(other_rev)
                tot_dgroom = tot_dgroom + 1
                tot_dpax = tot_dpax + bk_func.rpersonen[0]
                tot_drev =  to_decimal(tot_drev) + to_decimal(bk_func.rpreis[0])
                tot_d_fbrev =  to_decimal(tot_d_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                tot_dorev =  to_decimal(tot_dorev) + to_decimal(other_rev)

            elif get_month(bk_func.datum) == get_month(date_mdy(input_payload.to_date)):
                bk_statistic_list.mgroom = bk_statistic_list.mgroom + 1
                bk_statistic_list.mpax = bk_statistic_list.mpax + bk_func.rpersonen[0]
                bk_statistic_list.mrev =  to_decimal(bk_statistic_list.mrev) + to_decimal(bk_func.rpreis[0])
                bk_statistic_list.m_fbrev =  to_decimal(bk_statistic_list.m_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                bk_statistic_list.morev =  to_decimal(bk_statistic_list.morev) + to_decimal(other_rev)
                tot_mgroom = tot_mgroom + 1
                tot_mpax = tot_mpax + bk_func.rpersonen[0]
                tot_mrev =  to_decimal(tot_mrev) + to_decimal(bk_func.rpreis[0])
                tot_m_fbrev =  to_decimal(tot_m_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                tot_morev =  to_decimal(tot_morev) + to_decimal(other_rev)


            bk_statistic_list.ygroom = bk_statistic_list.ygroom + 1
            bk_statistic_list.ypax = bk_statistic_list.ypax + bk_func.rpersonen[0]
            bk_statistic_list.yrev =  to_decimal(bk_statistic_list.yrev) + to_decimal(bk_func.rpreis[0])
            bk_statistic_list.y_fbrev =  to_decimal(bk_statistic_list.y_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
            bk_statistic_list.yorev =  to_decimal(bk_statistic_list.yorev) + to_decimal(other_rev)
            tot_ygroom = tot_ygroom + 1
            tot_ypax = tot_ypax + bk_func.rpersonen[0]
            tot_yrev =  to_decimal(tot_yrev) + to_decimal(bk_func.rpreis[0])
            tot_y_fbrev =  to_decimal(tot_y_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
            tot_yorev =  to_decimal(tot_yorev) + to_decimal(other_rev)

        for bk_statistic_list in query(bk_statistic_list_list):
            bk_statistic_list.proz1 =  to_decimal(100.0) * to_decimal((bk_statistic_list.dgroom) / to_decimal(tot_dgroom) )
            bk_statistic_list.proz2 =  to_decimal(100.0) * to_decimal((bk_statistic_list.mgroom) / to_decimal(tot_mgroom) )
            bk_statistic_list.proz3 =  to_decimal(100.0) * to_decimal((bk_statistic_list.ygroom) / to_decimal(tot_ygroom) )


        bk_statistic_list = Bk_statistic_list()
        bk_statistic_list_list.append(bk_statistic_list)

        bk_statistic_list.bezeich = "T O T A L"
        bk_statistic_list.dgroom = tot_dgroom
        bk_statistic_list.proz1 =  to_decimal(100.00)
        bk_statistic_list.mgroom = tot_mgroom
        bk_statistic_list.proz2 =  to_decimal(100.00)
        bk_statistic_list.ygroom = tot_ygroom
        bk_statistic_list.proz3 =  to_decimal(100.00)
        bk_statistic_list.dpax = tot_dpax
        bk_statistic_list.mpax = tot_mpax
        bk_statistic_list.ypax = tot_ypax
        bk_statistic_list.drev =  to_decimal(tot_drev)
        bk_statistic_list.mrev =  to_decimal(tot_mrev)
        bk_statistic_list.yrev =  to_decimal(tot_yrev)
        bk_statistic_list.d_fbrev =  to_decimal(tot_d_fbrev)
        bk_statistic_list.m_fbrev =  to_decimal(tot_m_fbrev)
        bk_statistic_list.y_fbrev =  to_decimal(tot_y_fbrev)
        bk_statistic_list.dorev =  to_decimal(tot_dorev)
        bk_statistic_list.morev =  to_decimal(tot_morev)
        bk_statistic_list.yorev =  to_decimal(tot_yorev)

        if tot_dgroom == 0:
            bk_statistic_list.proz1 =  to_decimal("0")

        if tot_mgroom == 0:
            bk_statistic_list.proz2 =  to_decimal("0")

        if tot_ygroom == 0:
            bk_statistic_list.proz3 =  to_decimal("0")


    def create_list1():

        nonlocal bk_statistic_list_list, from_date, fb_rev, other_rev, tot_dgroom, tot_mgroom, tot_ygroom, tot_dpax, tot_mpax, tot_ypax, tot_drev, tot_mrev, tot_yrev, tot_d_fbrev, tot_m_fbrev, tot_y_fbrev, tot_dorev, tot_morev, tot_yorev, bk_veran, bk_func, queasy, artikel, bk_rart


        nonlocal bk_statistic_list, input_payload
        nonlocal bk_statistic_list_list


        bk_statistic_list_list.clear()
        from_date = date_mdy(1, 1, get_year(date_mdy(input_payload.to_date)))

        for bk_func in db_session.query(Bk_func).filter(
                 (Bk_func.datum >= from_date) & (Bk_func.datum <= date_mdy(input_payload.to_date))).order_by(Bk_func.technik[inc_value(1)]).all():

            bk_statistic_list = query(bk_statistic_list_list, filters=(lambda bk_statistic_list: bk_statistic_list.code == to_int(bk_func.technik[1])), first=True)

            if not bk_statistic_list:
                bk_statistic_list = Bk_statistic_list()
                bk_statistic_list_list.append(bk_statistic_list)

                bk_statistic_list.code = to_int(bk_func.technik[1])

                queasy = get_cache (Queasy, {"key": [(eq, 151)],"char1": [(eq, to_string(bk_func.technik[1]))]})

                if queasy:
                    bk_statistic_list.bezeich = queasy.char3


                else:
                    bk_statistic_list.bezeich = "Unknown"


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
                bk_statistic_list.dgroom = bk_statistic_list.dgroom + 1
                bk_statistic_list.dpax = bk_statistic_list.dpax + bk_func.rpersonen[0]
                bk_statistic_list.drev =  to_decimal(bk_statistic_list.drev) + to_decimal(bk_func.rpreis[0])
                bk_statistic_list.d_fbrev =  to_decimal(bk_statistic_list.d_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                bk_statistic_list.dorev =  to_decimal(bk_statistic_list.dorev) + to_decimal(other_rev)
                tot_dgroom = tot_dgroom + 1
                tot_dpax = tot_dpax + bk_func.rpersonen[0]
                tot_drev =  to_decimal(tot_drev) + to_decimal(bk_func.rpreis[0])
                tot_d_fbrev =  to_decimal(tot_d_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                tot_dorev =  to_decimal(tot_dorev) + to_decimal(other_rev)

            elif get_month(bk_func.datum) == get_month(date_mdy(input_payload.to_date)):
                bk_statistic_list.mgroom = bk_statistic_list.mgroom + 1
                bk_statistic_list.mpax = bk_statistic_list.mpax + bk_func.rpersonen[0]
                bk_statistic_list.mrev =  to_decimal(bk_statistic_list.mrev) + to_decimal(bk_func.rpreis[0])
                bk_statistic_list.m_fbrev =  to_decimal(bk_statistic_list.m_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                bk_statistic_list.morev =  to_decimal(bk_statistic_list.morev) + to_decimal(other_rev)
                tot_mgroom = tot_mgroom + 1
                tot_mpax = tot_mpax + bk_func.rpersonen[0]
                tot_mrev =  to_decimal(tot_mrev) + to_decimal(bk_func.rpreis[0])
                tot_m_fbrev =  to_decimal(tot_m_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
                tot_morev =  to_decimal(tot_morev) + to_decimal(other_rev)


            bk_statistic_list.ygroom = bk_statistic_list.ygroom + 1
            bk_statistic_list.ypax = bk_statistic_list.ypax + bk_func.rpersonen[0]
            bk_statistic_list.yrev =  to_decimal(bk_statistic_list.yrev) + to_decimal(bk_func.rpreis[0])
            bk_statistic_list.y_fbrev =  to_decimal(bk_statistic_list.y_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
            bk_statistic_list.yorev =  to_decimal(bk_statistic_list.yorev) + to_decimal(other_rev)
            tot_ygroom = tot_ygroom + 1
            tot_ypax = tot_ypax + bk_func.rpersonen[0]
            tot_yrev =  to_decimal(tot_yrev) + to_decimal(bk_func.rpreis[0])
            tot_y_fbrev =  to_decimal(tot_y_fbrev) + to_decimal(((bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev) )
            tot_yorev =  to_decimal(tot_yorev) + to_decimal(other_rev)

        for bk_statistic_list in query(bk_statistic_list_list):
            bk_statistic_list.proz1 =  to_decimal(100.0) * to_decimal((bk_statistic_list.dgroom) / to_decimal(tot_dgroom) )
            bk_statistic_list.proz2 =  to_decimal(100.0) * to_decimal((bk_statistic_list.mgroom) / to_decimal(tot_mgroom) )
            bk_statistic_list.proz3 =  to_decimal(100.0) * to_decimal((bk_statistic_list.ygroom) / to_decimal(tot_ygroom) )


        bk_statistic_list = Bk_statistic_list()
        bk_statistic_list_list.append(bk_statistic_list)

        bk_statistic_list.bezeich = "T O T A L"
        bk_statistic_list.dgroom = tot_dgroom
        bk_statistic_list.proz1 =  to_decimal(100.00)
        bk_statistic_list.mgroom = tot_mgroom
        bk_statistic_list.proz2 =  to_decimal(100.00)
        bk_statistic_list.ygroom = tot_ygroom
        bk_statistic_list.proz3 =  to_decimal(100.00)
        bk_statistic_list.dpax = tot_dpax
        bk_statistic_list.mpax = tot_mpax
        bk_statistic_list.ypax = tot_ypax
        bk_statistic_list.drev =  to_decimal(tot_drev)
        bk_statistic_list.mrev =  to_decimal(tot_mrev)
        bk_statistic_list.yrev =  to_decimal(tot_yrev)
        bk_statistic_list.d_fbrev =  to_decimal(tot_d_fbrev)
        bk_statistic_list.m_fbrev =  to_decimal(tot_m_fbrev)
        bk_statistic_list.y_fbrev =  to_decimal(tot_y_fbrev)
        bk_statistic_list.dorev =  to_decimal(tot_dorev)
        bk_statistic_list.morev =  to_decimal(tot_morev)
        bk_statistic_list.yorev =  to_decimal(tot_yorev)

        if tot_dgroom == 0:
            bk_statistic_list.proz1 =  to_decimal("0")

        if tot_mgroom == 0:
            bk_statistic_list.proz2 =  to_decimal("0")

        if tot_ygroom == 0:
            bk_statistic_list.proz3 =  to_decimal("0")

    input_payload = query(input_payload_list, first=True)

    if input_payload.disp_flag == 0:
        create_list()
    else:
        create_list1()

    return generate_output()