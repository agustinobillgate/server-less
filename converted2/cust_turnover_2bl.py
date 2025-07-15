#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.get_room_breakdown import get_room_breakdown
from models import Waehrung, Genstat, Guest, Htparam, Nation, Queasy, Artikel, exrate, Bill, Bill_line, Guest_queasy, H_artikel, H_bill_line, Res_line, Reservation, Sourccod, Segment, Arrangement, Zimmer

def cust_turnover_2bl(cardtype:int, sort_type:int, curr_sort1:int, fdate:date, tdate:date, check_ftd:bool, currency:string, excl_other:bool, curr_sort2:int):

    prepare_cache ([Waehrung, Genstat, Guest, Htparam, Nation, Queasy, Artikel, exrate, Guest_queasy, H_bill_line, Res_line, Reservation, Arrangement])

    cust_list_data = []
    bfast_art:int = 0
    lunch_art:int = 0
    dinner_art:int = 0
    lundin_art:int = 0
    service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    fact1:Decimal = to_decimal("0.0")
    datum:date = None
    end_date:date = None
    net_lodg:Decimal = to_decimal("0.0")
    fnet_lodg:Decimal = to_decimal("0.0")
    tot_breakfast:Decimal = to_decimal("0.0")
    tot_lunch:Decimal = to_decimal("0.0")
    tot_dinner:Decimal = to_decimal("0.0")
    tot_other:Decimal = to_decimal("0.0")
    tot_rmrev:Decimal = to_decimal("0.0")
    tot_vat:Decimal = to_decimal("0.0")
    tot_service:Decimal = to_decimal("0.0")
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
    t_logiernachte:Decimal = to_decimal("0.0")
    t_argtumsatz:Decimal = to_decimal("0.0")
    t_fb_umsatz:Decimal = to_decimal("0.0")
    t_sonst_umsatz:Decimal = to_decimal("0.0")
    t_ba_umsatz:Decimal = to_decimal("0.0")
    t_gesamtumsatz:Decimal = to_decimal("0.0")
    tot_logiernachte:Decimal = to_decimal("0.0")
    tot_argtumsatz:Decimal = to_decimal("0.0")
    tot_fb_umsatz:Decimal = to_decimal("0.0")
    tot_sonst_umsatz:Decimal = to_decimal("0.0")
    tot_ba_umsatz:Decimal = to_decimal("0.0")
    tot_gesamtumsatz:Decimal = to_decimal("0.0")
    tot_stayno:Decimal = to_decimal("0.0")
    loopj:int = 0
    found_it:bool = False
    exratenr:int = 0
    exrate:Decimal = to_decimal("0.0")
    curr_resnr2:int = 0
    curr_reslinnr2:int = 0
    curr_resnr1:int = 0
    curr_reslinnr1:int = 0
    waehrung = genstat = guest = htparam = nation = queasy = artikel = exrate = bill = bill_line = guest_queasy = h_artikel = h_bill_line = res_line = reservation = sourccod = segment = arrangement = zimmer = None

    cust_list = cust_list_detail = cust_list2 = t_waehrung = t_genstat = blist = glist = clist = None

    cust_list_data, Cust_list = create_model("Cust_list", {"gastnr":int, "cust_name":string, "gesamtumsatz":Decimal, "logiernachte":int, "argtumsatz":Decimal, "f_b_umsatz":Decimal, "sonst_umsatz":Decimal, "wohnort":string, "plz":string, "land":string, "sales_id":string, "ba_umsatz":Decimal, "ly_rev":Decimal, "region":string, "region1":string, "stayno":int, "resnr":string, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int})
    cust_list_detail_data, Cust_list_detail = create_model("Cust_list_detail", {"gastnr":int, "cust_name":string, "gesamtumsatz":string, "logiernachte":string, "argtumsatz":string, "f_b_umsatz":string, "sonst_umsatz":string, "wohnort":string, "plz":string, "land":string, "sales_id":string, "ba_umsatz":string, "ly_rev":string, "region":string, "region1":string, "stayno":string, "resnr":string, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int})
    cust_list2_data, Cust_list2 = create_model_like(Cust_list)
    t_waehrung_data, T_waehrung = create_model_like(Waehrung)

    T_genstat = create_buffer("T_genstat",Genstat)
    Blist = Cust_list_detail
    blist_data = cust_list_detail_data

    Glist = create_buffer("Glist",Guest)
    Clist = Cust_list_detail
    clist_data = cust_list_detail_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cust_list_data, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, vat2, fact1, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_resnr, curr_reslinnr, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, loopj, found_it, exratenr, exrate, curr_resnr2, curr_reslinnr2, curr_resnr1, curr_reslinnr1, waehrung, genstat, guest, htparam, nation, queasy, artikel, exrate, bill, bill_line, guest_queasy, h_artikel, h_bill_line, res_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal cardtype, sort_type, curr_sort1, fdate, tdate, check_ftd, currency, excl_other, curr_sort2
        nonlocal t_genstat, blist, glist, clist


        nonlocal cust_list, cust_list_detail, cust_list2, t_waehrung, t_genstat, blist, glist, clist
        nonlocal cust_list_data, cust_list_detail_data, cust_list2_data, t_waehrung_data

        return {"curr_sort2": curr_sort2, "cust-list": cust_list_data}

    def create_forecast():

        nonlocal cust_list_data, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, vat2, fact1, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, loopj, found_it, exratenr, exrate, curr_resnr2, curr_reslinnr2, curr_resnr1, curr_reslinnr1, waehrung, genstat, guest, htparam, nation, queasy, artikel, exrate, bill, bill_line, guest_queasy, h_artikel, h_bill_line, res_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal cardtype, sort_type, curr_sort1, fdate, tdate, check_ftd, currency, excl_other, curr_sort2
        nonlocal t_genstat, blist, glist, clist


        nonlocal cust_list, cust_list_detail, cust_list2, t_waehrung, t_genstat, blist, glist, clist
        nonlocal cust_list_data, cust_list_detail_data, cust_list2_data, t_waehrung_data

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

        if tdate < (ci_date - timedelta(days=1)):
            d2 = tdate
        else:
            d2 = ci_date - timedelta(days=1)
        d2 = d2 + timedelta(days=1)

        res_line_obj_list = {}
        res_line = Res_line()
        guest = Guest()
        for res_line.resnr, res_line.arrangement, res_line.reslinnr, res_line.zinr, res_line.gastnr, res_line.ankunft, res_line.abreise, res_line._recid, res_line.resstatus, res_line.zimmerfix, guest.name, guest.vorname1, guest.anrede1, guest.gastnr, guest.wohnort, guest.plz, guest.land, guest.phonetik3, guest._recid in db_session.query(Res_line.resnr, Res_line.arrangement, Res_line.reslinnr, Res_line.zinr, Res_line.gastnr, Res_line.ankunft, Res_line.abreise, Res_line._recid, Res_line.resstatus, Res_line.zimmerfix, Guest.name, Guest.vorname1, Guest.anrede1, Guest.gastnr, Guest.wohnort, Guest.plz, Guest.land, Guest.phonetik3, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == cardtype)).filter(
                 ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (not_ (Res_line.ankunft > tdate)) & (not_ (Res_line.abreise <= fdate))) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.gastnr, Res_line.resnr, Res_line.reslinnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
            curr_i = 0
            do_it = True

            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
            do_it = None != segment and segment.vip_level == 0

            if do_it and res_line.resstatus == 8:

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, ci_date)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})
                do_it = None != bill_line

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

            if do_it and zimmer:

                queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                if zimmer.sleeping:

                    if queasy and queasy.number3 == res_line.gastnr:
                        do_it = False
                else:

                    if queasy and queasy.number3 != res_line.gastnr:
                        pass
                    else:
                        do_it = False

            if do_it:

                cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == res_line.gastnr), first=True)

                if not cust_list:
                    cust_list = Cust_list()
                    cust_list_data.append(cust_list)

                    cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                            guest.anredefirm)
                    cust_list.gastnr = guest.gastnr
                    cust_list.wohnort = guest.wohnort
                    cust_list.plz = guest.plz
                    cust_list.land = guest.land
                    cust_list.sales_id = guest.phonetik3

                    nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                    if nation:

                        queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

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
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = tdate
                for datum in date_range(datum1,datum2) :
                    curr_i = curr_i + 1
                    net_lodg =  to_decimal("0")
                    fnet_lodg =  to_decimal("0")
                    tot_breakfast =  to_decimal("0")
                    tot_lunch =  to_decimal("0")
                    tot_dinner =  to_decimal("0")
                    tot_other =  to_decimal("0")
                    tot_rmrev =  to_decimal("0")
                    tot_vat =  to_decimal("0")
                    tot_service =  to_decimal("0")


                    fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, ci_date))

                    if currency != " ":
                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((net_lodg) + to_decimal(tot_breakfast) +\
                                tot_lunch + to_decimal(tot_dinner) + to_decimal(tot_other)) / to_decimal(exrate) )
                        cust_list.argtumsatz =  to_decimal(cust_list.argtumsatz) + to_decimal((net_lodg) / to_decimal(exrate) )
                        cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(((tot_breakfast) + to_decimal(tot_lunch) + to_decimal(tot_dinner)) / to_decimal(exrate) )
                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal((tot_other) / to_decimal(exrate) )


                    else:
                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(net_lodg) + to_decimal(tot_breakfast) +\
                                tot_lunch + to_decimal(tot_dinner) + to_decimal(tot_other)
                        cust_list.argtumsatz =  to_decimal(cust_list.argtumsatz) + to_decimal(net_lodg)
                        cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(tot_breakfast) + to_decimal(tot_lunch) + to_decimal(tot_dinner)
                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(tot_other)

                    if excl_other == False:

                        if curr_resnr != res_line.resnr or curr_reslinnr != res_line.reslinnr:
                            curr_resnr = res_line.resnr
                            curr_reslinnr = res_line.reslinnr

                            for bill in db_session.query(Bill).filter(
                                     (Bill.resnr == res_line.resnr) & (Bill.reslinnr == res_line.reslinnr)).order_by(Bill._recid).all():

                                bill_line_obj_list = {}
                                for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & (Artikel.artart == 0)).filter(
                                         (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum == datum)).order_by(Bill_line._recid).all():
                                    if bill_line_obj_list.get(bill_line._recid):
                                        continue
                                    else:
                                        bill_line_obj_list[bill_line._recid] = True


                                    service =  to_decimal("0")
                                    vat =  to_decimal("0")


                                    service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))

                                    if currency != "":

                                        exrate = get_cache (exrate, {"datum": [(eq, datum)],"artnr": [(eq, exratenr)]})

                                        if exrate:
                                            cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(((bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                            cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )


                                    else:
                                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )
                                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )

                    if ((res_line.ankunft < res_line.abreise) and res_line.abreise != datum) or (res_line.ankunft == res_line.abreise):

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and res_line.resstatus != 3 and not res_line.zimmerfix:
                            cust_list.logiernachte = cust_list.logiernachte + 1

        if excl_other == False:

            for guest_queasy in db_session.query(Guest_queasy).filter(
                     (Guest_queasy.key == ("gast-info").lower()) & (Guest_queasy.date1 >= fdate) & (Guest_queasy.date1 <= tdate)).order_by(Guest_queasy._recid).all():

                res_line = get_cache (Res_line, {"resnr": [(eq, guest_queasy.number2)],"reslinnr": [(eq, guest_queasy.number3)]})

                if res_line:

                    cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == res_line.gastnr), first=True)

                    if cust_list:
                        for loopj in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                            if entry(loopj - 1, cust_list.resnr, ";") == to_string(res_line.resnr):
                                found_it = True


                                break
                            else:
                                found_it = False

                        if found_it :

                            h_bill_line_obj_list = {}
                            for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                                     (H_bill_line.rechnr == to_int(guest_queasy.char1)) & (H_bill_line.departement == guest_queasy.number1)).order_by(H_bill_line._recid).all():
                                if h_bill_line_obj_list.get(h_bill_line._recid):
                                    continue
                                else:
                                    h_bill_line_obj_list[h_bill_line._recid] = True


                                service =  to_decimal("0")
                                vat =  to_decimal("0")


                                service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, guest_queasy.date1))

                                if currency != " ":

                                    exrate = get_cache (exrate, {"datum": [(eq, h_bill_line.bill_datum)],"artnr": [(eq, exratenr)]})

                                    if exrate:
                                        cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal((((guest_queasy.deci1) + to_decimal(guest_queasy.deci2)) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(((guest_queasy.deci3) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal((((guest_queasy.deci1) + to_decimal(guest_queasy.deci2) + to_decimal(guest_queasy.deci3)) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )


                                else:
                                    cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(((guest_queasy.deci1) + to_decimal(guest_queasy.deci2)) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )
                                    cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal((guest_queasy.deci3) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )
                                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((guest_queasy.deci1) + to_decimal(guest_queasy.deci2) + to_decimal(guest_queasy.deci3)) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )

        if get_day(fdate) == 29 and get_month(fdate) == 2:
            ly_fdate = date_mdy(get_month(fdate) , 28, get_year(fdate) - timedelta(days=1))
        else:
            ly_fdate = date_mdy(get_month(fdate) , get_day(fdate) , get_year(fdate) - timedelta(days=1))

        if get_day(tdate) == 29 and get_month(tdate) == 2:
            ly_tdate = date_mdy(get_month(tdate) , 28, get_year(tdate) - timedelta(days=1))
        else:
            ly_tdate = date_mdy(get_month(tdate) , get_day(tdate) , get_year(tdate) - timedelta(days=1))

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.datum, genstat.logis, genstat.res_deci, genstat.resnr, genstat.res_int, genstat.gastnr, genstat.resstatus, genstat._recid, guest.name, guest.vorname1, guest.anrede1, guest.gastnr, guest.wohnort, guest.plz, guest.land, guest.phonetik3, guest._recid in db_session.query(Genstat.datum, Genstat.logis, Genstat.res_deci, Genstat.resnr, Genstat.res_int, Genstat.gastnr, Genstat.resstatus, Genstat._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.gastnr, Guest.wohnort, Guest.plz, Guest.land, Guest.phonetik3, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                 (Genstat.datum >= ly_fdate) & (Genstat.datum <= ly_tdate) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.gesamtumsatz.desc(), Guest.logiernachte.desc(), Guest.name).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == guest.gastnr), first=True)

            if cust_list:

                if currency != " ":

                    exrate = get_cache (exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                    if exrate:
                        cust_list.ly_rev =  to_decimal(cust_list.ly_rev) + to_decimal(((genstat.logis) + to_decimal(genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])) / to_decimal(exrate.betrag) )


                else:
                    cust_list.ly_rev =  to_decimal(cust_list.ly_rev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])


    def cr_ftd():

        nonlocal cust_list_data, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, vat2, fact1, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, t_logiernachte, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, loopj, found_it, exratenr, exrate, curr_resnr2, curr_reslinnr2, curr_resnr1, curr_reslinnr1, waehrung, genstat, guest, htparam, nation, queasy, artikel, exrate, bill, bill_line, guest_queasy, h_artikel, h_bill_line, res_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal cardtype, sort_type, curr_sort1, fdate, tdate, check_ftd, currency, excl_other, curr_sort2
        nonlocal t_genstat, blist, glist, clist


        nonlocal cust_list, cust_list_detail, cust_list2, t_waehrung, t_genstat, blist, glist, clist
        nonlocal cust_list_data, cust_list_detail_data, cust_list2_data, t_waehrung_data

        t_argtumsatz:int = 0
        rate:Decimal = 1
        frate:Decimal = 1
        rmnite:int = 0
        curr_resnr:int = 0
        curr_reslinnr:int = 0
        cust_list2_data.clear()

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.datum, genstat.logis, genstat.res_deci, genstat.resnr, genstat.res_int, genstat.gastnr, genstat.resstatus, genstat._recid, guest.name, guest.vorname1, guest.anrede1, guest.gastnr, guest.wohnort, guest.plz, guest.land, guest.phonetik3, guest._recid in db_session.query(Genstat.datum, Genstat.logis, Genstat.res_deci, Genstat.resnr, Genstat.res_int, Genstat.gastnr, Genstat.resstatus, Genstat._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.gastnr, Guest.wohnort, Guest.plz, Guest.land, Guest.phonetik3, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                 (Genstat.datum >= fdate) & (Genstat.datum <= tdate) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.gastnr, Genstat.resnr, Guest.land).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == guest.gastnr), first=True)

            if not cust_list:
                cust_list = Cust_list()
                cust_list_data.append(cust_list)

                cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)
                cust_list.gastnr = guest.gastnr
                cust_list.wohnort = guest.wohnort
                cust_list.plz = guest.plz
                cust_list.land = guest.land
                cust_list.sales_id = guest.phonetik3

                nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                if nation:

                    queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

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

            artikel = get_cache (Artikel, {"zwkum": [(eq, bfast_art)]})

            if artikel:
                service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

            if currency != " ":

                exrate = get_cache (exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                if exrate:
                    cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])) / to_decimal(exrate.betrag) )
                    cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal((genstat.res_deci[4]) / to_decimal(exrate.betrag) )
                    cust_list.argtumsatz =  to_decimal(cust_list.argtumsatz) + to_decimal((genstat.logis) / to_decimal(exrate.betrag) )
                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((genstat.logis) + to_decimal(genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])) / to_decimal(exrate.betrag) )


            else:
                cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])
                cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(genstat.res_deci[4])
                cust_list.argtumsatz =  to_decimal(cust_list.argtumsatz) + to_decimal(genstat.logis)
                cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] +\
                    genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])

            if genstat.resstatus != 13:
                cust_list.logiernachte = cust_list.logiernachte + 1

            if excl_other == False:

                if curr_resnr != genstat.resnr or curr_reslinnr != genstat.res_int[0]:
                    curr_resnr = genstat.resnr
                    curr_reslinnr = genstat.res_int[0]

                    for bill in db_session.query(Bill).filter(
                             (Bill.resnr == genstat.resnr) & (Bill.reslinnr == genstat.res_int[0])).order_by(Bill._recid).all():

                        bill_line_obj_list = {}
                        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & (Artikel.artart == 0)).filter(
                                 (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum == genstat.datum)).order_by(Bill_line._recid).all():
                            if bill_line_obj_list.get(bill_line._recid):
                                continue
                            else:
                                bill_line_obj_list[bill_line._recid] = True


                            service =  to_decimal("0")
                            vat =  to_decimal("0")


                            service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

                            if currency != "":

                                exrate = get_cache (exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                if exrate:
                                    cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(((bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )


                            else:
                                cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )
                                cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )

        if excl_other == False:

            for guest_queasy in db_session.query(Guest_queasy).filter(
                     (Guest_queasy.key == ("gast-info").lower()) & (Guest_queasy.date1 >= fdate) & (Guest_queasy.date1 <= tdate)).order_by(Guest_queasy.number2).all():

                genstat = get_cache (Genstat, {"resnr": [(eq, guest_queasy.number2)],"res_int[0]": [(eq, guest_queasy.number3)],"datum": [(eq, guest_queasy.date1)],"res_logic[1]": [(eq, True)]})

                if genstat:

                    cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == genstat.gastnr), first=True)

                    if cust_list:
                        for loopj in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                            if entry(loopj - 1, cust_list.resnr, ";") == to_string(genstat.resnr):
                                found_it = True


                                break
                            else:
                                found_it = False

                        if found_it :

                            h_bill_line_obj_list = {}
                            for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                                     (H_bill_line.rechnr == to_int(guest_queasy.char1)) & (H_bill_line.departement == guest_queasy.number1)).order_by(H_bill_line._recid).all():
                                if h_bill_line_obj_list.get(h_bill_line._recid):
                                    continue
                                else:
                                    h_bill_line_obj_list[h_bill_line._recid] = True


                                service =  to_decimal("0")
                                vat =  to_decimal("0")


                                service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, guest_queasy.date1))

                                if currency != " ":

                                    exrate = get_cache (exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                    if exrate:
                                        cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal((((guest_queasy.deci1) + to_decimal(guest_queasy.deci2)) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(((guest_queasy.deci3) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal((((guest_queasy.deci1) + to_decimal(guest_queasy.deci2) + to_decimal(guest_queasy.deci3)) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )


                                else:
                                    cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(((guest_queasy.deci1) + to_decimal(guest_queasy.deci2)) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )
                                    cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal((guest_queasy.deci3) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )
                                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((guest_queasy.deci1) + to_decimal(guest_queasy.deci2) + to_decimal(guest_queasy.deci3)) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )

        for cust_list2 in query(cust_list2_data, sort_by=[("gesamtumsatz",True),("logiernachte",True),("cust_name",False)]):
            cust_list = Cust_list()
            cust_list_data.append(cust_list)

            buffer_copy(cust_list2, cust_list)

        t_genstat_obj_list = {}
        t_genstat = Genstat()
        guest = Guest()
        for t_genstat.datum, t_genstat.logis, t_genstat.res_deci, t_genstat.resnr, t_genstat.res_int, t_genstat.gastnr, t_genstat.resstatus, t_genstat._recid, guest.name, guest.vorname1, guest.anrede1, guest.gastnr, guest.wohnort, guest.plz, guest.land, guest.phonetik3, guest._recid in db_session.query(T_genstat.datum, T_genstat.logis, T_genstat.res_deci, T_genstat.resnr, T_genstat.res_int, T_genstat.gastnr, T_genstat.resstatus, T_genstat._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.gastnr, Guest.wohnort, Guest.plz, Guest.land, Guest.phonetik3, Guest._recid).join(Guest,(Guest.gastnr == T_genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                 (T_genstat.datum >= fdate) & (T_genstat.datum <= tdate) & (T_genstat.res_deci[inc_value(6)] != 0)).order_by(T_genstat._recid).all():
            if t_genstat_obj_list.get(t_genstat._recid):
                continue
            else:
                t_genstat_obj_list[t_genstat._recid] = True

            cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == t_genstat.gastnr), first=True)

            if cust_list:

                if currency != " ":

                    exrate = get_cache (exrate, {"datum": [(eq, t_genstat.datum)],"artnr": [(eq, exratenr)]})

                    if exrate:
                        cust_list.ba_umsatz =  to_decimal(cust_list.ba_umsatz) + to_decimal((t_genstat.res_deci[6]) / to_decimal(exrate.betrag) )
                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal((t_genstat.res_deci[6]) / to_decimal(exrate.betrag) )


                else:
                    cust_list.ba_umsatz =  to_decimal(cust_list.ba_umsatz) + to_decimal(t_genstat.res_deci[6])
                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(t_genstat.res_deci[6])


            else:
                cust_list = Cust_list()
                cust_list_data.append(cust_list)

                cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)
                cust_list.gastnr = guest.gastnr
                cust_list.wohnort = guest.wohnort
                cust_list.plz = guest.plz
                cust_list.land = guest.land
                cust_list.sales_id = guest.phonetik3

                if currency != " ":

                    exrate = get_cache (exrate, {"datum": [(eq, t_genstat.datum)],"artnr": [(eq, exratenr)]})

                    if exrate:
                        cust_list.ba_umsatz = ( to_decimal(t_genstat.res_deci[6]) / to_decimal(exrate.betrag) )
                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal((t_genstat.res_deci[6]) / to_decimal(exrate.betrag) )


                else:
                    cust_list.ba_umsatz =  to_decimal(t_genstat.res_deci[6])
                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(t_genstat.res_deci[6])

                nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                if nation:

                    queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                    if queasy:
                        cust_list.region = queasy.char1
                else:
                    cust_list.region = "UNKNOWN"


    def create_forecast_all():

        nonlocal cust_list_data, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, vat2, fact1, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, loopj, found_it, exratenr, exrate, curr_resnr2, curr_reslinnr2, curr_resnr1, curr_reslinnr1, waehrung, genstat, guest, htparam, nation, queasy, artikel, exrate, bill, bill_line, guest_queasy, h_artikel, h_bill_line, res_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal cardtype, sort_type, curr_sort1, fdate, tdate, check_ftd, currency, excl_other, curr_sort2
        nonlocal t_genstat, blist, glist, clist


        nonlocal cust_list, cust_list_detail, cust_list2, t_waehrung, t_genstat, blist, glist, clist
        nonlocal cust_list_data, cust_list_detail_data, cust_list2_data, t_waehrung_data

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

        if tdate < (ci_date - timedelta(days=1)):
            d2 = tdate
        else:
            d2 = ci_date - timedelta(days=1)
        d2 = d2 + timedelta(days=1)

        res_line_obj_list = {}
        res_line = Res_line()
        guest = Guest()
        for res_line.resnr, res_line.arrangement, res_line.reslinnr, res_line.zinr, res_line.gastnr, res_line.ankunft, res_line.abreise, res_line._recid, res_line.resstatus, res_line.zimmerfix, guest.name, guest.vorname1, guest.anrede1, guest.gastnr, guest.wohnort, guest.plz, guest.land, guest.phonetik3, guest._recid in db_session.query(Res_line.resnr, Res_line.arrangement, Res_line.reslinnr, Res_line.zinr, Res_line.gastnr, Res_line.ankunft, Res_line.abreise, Res_line._recid, Res_line.resstatus, Res_line.zimmerfix, Guest.name, Guest.vorname1, Guest.anrede1, Guest.gastnr, Guest.wohnort, Guest.plz, Guest.land, Guest.phonetik3, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
                 ((Res_line.active_flag <= 1) & (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (not_ (Res_line.ankunft > tdate)) & (not_ (Res_line.abreise <= fdate))) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.gastnr, Res_line.resnr, Res_line.reslinnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})
            curr_i = 0
            do_it = True

            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
            do_it = None != segment and segment.vip_level == 0

            if do_it and res_line.resstatus == 8:

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                bill_line = get_cache (Bill_line, {"departement": [(eq, 0)],"artnr": [(eq, arrangement.argt_artikelnr)],"bill_datum": [(eq, ci_date)],"massnr": [(eq, res_line.resnr)],"billin_nr": [(eq, res_line.reslinnr)]})
                do_it = None != bill_line

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

            if do_it and zimmer:

                queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                if zimmer.sleeping:

                    if queasy and queasy.number3 == res_line.gastnr:
                        do_it = False
                else:

                    if queasy and queasy.number3 != res_line.gastnr:
                        pass
                    else:
                        do_it = False

            if do_it:

                cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == res_line.gastnr), first=True)

                if not cust_list:
                    cust_list = Cust_list()
                    cust_list_data.append(cust_list)

                    cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                            guest.anredefirm)
                    cust_list.gastnr = guest.gastnr
                    cust_list.wohnort = guest.wohnort
                    cust_list.plz = guest.plz
                    cust_list.land = guest.land
                    cust_list.sales_id = guest.phonetik3

                    nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                    if nation:

                        queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

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
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = tdate
                for datum in date_range(datum1,datum2) :
                    curr_i = curr_i + 1
                    net_lodg =  to_decimal("0")
                    fnet_lodg =  to_decimal("0")
                    tot_breakfast =  to_decimal("0")
                    tot_lunch =  to_decimal("0")
                    tot_dinner =  to_decimal("0")
                    tot_other =  to_decimal("0")
                    tot_rmrev =  to_decimal("0")
                    tot_vat =  to_decimal("0")
                    tot_service =  to_decimal("0")


                    fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, ci_date))

                    if currency != " ":
                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((net_lodg) + to_decimal(tot_breakfast) +\
                                tot_lunch + to_decimal(tot_dinner) + to_decimal(tot_other)) / to_decimal(exrate) )
                        cust_list.argtumsatz =  to_decimal(cust_list.argtumsatz) + to_decimal((net_lodg) / to_decimal(exrate) )
                        cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal((tot_breakfast) + to_decimal(tot_lunch) + to_decimal(tot_dinner) / to_decimal(exrate) )
                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal((tot_other) / to_decimal(exrate) )


                    else:
                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(net_lodg) + to_decimal(tot_breakfast) +\
                                tot_lunch + to_decimal(tot_dinner) + to_decimal(tot_other)
                        cust_list.argtumsatz =  to_decimal(cust_list.argtumsatz) + to_decimal(net_lodg)
                        cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(tot_breakfast) + to_decimal(tot_lunch) + to_decimal(tot_dinner)
                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(tot_other)

                    if excl_other == False:

                        if curr_resnr != res_line.resnr or curr_reslinnr != res_line.reslinnr:
                            curr_resnr = res_line.resnr
                            curr_reslinnr = res_line.reslinnr

                            for bill in db_session.query(Bill).filter(
                                     (Bill.resnr == res_line.resnr) & (Bill.reslinnr == res_line.reslinnr)).order_by(Bill._recid).all():

                                bill_line_obj_list = {}
                                for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & (Artikel.artart == 0)).filter(
                                         (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum == datum)).order_by(Bill_line._recid).all():
                                    if bill_line_obj_list.get(bill_line._recid):
                                        continue
                                    else:
                                        bill_line_obj_list[bill_line._recid] = True


                                    service =  to_decimal("0")
                                    vat =  to_decimal("0")


                                    service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

                                    if currency != "":

                                        exrate = get_cache (exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                        if exrate:
                                            cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(((bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                            cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )


                                    else:
                                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )
                                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )

                    if ((res_line.ankunft < res_line.abreise) and res_line.abreise != datum) or (res_line.ankunft == res_line.abreise):

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and res_line.resstatus != 3 and not res_line.zimmerfix:
                            cust_list.logiernachte = cust_list.logiernachte + 1

        if excl_other == False:

            for guest_queasy in db_session.query(Guest_queasy).filter(
                     (Guest_queasy.key == ("gast-info").lower()) & (Guest_queasy.date1 >= fdate) & (Guest_queasy.date1 <= tdate)).order_by(Guest_queasy._recid).all():

                res_line = get_cache (Res_line, {"resnr": [(eq, guest_queasy.number2)],"reslinnr": [(eq, guest_queasy.number3)]})

                if res_line:

                    cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == res_line.gastnr), first=True)

                    if cust_list:
                        for loopj in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                            if entry(loopj - 1, cust_list.resnr, ";") == to_string(res_line.resnr):
                                found_it = True


                                break
                            else:
                                found_it = False

                        if found_it :

                            h_bill_line_obj_list = {}
                            for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                                     (H_bill_line.rechnr == to_int(guest_queasy.char1)) & (H_bill_line.departement == guest_queasy.number1)).order_by(H_bill_line._recid).all():
                                if h_bill_line_obj_list.get(h_bill_line._recid):
                                    continue
                                else:
                                    h_bill_line_obj_list[h_bill_line._recid] = True


                                service =  to_decimal("0")
                                vat =  to_decimal("0")


                                service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, guest_queasy.date1))

                                if currency != " ":

                                    exrate = get_cache (exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                    if exrate:
                                        cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal((((guest_queasy.deci1) + to_decimal(guest_queasy.deci2)) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(((guest_queasy.deci3) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal((((guest_queasy.deci1) + to_decimal(guest_queasy.deci2) + to_decimal(guest_queasy.deci3)) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )


                                else:
                                    cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(((guest_queasy.deci1) + to_decimal(guest_queasy.deci2)) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )
                                    cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal((guest_queasy.deci3) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )
                                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((guest_queasy.deci1) + to_decimal(guest_queasy.deci2) + to_decimal(guest_queasy.deci3)) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )

        if get_day(fdate) == 29 and get_month(fdate) == 2:
            ly_fdate = date_mdy(get_month(fdate) , 28, get_year(fdate) - timedelta(days=1))
        else:
            ly_fdate = date_mdy(get_month(fdate) , get_day(fdate) , get_year(fdate) - timedelta(days=1))

        if get_day(tdate) == 29 and get_month(tdate) == 2:
            ly_tdate = date_mdy(get_month(tdate) , 28, get_year(tdate) - timedelta(days=1))
        else:
            ly_tdate = date_mdy(get_month(tdate) , get_day(tdate) , get_year(tdate) - timedelta(days=1))

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.datum, genstat.logis, genstat.res_deci, genstat.resnr, genstat.res_int, genstat.gastnr, genstat.resstatus, genstat._recid, guest.name, guest.vorname1, guest.anrede1, guest.gastnr, guest.wohnort, guest.plz, guest.land, guest.phonetik3, guest._recid in db_session.query(Genstat.datum, Genstat.logis, Genstat.res_deci, Genstat.resnr, Genstat.res_int, Genstat.gastnr, Genstat.resstatus, Genstat._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.gastnr, Guest.wohnort, Guest.plz, Guest.land, Guest.phonetik3, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                 (Genstat.datum >= ly_fdate) & (Genstat.datum <= ly_tdate) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.gesamtumsatz.desc(), Guest.logiernachte.desc(), Guest.name).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == guest.gastnr), first=True)

            if cust_list:

                if currency != " ":

                    exrate = get_cache (exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                    if exrate:
                        cust_list.ly_rev =  to_decimal(cust_list.ly_rev) + to_decimal(((genstat.logis) + to_decimal(genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])) / to_decimal(exrate.betrag) )


                else:
                    cust_list.ly_rev =  to_decimal(cust_list.ly_rev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])


    def cr_ftd_all():

        nonlocal cust_list_data, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, vat2, fact1, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, t_logiernachte, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, loopj, found_it, exratenr, exrate, curr_resnr2, curr_reslinnr2, curr_resnr1, curr_reslinnr1, waehrung, genstat, guest, htparam, nation, queasy, artikel, exrate, bill, bill_line, guest_queasy, h_artikel, h_bill_line, res_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal cardtype, sort_type, curr_sort1, fdate, tdate, check_ftd, currency, excl_other, curr_sort2
        nonlocal t_genstat, blist, glist, clist


        nonlocal cust_list, cust_list_detail, cust_list2, t_waehrung, t_genstat, blist, glist, clist
        nonlocal cust_list_data, cust_list_detail_data, cust_list2_data, t_waehrung_data

        t_argtumsatz:int = 0
        rate:Decimal = 1
        frate:Decimal = 1
        rmnite:int = 0
        curr_resnr:int = 0
        curr_reslinnr:int = 0
        cust_list2_data.clear()

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.datum, genstat.logis, genstat.res_deci, genstat.resnr, genstat.res_int, genstat.gastnr, genstat.resstatus, genstat._recid, guest.name, guest.vorname1, guest.anrede1, guest.gastnr, guest.wohnort, guest.plz, guest.land, guest.phonetik3, guest._recid in db_session.query(Genstat.datum, Genstat.logis, Genstat.res_deci, Genstat.resnr, Genstat.res_int, Genstat.gastnr, Genstat.resstatus, Genstat._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.gastnr, Guest.wohnort, Guest.plz, Guest.land, Guest.phonetik3, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                 (Genstat.datum >= fdate) & (Genstat.datum <= tdate) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.gastnr, Genstat.resnr, Guest.land).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == guest.gastnr), first=True)

            if not cust_list:
                cust_list = Cust_list()
                cust_list_data.append(cust_list)

                cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)
                cust_list.gastnr = guest.gastnr
                cust_list.wohnort = guest.wohnort
                cust_list.plz = guest.plz
                cust_list.land = guest.land
                cust_list.sales_id = guest.phonetik3

                nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                if nation:

                    queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                    if queasy:
                        cust_list.region = queasy.char1
                else:
                    cust_list.region = "UNKNOWN"
            found = False

            if cust_list.resnr != "":

                if num_entries(cust_list.resnr, ";") >= 2:
                    for i in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                        if entry(i - 1, cust_list.resnr, ";") != "":

                            if to_int(entry(i - 1, cust_list.resnr, ";")) == genstat.resnr:
                                found = True
                                break

                if not found:
                    cust_list.resnr = cust_list.resnr + to_string(genstat.resnr) + ";"
            else:
                cust_list.resnr = cust_list.resnr + to_string(genstat.resnr) + ";"

            artikel = get_cache (Artikel, {"zwkum": [(eq, bfast_art)]})

            if artikel:
                service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

            if currency != " ":

                exrate = get_cache (exrate, {"datum": [(eq, t_genstat.datum)],"artnr": [(eq, exratenr)]})

                if exrate:
                    cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])) / to_decimal(exrate.betrag) )
                    cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal((genstat.res_deci[4]) / to_decimal(exrate.betrag) )
                    cust_list.argtumsatz =  to_decimal(cust_list.argtumsatz) + to_decimal((genstat.logis) / to_decimal(exrate.betrag) )
                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((genstat.logis) + to_decimal(genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])) / to_decimal(exrate.betrag) )


            else:
                cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])
                cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(genstat.res_deci[4])
                cust_list.argtumsatz =  to_decimal(cust_list.argtumsatz) + to_decimal(genstat.logis)
                cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] +\
                    genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])

            if genstat.resstatus != 13:
                cust_list.logiernachte = cust_list.logiernachte + 1

            if excl_other == False:

                if curr_resnr != genstat.resnr or curr_reslinnr != genstat.res_int[0]:
                    curr_resnr = genstat.resnr
                    curr_reslinnr = genstat.res_int[0]

                    for bill in db_session.query(Bill).filter(
                             (Bill.resnr == genstat.resnr) & (Bill.reslinnr == genstat.res_int[0])).order_by(Bill._recid).all():

                        bill_line_obj_list = {}
                        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & (Artikel.artart == 0)).filter(
                                 (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum == genstat.datum)).order_by(Bill_line._recid).all():
                            if bill_line_obj_list.get(bill_line._recid):
                                continue
                            else:
                                bill_line_obj_list[bill_line._recid] = True


                            service =  to_decimal("0")
                            vat =  to_decimal("0")


                            service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

                            if currency != "":

                                exrate = get_cache (exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                if exrate:
                                    cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(((bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )


                            else:
                                cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )
                                cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )

        if excl_other == False:

            for guest_queasy in db_session.query(Guest_queasy).filter(
                     (Guest_queasy.key == ("gast-info").lower()) & (Guest_queasy.date1 >= fdate) & (Guest_queasy.date1 <= tdate)).order_by(Guest_queasy.number2).all():

                genstat = get_cache (Genstat, {"resnr": [(eq, guest_queasy.number2)],"res_int[0]": [(eq, guest_queasy.number3)],"datum": [(eq, guest_queasy.date1)],"res_logic[1]": [(eq, True)]})

                if genstat:

                    cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == genstat.gastnr), first=True)

                    if cust_list:
                        for loopj in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                            if entry(loopj - 1, cust_list.resnr, ";") == to_string(genstat.resnr):
                                found_it = True


                                break
                            else:
                                found_it = False

                        if found_it :

                            h_bill_line_obj_list = {}
                            for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                                     (H_bill_line.rechnr == to_int(guest_queasy.char1)) & (H_bill_line.departement == guest_queasy.number1)).order_by(H_bill_line._recid).all():
                                if h_bill_line_obj_list.get(h_bill_line._recid):
                                    continue
                                else:
                                    h_bill_line_obj_list[h_bill_line._recid] = True


                                service =  to_decimal("0")
                                vat =  to_decimal("0")


                                service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, guest_queasy.date1))

                                if currency != " ":

                                    exrate = get_cache (exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                    if exrate:
                                        cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal((((guest_queasy.deci1) + to_decimal(guest_queasy.deci2)) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(((guest_queasy.deci3) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal((((guest_queasy.deci1) + to_decimal(guest_queasy.deci2) + to_decimal(guest_queasy.deci3)) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )


                                else:
                                    cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(((guest_queasy.deci1) + to_decimal(guest_queasy.deci2)) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )
                                    cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal((guest_queasy.deci3) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )
                                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((guest_queasy.deci1) + to_decimal(guest_queasy.deci2) + to_decimal(guest_queasy.deci3)) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )

        for cust_list2 in query(cust_list2_data, sort_by=[("gesamtumsatz",True),("logiernachte",True),("cust_name",False)]):
            cust_list = Cust_list()
            cust_list_data.append(cust_list)

            buffer_copy(cust_list2, cust_list)

        t_genstat_obj_list = {}
        t_genstat = Genstat()
        guest = Guest()
        for t_genstat.datum, t_genstat.logis, t_genstat.res_deci, t_genstat.resnr, t_genstat.res_int, t_genstat.gastnr, t_genstat.resstatus, t_genstat._recid, guest.name, guest.vorname1, guest.anrede1, guest.gastnr, guest.wohnort, guest.plz, guest.land, guest.phonetik3, guest._recid in db_session.query(T_genstat.datum, T_genstat.logis, T_genstat.res_deci, T_genstat.resnr, T_genstat.res_int, T_genstat.gastnr, T_genstat.resstatus, T_genstat._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.gastnr, Guest.wohnort, Guest.plz, Guest.land, Guest.phonetik3, Guest._recid).join(Guest,(Guest.gastnr == T_genstat.gastnr)).filter(
                 (T_genstat.datum >= fdate) & (T_genstat.datum <= tdate) & (T_genstat.res_deci[inc_value(6)] != 0)).order_by(T_genstat._recid).all():
            if t_genstat_obj_list.get(t_genstat._recid):
                continue
            else:
                t_genstat_obj_list[t_genstat._recid] = True

            cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == t_genstat.gastnr), first=True)

            if cust_list:

                if currency != " ":

                    exrate = get_cache (exrate, {"datum": [(eq, t_genstat.datum)],"artnr": [(eq, exratenr)]})

                    if exrate:
                        cust_list.ba_umsatz =  to_decimal(cust_list.ba_umsatz) + to_decimal((t_genstat.res_deci[6]) / to_decimal(exrate.betrag) )
                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal((t_genstat.res_deci[6]) / to_decimal(exrate.betrag) )


                else:
                    cust_list.ba_umsatz =  to_decimal(cust_list.ba_umsatz) + to_decimal(t_genstat.res_deci[6])
                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(t_genstat.res_deci[6])


            else:
                cust_list = Cust_list()
                cust_list_data.append(cust_list)

                cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)
                cust_list.gastnr = guest.gastnr
                cust_list.wohnort = guest.wohnort
                cust_list.plz = guest.plz
                cust_list.land = guest.land
                cust_list.sales_id = guest.phonetik3

                if currency != " ":

                    exrate = get_cache (exrate, {"datum": [(eq, t_genstat.datum)],"artnr": [(eq, exratenr)]})

                    if exrate:
                        cust_list.ba_umsatz = ( to_decimal(t_genstat.res_deci[6]) / to_decimal(exrate.betrag) )
                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal((t_genstat.res_deci[6]) / to_decimal(exrate.betrag) )


                else:
                    cust_list.ba_umsatz =  to_decimal(t_genstat.res_deci[6])
                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(t_genstat.res_deci[6])

                nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                if nation:

                    queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                    if queasy:
                        cust_list.region = queasy.char1
                else:
                    cust_list.region = "UNKNOWN"

    htparam = get_cache (Htparam, {"paramnr": [(eq, 125)]})

    if htparam:
        bfast_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate

    if currency != "":

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, currency)]})

        if waehrung:
            exratenr = waehrung.waehrungsnr
            exrate =  to_decimal(waehrung.ankauf)


    cust_list_data.clear()

    if cardtype == 3:

        if not check_ftd:

            genstat_obj_list = {}
            genstat = Genstat()
            guest = Guest()
            for genstat.datum, genstat.logis, genstat.res_deci, genstat.resnr, genstat.res_int, genstat.gastnr, genstat.resstatus, genstat._recid, guest.name, guest.vorname1, guest.anrede1, guest.gastnr, guest.wohnort, guest.plz, guest.land, guest.phonetik3, guest._recid in db_session.query(Genstat.datum, Genstat.logis, Genstat.res_deci, Genstat.resnr, Genstat.res_int, Genstat.gastnr, Genstat.resstatus, Genstat._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.gastnr, Guest.wohnort, Guest.plz, Guest.land, Guest.phonetik3, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                     (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.gesamtumsatz.desc(), Guest.logiernachte.desc(), Guest.name).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == guest.gastnr), first=True)

                if not cust_list:
                    cust_list = Cust_list()
                    cust_list_data.append(cust_list)

                    cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                            guest.anredefirma)
                    cust_list.gastnr = guest.gastnr
                    cust_list.wohnort = guest.wohnort
                    cust_list.plz = guest.plz
                    cust_list.land = guest.land
                    cust_list.sales_id = guest.phonetik3

                    nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                    if nation:

                        queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                        if queasy:
                            cust_list.region = queasy.char1
                    else:
                        cust_list.region = "UNKOWN"

                artikel = get_cache (Artikel, {"zwkum": [(eq, bfast_art)]})

                if artikel:
                    service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

                if currency != " ":

                    exrate = get_cache (exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                    if exrate:
                        cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])) / to_decimal(exrate.betrag) )
                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal((genstat.res_deci[4]) / to_decimal(exrate.betrag) )
                        cust_list.argtumsatz =  to_decimal(cust_list.argtumsatz) + to_decimal((genstat.logis) / to_decimal(exrate.betrag) )
                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((genstat.logis) + to_decimal(genstat.res_deci[1] +\
                                genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])) / to_decimal(exrate.betrag) )
                        cust_list.logiernachte = cust_list.logiernachte + 1


                else:
                    cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])
                    cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(genstat.res_deci[4])
                    cust_list.argtumsatz =  to_decimal(cust_list.argtumsatz) + to_decimal(genstat.logis)
                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    cust_list.logiernachte = cust_list.logiernachte + 1

                if excl_other == False:

                    if curr_resnr2 != genstat.resnr or curr_reslinnr2 != genstat.res_int[0]:
                        curr_resnr2 = genstat.resnr
                        curr_reslinnr2 = genstat.res_int[0]

                        for bill in db_session.query(Bill).filter(
                                 (Bill.resnr == genstat.resnr) & (Bill.reslinnr == genstat.res_int[0])).order_by(Bill._recid).all():

                            bill_line_obj_list = {}
                            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & (Artikel.artart == 0)).filter(
                                     (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum == genstat.datum)).order_by(Bill_line._recid).all():
                                if bill_line_obj_list.get(bill_line._recid):
                                    continue
                                else:
                                    bill_line_obj_list[bill_line._recid] = True


                                service =  to_decimal("0")
                                vat =  to_decimal("0")


                                service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

                                if currency != "":

                                    exrate = get_cache (exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                    if exrate:
                                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(((bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )


                                else:
                                    cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )
                                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )

            if excl_other == False:

                for guest_queasy in db_session.query(Guest_queasy).filter(
                         (Guest_queasy.key == ("gast-info").lower()) & (Guest_queasy.date1 >= fdate) & (Guest_queasy.date1 <= tdate)).order_by(Guest_queasy._recid).all():

                    genstat = get_cache (Genstat, {"resnr": [(eq, guest_queasy.number2)],"res_int[0]": [(eq, guest_queasy.number3)],"datum": [(eq, guest_queasy.date1)],"res_logic[1]": [(eq, True)]})

                    if genstat:

                        cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == genstat.gastnr), first=True)

                        if cust_list:
                            for loopj in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                                if entry(loopj - 1, cust_list.resnr, ";") == to_string(genstat.resnr):
                                    found_it = True


                                    break
                                else:
                                    found_it = False

                            if found_it :

                                h_bill_line_obj_list = {}
                                for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                                         (H_bill_line.rechnr == to_int(guest_queasy.char1)) & (H_bill_line.departement == guest_queasy.number1)).order_by(H_bill_line._recid).all():
                                    if h_bill_line_obj_list.get(h_bill_line._recid):
                                        continue
                                    else:
                                        h_bill_line_obj_list[h_bill_line._recid] = True


                                    service =  to_decimal("0")
                                    vat =  to_decimal("0")


                                    service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, guest_queasy.date1))

                                    if currency != " ":

                                        exrate = get_cache (exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                        if exrate:
                                            cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal((((guest_queasy.deci1) + to_decimal(guest_queasy.deci2)) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                            cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(((guest_queasy.deci3) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                            cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal((((guest_queasy.deci1) + to_decimal(guest_queasy.deci2) + to_decimal(guest_queasy.deci3)) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )


                                    else:
                                        cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(((guest_queasy.deci1) + to_decimal(guest_queasy.deci2)) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )
                                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal((guest_queasy.deci3) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )
                                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((guest_queasy.deci1) + to_decimal(guest_queasy.deci2) + to_decimal(guest_queasy.deci3)) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )

            t_genstat_obj_list = {}
            t_genstat = Genstat()
            guest = Guest()
            for t_genstat.datum, t_genstat.logis, t_genstat.res_deci, t_genstat.resnr, t_genstat.res_int, t_genstat.gastnr, t_genstat.resstatus, t_genstat._recid, guest.name, guest.vorname1, guest.anrede1, guest.gastnr, guest.wohnort, guest.plz, guest.land, guest.phonetik3, guest._recid in db_session.query(T_genstat.datum, T_genstat.logis, T_genstat.res_deci, T_genstat.resnr, T_genstat.res_int, T_genstat.gastnr, T_genstat.resstatus, T_genstat._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.gastnr, Guest.wohnort, Guest.plz, Guest.land, Guest.phonetik3, Guest._recid).join(Guest,(Guest.gastnr == T_genstat.gastnr)).filter(
                     (T_genstat.datum >= fdate) & (T_genstat.datum <= tdate) & (T_genstat.res_deci[inc_value(6)] != 0)).order_by(Guest.gesamtumsatz.desc(), Guest.logiernachte.desc(), Guest.name).all():
                if t_genstat_obj_list.get(t_genstat._recid):
                    continue
                else:
                    t_genstat_obj_list[t_genstat._recid] = True

                cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == t_genstat.gastnr), first=True)

                if cust_list:

                    if currency != "":

                        exrate = get_cache (exrate, {"datum": [(eq, t_genstat.datum)],"artnr": [(eq, exratenr)]})

                        if exrate:
                            cust_list.ba_umsatz =  to_decimal(t_genstat.res_deci[6]) / to_decimal(exrate.betrag)
                            cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal((t_genstat.res_deci[6]) / to_decimal(exrate.betrag) )


                    else:
                        cust_list.ba_umsatz =  to_decimal(cust_list.ba_umsatz) + to_decimal(t_genstat.res_deci[6])
                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(t_genstat.res_deci[6])


                else:
                    cust_list = Cust_list()
                    cust_list_data.append(cust_list)

                    cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                            guest.anredefirm)
                    cust_list.gastnr = guest.gastnr
                    cust_list.wohnort = guest.wohnort
                    cust_list.plz = guest.plz
                    cust_list.land = guest.land
                    cust_list.sales_id = guest.phonetik3

                    if currency != " ":

                        exrate = get_cache (exrate, {"datum": [(eq, t_genstat.datum)],"artnr": [(eq, exratenr)]})

                        if exrate:
                            cust_list.ba_umsatz =  to_decimal(t_genstat.res_deci[6]) / to_decimal(exrate.betrag)
                            cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal((t_genstat.res_deci[6]) / to_decimal(exrate.betrag) )


                    else:
                        cust_list.ba_umsatz =  to_decimal(t_genstat.res_deci[6])
                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(t_genstat.res_deci[6])

                    nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                    if nation:

                        queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

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

            genstat_obj_list = {}
            genstat = Genstat()
            guest = Guest()
            for genstat.datum, genstat.logis, genstat.res_deci, genstat.resnr, genstat.res_int, genstat.gastnr, genstat.resstatus, genstat._recid, guest.name, guest.vorname1, guest.anrede1, guest.gastnr, guest.wohnort, guest.plz, guest.land, guest.phonetik3, guest._recid in db_session.query(Genstat.datum, Genstat.logis, Genstat.res_deci, Genstat.resnr, Genstat.res_int, Genstat.gastnr, Genstat.resstatus, Genstat._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.gastnr, Guest.wohnort, Guest.plz, Guest.land, Guest.phonetik3, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                     (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Guest.gesamtumsatz.desc(), Guest.logiernachte.desc(), Guest.name).all():
                if genstat_obj_list.get(genstat._recid):
                    continue
                else:
                    genstat_obj_list[genstat._recid] = True

                cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == guest.gastnr), first=True)

                if not cust_list:
                    cust_list = Cust_list()
                    cust_list_data.append(cust_list)

                    cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                            guest.anredefirm)
                    cust_list.gastnr = guest.gastnr
                    cust_list.wohnort = guest.wohnort
                    cust_list.plz = guest.plz
                    cust_list.land = guest.land
                    cust_list.sales_id = guest.phonetik3

                    nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                    if nation:

                        queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                        if queasy:
                            cust_list.region = queasy.char1
                    else:
                        cust_list.region = "UNKOWN"

                artikel = get_cache (Artikel, {"zwkum": [(eq, bfast_art)]})

                if artikel:
                    service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

                if currency != " ":

                    exrate = get_cache (exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                    if exrate:
                        cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])) / to_decimal(exrate.betrag) )
                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal((genstat.res_deci[4]) / to_decimal(exrate.betrag) )
                        cust_list.argtumsatz =  to_decimal(cust_list.argtumsatz) + to_decimal((genstat.logis) / to_decimal(exrate.betrag) )
                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((genstat.logis) + to_decimal(genstat.res_deci[1] +\
                                genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])) / to_decimal(exrate.betrag) )
                        cust_list.logiernachte = cust_list.logiernachte + 1


                else:
                    cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])
                    cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(genstat.res_deci[4])
                    cust_list.argtumsatz =  to_decimal(cust_list.argtumsatz) + to_decimal(genstat.logis)
                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
                    cust_list.logiernachte = cust_list.logiernachte + 1

                if excl_other == False:

                    if curr_resnr1 != genstat.resnr or curr_reslinnr1 != genstat.res_int[0]:
                        curr_resnr1 = genstat.resnr
                        curr_reslinnr1 = genstat.res_int[0]

                        for bill in db_session.query(Bill).filter(
                                 (Bill.resnr == genstat.resnr) & (Bill.reslinnr == genstat.res_int[0])).order_by(Bill._recid).all():

                            bill_line_obj_list = {}
                            for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & (Artikel.artart == 0)).filter(
                                     (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum == genstat.datum)).order_by(Bill_line._recid).all():
                                if bill_line_obj_list.get(bill_line._recid):
                                    continue
                                else:
                                    bill_line_obj_list[bill_line._recid] = True


                                service =  to_decimal("0")
                                vat =  to_decimal("0")


                                service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

                                if currency != "":

                                    exrate = get_cache (exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                    if exrate:
                                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(((bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )


                                else:
                                    cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )
                                    cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(bill_line.betrag) / to_decimal((1) + to_decimal(service) + to_decimal(vat) )

            if excl_other == False:

                for guest_queasy in db_session.query(Guest_queasy).filter(
                         (Guest_queasy.key == ("gast-info").lower()) & (Guest_queasy.date1 >= fdate) & (Guest_queasy.date1 <= tdate)).order_by(Guest_queasy._recid).all():

                    genstat = get_cache (Genstat, {"resnr": [(eq, guest_queasy.number2)],"res_int[0]": [(eq, guest_queasy.number3)],"datum": [(eq, guest_queasy.date1)],"res_logic[1]": [(eq, True)]})

                    if genstat:

                        cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == genstat.gastnr), first=True)

                        if cust_list:
                            for loopj in range(1,num_entries(cust_list.resnr, ";")  + 1) :

                                if entry(loopj - 1, cust_list.resnr, ";") == to_string(genstat.resnr):
                                    found_it = True


                                    break
                                else:
                                    found_it = False

                            if found_it :

                                h_bill_line_obj_list = {}
                                for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                                         (H_bill_line.rechnr == to_int(guest_queasy.char1)) & (H_bill_line.departement == guest_queasy.number1)).order_by(H_bill_line._recid).all():
                                    if h_bill_line_obj_list.get(h_bill_line._recid):
                                        continue
                                    else:
                                        h_bill_line_obj_list[h_bill_line._recid] = True


                                    service =  to_decimal("0")
                                    vat =  to_decimal("0")


                                    service, vat, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, guest_queasy.date1))

                                    if currency != " ":

                                        exrate = get_cache (exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                        if exrate:
                                            cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal((((guest_queasy.deci1) + to_decimal(guest_queasy.deci2)) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                            cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal(((guest_queasy.deci3) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )
                                            cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal((((guest_queasy.deci1) + to_decimal(guest_queasy.deci2) + to_decimal(guest_queasy.deci3)) / to_decimal((1) + to_decimal(service) + to_decimal(vat))) / to_decimal(exrate.betrag) )


                                    else:
                                        cust_list.f_b_umsatz =  to_decimal(cust_list.f_b_umsatz) + to_decimal(((guest_queasy.deci1) + to_decimal(guest_queasy.deci2)) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )
                                        cust_list.sonst_umsatz =  to_decimal(cust_list.sonst_umsatz) + to_decimal((guest_queasy.deci3) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )
                                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(((guest_queasy.deci1) + to_decimal(guest_queasy.deci2) + to_decimal(guest_queasy.deci3)) / to_decimal((1) + to_decimal(service) + to_decimal(vat)) )

            t_genstat_obj_list = {}
            t_genstat = Genstat()
            guest = Guest()
            for t_genstat.datum, t_genstat.logis, t_genstat.res_deci, t_genstat.resnr, t_genstat.res_int, t_genstat.gastnr, t_genstat.resstatus, t_genstat._recid, guest.name, guest.vorname1, guest.anrede1, guest.gastnr, guest.wohnort, guest.plz, guest.land, guest.phonetik3, guest._recid in db_session.query(T_genstat.datum, T_genstat.logis, T_genstat.res_deci, T_genstat.resnr, T_genstat.res_int, T_genstat.gastnr, T_genstat.resstatus, T_genstat._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.gastnr, Guest.wohnort, Guest.plz, Guest.land, Guest.phonetik3, Guest._recid).join(Guest,(Guest.gastnr == T_genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                     (T_genstat.datum >= fdate) & (T_genstat.datum <= tdate) & (T_genstat.res_deci[inc_value(6)] != 0)).order_by(Guest.gesamtumsatz.desc(), Guest.logiernachte.desc(), Guest.name).all():
                if t_genstat_obj_list.get(t_genstat._recid):
                    continue
                else:
                    t_genstat_obj_list[t_genstat._recid] = True

                cust_list = query(cust_list_data, filters=(lambda cust_list: cust_list.gastnr == t_genstat.gastnr), first=True)

                if cust_list:

                    if currency != " ":

                        exrate = get_cache (exrate, {"datum": [(eq, t_genstat.datum)],"artnr": [(eq, exratenr)]})

                        if exrate:
                            cust_list.ba_umsatz =  to_decimal(cust_list.ba_umsatz) + to_decimal((t_genstat.res_deci[6]) / to_decimal(exrate.betrag) )
                            cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal((t_genstat.res_deci[6]) / to_decimal(exrate.betrag) )


                    else:
                        cust_list.ba_umsatz =  to_decimal(cust_list.ba_umsatz) + to_decimal(t_genstat.res_deci[6])
                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(t_genstat.res_deci[6])


                else:
                    cust_list = Cust_list()
                    cust_list_data.append(cust_list)

                    cust_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                            guest.anredefirm)
                    cust_list.gastnr = guest.gastnr
                    cust_list.wohnort = guest.wohnort
                    cust_list.plz = guest.plz
                    cust_list.land = guest.land
                    cust_list.sales_id = guest.phonetik3

                    if currency != " ":

                        exrate = get_cache (exrate, {"datum": [(eq, t_genstat.datum)],"artnr": [(eq, exratenr)]})

                        if exrate:
                            cust_list.ba_umsatz = ( to_decimal(t_genstat.res_deci[6]) / to_decimal(exrate.betrag) )
                            cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal((t_genstat.res_deci[6]) / to_decimal(exrate.betrag) )


                    else:
                        cust_list.ba_umsatz =  to_decimal(t_genstat.res_deci[6])
                        cust_list.gesamtumsatz =  to_decimal(cust_list.gesamtumsatz) + to_decimal(t_genstat.res_deci[6])

                    nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                    if nation:

                        queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                        if queasy:
                            cust_list.region = queasy.char1
                    else:
                        cust_list.region = "UNKNOWN"
        else:
            cr_ftd()

        if tdate != None and tdate >= ci_date and check_ftd:
            create_forecast()

    return generate_output()