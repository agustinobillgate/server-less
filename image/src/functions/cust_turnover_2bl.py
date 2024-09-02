from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servvat import calc_servvat
from functions.get_room_breakdown import get_room_breakdown
from models import Waehrung, Genstat, Guest, Htparam, Nation, Queasy, Artikel, exrate, Bill, Bill_line, Guest_queasy, H_artikel, H_bill_line, Res_line, Reservation, Sourccod, Segment, Arrangement, Zimmer

def cust_turnover_2bl(cardtype:int, sort_type:int, curr_sort1:int, fdate:date, tdate:date, check_ftd:bool, currency:str, excl_other:bool, curr_sort2:int):
    cust_list_list = []
    bfast_art:int = 0
    lunch_art:int = 0
    dinner_art:int = 0
    lundin_art:int = 0
    service:decimal = 0
    vat:decimal = 0
    datum:date = None
    end_date:date = None
    net_lodg:decimal = 0
    fnet_lodg:decimal = 0
    tot_breakfast:decimal = 0
    tot_lunch:decimal = 0
    tot_dinner:decimal = 0
    tot_other:decimal = 0
    tot_rmrev:decimal = 0
    tot_vat:decimal = 0
    tot_service:decimal = 0
    curr_i:int = 0
    i:int = 0
    found:bool = False
    ly_fdate:date = None
    ly_tdate:date = None
    ci_date:date = None
    pos:int = 0
    curr_gastnr:int = 0
    curr_resnr:int = 0
    curr_reslinnr:int = 0
    t_logiernachte:decimal = 0
    t_argtumsatz:decimal = 0
    t_fb_umsatz:decimal = 0
    t_sonst_umsatz:decimal = 0
    t_ba_umsatz:decimal = 0
    t_gesamtumsatz:decimal = 0
    tot_logiernachte:decimal = 0
    tot_argtumsatz:decimal = 0
    tot_fb_umsatz:decimal = 0
    tot_sonst_umsatz:decimal = 0
    tot_ba_umsatz:decimal = 0
    tot_gesamtumsatz:decimal = 0
    tot_stayno:decimal = 0
    loopj:int = 0
    found_it:bool = False
    exratenr:int = 0
    exrate:decimal = 0
    curr_resnr2:int = 0
    curr_reslinnr2:int = 0
    curr_resnr1:int = 0
    curr_reslinnr1:int = 0
    waehrung = genstat = guest = htparam = nation = queasy = artikel = exrate = bill = bill_line = guest_queasy = h_artikel = h_bill_line = res_line = reservation = sourccod = segment = arrangement = zimmer = None

    cust_list = cust_list_detail = cust_list2 = t_waehrung = t_genstat = blist = glist = clist = None

    cust_list_list, Cust_list = create_model("Cust_list", {"gastnr":int, "cust_name":str, "gesamtumsatz":decimal, "logiernachte":int, "argtumsatz":decimal, "f_b_umsatz":decimal, "sonst_umsatz":decimal, "wohnort":str, "plz":str, "land":str, "sales_id":str, "ba_umsatz":decimal, "ly_rev":decimal, "region":str, "region1":str, "stayno":int, "resnr":str, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int})
    cust_list_detail_list, Cust_list_detail = create_model("Cust_list_detail", {"gastnr":int, "cust_name":str, "gesamtumsatz":str, "logiernachte":str, "argtumsatz":str, "f_b_umsatz":str, "sonst_umsatz":str, "wohnort":str, "plz":str, "land":str, "sales_id":str, "ba_umsatz":str, "ly_rev":str, "region":str, "region1":str, "stayno":str, "resnr":str, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int})
    cust_list2_list, Cust_list2 = create_model_like(Cust_list)
    t_waehrung_list, T_waehrung = create_model_like(Waehrung)

    T_genstat = Genstat
    Blist = Cust_list_detail
    blist_list = cust_list_detail_list

    Glist = Guest
    Clist = Cust_list_detail
    clist_list = cust_list_detail_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cust_list_list, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_resnr, curr_reslinnr, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, loopj, found_it, exratenr, exrate, curr_resnr2, curr_reslinnr2, curr_resnr1, curr_reslinnr1, waehrung, genstat, guest, htparam, nation, queasy, artikel, exrate, bill, bill_line, guest_queasy, h_artikel, h_bill_line, res_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal t_genstat, blist, glist, clist


        nonlocal cust_list, cust_list_detail, cust_list2, t_waehrung, t_genstat, blist, glist, clist
        nonlocal cust_list_list, cust_list_detail_list, cust_list2_list, t_waehrung_list
        return {"cust-list": cust_list_list}

    def create_forecast():

        nonlocal cust_list_list, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_resnr, curr_reslinnr, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, loopj, found_it, exratenr, exrate, curr_resnr2, curr_reslinnr2, curr_resnr1, curr_reslinnr1, waehrung, genstat, guest, htparam, nation, queasy, artikel, exrate, bill, bill_line, guest_queasy, h_artikel, h_bill_line, res_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal t_genstat, blist, glist, clist


        nonlocal cust_list, cust_list_detail, cust_list2, t_waehrung, t_genstat, blist, glist, clist
        nonlocal cust_list_list, cust_list_detail_list, cust_list2_list, t_waehrung_list

        do_it:bool = True
        datum:date = None
        datum1:date = None
        datum2:date = None
        d2:date = None
        curr_resnr:int = 0
        curr_reslinnr:int = 0

        if fdate != ci_date and fdate < ci_date:
            fdate = ci_date
        datum1 = fdate

        if tdate < (ci_date - 1):
            d2 = tdate
        else:
            d2 = ci_date - 1
        d2 = d2 + 1

        res_line_obj_list = []
        for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnr) &  (Guest.karteityp == cardtype)).filter(
                ((Res_line.active_flag <= 1) &  (Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 12) &  (not (Res_line.ankunft > tdate)) &  (not (Res_line.abreise <= fdate))) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

            sourccod = db_session.query(Sourccod).filter(
                    (Sourccod.source_code == reservation.resart)).first()
            curr_i = 0
            do_it = True

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == reservation.segmentcode)).first()
            do_it = None != segment and segment.vip_level == 0

            if do_it and res_line.resstatus == 8:

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == res_line.arrangement)).first()

                bill_line = db_session.query(Bill_line).filter(
                        (Bill_line.departement == 0) &  (Bill_line.artnr == arrangement.argt_artikelnr) &  (Bill_line.bill_datum == ci_date) &  (Bill_line.massnr == res_line.resnr) &  (Bill_line.billin_nr == res_line.reslinnr)).first()
                do_it = None != bill_line

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == res_line.zinr)).first()

            if do_it and zimmer:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 14) &  (Queasy.char1 == res_line.zinr) &  (Queasy.date1 <= datum) &  (Queasy.date2 >= datum)).first()

                if zimmer.sleeping:

                    if queasy and queasy.number3 == res_line.gastnr:
                        do_it = False
                else:

                    if queasy and queasy.number3 != res_line.gastnr:
                        1
                    else:
                        do_it = False

            if do_it:

                cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == res_line.gastnr), first=True)

                if not cust_list:
                    cust_list = Cust_list()
                    cust_list_list.append(cust_list)

                    cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                            guest.anredefirm)
                    cust_list.gastnr = guest.gastnr
                    cust_list.wohnort = guest.wohnort
                    cust_list.plz = guest.plz
                    cust_list.land = guest.land
                    cust_list.sales_id = guest.phonetik3

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == guest.land)).first()

                    if nation:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                        if queasy:
                            cust_list.region = queasy.char1
                    else:
                        cust_list.region = "UNKNOWN"
                found = False

                if cust_list.resnr != "":
                    for i in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                        if entry(i - 1, cust_list.resnr, ";") != "":

                            if to_int(entry(i - 1, cust_list.resnr, ";")) == res_line.resnr:
                                found = True
                                break

                    if not found:
                        cust_list.resnr = cust_list.resnr + to_string(res_line.resnr) + ";"
                else:
                    cust_list.resnr = cust_list.resnr + to_string(res_line.resnr) + ";"

                if res_line.ankunft > fdate:
                    datum1 = res_line.ankunft
                else:
                    datum1 = fdate

                if res_line.abreise < tdate:
                    datum2 = res_line.abreise - 1
                else:
                    datum2 = tdate
                for datum in range(datum1,datum2 + 1) :
                    curr_i = curr_i + 1
                    net_lodg = 0
                    fnet_lodg = 0
                    tot_breakfast = 0
                    tot_lunch = 0
                    tot_dinner = 0
                    tot_other = 0
                    tot_rmrev = 0
                    tot_vat = 0
                    tot_service = 0


                    fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, ci_date))

                    if currency != " ":
                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((net_lodg + tot_breakfast +\
                                tot_lunch + tot_dinner + tot_other) / exrate)
                        cust_list.argtumsatz = cust_list.argtumsatz + (net_lodg / exrate)
                        cust_list.f_b_umsatz = cust_list.f_b_umsatz + ((tot_breakfast + tot_lunch + tot_dinner) / exrate)
                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + (tot_other / exrate)


                    else:
                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + net_lodg + tot_breakfast +\
                                tot_lunch + tot_dinner + tot_other
                        cust_list.argtumsatz = cust_list.argtumsatz + net_lodg
                        cust_list.f_b_umsatz = cust_list.f_b_umsatz + tot_breakfast + tot_lunch + tot_dinner
                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + tot_other

                    if excl_other == False:

                        if curr_resnr != res_line.resnr or curr_reslinnr != res_line.reslinnr:
                            curr_resnr = res_line.resnr
                            curr_reslinnr = res_line.reslinnr

                            for bill in db_session.query(Bill).filter(
                                    (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr)).all():

                                bill_line_obj_list = []
                                for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) &  (Artikel.departement == Bill_line.departement) &  (Artikel.artart == 0)).filter(
                                        (Bill_line.rechnr == bill.rechnr) &  (Bill_line.bill_datum == datum)).all():
                                    if bill_line._recid in bill_line_obj_list:
                                        continue
                                    else:
                                        bill_line_obj_list.append(bill_line._recid)


                                    service = 0
                                    vat = 0


                                    service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, genstat.datum, artikel.service_code, artikel.mwst_code))

                                    if currency != "":

                                        exrate = db_session.query(exrate).filter(
                                                (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                        if exrate:
                                            cust_list.sonst_umsatz = cust_list.sonst_umsatz + ((bill_line.betrag / (1 + service + vat)) / exrate.betrag)
                                            cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((bill_line.betrag / (1 + service + vat)) / exrate.betrag)


                                    else:
                                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + bill_line.betrag / (1 + service + vat)
                                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + bill_line.betrag / (1 + service + vat)

                    if ((res_line.ankunft < res_line.abreise) and res_line.abreise != datum) or (res_line.ankunft == res_line.abreise):

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and res_line.resstatus != 3 and not res_line.zimmerfix:
                            cust_list.logiernachte = cust_list.logiernachte + 1

        if excl_other == False:

            for guest_queasy in db_session.query(Guest_queasy).filter(
                    (func.lower(Guest_queasy.key) == "gast_info") &  (Guest_queasy.date1 >= fdate) &  (Guest_queasy.date1 <= tdate)).all():

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == guest_queasy.number2) &  (Res_line.reslinnr == guest_queasy.number3)).first()

                if res_line:

                    cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == res_line.gastnr), first=True)

                    if cust_list:
                        for loopj in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                            if entry(loopj - 1, cust_list.resnr, ";") == to_string(res_line.resnr):
                                found_it = True


                                break
                            else:
                                found_it = False

                        if found_it :

                            h_bill_line_obj_list = []
                            for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).filter(
                                    (H_bill_line.rechnr == to_int(guest_queasy.char1)) &  (H_bill_line.departement == guest_queasy.number1)).all():
                                if h_bill_line._recid in h_bill_line_obj_list:
                                    continue
                                else:
                                    h_bill_line_obj_list.append(h_bill_line._recid)


                                service = 0
                                vat = 0


                                service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, guest_queasy.date1, artikel.service_code, artikel.mwst_code))

                                if currency != " ":

                                    exrate = db_session.query(exrate).filter(
                                            (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                    if exrate:
                                        cust_list.f_b_umsatz = cust_list.f_b_umsatz + (((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service + vat)) / exrate.betrag)
                                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + ((guest_queasy.deci3 / (1 + service + vat)) / exrate.betrag)
                                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + (((guest_queasy.deci1 + guest_queasy.deci2 + guest_queasy.deci3) / (1 + service + vat)) / exrate.betrag)


                                else:
                                    cust_list.f_b_umsatz = cust_list.f_b_umsatz + ((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service + vat))
                                    cust_list.sonst_umsatz = cust_list.sonst_umsatz + (guest_queasy.deci3 / (1 + service + vat))
                                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((guest_queasy.deci1 + guest_queasy.deci2 + guest_queasy.deci3) / (1 + service + vat))

        if get_day(fdate) == 29 and get_month(fdate) == 2:
            ly_fdate = date_mdy(get_month(fdate) , 28, get_year(fdate) - 1)
        else:
            ly_fdate = date_mdy(get_month(fdate) , get_day(fdate) , get_year(fdate) - 1)

        if get_day(tdate) == 29 and get_month(tdate) == 2:
            ly_tdate = date_mdy(get_month(tdate) , 28, get_year(tdate) - 1)
        else:
            ly_tdate = date_mdy(get_month(tdate) , get_day(tdate) , get_year(tdate) - 1)

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr) &  (Guest.karteityp == cardtype)).filter(
                (Genstat.datum >= ly_fdate) &  (Genstat.datum <= ly_tdate) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == guest.gastnr), first=True)

            if cust_list:

                if currency != " ":

                    exrate = db_session.query(exrate).filter(
                            (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                    if exrate:
                        cust_list.ly_rev = cust_list.ly_rev + ((genstat.logis + genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]) / exrate.betrag)


                else:
                    cust_list.ly_rev = cust_list.ly_rev + genstat.logis + genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]

    def cr_ftd():

        nonlocal cust_list_list, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_resnr, curr_reslinnr, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, loopj, found_it, exratenr, exrate, curr_resnr2, curr_reslinnr2, curr_resnr1, curr_reslinnr1, waehrung, genstat, guest, htparam, nation, queasy, artikel, exrate, bill, bill_line, guest_queasy, h_artikel, h_bill_line, res_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal t_genstat, blist, glist, clist


        nonlocal cust_list, cust_list_detail, cust_list2, t_waehrung, t_genstat, blist, glist, clist
        nonlocal cust_list_list, cust_list_detail_list, cust_list2_list, t_waehrung_list

        t_argtumsatz:int = 0
        rate:decimal = 1
        frate:decimal = 1
        rmnite:int = 0
        curr_resnr:int = 0
        curr_reslinnr:int = 0
        cust_list2_list.clear()

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr) &  (Guest.karteityp == cardtype)).filter(
                (Genstat.datum >= fdate) &  (Genstat.datum <= tdate) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == guest.gastnr), first=True)

            if not cust_list:
                cust_list = Cust_list()
                cust_list_list.append(cust_list)

                cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)
                cust_list.gastnr = guest.gastnr
                cust_list.wohnort = guest.wohnort
                cust_list.plz = guest.plz
                cust_list.land = guest.land
                cust_list.sales_id = guest.phonetik3

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == guest.land)).first()

                if nation:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                    if queasy:
                        cust_list.region = queasy.char1
                else:
                    cust_list.region = "UNKNOWN"
            found = False

            if cust_list.resnr != "":
                for i in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                    if entry(i - 1, cust_list.resnr, ";") != "":

                        if to_int(entry(i - 1, cust_list.resnr, ";")) == genstat.resnr:
                            found = True
                            break

                if not found:
                    cust_list.resnr = cust_list.resnr + to_string(genstat.resnr) + ";"
            else:
                cust_list.resnr = cust_list.resnr + to_string(genstat.resnr) + ";"

            artikel = db_session.query(Artikel).filter(
                    (Artikel.zwkum == bfast_art)).first()

            if artikel:
                service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, genstat.datum, artikel.service_code, artikel.mwst_code))

            if currency != " ":

                exrate = db_session.query(exrate).filter(
                        (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                if exrate:
                    cust_list.f_b_umsatz = cust_list.f_b_umsatz + ((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) / exrate.betrag)
                    cust_list.sonst_umsatz = cust_list.sonst_umsatz + (genstat.res_deci[4] / exrate.betrag)
                    cust_list.argtumsatz = cust_list.argtumsatz + (genstat.logis / exrate.betrag)
                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((genstat.logis + genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]) / exrate.betrag)


            else:
                cust_list.f_b_umsatz = cust_list.f_b_umsatz + genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]
                cust_list.sonst_umsatz = cust_list.sonst_umsatz + genstat.res_deci[4]
                cust_list.argtumsatz = cust_list.argtumsatz + genstat.logis
                cust_list.gesamtumsatz = cust_list.gesamtumsatz + genstat.logis + genstat.res_deci[1] +\
                    genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]

            if genstat.resstatus != 13:
                cust_list.logiernachte = cust_list.logiernachte + 1

            if excl_other == False:

                if curr_resnr != genstat.resnr or curr_reslinnr != genstat.res_int[0]:
                    curr_resnr = genstat.resnr
                    curr_reslinnr = genstat.res_int[0]

                    for bill in db_session.query(Bill).filter(
                            (Bill.resnr == genstat.resnr) &  (Bill.reslinnr == genstat.res_int[0])).all():

                        bill_line_obj_list = []
                        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) &  (Artikel.departement == Bill_line.departement) &  (Artikel.artart == 0)).filter(
                                (Bill_line.rechnr == bill.rechnr) &  (Bill_line.bill_datum == genstat.datum)).all():
                            if bill_line._recid in bill_line_obj_list:
                                continue
                            else:
                                bill_line_obj_list.append(bill_line._recid)


                            service = 0
                            vat = 0


                            service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, genstat.datum, artikel.service_code, artikel.mwst_code))

                            if currency != "":

                                exrate = db_session.query(exrate).filter(
                                        (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                if exrate:
                                    cust_list.sonst_umsatz = cust_list.sonst_umsatz + ((bill_line.betrag / (1 + service + vat)) / exrate.betrag)
                                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((bill_line.betrag / (1 + service + vat)) / exrate.betrag)


                            else:
                                cust_list.sonst_umsatz = cust_list.sonst_umsatz + bill_line.betrag / (1 + service + vat)
                                cust_list.gesamtumsatz = cust_list.gesamtumsatz + bill_line.betrag / (1 + service + vat)

        if excl_other == False:

            for guest_queasy in db_session.query(Guest_queasy).filter(
                    (func.lower(Guest_queasy.key) == "gast_info") &  (Guest_queasy.date1 >= fdate) &  (Guest_queasy.date1 <= tdate)).all():

                genstat = db_session.query(Genstat).filter(
                        (Genstat.resnr == guest_queasy.number2) &  (Genstat.res_int[0] == guest_queasy.number3) &  (Genstat.datum == guest_queasy.date1) &  (Genstat.res_logic[1])).first()

                if genstat:

                    cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == genstat.gastnr), first=True)

                    if cust_list:
                        for loopj in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                            if entry(loopj - 1, cust_list.resnr, ";") == to_string(genstat.resnr):
                                found_it = True


                                break
                            else:
                                found_it = False

                        if found_it :

                            h_bill_line_obj_list = []
                            for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).filter(
                                    (H_bill_line.rechnr == to_int(guest_queasy.char1)) &  (H_bill_line.departement == guest_queasy.number1)).all():
                                if h_bill_line._recid in h_bill_line_obj_list:
                                    continue
                                else:
                                    h_bill_line_obj_list.append(h_bill_line._recid)


                                service = 0
                                vat = 0


                                service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, guest_queasy.date1, artikel.service_code, artikel.mwst_code))

                                if currency != " ":

                                    exrate = db_session.query(exrate).filter(
                                            (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                    if exrate:
                                        cust_list.f_b_umsatz = cust_list.f_b_umsatz + (((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service + vat)) / exrate.betrag)
                                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + ((guest_queasy.deci3 / (1 + service + vat)) / exrate.betrag)
                                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + (((guest_queasy.deci1 + guest_queasy.deci2 + guest_queasy.deci3) / (1 + service + vat)) / exrate.betrag)


                                else:
                                    cust_list.f_b_umsatz = cust_list.f_b_umsatz + ((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service + vat))
                                    cust_list.sonst_umsatz = cust_list.sonst_umsatz + (guest_queasy.deci3 / (1 + service + vat))
                                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((guest_queasy.deci1 + guest_queasy.deci2 + guest_queasy.deci3) / (1 + service + vat))

        for cust_list2 in query(cust_list2_list):
            cust_list = Cust_list()
            cust_list_list.append(cust_list)

            buffer_copy(cust_list2, cust_list)

        t_genstat_obj_list = []
        for t_genstat, guest in db_session.query(T_genstat, Guest).join(Guest,(Guest.gastnr == T_genstat.gastnr) &  (Guest.karteityp == cardtype)).filter(
                (T_genstat.datum >= fdate) &  (T_genstat.datum <= tdate) &  (T_genstat.res_deci[6] != 0)).all():
            if t_genstat._recid in t_genstat_obj_list:
                continue
            else:
                t_genstat_obj_list.append(t_genstat._recid)

            cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == t_genstat.gastnr), first=True)

            if cust_list:

                if currency != " ":

                    exrate = db_session.query(exrate).filter(
                            (exrate.datum == t_genstat.datum) &  (exrate.artnr == exratenr)).first()

                    if exrate:
                        cust_list.ba_umsatz = cust_list.ba_umsatz + (t_genstat.res_deci[6] / exrate.betrag)
                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + (t_genstat.res_deci[6] / exrate.betrag)


                else:
                    cust_list.ba_umsatz = cust_list.ba_umsatz + t_genstat.res_deci[6]
                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + t_genstat.res_deci[6]


            else:
                cust_list = Cust_list()
                cust_list_list.append(cust_list)

                cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)
                cust_list.gastnr = guest.gastnr
                cust_list.wohnort = guest.wohnort
                cust_list.plz = guest.plz
                cust_list.land = guest.land
                cust_list.sales_id = guest.phonetik3

                if currency != " ":

                    exrate = db_session.query(exrate).filter(
                            (exrate.datum == t_genstat.datum) &  (exrate.artnr == exratenr)).first()

                    if exrate:
                        cust_list.ba_umsatz = (t_genstat.res_deci[6] / exrate.betrag)
                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + (t_genstat.res_deci[6] / exrate.betrag)


                else:
                    cust_list.ba_umsatz = t_genstat.res_deci[6]
                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + t_genstat.res_deci[6]

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == guest.land)).first()

                if nation:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                    if queasy:
                        cust_list.region = queasy.char1
                else:
                    cust_list.region = "UNKNOWN"

    def create_forecast_all():

        nonlocal cust_list_list, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_resnr, curr_reslinnr, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, loopj, found_it, exratenr, exrate, curr_resnr2, curr_reslinnr2, curr_resnr1, curr_reslinnr1, waehrung, genstat, guest, htparam, nation, queasy, artikel, exrate, bill, bill_line, guest_queasy, h_artikel, h_bill_line, res_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal t_genstat, blist, glist, clist


        nonlocal cust_list, cust_list_detail, cust_list2, t_waehrung, t_genstat, blist, glist, clist
        nonlocal cust_list_list, cust_list_detail_list, cust_list2_list, t_waehrung_list

        do_it:bool = True
        datum:date = None
        datum1:date = None
        datum2:date = None
        d2:date = None
        curr_resnr:int = 0
        curr_reslinnr:int = 0

        if fdate != ci_date and fdate < ci_date:
            fdate = ci_date
        datum1 = fdate

        if tdate < (ci_date - 1):
            d2 = tdate
        else:
            d2 = ci_date - 1
        d2 = d2 + 1

        res_line_obj_list = []
        for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                ((Res_line.active_flag <= 1) &  (Res_line.resstatus <= 13) &  (Res_line.resstatus != 4) &  (Res_line.resstatus != 12) &  (not (Res_line.ankunft > tdate)) &  (not (Res_line.abreise <= fdate))) |  ((Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == ci_date)) &  (Res_line.gastnr > 0) &  (Res_line.l_zuordnung[2] == 0)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

            sourccod = db_session.query(Sourccod).filter(
                    (Sourccod.source_code == reservation.resart)).first()
            curr_i = 0
            do_it = True

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == reservation.segmentcode)).first()
            do_it = None != segment and segment.vip_level == 0

            if do_it and res_line.resstatus == 8:

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == res_line.arrangement)).first()

                bill_line = db_session.query(Bill_line).filter(
                        (Bill_line.departement == 0) &  (Bill_line.artnr == arrangement.argt_artikelnr) &  (Bill_line.bill_datum == ci_date) &  (Bill_line.massnr == res_line.resnr) &  (Bill_line.billin_nr == res_line.reslinnr)).first()
                do_it = None != bill_line

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == res_line.zinr)).first()

            if do_it and zimmer:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 14) &  (Queasy.char1 == res_line.zinr) &  (Queasy.date1 <= datum) &  (Queasy.date2 >= datum)).first()

                if zimmer.sleeping:

                    if queasy and queasy.number3 == res_line.gastnr:
                        do_it = False
                else:

                    if queasy and queasy.number3 != res_line.gastnr:
                        1
                    else:
                        do_it = False

            if do_it:

                cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == res_line.gastnr), first=True)

                if not cust_list:
                    cust_list = Cust_list()
                    cust_list_list.append(cust_list)

                    cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                            guest.anredefirm)
                    cust_list.gastnr = guest.gastnr
                    cust_list.wohnort = guest.wohnort
                    cust_list.plz = guest.plz
                    cust_list.land = guest.land
                    cust_list.sales_id = guest.phonetik3

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == guest.land)).first()

                    if nation:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                        if queasy:
                            cust_list.region = queasy.char1
                    else:
                        cust_list.region = "UNKNOWN"
                found = False

                if cust_list.resnr != "":
                    for i in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                        if entry(i - 1, cust_list.resnr, ";") != "":

                            if to_int(entry(i - 1, cust_list.resnr, ";")) == res_line.resnr:
                                found = True
                                break

                    if not found:
                        cust_list.resnr = cust_list.resnr + to_string(res_line.resnr) + ";"
                else:
                    cust_list.resnr = cust_list.resnr + to_string(res_line.resnr) + ";"

                if res_line.ankunft > fdate:
                    datum1 = res_line.ankunft
                else:
                    datum1 = fdate

                if res_line.abreise < tdate:
                    datum2 = res_line.abreise - 1
                else:
                    datum2 = tdate
                for datum in range(datum1,datum2 + 1) :
                    curr_i = curr_i + 1
                    net_lodg = 0
                    fnet_lodg = 0
                    tot_breakfast = 0
                    tot_lunch = 0
                    tot_dinner = 0
                    tot_other = 0
                    tot_rmrev = 0
                    tot_vat = 0
                    tot_service = 0


                    fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, ci_date))

                    if currency != " ":
                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((net_lodg + tot_breakfast +\
                                tot_lunch + tot_dinner + tot_other) / exrate)
                        cust_list.argtumsatz = cust_list.argtumsatz + (net_lodg / exrate)
                        cust_list.f_b_umsatz = cust_list.f_b_umsatz + (tot_breakfast + tot_lunch + tot_dinner / exrate)
                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + (tot_other / exrate)


                    else:
                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + net_lodg + tot_breakfast +\
                                tot_lunch + tot_dinner + tot_other
                        cust_list.argtumsatz = cust_list.argtumsatz + net_lodg
                        cust_list.f_b_umsatz = cust_list.f_b_umsatz + tot_breakfast + tot_lunch + tot_dinner
                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + tot_other

                    if excl_other == False:

                        if curr_resnr != res_line.resnr or curr_reslinnr != res_line.reslinnr:
                            curr_resnr = res_line.resnr
                            curr_reslinnr = res_line.reslinnr

                            for bill in db_session.query(Bill).filter(
                                    (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr)).all():

                                bill_line_obj_list = []
                                for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) &  (Artikel.departement == Bill_line.departement) &  (Artikel.artart == 0)).filter(
                                        (Bill_line.rechnr == bill.rechnr) &  (Bill_line.bill_datum == datum)).all():
                                    if bill_line._recid in bill_line_obj_list:
                                        continue
                                    else:
                                        bill_line_obj_list.append(bill_line._recid)


                                    service = 0
                                    vat = 0


                                    service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, genstat.datum, artikel.service_code, artikel.mwst_code))

                                    if currency != "":

                                        exrate = db_session.query(exrate).filter(
                                                (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                        if exrate:
                                            cust_list.sonst_umsatz = cust_list.sonst_umsatz + ((bill_line.betrag / (1 + service + vat)) / exrate.betrag)
                                            cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((bill_line.betrag / (1 + service + vat)) / exrate.betrag)


                                    else:
                                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + bill_line.betrag / (1 + service + vat)
                                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + bill_line.betrag / (1 + service + vat)

                    if ((res_line.ankunft < res_line.abreise) and res_line.abreise != datum) or (res_line.ankunft == res_line.abreise):

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and res_line.resstatus != 3 and not res_line.zimmerfix:
                            cust_list.logiernachte = cust_list.logiernachte + 1

        if excl_other == False:

            for guest_queasy in db_session.query(Guest_queasy).filter(
                    (func.lower(Guest_queasy.key) == "gast_info") &  (Guest_queasy.date1 >= fdate) &  (Guest_queasy.date1 <= tdate)).all():

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == guest_queasy.number2) &  (Res_line.reslinnr == guest_queasy.number3)).first()

                if res_line:

                    cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == res_line.gastnr), first=True)

                    if cust_list:
                        for loopj in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                            if entry(loopj - 1, cust_list.resnr, ";") == to_string(res_line.resnr):
                                found_it = True


                                break
                            else:
                                found_it = False

                        if found_it :

                            h_bill_line_obj_list = []
                            for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).filter(
                                    (H_bill_line.rechnr == to_int(guest_queasy.char1)) &  (H_bill_line.departement == guest_queasy.number1)).all():
                                if h_bill_line._recid in h_bill_line_obj_list:
                                    continue
                                else:
                                    h_bill_line_obj_list.append(h_bill_line._recid)


                                service = 0
                                vat = 0


                                service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, guest_queasy.date1, artikel.service_code, artikel.mwst_code))

                                if currency != " ":

                                    exrate = db_session.query(exrate).filter(
                                            (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                    if exrate:
                                        cust_list.f_b_umsatz = cust_list.f_b_umsatz + (((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service + vat)) / exrate.betrag)
                                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + ((guest_queasy.deci3 / (1 + service + vat)) / exrate.betrag)
                                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + (((guest_queasy.deci1 + guest_queasy.deci2 + guest_queasy.deci3) / (1 + service + vat)) / exrate.betrag)


                                else:
                                    cust_list.f_b_umsatz = cust_list.f_b_umsatz + ((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service + vat))
                                    cust_list.sonst_umsatz = cust_list.sonst_umsatz + (guest_queasy.deci3 / (1 + service + vat))
                                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((guest_queasy.deci1 + guest_queasy.deci2 + guest_queasy.deci3) / (1 + service + vat))

        if get_day(fdate) == 29 and get_month(fdate) == 2:
            ly_fdate = date_mdy(get_month(fdate) , 28, get_year(fdate) - 1)
        else:
            ly_fdate = date_mdy(get_month(fdate) , get_day(fdate) , get_year(fdate) - 1)

        if get_day(tdate) == 29 and get_month(tdate) == 2:
            ly_tdate = date_mdy(get_month(tdate) , 28, get_year(tdate) - 1)
        else:
            ly_tdate = date_mdy(get_month(tdate) , get_day(tdate) , get_year(tdate) - 1)

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                (Genstat.datum >= ly_fdate) &  (Genstat.datum <= ly_tdate) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == guest.gastnr), first=True)

            if cust_list:

                if currency != " ":

                    exrate = db_session.query(exrate).filter(
                            (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                    if exrate:
                        cust_list.ly_rev = cust_list.ly_rev + ((genstat.logis + genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]) / exrate.betrag)


                else:
                    cust_list.ly_rev = cust_list.ly_rev + genstat.logis + genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]

    def cr_ftd_all():

        nonlocal cust_list_list, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_resnr, curr_reslinnr, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, loopj, found_it, exratenr, exrate, curr_resnr2, curr_reslinnr2, curr_resnr1, curr_reslinnr1, waehrung, genstat, guest, htparam, nation, queasy, artikel, exrate, bill, bill_line, guest_queasy, h_artikel, h_bill_line, res_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal t_genstat, blist, glist, clist


        nonlocal cust_list, cust_list_detail, cust_list2, t_waehrung, t_genstat, blist, glist, clist
        nonlocal cust_list_list, cust_list_detail_list, cust_list2_list, t_waehrung_list

        t_argtumsatz:int = 0
        rate:decimal = 1
        frate:decimal = 1
        rmnite:int = 0
        curr_resnr:int = 0
        curr_reslinnr:int = 0
        cust_list2_list.clear()

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                (Genstat.datum >= fdate) &  (Genstat.datum <= tdate) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == guest.gastnr), first=True)

            if not cust_list:
                cust_list = Cust_list()
                cust_list_list.append(cust_list)

                cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)
                cust_list.gastnr = guest.gastnr
                cust_list.wohnort = guest.wohnort
                cust_list.plz = guest.plz
                cust_list.land = guest.land
                cust_list.sales_id = guest.phonetik3

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == guest.land)).first()

                if nation:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                    if queasy:
                        cust_list.region = queasy.char1
                else:
                    cust_list.region = "UNKNOWN"
            found = False

            if cust_list.resnr != "":
                for i in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                    if entry(i - 1, cust_list.resnr, ";") != "":

                        if to_int(entry(i - 1, cust_list.resnr, ";")) == genstat.resnr:
                            found = True
                            break

                if not found:
                    cust_list.resnr = cust_list.resnr + to_string(genstat.resnr) + ";"
            else:
                cust_list.resnr = cust_list.resnr + to_string(genstat.resnr) + ";"

            artikel = db_session.query(Artikel).filter(
                    (Artikel.zwkum == bfast_art)).first()

            if artikel:
                service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, genstat.datum, artikel.service_code, artikel.mwst_code))

            if currency != " ":

                exrate = db_session.query(exrate).filter(
                        (exrate.datum == t_genstat.datum) &  (exrate.artnr == exratenr)).first()

                if exrate:
                    cust_list.f_b_umsatz = cust_list.f_b_umsatz + ((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) / exrate.betrag)
                    cust_list.sonst_umsatz = cust_list.sonst_umsatz + (genstat.res_deci[4] / exrate.betrag)
                    cust_list.argtumsatz = cust_list.argtumsatz + (genstat.logis / exrate.betrag)
                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((genstat.logis + genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]) / exrate.betrag)


            else:
                cust_list.f_b_umsatz = cust_list.f_b_umsatz + genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]
                cust_list.sonst_umsatz = cust_list.sonst_umsatz + genstat.res_deci[4]
                cust_list.argtumsatz = cust_list.argtumsatz + genstat.logis
                cust_list.gesamtumsatz = cust_list.gesamtumsatz + genstat.logis + genstat.res_deci[1] +\
                    genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]

            if genstat.resstatus != 13:
                cust_list.logiernachte = cust_list.logiernachte + 1

            if excl_other == False:

                if curr_resnr != genstat.resnr or curr_reslinnr != genstat.res_int[0]:
                    curr_resnr = genstat.resnr
                    curr_reslinnr = genstat.res_int[0]

                    for bill in db_session.query(Bill).filter(
                            (Bill.resnr == genstat.resnr) &  (Bill.reslinnr == genstat.res_int[0])).all():

                        bill_line_obj_list = []
                        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) &  (Artikel.departement == Bill_line.departement) &  (Artikel.artart == 0)).filter(
                                (Bill_line.rechnr == bill.rechnr) &  (Bill_line.bill_datum == genstat.datum)).all():
                            if bill_line._recid in bill_line_obj_list:
                                continue
                            else:
                                bill_line_obj_list.append(bill_line._recid)


                            service = 0
                            vat = 0


                            service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, genstat.datum, artikel.service_code, artikel.mwst_code))

                            if currency != "":

                                exrate = db_session.query(exrate).filter(
                                        (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                if exrate:
                                    cust_list.sonst_umsatz = cust_list.sonst_umsatz + ((bill_line.betrag / (1 + service + vat)) / exrate.betrag)
                                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((bill_line.betrag / (1 + service + vat)) / exrate.betrag)


                            else:
                                cust_list.sonst_umsatz = cust_list.sonst_umsatz + bill_line.betrag / (1 + service + vat)
                                cust_list.gesamtumsatz = cust_list.gesamtumsatz + bill_line.betrag / (1 + service + vat)

        if excl_other == False:

            for guest_queasy in db_session.query(Guest_queasy).filter(
                    (func.lower(Guest_queasy.key) == "gast_info") &  (Guest_queasy.date1 >= fdate) &  (Guest_queasy.date1 <= tdate)).all():

                genstat = db_session.query(Genstat).filter(
                        (Genstat.resnr == guest_queasy.number2) &  (Genstat.res_int[0] == guest_queasy.number3) &  (Genstat.datum == guest_queasy.date1) &  (Genstat.res_logic[1])).first()

                if genstat:

                    cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == genstat.gastnr), first=True)

                    if cust_list:
                        for loopj in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                            if entry(loopj - 1, cust_list.resnr, ";") == to_string(genstat.resnr):
                                found_it = True


                                break
                            else:
                                found_it = False

                        if found_it :

                            h_bill_line_obj_list = []
                            for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).filter(
                                    (H_bill_line.rechnr == to_int(guest_queasy.char1)) &  (H_bill_line.departement == guest_queasy.number1)).all():
                                if h_bill_line._recid in h_bill_line_obj_list:
                                    continue
                                else:
                                    h_bill_line_obj_list.append(h_bill_line._recid)


                                service = 0
                                vat = 0


                                service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, guest_queasy.date1, artikel.service_code, artikel.mwst_code))

                                if currency != " ":

                                    exrate = db_session.query(exrate).filter(
                                            (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                    if exrate:
                                        cust_list.f_b_umsatz = cust_list.f_b_umsatz + (((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service + vat)) / exrate.betrag)
                                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + ((guest_queasy.deci3 / (1 + service + vat)) / exrate.betrag)
                                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + (((guest_queasy.deci1 + guest_queasy.deci2 + guest_queasy.deci3) / (1 + service + vat)) / exrate.betrag)


                                else:
                                    cust_list.f_b_umsatz = cust_list.f_b_umsatz + ((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service + vat))
                                    cust_list.sonst_umsatz = cust_list.sonst_umsatz + (guest_queasy.deci3 / (1 + service + vat))
                                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((guest_queasy.deci1 + guest_queasy.deci2 + guest_queasy.deci3) / (1 + service + vat))

        for cust_list2 in query(cust_list2_list):
            cust_list = Cust_list()
            cust_list_list.append(cust_list)

            buffer_copy(cust_list2, cust_list)

        t_genstat_obj_list = []
        for t_genstat, guest in db_session.query(T_genstat, Guest).join(Guest,(Guest.gastnr == T_genstat.gastnr)).filter(
                (T_genstat.datum >= fdate) &  (T_genstat.datum <= tdate) &  (T_genstat.res_deci[6] != 0)).all():
            if t_genstat._recid in t_genstat_obj_list:
                continue
            else:
                t_genstat_obj_list.append(t_genstat._recid)

            cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == t_genstat.gastnr), first=True)

            if cust_list:

                if currency != " ":

                    exrate = db_session.query(exrate).filter(
                            (exrate.datum == t_genstat.datum) &  (exrate.artnr == exratenr)).first()

                    if exrate:
                        cust_list.ba_umsatz = cust_list.ba_umsatz + (t_genstat.res_deci[6] / exrate.betrag)
                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + (t_genstat.res_deci[6] / exrate.betrag)


                else:
                    cust_list.ba_umsatz = cust_list.ba_umsatz + t_genstat.res_deci[6]
                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + t_genstat.res_deci[6]


            else:
                cust_list = Cust_list()
                cust_list_list.append(cust_list)

                cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)
                cust_list.gastnr = guest.gastnr
                cust_list.wohnort = guest.wohnort
                cust_list.plz = guest.plz
                cust_list.land = guest.land
                cust_list.sales_id = guest.phonetik3

                if currency != " ":

                    exrate = db_session.query(exrate).filter(
                            (exrate.datum == t_genstat.datum) &  (exrate.artnr == exratenr)).first()

                    if exrate:
                        cust_list.ba_umsatz = (t_genstat.res_deci[6] / exrate.betrag)
                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + (t_genstat.res_deci[6] / exrate.betrag)


                else:
                    cust_list.ba_umsatz = t_genstat.res_deci[6]
                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + t_genstat.res_deci[6]

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == guest.land)).first()

                if nation:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                    if queasy:
                        cust_list.region = queasy.char1
                else:
                    cust_list.region = "UNKNOWN"


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 125)).first()
    bfast_art = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    if currency != "":

        waehrung = db_session.query(Waehrung).filter(
                (func.lower(Waehrung.wabkurz) == (currency).lower())).first()

        if waehrung:
            exratenr = waehrungsnr
            exrate = waehrung.ankauf


    cust_list_list.clear()

    if cardtype == 3:

        if not check_ftd:

            genstat_obj_list = []
            for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                    (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)

                cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == guest.gastnr), first=True)

                if not cust_list:
                    cust_list = Cust_list()
                    cust_list_list.append(cust_list)

                    cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                            guest.anredefirm)
                    cust_list.gastnr = guest.gastnr
                    cust_list.wohnort = guest.wohnort
                    cust_list.plz = guest.plz
                    cust_list.land = guest.land
                    cust_list.sales_id = guest.phonetik3

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == guest.land)).first()

                    if nation:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                        if queasy:
                            cust_list.region = queasy.char1
                    else:
                        cust_list.region = "UNKOWN"

                artikel = db_session.query(Artikel).filter(
                        (Artikel.zwkum == bfast_art)).first()

                if artikel:
                    service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, genstat.datum, artikel.service_code, artikel.mwst_code))

                if currency != " ":

                    exrate = db_session.query(exrate).filter(
                            (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                    if exrate:
                        cust_list.f_b_umsatz = cust_list.f_b_umsatz + ((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) / exrate.betrag)
                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + (genstat.res_deci[4] / exrate.betrag)
                        cust_list.argtumsatz = cust_list.argtumsatz + (genstat.logis / exrate.betrag)
                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((genstat.logis + genstat.res_deci[1] +\
                                genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]) / exrate.betrag)
                        cust_list.logiernachte = cust_list.logiernachte + 1


                else:
                    cust_list.f_b_umsatz = cust_list.f_b_umsatz + genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]
                    cust_list.sonst_umsatz = cust_list.sonst_umsatz + genstat.res_deci[4]
                    cust_list.argtumsatz = cust_list.argtumsatz + genstat.logis
                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + genstat.logis + genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]
                    cust_list.logiernachte = cust_list.logiernachte + 1

                if excl_other == False:

                    if curr_resnr2 != genstat.resnr or curr_reslinnr2 != genstat.res_int[0]:
                        curr_resnr2 = genstat.resnr
                        curr_reslinnr2 = genstat.res_int[0]

                        for bill in db_session.query(Bill).filter(
                                (Bill.resnr == genstat.resnr) &  (Bill.reslinnr == genstat.res_int[0])).all():

                            bill_line_obj_list = []
                            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) &  (Artikel.departement == Bill_line.departement) &  (Artikel.artart == 0)).filter(
                                    (Bill_line.rechnr == bill.rechnr) &  (Bill_line.bill_datum == genstat.datum)).all():
                                if bill_line._recid in bill_line_obj_list:
                                    continue
                                else:
                                    bill_line_obj_list.append(bill_line._recid)


                                service = 0
                                vat = 0


                                service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, genstat.datum, artikel.service_code, artikel.mwst_code))

                                if currency != "":

                                    exrate = db_session.query(exrate).filter(
                                            (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                    if exrate:
                                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + ((bill_line.betrag / (1 + service + vat)) / exrate.betrag)
                                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((bill_line.betrag / (1 + service + vat)) / exrate.betrag)


                                else:
                                    cust_list.sonst_umsatz = cust_list.sonst_umsatz + bill_line.betrag / (1 + service + vat)
                                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + bill_line.betrag / (1 + service + vat)

            if excl_other == False:

                for guest_queasy in db_session.query(Guest_queasy).filter(
                        (func.lower(Guest_queasy.key) == "gast_info") &  (Guest_queasy.date1 >= fdate) &  (Guest_queasy.date1 <= tdate)).all():

                    genstat = db_session.query(Genstat).filter(
                            (Genstat.resnr == guest_queasy.number2) &  (Genstat.res_int[0] == guest_queasy.number3) &  (Genstat.datum == guest_queasy.date1) &  (Genstat.res_logic[1])).first()

                    if genstat:

                        cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == genstat.gastnr), first=True)

                        if cust_list:
                            for loopj in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                                if entry(loopj - 1, cust_list.resnr, ";") == to_string(genstat.resnr):
                                    found_it = True


                                    break
                                else:
                                    found_it = False

                            if found_it :

                                h_bill_line_obj_list = []
                                for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).filter(
                                        (H_bill_line.rechnr == to_int(guest_queasy.char1)) &  (H_bill_line.departement == guest_queasy.number1)).all():
                                    if h_bill_line._recid in h_bill_line_obj_list:
                                        continue
                                    else:
                                        h_bill_line_obj_list.append(h_bill_line._recid)


                                    service = 0
                                    vat = 0


                                    service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, guest_queasy.date1, artikel.service_code, artikel.mwst_code))

                                    if currency != " ":

                                        exrate = db_session.query(exrate).filter(
                                                (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                        if exrate:
                                            cust_list.f_b_umsatz = cust_list.f_b_umsatz + (((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service + vat)) / exrate.betrag)
                                            cust_list.sonst_umsatz = cust_list.sonst_umsatz + ((guest_queasy.deci3 / (1 + service + vat)) / exrate.betrag)
                                            cust_list.gesamtumsatz = cust_list.gesamtumsatz + (((guest_queasy.deci1 + guest_queasy.deci2 + guest_queasy.deci3) / (1 + service + vat)) / exrate.betrag)


                                    else:
                                        cust_list.f_b_umsatz = cust_list.f_b_umsatz + ((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service + vat))
                                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + (guest_queasy.deci3 / (1 + service + vat))
                                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((guest_queasy.deci1 + guest_queasy.deci2 + guest_queasy.deci3) / (1 + service + vat))

            t_genstat_obj_list = []
            for t_genstat, guest in db_session.query(T_genstat, Guest).join(Guest,(Guest.gastnr == T_genstat.gastnr)).filter(
                    (T_genstat.datum >= fdate) &  (T_genstat.datum <= tdate) &  (T_genstat.res_deci[6] != 0)).all():
                if t_genstat._recid in t_genstat_obj_list:
                    continue
                else:
                    t_genstat_obj_list.append(t_genstat._recid)

                cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == t_genstat.gastnr), first=True)

                if cust_list:

                    if currency != "":

                        exrate = db_session.query(exrate).filter(
                                (exrate.datum == t_genstat.datum) &  (exrate.artnr == exratenr)).first()

                        if exrate:
                            cust_list.ba_umsatz = t_genstat.res_deci[6] / exrate.betrag
                            cust_list.gesamtumsatz = cust_list.gesamtumsatz + (t_genstat.res_deci[6] / exrate.betrag)


                    else:
                        cust_list.ba_umsatz = cust_list.ba_umsatz + t_genstat.res_deci[6]
                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + t_genstat.res_deci[6]


                else:
                    cust_list = Cust_list()
                    cust_list_list.append(cust_list)

                    cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                            guest.anredefirm)
                    cust_list.gastnr = guest.gastnr
                    cust_list.wohnort = guest.wohnort
                    cust_list.plz = guest.plz
                    cust_list.land = guest.land
                    cust_list.sales_id = guest.phonetik3

                    if currency != " ":

                        exrate = db_session.query(exrate).filter(
                                (exrate.datum == t_genstat.datum) &  (exrate.artnr == exratenr)).first()

                        if exrate:
                            cust_list.ba_umsatz = t_genstat.res_deci[6] / exrate.betrag
                            cust_list.gesamtumsatz = cust_list.gesamtumsatz + (t_genstat.res_deci[6] / exrate.betrag)


                    else:
                        cust_list.ba_umsatz = t_genstat.res_deci[6]
                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + t_genstat.res_deci[6]

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == guest.land)).first()

                    if nation:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                        if queasy:
                            cust_list.region = queasy.char1
                    else:
                        cust_list.region = "UNKNOWN"
        else:
            cr_ftd_all()

        if tdate != None and tdate >= ci_date and check_ftd:
            create_forecast_all()
    else:

        if not check_ftd:

            genstat_obj_list = []
            for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr) &  (Guest.karteityp == cardtype)).filter(
                    (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                if genstat._recid in genstat_obj_list:
                    continue
                else:
                    genstat_obj_list.append(genstat._recid)

                cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == guest.gastnr), first=True)

                if not cust_list:
                    cust_list = Cust_list()
                    cust_list_list.append(cust_list)

                    cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                            guest.anredefirm)
                    cust_list.gastnr = guest.gastnr
                    cust_list.wohnort = guest.wohnort
                    cust_list.plz = guest.plz
                    cust_list.land = guest.land
                    cust_list.sales_id = guest.phonetik3

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == guest.land)).first()

                    if nation:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                        if queasy:
                            cust_list.region = queasy.char1
                    else:
                        cust_list.region = "UNKOWN"

                artikel = db_session.query(Artikel).filter(
                        (Artikel.zwkum == bfast_art)).first()

                if artikel:
                    service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, genstat.datum, artikel.service_code, artikel.mwst_code))

                if currency != " ":

                    exrate = db_session.query(exrate).filter(
                            (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                    if exrate:
                        cust_list.f_b_umsatz = cust_list.f_b_umsatz + ((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) / exrate.betrag)
                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + (genstat.res_deci[4] / exrate.betrag)
                        cust_list.argtumsatz = cust_list.argtumsatz + (genstat.logis / exrate.betrag)
                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((genstat.logis + genstat.res_deci[1] +\
                                genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]) / exrate.betrag)
                        cust_list.logiernachte = cust_list.logiernachte + 1


                else:
                    cust_list.f_b_umsatz = cust_list.f_b_umsatz + genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]
                    cust_list.sonst_umsatz = cust_list.sonst_umsatz + genstat.res_deci[4]
                    cust_list.argtumsatz = cust_list.argtumsatz + genstat.logis
                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + genstat.logis + genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]
                    cust_list.logiernachte = cust_list.logiernachte + 1

                if excl_other == False:

                    if curr_resnr1 != genstat.resnr or curr_reslinnr1 != genstat.res_int[0]:
                        curr_resnr1 = genstat.resnr
                        curr_reslinnr1 = genstat.res_int[0]

                        for bill in db_session.query(Bill).filter(
                                (Bill.resnr == genstat.resnr) &  (Bill.reslinnr == genstat.res_int[0])).all():

                            bill_line_obj_list = []
                            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) &  (Artikel.departement == Bill_line.departement) &  (Artikel.artart == 0)).filter(
                                    (Bill_line.rechnr == bill.rechnr) &  (Bill_line.bill_datum == genstat.datum)).all():
                                if bill_line._recid in bill_line_obj_list:
                                    continue
                                else:
                                    bill_line_obj_list.append(bill_line._recid)


                                service = 0
                                vat = 0


                                service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, genstat.datum, artikel.service_code, artikel.mwst_code))

                                if currency != "":

                                    exrate = db_session.query(exrate).filter(
                                            (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                    if exrate:
                                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + ((bill_line.betrag / (1 + service + vat)) / exrate.betrag)
                                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((bill_line.betrag / (1 + service + vat)) / exrate.betrag)


                                else:
                                    cust_list.sonst_umsatz = cust_list.sonst_umsatz + bill_line.betrag / (1 + service + vat)
                                    cust_list.gesamtumsatz = cust_list.gesamtumsatz + bill_line.betrag / (1 + service + vat)

            if excl_other == False:

                for guest_queasy in db_session.query(Guest_queasy).filter(
                        (func.lower(Guest_queasy.key) == "gast_info") &  (Guest_queasy.date1 >= fdate) &  (Guest_queasy.date1 <= tdate)).all():

                    genstat = db_session.query(Genstat).filter(
                            (Genstat.resnr == guest_queasy.number2) &  (Genstat.res_int[0] == guest_queasy.number3) &  (Genstat.datum == guest_queasy.date1) &  (Genstat.res_logic[1])).first()

                    if genstat:

                        cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == genstat.gastnr), first=True)

                        if cust_list:
                            for loopj in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                                if entry(loopj - 1, cust_list.resnr, ";") == to_string(genstat.resnr):
                                    found_it = True


                                    break
                                else:
                                    found_it = False

                            if found_it :

                                h_bill_line_obj_list = []
                                for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).filter(
                                        (H_bill_line.rechnr == to_int(guest_queasy.char1)) &  (H_bill_line.departement == guest_queasy.number1)).all():
                                    if h_bill_line._recid in h_bill_line_obj_list:
                                        continue
                                    else:
                                        h_bill_line_obj_list.append(h_bill_line._recid)


                                    service = 0
                                    vat = 0


                                    service, vat = get_output(calc_servvat(artikel.departement, artikel.artnr, guest_queasy.date1, artikel.service_code, artikel.mwst_code))

                                    if currency != " ":

                                        exrate = db_session.query(exrate).filter(
                                                (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                        if exrate:
                                            cust_list.f_b_umsatz = cust_list.f_b_umsatz + (((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service + vat)) / exrate.betrag)
                                            cust_list.sonst_umsatz = cust_list.sonst_umsatz + ((guest_queasy.deci3 / (1 + service + vat)) / exrate.betrag)
                                            cust_list.gesamtumsatz = cust_list.gesamtumsatz + (((guest_queasy.deci1 + guest_queasy.deci2 + guest_queasy.deci3) / (1 + service + vat)) / exrate.betrag)


                                    else:
                                        cust_list.f_b_umsatz = cust_list.f_b_umsatz + ((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service + vat))
                                        cust_list.sonst_umsatz = cust_list.sonst_umsatz + (guest_queasy.deci3 / (1 + service + vat))
                                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + ((guest_queasy.deci1 + guest_queasy.deci2 + guest_queasy.deci3) / (1 + service + vat))

            t_genstat_obj_list = []
            for t_genstat, guest in db_session.query(T_genstat, Guest).join(Guest,(Guest.gastnr == T_genstat.gastnr) &  (Guest.karteityp == cardtype)).filter(
                    (T_genstat.datum >= fdate) &  (T_genstat.datum <= tdate) &  (T_genstat.res_deci[6] != 0)).all():
                if t_genstat._recid in t_genstat_obj_list:
                    continue
                else:
                    t_genstat_obj_list.append(t_genstat._recid)

                cust_list = query(cust_list_list, filters=(lambda cust_list :cust_list.gastnr == t_genstat.gastnr), first=True)

                if cust_list:

                    if currency != " ":

                        exrate = db_session.query(exrate).filter(
                                (exrate.datum == t_genstat.datum) &  (exrate.artnr == exratenr)).first()

                        if exrate:
                            cust_list.ba_umsatz = cust_list.ba_umsatz + (t_genstat.res_deci[6] / exrate.betrag)
                            cust_list.gesamtumsatz = cust_list.gesamtumsatz + (t_genstat.res_deci[6] / exrate.betrag)


                    else:
                        cust_list.ba_umsatz = cust_list.ba_umsatz + t_genstat.res_deci[6]
                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + t_genstat.res_deci[6]


                else:
                    cust_list = Cust_list()
                    cust_list_list.append(cust_list)

                    cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                            guest.anredefirm)
                    cust_list.gastnr = guest.gastnr
                    cust_list.wohnort = guest.wohnort
                    cust_list.plz = guest.plz
                    cust_list.land = guest.land
                    cust_list.sales_id = guest.phonetik3

                    if currency != " ":

                        exrate = db_session.query(exrate).filter(
                                (exrate.datum == t_genstat.datum) &  (exrate.artnr == exratenr)).first()

                        if exrate:
                            cust_list.ba_umsatz = (t_genstat.res_deci[6] / exrate.betrag)
                            cust_list.gesamtumsatz = cust_list.gesamtumsatz + (t_genstat.res_deci[6] / exrate.betrag)


                    else:
                        cust_list.ba_umsatz = t_genstat.res_deci[6]
                        cust_list.gesamtumsatz = cust_list.gesamtumsatz + t_genstat.res_deci[6]

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == guest.land)).first()

                    if nation:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                        if queasy:
                            cust_list.region = queasy.char1
                    else:
                        cust_list.region = "UNKNOWN"
        else:
            cr_ftd()

        if tdate != None and tdate >= ci_date and check_ftd:
            create_forecast()

    return generate_output()