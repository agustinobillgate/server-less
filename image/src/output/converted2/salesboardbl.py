#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_room_breakdown import get_room_breakdown
from models import Htparam, Guest, Guestseg, Segment, Genstat, Reservation, Res_line

def salesboardbl(fdate:date, curr_task:int):

    prepare_cache ([Htparam, Guest, Guestseg, Segment, Genstat, Res_line])

    month_list_list = []
    tguest_list = []
    mtd_list_list = []
    year_list_list = []
    fdate1:date = None
    first_day:date = None
    frdate:date = None
    todate:date = None
    date1:date = None
    date2:date = None
    startdate:date = None
    enddate:date = None
    ci_date:date = None
    dummy_indv:int = 0
    dummy_walkin:int = 0
    bfast_art:int = 0
    service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    htparam = guest = guestseg = segment = genstat = reservation = res_line = None

    month_list = mtd_list = tguest = reslist = year_list = None

    month_list_list, Month_list = create_model("Month_list", {"gastnr":int, "name":string, "occ":int, "rmrev":Decimal, "fbrev":Decimal, "otherrev":Decimal})
    mtd_list_list, Mtd_list = create_model_like(Month_list)
    tguest_list, Tguest = create_model("Tguest", {"gastnr":int, "name":string, "adresse1":string, "adresse2":string, "wohnort":string, "plz":string, "land":string, "telefon":string, "segment1":string})
    reslist_list, Reslist = create_model("Reslist", {"gastnr":int, "name":string, "rnight":int, "rrev":Decimal, "datum":date})
    year_list_list, Year_list = create_model("Year_list", {"gastnr":int, "name":string, "rnight":int, "rrev":Decimal, "curr_month":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal month_list_list, tguest_list, mtd_list_list, year_list_list, fdate1, first_day, frdate, todate, date1, date2, startdate, enddate, ci_date, dummy_indv, dummy_walkin, bfast_art, service, vat, htparam, guest, guestseg, segment, genstat, reservation, res_line
        nonlocal fdate, curr_task


        nonlocal month_list, mtd_list, tguest, reslist, year_list
        nonlocal month_list_list, mtd_list_list, tguest_list, reslist_list, year_list_list

        return {"month-list": month_list_list, "tguest": tguest_list, "mtd-list": mtd_list_list, "year-list": year_list_list}

    def create_genstat(date1:date, date2:date):

        nonlocal month_list_list, tguest_list, mtd_list_list, year_list_list, fdate1, first_day, frdate, todate, startdate, enddate, ci_date, dummy_indv, dummy_walkin, bfast_art, service, vat, htparam, guest, guestseg, segment, genstat, reservation, res_line
        nonlocal fdate, curr_task


        nonlocal month_list, mtd_list, tguest, reslist, year_list
        nonlocal month_list_list, mtd_list_list, tguest_list, reslist_list, year_list_list

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.datum, genstat.gastnr, genstat.logis, genstat.res_deci, genstat.gratis, genstat._recid, guest.name, guest.anredefirma, guest.gastnr, guest.adresse1, guest.adresse2, guest.adresse3, guest.wohnort, guest.plz, guest.land, guest.telefon, guest._recid in db_session.query(Genstat.datum, Genstat.gastnr, Genstat.logis, Genstat.res_deci, Genstat.gratis, Genstat._recid, Guest.name, Guest.anredefirma, Guest.gastnr, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.wohnort, Guest.plz, Guest.land, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr) & ((Guest.karteityp == 1) | (Guest.karteityp == 2))).filter(
                 (Genstat.datum >= date1) & (Genstat.datum <= date2) & (Genstat.gastnr > 0) & (Genstat.zinr != "") & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.res_logic[inc_value(1)]) & (Genstat.resstatus != 13)).order_by(Genstat._recid).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            year_list = query(year_list_list, filters=(lambda year_list: year_list.curr_month == get_month(genstat.datum) and year_list.gastnr == genstat.gastnr), first=True)

            if not year_list:
                year_list = Year_list()
                year_list_list.append(year_list)

                year_list.curr_month = get_month(genstat.datum)
                year_list.gastnr = genstat.gastnr
                year_list.name = guest.name + " " + guest.anredefirma
                year_list.rnight = year_list.rnight + 1

                if genstat.gratis == 0:
                    year_list.rrev =  to_decimal(year_list.rrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])
            else:
                year_list.rnight = year_list.rnight + 1

            if genstat.gratis == 0:
                year_list.rrev =  to_decimal(year_list.rrev) + to_decimal(genstat.logis) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4])


    def create_rline(date1:date, date2:date):

        nonlocal month_list_list, tguest_list, mtd_list_list, year_list_list, fdate1, first_day, frdate, todate, startdate, enddate, ci_date, dummy_indv, dummy_walkin, bfast_art, service, vat, htparam, guest, guestseg, segment, genstat, reservation, res_line
        nonlocal fdate, curr_task


        nonlocal month_list, mtd_list, tguest, reslist, year_list
        nonlocal month_list_list, mtd_list_list, tguest_list, reslist_list, year_list_list

        dat1:date = None
        dat2:date = None
        datum:date = None
        curr_i:int = 0
        net_lodg:Decimal = to_decimal("0.0")
        fnet_lodg:Decimal = to_decimal("0.0")
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")

        res_line_obj_list = {}
        for res_line, reservation, guest in db_session.query(Res_line, Reservation, Guest).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Res_line.gastnr) & ((Guest.karteityp == 1) | (Guest.karteityp == 2))).filter(
                 ((Res_line.resstatus <= 6) & (Res_line.resstatus != 4) & (Res_line.resstatus != 3) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.active_flag <= 1) & (not_ (Res_line.ankunft > date2)) & (not_ (Res_line.abreise < date1))) | ((Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr, Res_line.reslinnr.desc()).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True


            dat1 = date1

            if res_line.ankunft > dat1:
                dat1 = res_line.ankunft

            if res_line.abreise == res_line.ankunft:
                dat2 = res_line.abreise
            else:
                dat2 = res_line.abreise - timedelta(days=1)

            if dat2 > date2:
                dat2 = date2
            curr_i = 0
            for datum in date_range(dat1,dat2) :
                curr_i = curr_i + 1

                year_list = query(year_list_list, filters=(lambda year_list: year_list.curr_month == get_month(datum) and year_list.gastnr == res_line.gastnr), first=True)

                if not year_list:
                    year_list = Year_list()
                    year_list_list.append(year_list)

                    year_list.curr_month = get_month(datum)
                    year_list.gastnr = res_line.gastnr
                    year_list.name = guest.name + " " + guest.anredefirma

                    if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                        year_list.rnight = year_list.rnight + res_line.zimmeranz

                    if res_line.zipreis != 0:
                        fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, ci_date))
                        year_list.rrev =  to_decimal(year_list.rrev) + to_decimal(net_lodg) + to_decimal(tot_breakfast) + to_decimal(tot_lunch) + to_decimal(tot_dinner) + to_decimal(tot_other)
                else:

                    if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                        year_list.rnight = year_list.rnight + res_line.zimmeranz

                    if res_line.zipreis != 0:
                        fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, ci_date))
                        year_list.rrev =  to_decimal(year_list.rrev) + to_decimal(net_lodg) + to_decimal(tot_breakfast) + to_decimal(tot_lunch) + to_decimal(tot_dinner) + to_decimal(tot_other)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 109)]})
    dummy_walkin = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 123)]})
    dummy_indv = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 125)]})
    bfast_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if curr_task == 0:
        fdate1 = fdate - timedelta(days=1)

    elif curr_task == 1:
        fdate1 = fdate

    for guest in db_session.query(Guest).filter(
             ((Guest.karteityp == 1) | (Guest.karteityp == 2)) & (Guest.anlage_datum == fdate1)).order_by(Guest._recid).all():
        tguest = Tguest()
        tguest_list.append(tguest)

        tguest.gastnr = guest.gastnr
        tguest.name = guest.name + " " + guest.anredefirma
        tguest.adresse1 = guest.adresse1
        tguest.adresse2 = guest.adresse2 + " " + guest.adresse3
        tguest.wohnort = guest.wohnort
        tguest.plz = guest.plz
        tguest.land = guest.land
        tguest.telefon = guest.telefon

        guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})

        if guestseg:

            segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

            if segment:
                tguest.segment1 = entry(0, segment.bezeich, "$$0")
    frdate = date_mdy(get_month(fdate1) , 1, get_year(fdate1))
    enddate = date_mdy(12, 31, get_year(fdate1))
    todate = fdate1

    genstat_obj_list = {}
    genstat = Genstat()
    guest = Guest()
    for genstat.datum, genstat.gastnr, genstat.logis, genstat.res_deci, genstat.gratis, genstat._recid, guest.name, guest.anredefirma, guest.gastnr, guest.adresse1, guest.adresse2, guest.adresse3, guest.wohnort, guest.plz, guest.land, guest.telefon, guest._recid in db_session.query(Genstat.datum, Genstat.gastnr, Genstat.logis, Genstat.res_deci, Genstat.gratis, Genstat._recid, Guest.name, Guest.anredefirma, Guest.gastnr, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.wohnort, Guest.plz, Guest.land, Guest.telefon, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr) & ((Guest.karteityp == 1) | (Guest.karteityp == 2))).filter(
                 (Genstat.datum >= frdate) & (Genstat.datum <= todate) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)]) & (Genstat.resstatus != 13)).order_by(Genstat._recid).all():
        if genstat_obj_list.get(genstat._recid):
            continue
        else:
            genstat_obj_list[genstat._recid] = True

        mtd_list = query(mtd_list_list, filters=(lambda mtd_list: mtd_list.gastnr == genstat.gastnr), first=True)

        if not mtd_list:
            mtd_list = Mtd_list()
            mtd_list_list.append(mtd_list)

            mtd_list.gastnr = genstat.gastnr
            mtd_list.name = guest.name + " " + guest.anredefirma


        mtd_list.occ = mtd_list.occ + 1
        mtd_list.rmrev =  to_decimal(mtd_list.rmrev) + to_decimal(genstat.logis)


        mtd_list.fbrev =  to_decimal(mtd_list.fbrev) + to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])


        mtd_list.otherrev =  to_decimal(mtd_list.otherrev) + to_decimal(genstat.res_deci[4])
    create_rline(ci_date, enddate)

    return generate_output()