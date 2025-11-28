#using conversion tools version: 1.0.0.117
#-----------------------------------------------------------
# Manual Update: exrate variable -> eexrate, Rd 16-July-25
# Rd, 28/11/2025, with_for_update added
#-----------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.get_room_breakdown import get_room_breakdown
from models import Genstat, Guest, Bill_line, Bill, Htparam, Waehrung, Nation, Queasy, Exrate, Res_line, Artikel, Guest_queasy, H_artikel, H_bill_line, Reservation, Sourccod, Segment, Arrangement, Zimmer

def cust_turnover_sorting_detail_cldbl(cardtype:int, sort_type:int, fdate:date, tdate:date, check_ftd:bool, currency:string, excl_other:bool, curr_sort2:int):

    prepare_cache ([Genstat, Guest, Htparam, Waehrung, Nation, Queasy, Exrate, Res_line, Artikel, Guest_queasy, Reservation, Arrangement])

    b_list_data = []
    bfast_art:int = 0
    lunch_art:int = 0
    dinner_art:int = 0
    lundin_art:int = 0
    service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
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
    curr_gname:string = ""
    curr_gastnr2:int = 0
    t_logiernachte:Decimal = to_decimal("0.0")
    t_argtumsatz:Decimal = to_decimal("0.0")
    t_fb_umsatz:Decimal = to_decimal("0.0")
    t_sonst_umsatz:Decimal = to_decimal("0.0")
    t_ba_umsatz:Decimal = to_decimal("0.0")
    t_gesamtumsatz:Decimal = to_decimal("0.0")
    t_lyear:Decimal = to_decimal("0.0")
    t_nofrm:Decimal = to_decimal("0.0")
    tot_logiernachte:Decimal = to_decimal("0.0")
    tot_argtumsatz:Decimal = to_decimal("0.0")
    tot_fb_umsatz:Decimal = to_decimal("0.0")
    tot_sonst_umsatz:Decimal = to_decimal("0.0")
    tot_ba_umsatz:Decimal = to_decimal("0.0")
    tot_gesamtumsatz:Decimal = to_decimal("0.0")
    tot_stayno:Decimal = to_decimal("0.0")
    tot_lyear:Decimal = to_decimal("0.0")
    tot_nofrm:Decimal = to_decimal("0.0")
    gt_logiernachte:Decimal = to_decimal("0.0")
    gt_argtumsatz:Decimal = to_decimal("0.0")
    gt_fb_umsatz:Decimal = to_decimal("0.0")
    gt_sonst_umsatz:Decimal = to_decimal("0.0")
    gt_ba_umsatz:Decimal = to_decimal("0.0")
    gt_gesamtumsatz:Decimal = to_decimal("0.0")
    gt_stayno:Decimal = to_decimal("0.0")
    gt_lyear:Decimal = to_decimal("0.0")
    gt_nofrm:Decimal = to_decimal("0.0")
    curr_resnr1:int = 0
    curr_reslinnr1:int = 0
    found1:bool = False
    loopj:int = 0
    exratenr:int = 0
    eexrate:Decimal = to_decimal("0.0")
    service2:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    vat22:Decimal = to_decimal("0.0")
    fact1:Decimal = to_decimal("0.0")
    genstat = guest = bill_line = bill = htparam = waehrung = nation = queasy = exrate = res_line = artikel = guest_queasy = h_artikel = h_bill_line = reservation = sourccod = segment = arrangement = zimmer = None

    cust_list_detail = b_list = t_genstat = blist = glist = bguest = clist = bline = bbuf = clist = clist = None

    cust_list_detail_data, Cust_list_detail = create_model("Cust_list_detail", {"gastnr":int, "cust_name":string, "gname":string, "gesamtumsatz":string, "logiernachte":string, "argtumsatz":string, "f_b_umsatz":string, "sonst_umsatz":string, "wohnort":string, "plz":string, "land":string, "sales_id":string, "ba_umsatz":string, "ly_rev":string, "region":string, "region1":string, "stayno":string, "resnr":string, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int, "count_room":string, "rm_sharer":string, "arrival":date, "depart":date, "gastnrmember":int})
    b_list_data, B_list = create_model("B_list", {"gastnr":int, "cust_name":string, "gname":string, "gesamtumsatz":string, "logiernachte":string, "argtumsatz":string, "f_b_umsatz":string, "sonst_umsatz":string, "wohnort":string, "plz":string, "land":string, "sales_id":string, "ba_umsatz":string, "ly_rev":string, "region":string, "region1":string, "stayno":string, "resnr":string, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int, "count_room":string, "rm_sharer":string, "arrival":date, "depart":date, "gastnrmember":int})

    T_genstat = create_buffer("T_genstat",Genstat)
    Blist = Cust_list_detail
    blist_data = cust_list_detail_data

    Glist = create_buffer("Glist",Guest)
    Bguest = create_buffer("Bguest",Guest)
    Clist = Cust_list_detail
    clist_data = cust_list_detail_data

    Bline = create_buffer("Bline",Bill_line)
    Bbuf = create_buffer("Bbuf",Bill)


    db_session = local_storage.db_session
    currency = currency.strip()

    def generate_output():
        nonlocal b_list_data, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_resnr, curr_reslinnr, curr_gname, curr_gastnr2, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, t_lyear, t_nofrm, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, tot_lyear, tot_nofrm, gt_logiernachte, gt_argtumsatz, gt_fb_umsatz, gt_sonst_umsatz, gt_ba_umsatz, gt_gesamtumsatz, gt_stayno, gt_lyear, gt_nofrm, curr_resnr1, curr_reslinnr1, found1, loopj, exratenr, eexrate, service2, vat2, vat22, fact1, genstat, guest, bill_line, bill, htparam, waehrung, nation, queasy, exrate, res_line, artikel, guest_queasy, h_artikel, h_bill_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal cardtype, sort_type, fdate, tdate, check_ftd, currency, excl_other, curr_sort2
        nonlocal t_genstat, blist, glist, bguest, clist, bline, bbuf


        nonlocal cust_list_detail, b_list, t_genstat, blist, glist, bguest, clist, bline, bbuf, clist, clist
        nonlocal cust_list_detail_data, b_list_data

        return {"curr_sort2": curr_sort2, "b-list": b_list_data}

    def create_detail():

        nonlocal b_list_data, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_resnr, curr_reslinnr, curr_gname, curr_gastnr2, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, t_lyear, t_nofrm, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, tot_lyear, tot_nofrm, gt_logiernachte, gt_argtumsatz, gt_fb_umsatz, gt_sonst_umsatz, gt_ba_umsatz, gt_gesamtumsatz, gt_stayno, gt_lyear, gt_nofrm, curr_resnr1, curr_reslinnr1, found1, loopj, exratenr, eexrate, service2, vat2, vat22, fact1, genstat, guest, bill_line, bill, htparam, waehrung, nation, queasy, exrate, res_line, artikel, guest_queasy, h_artikel, h_bill_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal cardtype, sort_type, fdate, tdate, check_ftd, currency, excl_other, curr_sort2
        nonlocal t_genstat, blist, glist, bguest, clist, bline, bbuf


        nonlocal cust_list_detail, b_list, t_genstat, blist, glist, bguest, clist, bline, bbuf, clist, clist
        nonlocal cust_list_detail_data, b_list_data

        if currency != "":

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, currency)]})

            if waehrung:
                exratenr = waehrung.waehrungsnr
                eexrate =  to_decimal(waehrung.ankauf)

        if cardtype == 3:

            if not check_ftd:

                genstat_obj_list = {}
                genstat = Genstat()
                guest = Guest()
                for genstat.gastnrmember, genstat.gastnr, genstat.resnr, genstat.res_int, genstat.res_date, genstat.datum, genstat.res_deci, genstat.logis, genstat.resstatus, genstat._recid, guest.phonetik3, guest.name, guest.anredefirma, guest.vorname1, guest.plz, guest.land, guest.wohnort, guest.anrede1, guest._recid in db_session.query(Genstat.gastnrmember, Genstat.gastnr, Genstat.resnr, Genstat.res_int, Genstat.res_date, Genstat.datum, Genstat.res_deci, Genstat.logis, Genstat.resstatus, Genstat._recid, Guest.phonetik3, Guest.name, Guest.anredefirma, Guest.vorname1, Guest.plz, Guest.land, Guest.wohnort, Guest.anrede1, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                         (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.gastnr, Guest.land, Genstat.resnr).all():
                    if genstat_obj_list.get(genstat._recid):
                        continue
                    else:
                        genstat_obj_list[genstat._recid] = True

                    bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                    cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gastnrmember == genstat.gastnrmember), first=True)

                    if not cust_list_detail:
                        cust_list_detail = Cust_list_detail()
                        cust_list_detail_data.append(cust_list_detail)

                        cust_list_detail.gastnr = genstat.gastnr
                        cust_list_detail.resno = genstat.resnr
                        cust_list_detail.reslinnr = genstat.res_int[0]
                        cust_list_detail.gname = bguest.name
                        cust_list_detail.arrival = genstat.res_date[0]
                        cust_list_detail.depart = genstat.res_date[1]
                        cust_list_detail.gastnrmember = genstat.gastnrmember

                        glist = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                        if glist:
                            cust_list_detail.cust_name = glist.name + "," + glist.anredefirma + " " + glist.vorname1
                            cust_list_detail.plz = glist.plz
                            cust_list_detail.land = glist.land
                            cust_list_detail.sales_id = glist.phonetik3
                            cust_list_detail.wohnort = glist.wohnort

                            nation = get_cache (Nation, {"kurzbez": [(eq, glist.land)]})

                            if nation:

                                queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                                if queasy:
                                    cust_list_detail.region = queasy.char1
                            else:
                                cust_list_detail.region = "UNKOWN"

                            if cust_list_detail.sales_id == "":
                                cust_list_detail.sales_id = guest.phonetik3


                        else:
                            cust_list_detail.cust_name = guest.name + "," + guest.anredefirma + " " + guest.vorname1
                            cust_list_detail.plz = guest.plz
                            cust_list_detail.land = guest.land
                            cust_list_detail.sales_id = guest.phonetik3
                            cust_list_detail.wohnort = guest.wohnort

                            nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                            if nation:

                                queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                                if queasy:
                                    cust_list_detail.region = queasy.char1
                            else:
                                cust_list_detail.region = "UNKOWN"
                    found1 = False

                    clist = query(clist_data, filters=(lambda clist: clist.gastnr == genstat.gastnr and clist.gname == bguest.NAME), first=True)

                    if clist:

                        if clist.resnr != " ":
                            for loopj in range(1,num_entries(clist.resnr, ";")  + 1) :

                                if entry(loopj - 1, clist.resnr, ";") != " ":

                                    if to_int(entry(loopj - 1, clist.resnr, ";")) == genstat.resnr:
                                        found1 = True


                                        break

                            if not found1:
                                clist.resnr = clist.resnr + to_string(genstat.resnr) + ";"

                        elif clist.resnr == " ":
                            clist.resnr = clist.resnr + to_string(genstat.resnr) + ";"

                    if currency != " ":

                        exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                        if exrate:
                            cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + ((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + (genstat.res_deci[4] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.argtumsatz = to_string(to_decimal(cust_list_detail.argtumsatz) + (genstat.logis / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + ((genstat.logis + genstat.res_deci[1] +\
                                    genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4] + genstat.res_deci[6]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.ba_umsatz = to_string(to_decimal(cust_list_detail.ba_umsatz) + (genstat.res_deci[6] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                    else:
                        cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + genstat.res_deci[4], "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.argtumsatz = to_string(to_decimal(cust_list_detail.argtumsatz) + genstat.logis, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + genstat.logis + genstat.res_deci[1] +\
                                genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4] + genstat.res_deci[6] , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.ba_umsatz = to_string(to_decimal(cust_list_detail.ba_umsatz) + genstat.res_deci[6], "->>>,>>>,>>>,>>9.99")

                    if genstat.resstatus != 13:
                        cust_list_detail.logiernachte = to_string(to_int(cust_list_detail.logiernachte) + 1, ">>>,>>9")


                    else:
                        cust_list_detail.rm_sharer = "*"

                    if curr_resnr1 != genstat.resnr or curr_reslinnr1 != genstat.res_int[0]:
                        curr_resnr1 = genstat.resnr
                        curr_reslinnr1 = genstat.res_int[0]

                        if genstat.resstatus == 6:

                            res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                            if res_line:
                                cust_list_detail.count_room = to_string(to_int(cust_list_detail.count_room) + res_line.zimmeranz, ">>,>>>,>>>,>>9")

                        if excl_other == False:

                            for bill in db_session.query(Bill).filter(
                                     (Bill.resnr == genstat.resnr) & (Bill.reslinnr == genstat.res_int[0])).order_by(Bill._recid).all():

                                bill_line_obj_list = {}
                                for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & (Artikel.artart == 0)).filter(
                                         (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum == genstat.datum)).order_by(Bill_line._recid).all():
                                    if bill_line_obj_list.get(bill_line._recid):
                                        continue
                                    else:
                                        bill_line_obj_list[bill_line._recid] = True


                                    service2 =  to_decimal("0")
                                    vat2 =  to_decimal("0")


                                    service2, vat2, vat22, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

                                    if currency != " ":

                                        exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                        if exrate:
                                            cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + ((bill_line.betrag / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                            cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + ((bill_line.betrag / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                                    else:
                                        cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + bill_line.betrag / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + bill_line.betrag / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")

                if excl_other == False:

                    for guest_queasy in db_session.query(Guest_queasy).filter(
                             (Guest_queasy.key == ("gast-info").lower()) & (Guest_queasy.date1 >= fdate) & (Guest_queasy.date1 <= tdate)).order_by(Guest_queasy._recid).all():

                        genstat = get_cache (Genstat, {"resnr": [(eq, guest_queasy.number2)],"res_int[0]": [(eq, guest_queasy.number3)],"datum": [(eq, guest_queasy.date1)],"res_logic[1]": [(eq, True)]})

                        if genstat:

                            bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                            cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gname == bguest.NAME), first=True)

                            if cust_list_detail:

                                h_bill_line_obj_list = {}
                                for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                                         (H_bill_line.rechnr == to_int(guest_queasy.char1)) & (H_bill_line.departement == guest_queasy.number1)).order_by(H_bill_line._recid).all():
                                    if h_bill_line_obj_list.get(h_bill_line._recid):
                                        continue
                                    else:
                                        h_bill_line_obj_list[h_bill_line._recid] = True


                                    service2 =  to_decimal("0")
                                    vat2 =  to_decimal("0")


                                    service2, vat2, vat22, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, guest_queasy.date1))

                                    if currency != " ":

                                        exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                        if exrate:
                                            cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                            cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + ((guest_queasy.deci3 / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                            cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + (((guest_queasy.deci1 + guest_queasy.deci2 +\
                                                guest_queasy.deci3) / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                                    else:
                                        cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (guest_queasy.deci1 + guest_queasy.deci2) / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + guest_queasy.deci3 / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + (guest_queasy.deci1 + guest_queasy.deci2 +\
                                            guest_queasy.deci3) / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")


            else:
                cr_ftd1()

            if tdate != None and tdate >= ci_date and check_ftd:
                create_forecast1()
        else:

            if not check_ftd:

                genstat_obj_list = {}
                genstat = Genstat()
                guest = Guest()
                for genstat.gastnrmember, genstat.gastnr, genstat.resnr, genstat.res_int, genstat.res_date, genstat.datum, genstat.res_deci, genstat.logis, genstat.resstatus, genstat._recid, guest.phonetik3, guest.name, guest.anredefirma, guest.vorname1, guest.plz, guest.land, guest.wohnort, guest.anrede1, guest._recid in db_session.query(Genstat.gastnrmember, Genstat.gastnr, Genstat.resnr, Genstat.res_int, Genstat.res_date, Genstat.datum, Genstat.res_deci, Genstat.logis, Genstat.resstatus, Genstat._recid, Guest.phonetik3, Guest.name, Guest.anredefirma, Guest.vorname1, Guest.plz, Guest.land, Guest.wohnort, Guest.anrede1, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                         (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.gastnr, Guest.land, Genstat.resnr).all():
                    if genstat_obj_list.get(genstat._recid):
                        continue
                    else:
                        genstat_obj_list[genstat._recid] = True

                    bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                    cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gastnrmember == genstat.gastnrmember), first=True)

                    if not cust_list_detail:
                        cust_list_detail = Cust_list_detail()
                        cust_list_detail_data.append(cust_list_detail)

                        cust_list_detail.gastnr = genstat.gastnr
                        cust_list_detail.resno = genstat.resnr
                        cust_list_detail.reslinnr = genstat.res_int[0]
                        cust_list_detail.gname = bguest.name
                        cust_list_detail.gastnrmember = genstat.gastnrmember

                        glist = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                        if glist:
                            cust_list_detail.cust_name = glist.name + "," + glist.anredefirma + " " + glist.vorname1
                            cust_list_detail.plz = glist.plz
                            cust_list_detail.land = glist.land
                            cust_list_detail.sales_id = glist.phonetik3
                            cust_list_detail.wohnort = glist.wohnort

                            nation = get_cache (Nation, {"kurzbez": [(eq, glist.land)]})

                            if nation:

                                queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                                if queasy:
                                    cust_list_detail.region = queasy.char1
                            else:
                                cust_list_detail.region = "UNKOWN"

                            if cust_list_detail.sales_id == "":
                                cust_list_detail.sales_id = guest.phonetik3


                        else:
                            cust_list_detail.cust_name = guest.name + "," + guest.anredefirma + " " + guest.vorname1
                            cust_list_detail.plz = guest.plz
                            cust_list_detail.land = guest.land
                            cust_list_detail.sales_id = guest.phonetik3
                            cust_list_detail.wohnort = guest.wohnort

                            nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                            if nation:

                                queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                                if queasy:
                                    cust_list_detail.region = queasy.char1
                            else:
                                cust_list_detail.region = "UNKOWN"
                    found1 = False

                    clist = query(clist_data, filters=(lambda clist: clist.gastnr == genstat.gastnr and clist.gname == bguest.NAME), first=True)

                    if clist:

                        if clist.resnr != " ":
                            for loopj in range(1,num_entries(clist.resnr, ";")  + 1) :

                                if entry(loopj - 1, clist.resnr, ";") != " ":

                                    if to_int(entry(loopj - 1, clist.resnr, ";")) == genstat.resnr:
                                        found1 = True


                                        break

                            if not found1:
                                clist.resnr = clist.resnr + to_string(genstat.resnr) + ";"

                        elif clist.resnr == " ":
                            clist.resnr = clist.resnr + to_string(genstat.resnr) + ";"

                    if currency != " ":

                        exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                        if exrate:
                            cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + ((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + (genstat.res_deci[4] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.argtumsatz = to_string(to_decimal(cust_list_detail.argtumsatz) + (genstat.logis / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + ((genstat.logis + genstat.res_deci[1] +\
                                    genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4] + genstat.res_deci[6]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.ba_umsatz = to_string(to_decimal(cust_list_detail.ba_umsatz) + (genstat.res_deci[6] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                    else:
                        cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + genstat.res_deci[4], "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.argtumsatz = to_string(to_decimal(cust_list_detail.argtumsatz) + genstat.logis, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + genstat.logis + genstat.res_deci[1] +\
                                genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4] + genstat.res_deci[6] , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.ba_umsatz = to_string(to_decimal(cust_list_detail.ba_umsatz) + genstat.res_deci[6], "->>>,>>>,>>>,>>9.99")

                    if genstat.resstatus != 13:
                        cust_list_detail.logiernachte = to_string(to_int(cust_list_detail.logiernachte) + 1, ">>>,>>9")


                    else:
                        cust_list_detail.rm_sharer = "*"

                    if curr_resnr1 != genstat.resnr or curr_reslinnr1 != genstat.res_int[0]:
                        curr_resnr1 = genstat.resnr
                        curr_reslinnr1 = genstat.res_int[0]

                        if genstat.resstatus == 6:

                            res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                            if res_line:
                                cust_list_detail.count_room = to_string(to_int(cust_list_detail.count_room) + res_line.zimmeranz, ">>,>>>,>>>,>>9")

                        if excl_other == False:

                            for bill in db_session.query(Bill).filter(
                                     (Bill.resnr == genstat.resnr) & (Bill.reslinnr == genstat.res_int[0])).order_by(Bill._recid).all():

                                bill_line_obj_list = {}
                                for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & (Artikel.artart == 0)).filter(
                                         (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum == genstat.datum)).order_by(Bill_line._recid).all():
                                    if bill_line_obj_list.get(bill_line._recid):
                                        continue
                                    else:
                                        bill_line_obj_list[bill_line._recid] = True


                                    service2 =  to_decimal("0")
                                    vat2 =  to_decimal("0")


                                    service2, vat2, vat22, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

                                    if currency != " ":

                                        exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                        if exrate:
                                            cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + ((bill_line.betrag / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                            cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + ((bill_line.betrag / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                                    else:
                                        cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + bill_line.betrag / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + bill_line.betrag / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")

                if excl_other == False:

                    for guest_queasy in db_session.query(Guest_queasy).filter(
                             (Guest_queasy.key == ("gast-info").lower()) & (Guest_queasy.date1 >= fdate) & (Guest_queasy.date1 <= tdate)).order_by(Guest_queasy._recid).all():

                        genstat = get_cache (Genstat, {"resnr": [(eq, guest_queasy.number2)],"res_int[0]": [(eq, guest_queasy.number3)],"datum": [(eq, guest_queasy.date1)],"res_logic[1]": [(eq, True)]})

                        if genstat:

                            bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                            cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gname == bguest.NAME), first=True)

                            if cust_list_detail:

                                h_bill_line_obj_list = {}
                                for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                                         (H_bill_line.rechnr == to_int(guest_queasy.char1)) & (H_bill_line.departement == guest_queasy.number1)).order_by(H_bill_line._recid).all():
                                    if h_bill_line_obj_list.get(h_bill_line._recid):
                                        continue
                                    else:
                                        h_bill_line_obj_list[h_bill_line._recid] = True


                                    service2 =  to_decimal("0")
                                    vat2 =  to_decimal("0")


                                    service2, vat2, vat22, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, guest_queasy.date1))

                                    if currency != " ":

                                        exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                        if exrate:
                                            cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                            cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + ((guest_queasy.deci3 / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                            cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + (((guest_queasy.deci1 + guest_queasy.deci2 +\
                                                guest_queasy.deci3) / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                                    else:
                                        cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (guest_queasy.deci1 + guest_queasy.deci2) / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + guest_queasy.deci3 / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + (guest_queasy.deci1 + guest_queasy.deci2 +\
                                            guest_queasy.deci3) / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")


            else:
                cr_ftd()

            if tdate != None and tdate >= ci_date and check_ftd:
                create_forecast()


    def cr_ftd():

        nonlocal b_list_data, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_gname, curr_gastnr2, t_logiernachte, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, t_lyear, t_nofrm, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, tot_lyear, tot_nofrm, gt_logiernachte, gt_argtumsatz, gt_fb_umsatz, gt_sonst_umsatz, gt_ba_umsatz, gt_gesamtumsatz, gt_stayno, gt_lyear, gt_nofrm, curr_resnr1, curr_reslinnr1, found1, loopj, exratenr, eexrate, service2, vat2, vat22, fact1, genstat, guest, bill_line, bill, htparam, waehrung, nation, queasy, exrate, res_line, artikel, guest_queasy, h_artikel, h_bill_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal cardtype, sort_type, fdate, tdate, check_ftd, currency, excl_other, curr_sort2
        nonlocal t_genstat, blist, glist, bguest, clist, bline, bbuf


        nonlocal cust_list_detail, b_list, t_genstat, blist, glist, bguest, clist, bline, bbuf, clist, clist
        nonlocal cust_list_detail_data, b_list_data

        t_argtumsatz:int = 0
        rate:Decimal = 1
        frate:Decimal = 1
        rmnite:int = 0
        curr_resnr:int = 0
        curr_reslinnr:int = 0
        loopi:int = 0
        found:bool = False
        t_genstat = None
        T_genstat =  create_buffer("T_genstat",Genstat)
        Clist = Cust_list_detail
        clist_data = cust_list_detail_data

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.gastnrmember, genstat.gastnr, genstat.resnr, genstat.res_int, genstat.res_date, genstat.datum, genstat.res_deci, genstat.logis, genstat.resstatus, genstat._recid, guest.phonetik3, guest.name, guest.anredefirma, guest.vorname1, guest.plz, guest.land, guest.wohnort, guest.anrede1, guest._recid in db_session.query(Genstat.gastnrmember, Genstat.gastnr, Genstat.resnr, Genstat.res_int, Genstat.res_date, Genstat.datum, Genstat.res_deci, Genstat.logis, Genstat.resstatus, Genstat._recid, Guest.phonetik3, Guest.name, Guest.anredefirma, Guest.vorname1, Guest.plz, Guest.land, Guest.wohnort, Guest.anrede1, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                 (Genstat.datum >= fdate) & (Genstat.datum <= tdate) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.gastnr, Genstat.resnr, Guest.land).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

            cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gastnrmember == genstat.gastnrmember), first=True)

            if not cust_list_detail:
                cust_list_detail = Cust_list_detail()
                cust_list_detail_data.append(cust_list_detail)

                cust_list_detail.gastnr = genstat.gastnr
                cust_list_detail.resno = genstat.resnr
                cust_list_detail.reslinnr = genstat.res_int[0]
                cust_list_detail.gname = bguest.name
                cust_list_detail.arrival = genstat.res_date[0]
                cust_list_detail.depart = genstat.res_date[1]
                cust_list_detail.gastnrmember = genstat.gastnrmember

                glist = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                if glist:
                    cust_list_detail.cust_name = glist.name + "," + glist.anredefirma + " " + glist.vorname1 + to_string(genstat.gastnrmember)
                    cust_list_detail.plz = glist.plz
                    cust_list_detail.land = glist.land
                    cust_list_detail.sales_id = glist.phonetik3
                    cust_list_detail.wohnort = glist.wohnort

                    nation = get_cache (Nation, {"kurzbez": [(eq, glist.land)]})

                    if nation:

                        queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                        if queasy:
                            cust_list_detail.region = queasy.char1
                    else:
                        cust_list_detail.region = "UNKOWN"

                    if cust_list_detail.sales_id == "":
                        cust_list_detail.sales_id = guest.phonetik3


                else:
                    cust_list_detail.cust_name = guest.name + "," + guest.anredefirma + " " + guest.vorname1
                    cust_list_detail.plz = guest.plz
                    cust_list_detail.land = guest.land
                    cust_list_detail.sales_id = guest.phonetik3
                    cust_list_detail.wohnort = guest.wohnort

                    nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                    if nation:

                        queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                        if queasy:
                            cust_list_detail.region = queasy.char1
                    else:
                        cust_list_detail.region = "UNKOWN"
            found = False

            clist = query(clist_data, filters=(lambda clist: clist.gastnr == genstat.gastnr and clist.gname == bguest.NAME), first=True)

            if clist:

                if clist.resnr != " ":
                    for loopi in range(1,num_entries(clist.resnr, ";")  + 1) :

                        if entry(loopi - 1, clist.resnr, ";") != " ":

                            if to_int(entry(loopi - 1, clist.resnr, ";")) == genstat.resnr:
                                found = True


                                break

                    if not found:
                        clist.resnr = clist.resnr + to_string(genstat.resnr) + ";"

                elif clist.resnr == " ":
                    clist.resnr = clist.resnr + to_string(genstat.resnr) + ";"

            if currency != " ":

                exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                if exrate:
                    cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + ((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + (genstat.res_deci[4] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.argtumsatz = to_string(to_decimal(cust_list_detail.argtumsatz) + (genstat.logis / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + ((genstat.logis + genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4] + genstat.res_deci[6]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.ba_umsatz = to_string(to_decimal(cust_list_detail.ba_umsatz) + (genstat.res_deci[6] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


            else:
                cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) , "->>>,>>>,>>>,>>9.99")
                cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + genstat.res_deci[4], "->>>,>>>,>>>,>>9.99")
                cust_list_detail.argtumsatz = to_string(to_decimal(cust_list_detail.argtumsatz) + genstat.logis, "->>>,>>>,>>>,>>9.99")
                cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + genstat.logis + genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4] + genstat.res_deci[6] , "->>>,>>>,>>>,>>9.99")
                cust_list_detail.ba_umsatz = to_string(to_decimal(cust_list_detail.ba_umsatz) + genstat.res_deci[6], "->>>,>>>,>>>,>>9.99")

            if genstat.resstatus != 13:
                cust_list_detail.logiernachte = to_string(to_int(cust_list_detail.logiernachte) + 1, ">>>,>>9")


            else:
                cust_list_detail.rm_sharer = "*"

            if excl_other == False:

                if curr_resnr != genstat.resnr or curr_reslinnr != genstat.res_int[0]:
                    curr_resnr = genstat.resnr
                    curr_reslinnr = genstat.res_int[0]

                    if genstat.resstatus == 6:

                        res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                        if res_line:
                            cust_list_detail.count_room = to_string(to_int(cust_list_detail.count_room) + res_line.zimmeranz, ">>,>>>,>>>,>>9")

                    for bill in db_session.query(Bill).filter(
                             (Bill.resnr == genstat.resnr) & (Bill.reslinnr == genstat.res_int[0])).order_by(Bill._recid).all():

                        bill_line_obj_list = {}
                        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & (Artikel.artart == 0)).filter(
                                 (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum == genstat.datum)).order_by(Bill_line._recid).all():
                            if bill_line_obj_list.get(bill_line._recid):
                                continue
                            else:
                                bill_line_obj_list[bill_line._recid] = True


                            service2 =  to_decimal("0")


                            vat2 =  to_decimal("0")
                            service2, vat2, vat22, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

                            if currency != "":

                                exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                if exrate:
                                    cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + ((bill_line.betrag / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                    cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + ((bill_line.betrag / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                            else:
                                cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + bill_line.betrag / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + bill_line.betrag / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")

        if excl_other == False:

            for guest_queasy in db_session.query(Guest_queasy).filter(
                     (Guest_queasy.key == ("gast-info").lower()) & (Guest_queasy.date1 >= fdate) & (Guest_queasy.date1 <= tdate)).order_by(Guest_queasy.number2).all():

                genstat = get_cache (Genstat, {"resnr": [(eq, guest_queasy.number2)],"res_int[0]": [(eq, guest_queasy.number3)],"datum": [(eq, guest_queasy.date1)],"res_logic[1]": [(eq, True)]})

                if genstat:

                    bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                    cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gname == bguest.NAME), first=True)

                    if cust_list_detail:

                        h_bill_line_obj_list = {}
                        for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                                 (H_bill_line.rechnr == to_int(guest_queasy.char1)) & (H_bill_line.departement == guest_queasy.number1)).order_by(H_bill_line._recid).all():
                            if h_bill_line_obj_list.get(h_bill_line._recid):
                                continue
                            else:
                                h_bill_line_obj_list[h_bill_line._recid] = True


                            service2 =  to_decimal("0")
                            vat2 =  to_decimal("0")


                            service2, vat2, vat22, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, guest_queasy.date1))

                            if currency != " ":

                                exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                if exrate:
                                    cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                    cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + ((guest_queasy.deci3 / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                    cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + (((guest_queasy.deci1 + guest_queasy.deci2 +\
                                        guest_queasy.deci3) / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                            else:
                                cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (guest_queasy.deci1 + guest_queasy.deci2) / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + guest_queasy.deci3 / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + (guest_queasy.deci1 + guest_queasy.deci2 +\
                                    guest_queasy.deci3) / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")

        t_genstat_obj_list = {}
        t_genstat = Genstat()
        guest = Guest()
        for t_genstat.gastnrmember, t_genstat.gastnr, t_genstat.resnr, t_genstat.res_int, t_genstat.res_date, t_genstat.datum, t_genstat.res_deci, t_genstat.logis, t_genstat.resstatus, t_genstat._recid, guest.phonetik3, guest.name, guest.anredefirma, guest.vorname1, guest.plz, guest.land, guest.wohnort, guest.anrede1, guest._recid in db_session.query(T_genstat.gastnrmember, T_genstat.gastnr, T_genstat.resnr, T_genstat.res_int, T_genstat.res_date, T_genstat.datum, T_genstat.res_deci, T_genstat.logis, T_genstat.resstatus, T_genstat._recid, Guest.phonetik3, Guest.name, Guest.anredefirma, Guest.vorname1, Guest.plz, Guest.land, Guest.wohnort, Guest.anrede1, Guest._recid).join(Guest,(Guest.gastnr == T_genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                 (T_genstat.datum >= fdate) & (T_genstat.datum <= tdate) & (T_genstat.res_deci[inc_value(6)] != 0) & not_ (T_genstat.res_logic[inc_value(1)])).order_by(T_genstat._recid).all():
            if t_genstat_obj_list.get(t_genstat._recid):
                continue
            else:
                t_genstat_obj_list[t_genstat._recid] = True

            bguest = get_cache (Guest, {"gastnr": [(eq, t_genstat.gastnrmember)]})

            cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == t_genstat.gastnr and cust_list_detail.gastnrmember == t_genstat.gastnrmember), first=True)

            if not cust_list_detail:
                cust_list_detail = Cust_list_detail()
                cust_list_detail_data.append(cust_list_detail)

                cust_list_detail.gastnr = t_genstat.gastnr
                cust_list_detail.resno = t_genstat.resnr
                cust_list_detail.reslinnr = t_genstat.res_int[0]
                cust_list_detail.gname = bguest.name
                cust_list_detail.arrival = t_genstat.res_date[0]
                cust_list_detail.depart = t_genstat.res_date[1]
                cust_list_detail.gastnrmember = t_genstat.gastnrmember

            glist = get_cache (Guest, {"gastnr": [(eq, t_genstat.gastnrmember)]})

            if glist:
                cust_list_detail.cust_name = glist.name + "," + glist.anredefirma + " " + glist.vorname1 + to_string(t_genstat.gastnrmember)
                cust_list_detail.plz = glist.plz
                cust_list_detail.land = glist.land
                cust_list_detail.sales_id = glist.phonetik3
                cust_list_detail.wohnort = glist.wohnort

                nation = get_cache (Nation, {"kurzbez": [(eq, glist.land)]})

                if nation:

                    queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                    if queasy:
                        cust_list_detail.region = queasy.char1
                else:
                    cust_list_detail.region = "UNKOWN"

                if cust_list_detail.sales_id == "":
                    cust_list_detail.sales_id = guest.phonetik3

            if currency != " ":

                exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                if exrate:
                    cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + ((t_genstat.logis + t_genstat.res_deci[1] +\
                            t_genstat.res_deci[2] + t_genstat.res_deci[3] + t_genstat.res_deci[4] + t_genstat.res_deci[6]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.ba_umsatz = to_string(to_decimal(cust_list_detail.ba_umsatz) + (t_genstat.res_deci[6] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


            else:
                cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + t_genstat.logis + t_genstat.res_deci[1] +\
                        t_genstat.res_deci[2] + t_genstat.res_deci[3] + t_genstat.res_deci[4] + t_genstat.res_deci[6] , "->>>,>>>,>>>,>>9.99")
                cust_list_detail.ba_umsatz = to_string(to_decimal(cust_list_detail.ba_umsatz) + t_genstat.res_deci[6], "->>>,>>>,>>>,>>9.99")


    def create_forecast():

        nonlocal b_list_data, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_gname, curr_gastnr2, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, t_lyear, t_nofrm, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, tot_lyear, tot_nofrm, gt_logiernachte, gt_argtumsatz, gt_fb_umsatz, gt_sonst_umsatz, gt_ba_umsatz, gt_gesamtumsatz, gt_stayno, gt_lyear, gt_nofrm, curr_resnr1, curr_reslinnr1, found1, loopj, exratenr, eexrate, service2, vat2, vat22, fact1, genstat, guest, bill_line, bill, htparam, waehrung, nation, queasy, exrate, res_line, artikel, guest_queasy, h_artikel, h_bill_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal cardtype, sort_type, fdate, tdate, check_ftd, currency, excl_other, curr_sort2
        nonlocal t_genstat, blist, glist, bguest, clist, bline, bbuf


        nonlocal cust_list_detail, b_list, t_genstat, blist, glist, bguest, clist, bline, bbuf, clist, clist
        nonlocal cust_list_detail_data, b_list_data

        do_it:bool = True
        datum:date = None
        datum1:date = None
        datum2:date = None
        d2:date = None
        curr_resnr:int = 0
        curr_reslinnr:int = 0
        found:bool = False
        loopi:int = 0
        count_rm:int = 0

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
        for res_line.zimmeranz, res_line.resnr, res_line.arrangement, res_line.reslinnr, res_line.zinr, res_line.gastnr, res_line.gastnrmember, res_line.name, res_line.ankunft, res_line.abreise, res_line._recid, res_line.resstatus, res_line.zimmerfix, guest.phonetik3, guest.name, guest.anredefirma, guest.vorname1, guest.plz, guest.land, guest.wohnort, guest.anrede1, guest._recid in db_session.query(Res_line.zimmeranz, Res_line.resnr, Res_line.arrangement, Res_line.reslinnr, Res_line.zinr, Res_line.gastnr, Res_line.gastnrmember, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line._recid, Res_line.resstatus, Res_line.zimmerfix, Guest.phonetik3, Guest.name, Guest.anredefirma, Guest.vorname1, Guest.plz, Guest.land, Guest.wohnort, Guest.anrede1, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == cardtype)).filter(
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

            # zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
            zimmer = db_session.query(Zimmer).filter(Zimmer.zinr == res_line.zinr).with_for_update().first()

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

                cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == res_line.gastnr and cust_list_detail.gastnrmember == res_line.gastnrmember), first=True)

                if not cust_list_detail:
                    cust_list_detail = Cust_list_detail()
                    cust_list_detail_data.append(cust_list_detail)

                    cust_list_detail.gastnr = res_line.gastnr
                    cust_list_detail.resno = res_line.resnr
                    cust_list_detail.reslinnr = res_line.reslinnr
                    cust_list_detail.gname = res_line.name
                    cust_list_detail.arrival = res_line.ankunft
                    cust_list_detail.depart = res_line.abreise
                    cust_list_detail.gastnrmember = res_line.gastnrmember

                    glist = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if glist:
                        cust_list_detail.cust_name = glist.name + "," + glist.anredefirma + " " + glist.vorname1
                        cust_list_detail.plz = glist.plz
                        cust_list_detail.land = glist.land
                        cust_list_detail.sales_id = glist.phonetik3
                        cust_list_detail.wohnort = glist.wohnort

                        nation = get_cache (Nation, {"kurzbez": [(eq, glist.land)]})

                        if nation:

                            queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                            if queasy:
                                cust_list_detail.region = queasy.char1
                        else:
                            cust_list_detail.region = "UNKOWN"

                        if cust_list_detail.sales_id == "":
                            cust_list_detail.sales_id = guest.phonetik3


                    else:
                        cust_list_detail.cust_name = guest.name + "," + guest.anredefirma + " " + guest.vorname1
                        cust_list_detail.plz = guest.plz
                        cust_list_detail.land = guest.land
                        cust_list_detail.sales_id = guest.phonetik3
                        cust_list_detail.wohnort = guest.wohnort

                        nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                        if nation:

                            queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                            if queasy:
                                cust_list_detail.region = queasy.char1
                        else:
                            cust_list_detail.region = "UNKOWN"
                found = False

                clist = query(clist_data, filters=(lambda clist: clist.gastnr == res_line.gastnr and clist.gname == res_line.NAME), first=True)

                if clist:

                    if clist.resnr != " ":
                        for loopi in range(1,num_entries(clist.resnr, ";")  + 1) :

                            if entry(loopi - 1, clist.resnr, ";") != " ":

                                if to_int(entry(loopi - 1, clist.resnr, ";")) == res_line.resnr:
                                    found = True


                                    break

                        if not found:
                            clist.resnr = clist.resnr + to_string(res_line.resnr) + ";"

                    elif clist.resnr == " ":
                        clist.resnr = clist.resnr + to_string(res_line.resnr) + ";"

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

                    if curr_resnr != res_line.resnr or curr_reslinnr != res_line.reslinnr:
                        curr_resnr = res_line.resnr
                        curr_reslinnr = res_line.reslinnr

                        if curr_resnr != 0:

                            if ((res_line.ankunft < res_line.abreise) and res_line.abreise != datum) or (res_line.ankunft == res_line.abreise):

                                if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                                    cust_list_detail.count_room = to_string(to_int(cust_list_detail.count_room) + res_line.zimmeranz, ">>,>>>,>>>,>>9")
                                    tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(res_line.zimmeranz)
                                    gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(res_line.zimmeranz)

                        if excl_other == False:

                            for bill in db_session.query(Bill).filter(
                                     (Bill.resnr == res_line.resnr) & (Bill.reslinnr == res_line.reslinnr)).order_by(Bill._recid).all():

                                bill_line_obj_list = {}
                                for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & (Artikel.artart == 0)).filter(
                                         (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum == datum)).order_by(Bill_line._recid).all():
                                    if bill_line_obj_list.get(bill_line._recid):
                                        continue
                                    else:
                                        bill_line_obj_list[bill_line._recid] = True


                                    service2 =  to_decimal("0")
                                    vat2 =  to_decimal("0")


                                    service2, vat2, vat22, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))

                                    if currency != " ":
                                        cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + ((bill_line.betrag / (1 + service2 + vat2)) / eexrate) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + ((bill_line.betrag / (1 + service2 + vat2)) / eexrate) , "->>>,>>>,>>>,>>9.99")


                                    else:
                                        cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + bill_line.betrag / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + bill_line.betrag / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")

                    if currency != " ":
                        cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + ((tot_breakfast + tot_lunch + tot_dinner) / eexrate) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + (tot_other / eexrate) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.argtumsatz = to_string(to_decimal(cust_list_detail.argtumsatz) + (net_lodg / eexrate) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + ((net_lodg + tot_breakfast +\
                            tot_lunch + tot_dinner + tot_other) / eexrate) , "->>>,>>>,>>>,>>9.99")


                    else:
                        cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + tot_breakfast + tot_lunch + tot_dinner, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + tot_other, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.argtumsatz = to_string(to_decimal(cust_list_detail.argtumsatz) + net_lodg, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + net_lodg + tot_breakfast +\
                            tot_lunch + tot_dinner + tot_other , "->>>,>>>,>>>,>>9.99")

                    if ((res_line.ankunft < res_line.abreise) and res_line.abreise != datum) or (res_line.ankunft == res_line.abreise):

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            cust_list_detail.logiernachte = to_string(to_int(cust_list_detail.logiernachte) + 1, ">>>,>>9")

                        elif res_line.resstatus == 11 or res_line.resstatus == 13:
                            cust_list_detail.rm_sharer = "*"

                if ((res_line.ankunft < res_line.abreise) and res_line.abreise != datum) or (res_line.ankunft == res_line.abreise):

                    if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                        cust_list_detail.logiernachte = to_string(to_int(cust_list_detail.logiernachte) * res_line.zimmeranz, ">>>,>>9")

        if excl_other == False:

            for guest_queasy in db_session.query(Guest_queasy).filter(
                     (Guest_queasy.key == ("gast-info").lower()) & (Guest_queasy.date1 >= fdate) & (Guest_queasy.date1 <= tdate)).order_by(Guest_queasy._recid).all():

                res_line = get_cache (Res_line, {"resnr": [(eq, guest_queasy.number2)],"reslinnr": [(eq, guest_queasy.number3)]})

                if res_line:

                    cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == res_line.gastnr and cust_list_detail.resno == res_line.resnr and cust_list_detail.gname == res_line.NAME), first=True)

                    if cust_list_detail:

                        h_bill_line_obj_list = {}
                        for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                                 (H_bill_line.rechnr == to_int(guest_queasy.char1)) & (H_bill_line.departement == guest_queasy.number1)).order_by(H_bill_line._recid).all():
                            if h_bill_line_obj_list.get(h_bill_line._recid):
                                continue
                            else:
                                h_bill_line_obj_list[h_bill_line._recid] = True


                            service2 =  to_decimal("0")
                            vat2 =  to_decimal("0")


                            service2, vat2, vat22, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, guest_queasy.date1))

                            if currency != " ":
                                cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service2 + vat2)) / eexrate) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + ((guest_queasy.deci3 / (1 + service2 + vat2)) / eexrate) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + (((guest_queasy.deci1 + guest_queasy.deci2 +\
                                    guest_queasy.deci3) / (1 + service2 + vat2)) / eexrate) , "->>>,>>>,>>>,>>9.99")


                            else:
                                cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (guest_queasy.deci1 + guest_queasy.deci2) / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + guest_queasy.deci3 / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + (guest_queasy.deci1 + guest_queasy.deci2 +\
                                    guest_queasy.deci3) / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")

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
        for genstat.gastnrmember, genstat.gastnr, genstat.resnr, genstat.res_int, genstat.res_date, genstat.datum, genstat.res_deci, genstat.logis, genstat.resstatus, genstat._recid, guest.phonetik3, guest.name, guest.anredefirma, guest.vorname1, guest.plz, guest.land, guest.wohnort, guest.anrede1, guest._recid in db_session.query(Genstat.gastnrmember, Genstat.gastnr, Genstat.resnr, Genstat.res_int, Genstat.res_date, Genstat.datum, Genstat.res_deci, Genstat.logis, Genstat.resstatus, Genstat._recid, Guest.phonetik3, Guest.name, Guest.anredefirma, Guest.vorname1, Guest.plz, Guest.land, Guest.wohnort, Guest.anrede1, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr) & (Guest.karteityp == cardtype)).filter(
                 (Genstat.datum >= ly_fdate) & (Genstat.datum <= ly_tdate) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.gastnr, Guest.land, Genstat.resnr).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

            cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.resno == genstat.resnr and cust_list_detail.gname == bguest.NAME), first=True)

            if cust_list_detail:

                if currency != " ":

                    exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                    if exrate:
                        cust_list_detail.ly_rev = to_string(to_decimal(cust_list_detail.ly_rev) + ((genstat.logis + genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                else:
                    cust_list_detail.ly_rev = to_string(to_decimal(cust_list_detail.ly_rev) + genstat.logis + genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4], "->>>,>>>,>>>,>>9.99")


    def cr_ftd1():

        nonlocal b_list_data, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_gname, curr_gastnr2, t_logiernachte, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, t_lyear, t_nofrm, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, tot_lyear, tot_nofrm, gt_logiernachte, gt_argtumsatz, gt_fb_umsatz, gt_sonst_umsatz, gt_ba_umsatz, gt_gesamtumsatz, gt_stayno, gt_lyear, gt_nofrm, curr_resnr1, curr_reslinnr1, found1, loopj, exratenr, eexrate, service2, vat2, vat22, fact1, genstat, guest, bill_line, bill, htparam, waehrung, nation, queasy, exrate, res_line, artikel, guest_queasy, h_artikel, h_bill_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal cardtype, sort_type, fdate, tdate, check_ftd, currency, excl_other, curr_sort2
        nonlocal t_genstat, blist, glist, bguest, clist, bline, bbuf


        nonlocal cust_list_detail, b_list, t_genstat, blist, glist, bguest, clist, bline, bbuf, clist, clist
        nonlocal cust_list_detail_data, b_list_data

        t_argtumsatz:int = 0
        rate:Decimal = 1
        frate:Decimal = 1
        rmnite:int = 0
        curr_resnr:int = 0
        curr_reslinnr:int = 0
        loopi:int = 0
        found:bool = False
        t_genstat = None
        T_genstat =  create_buffer("T_genstat",Genstat)
        Clist = Cust_list_detail
        clist_data = cust_list_detail_data

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.gastnrmember, genstat.gastnr, genstat.resnr, genstat.res_int, genstat.res_date, genstat.datum, genstat.res_deci, genstat.logis, genstat.resstatus, genstat._recid, guest.phonetik3, guest.name, guest.anredefirma, guest.vorname1, guest.plz, guest.land, guest.wohnort, guest.anrede1, guest._recid in db_session.query(Genstat.gastnrmember, Genstat.gastnr, Genstat.resnr, Genstat.res_int, Genstat.res_date, Genstat.datum, Genstat.res_deci, Genstat.logis, Genstat.resstatus, Genstat._recid, Guest.phonetik3, Guest.name, Guest.anredefirma, Guest.vorname1, Guest.plz, Guest.land, Guest.wohnort, Guest.anrede1, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                 (Genstat.datum >= fdate) & (Genstat.datum <= tdate) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.gastnr, Genstat.resnr, Guest.land).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

            cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gastnrmember == genstat.gastnrmember), first=True)

            if not cust_list_detail:
                cust_list_detail = Cust_list_detail()
                cust_list_detail_data.append(cust_list_detail)

                cust_list_detail.gastnr = genstat.gastnr
                cust_list_detail.resno = genstat.resnr
                cust_list_detail.reslinnr = genstat.res_int[0]
                cust_list_detail.gname = bguest.name
                cust_list_detail.arrival = genstat.res_date[0]
                cust_list_detail.depart = genstat.res_date[1]
                cust_list_detail.gastnrmember = genstat.gastnrmember

                glist = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                if glist:
                    cust_list_detail.cust_name = glist.name + "," + glist.anredefirma + " " + glist.vorname1
                    cust_list_detail.plz = glist.plz
                    cust_list_detail.land = glist.land
                    cust_list_detail.sales_id = glist.phonetik3
                    cust_list_detail.wohnort = glist.wohnort

                    nation = get_cache (Nation, {"kurzbez": [(eq, glist.land)]})

                    if nation:

                        queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                        if queasy:
                            cust_list_detail.region = queasy.char1
                    else:
                        cust_list_detail.region = "UNKOWN"

                    if cust_list_detail.sales_id == "":
                        cust_list_detail.sales_id = guest.phonetik3


                else:
                    cust_list_detail.cust_name = guest.name + "," + guest.anredefirma + " " + guest.vorname1
                    cust_list_detail.plz = guest.plz
                    cust_list_detail.land = guest.land
                    cust_list_detail.sales_id = guest.phonetik3
                    cust_list_detail.wohnort = guest.wohnort

                    nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                    if nation:

                        queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                        if queasy:
                            cust_list_detail.region = queasy.char1
                    else:
                        cust_list_detail.region = "UNKOWN"
            found = False

            clist = query(clist_data, filters=(lambda clist: clist.gastnr == genstat.gastnr and clist.gname == bguest.NAME), first=True)

            if clist:

                if clist.resnr != " ":
                    for loopi in range(1,num_entries(clist.resnr, ";")  + 1) :

                        if entry(loopi - 1, clist.resnr, ";") != " ":

                            if to_int(entry(loopi - 1, clist.resnr, ";")) == genstat.resnr:
                                found = True


                                break

                    if not found:
                        clist.resnr = clist.resnr + to_string(genstat.resnr) + ";"

                elif clist.resnr == " ":
                    clist.resnr = clist.resnr + to_string(genstat.resnr) + ";"

            if currency != " ":

                exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                if exrate:
                    cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + ((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + (genstat.res_deci[4] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.argtumsatz = to_string(to_decimal(cust_list_detail.argtumsatz) + (genstat.logis / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + ((genstat.logis + genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4] + genstat.res_deci[6]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.ba_umsatz = to_string(to_decimal(cust_list_detail.ba_umsatz) + (genstat.res_deci[6] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


            else:
                cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) , "->>>,>>>,>>>,>>9.99")
                cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + genstat.res_deci[4], "->>>,>>>,>>>,>>9.99")
                cust_list_detail.argtumsatz = to_string(to_decimal(cust_list_detail.argtumsatz) + genstat.logis, "->>>,>>>,>>>,>>9.99")
                cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + genstat.logis + genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4] + genstat.res_deci[6], "->>>,>>>,>>>,>>9.99")
                cust_list_detail.ba_umsatz = to_string(to_decimal(cust_list_detail.ba_umsatz) + genstat.res_deci[6], "->>>,>>>,>>>,>>9.99")

            if genstat.resstatus != 13:
                cust_list_detail.logiernachte = to_string(to_int(cust_list_detail.logiernachte) + 1, ">>>,>>9")


            else:
                cust_list_detail.rm_sharer = "*"

            if excl_other == False:

                if curr_resnr != genstat.resnr or curr_reslinnr != genstat.res_int[0]:
                    curr_resnr = genstat.resnr
                    curr_reslinnr = genstat.res_int[0]

                    if genstat.resstatus == 6:

                        res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                        if res_line:
                            cust_list_detail.count_room = to_string(to_int(cust_list_detail.count_room) + res_line.zimmeranz, ">>,>>>,>>>,>>9")

                    for bill in db_session.query(Bill).filter(
                             (Bill.resnr == genstat.resnr) & (Bill.reslinnr == genstat.res_int[0])).order_by(Bill._recid).all():

                        bill_line_obj_list = {}
                        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & (Artikel.artart == 0)).filter(
                                 (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum == genstat.datum)).order_by(Bill_line._recid).all():
                            if bill_line_obj_list.get(bill_line._recid):
                                continue
                            else:
                                bill_line_obj_list[bill_line._recid] = True


                            service2 =  to_decimal("0")
                            vat2 =  to_decimal("0")


                            service2, vat2, vat22, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

                            if currency != " ":

                                exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                if exrate:
                                    cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + ((bill_line.betrag / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                    cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + ((bill_line.betrag / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                            else:
                                cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + bill_line.betrag / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + bill_line.betrag / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")

        if excl_other == False:

            for guest_queasy in db_session.query(Guest_queasy).filter(
                     (Guest_queasy.key == ("gast-info").lower()) & (Guest_queasy.date1 >= fdate) & (Guest_queasy.date1 <= tdate)).order_by(Guest_queasy.number2).all():

                genstat = get_cache (Genstat, {"resnr": [(eq, guest_queasy.number2)],"res_int[0]": [(eq, guest_queasy.number3)],"datum": [(eq, guest_queasy.date1)],"res_logic[1]": [(eq, True)]})

                if genstat:

                    bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

                    cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gname == bguest.NAME), first=True)

                    if cust_list_detail:

                        h_bill_line_obj_list = {}
                        for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                                 (H_bill_line.rechnr == to_int(guest_queasy.char1)) & (H_bill_line.departement == guest_queasy.number1)).order_by(H_bill_line._recid).all():
                            if h_bill_line_obj_list.get(h_bill_line._recid):
                                continue
                            else:
                                h_bill_line_obj_list[h_bill_line._recid] = True


                            service2 =  to_decimal("0")
                            vat2 =  to_decimal("0")


                            service2, vat2, vat22, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, guest_queasy.date1))

                            if currency != " ":

                                exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                                if exrate:
                                    cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                    cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + ((guest_queasy.deci3 / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                    cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + (((guest_queasy.deci1 + guest_queasy.deci2 +\
                                        guest_queasy.deci3) / (1 + service2 + vat2)) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                            else:
                                cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (guest_queasy.deci1 + guest_queasy.deci2) / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + guest_queasy.deci3 / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + (guest_queasy.deci1 + guest_queasy.deci2 +\
                                    guest_queasy.deci3) / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")

        t_genstat_obj_list = {}
        t_genstat = Genstat()
        guest = Guest()
        for t_genstat.gastnrmember, t_genstat.gastnr, t_genstat.resnr, t_genstat.res_int, t_genstat.res_date, t_genstat.datum, t_genstat.res_deci, t_genstat.logis, t_genstat.resstatus, t_genstat._recid, guest.phonetik3, guest.name, guest.anredefirma, guest.vorname1, guest.plz, guest.land, guest.wohnort, guest.anrede1, guest._recid in db_session.query(T_genstat.gastnrmember, T_genstat.gastnr, T_genstat.resnr, T_genstat.res_int, T_genstat.res_date, T_genstat.datum, T_genstat.res_deci, T_genstat.logis, T_genstat.resstatus, T_genstat._recid, Guest.phonetik3, Guest.name, Guest.anredefirma, Guest.vorname1, Guest.plz, Guest.land, Guest.wohnort, Guest.anrede1, Guest._recid).join(Guest,(Guest.gastnr == T_genstat.gastnr)).filter(
                 (T_genstat.datum >= fdate) & (T_genstat.datum <= tdate) & (T_genstat.res_deci[inc_value(6)] != 0) & not_ (T_genstat.res_logic[inc_value(1)])).order_by(T_genstat._recid).all():
            if t_genstat_obj_list.get(t_genstat._recid):
                continue
            else:
                t_genstat_obj_list[t_genstat._recid] = True

            bguest = get_cache (Guest, {"gastnr": [(eq, t_genstat.gastnrmember)]})

            cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == t_genstat.gastnr and cust_list_detail.gastnrmember == t_genstat.gastnrmember), first=True)

            if not cust_list_detail:
                cust_list_detail = Cust_list_detail()
                cust_list_detail_data.append(cust_list_detail)

                cust_list_detail.gastnr = t_genstat.gastnr
                cust_list_detail.resno = t_genstat.resnr
                cust_list_detail.reslinnr = t_genstat.res_int[0]
                cust_list_detail.gname = bguest.name
                cust_list_detail.arrival = t_genstat.res_date[0]
                cust_list_detail.depart = t_genstat.res_date[1]
                cust_list_detail.gastnrmember = t_genstat.gastnrmember

            glist = get_cache (Guest, {"gastnr": [(eq, t_genstat.gastnrmember)]})

            if glist:
                cust_list_detail.cust_name = glist.name + "," + glist.anredefirma + " " + glist.vorname1 + to_string(t_genstat.gastnrmember)
                cust_list_detail.plz = glist.plz
                cust_list_detail.land = glist.land
                cust_list_detail.sales_id = glist.phonetik3
                cust_list_detail.wohnort = glist.wohnort

                nation = get_cache (Nation, {"kurzbez": [(eq, glist.land)]})

                if nation:

                    queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                    if queasy:
                        cust_list_detail.region = queasy.char1
                else:
                    cust_list_detail.region = "UNKOWN"

                if cust_list_detail.sales_id == "":
                    cust_list_detail.sales_id = guest.phonetik3

            if currency != " ":

                exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                if exrate:
                    cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + ((t_genstat.logis + t_genstat.res_deci[1] +\
                            t_genstat.res_deci[2] + t_genstat.res_deci[3] + t_genstat.res_deci[4] + t_genstat.res_deci[6]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.ba_umsatz = to_string(to_decimal(cust_list_detail.ba_umsatz) + (t_genstat.res_deci[6] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


            else:
                cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + t_genstat.logis + t_genstat.res_deci[1] +\
                        t_genstat.res_deci[2] + t_genstat.res_deci[3] + t_genstat.res_deci[4] + t_genstat.res_deci[6] , "->>>,>>>,>>>,>>9.99")
                cust_list_detail.ba_umsatz = to_string(to_decimal(cust_list_detail.ba_umsatz) + t_genstat.res_deci[6], "->>>,>>>,>>>,>>9.99")


    def create_forecast1():

        nonlocal b_list_data, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_gname, curr_gastnr2, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, t_lyear, t_nofrm, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, tot_lyear, tot_nofrm, gt_logiernachte, gt_argtumsatz, gt_fb_umsatz, gt_sonst_umsatz, gt_ba_umsatz, gt_gesamtumsatz, gt_stayno, gt_lyear, gt_nofrm, curr_resnr1, curr_reslinnr1, found1, loopj, exratenr, eexrate, service2, vat2, vat22, fact1, genstat, guest, bill_line, bill, htparam, waehrung, nation, queasy, exrate, res_line, artikel, guest_queasy, h_artikel, h_bill_line, reservation, sourccod, segment, arrangement, zimmer
        nonlocal cardtype, sort_type, fdate, tdate, check_ftd, currency, excl_other, curr_sort2
        nonlocal t_genstat, blist, glist, bguest, clist, bline, bbuf


        nonlocal cust_list_detail, b_list, t_genstat, blist, glist, bguest, clist, bline, bbuf, clist, clist
        nonlocal cust_list_detail_data, b_list_data

        do_it:bool = True
        datum:date = None
        datum1:date = None
        datum2:date = None
        d2:date = None
        curr_resnr:int = 0
        curr_reslinnr:int = 0
        found:bool = False
        loopi:int = 0
        count_rm:int = 0
        num_year:int = 0

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
        for res_line.zimmeranz, res_line.resnr, res_line.arrangement, res_line.reslinnr, res_line.zinr, res_line.gastnr, res_line.gastnrmember, res_line.name, res_line.ankunft, res_line.abreise, res_line._recid, res_line.resstatus, res_line.zimmerfix, guest.phonetik3, guest.name, guest.anredefirma, guest.vorname1, guest.plz, guest.land, guest.wohnort, guest.anrede1, guest._recid in db_session.query(Res_line.zimmeranz, Res_line.resnr, Res_line.arrangement, Res_line.reslinnr, Res_line.zinr, Res_line.gastnr, Res_line.gastnrmember, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line._recid, Res_line.resstatus, Res_line.zimmerfix, Guest.phonetik3, Guest.name, Guest.anredefirma, Guest.vorname1, Guest.plz, Guest.land, Guest.wohnort, Guest.anrede1, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnr)).filter(
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

                cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == res_line.gastnr and cust_list_detail.gastnrmember == res_line.gastnrmember), first=True)

                if not cust_list_detail:
                    cust_list_detail = Cust_list_detail()
                    cust_list_detail_data.append(cust_list_detail)

                    cust_list_detail.gastnr = res_line.gastnr
                    cust_list_detail.resno = res_line.resnr
                    cust_list_detail.reslinnr = res_line.reslinnr
                    cust_list_detail.gname = res_line.name
                    cust_list_detail.arrival = res_line.ankunft
                    cust_list_detail.depart = res_line.abreise
                    cust_list_detail.gastnrmember = res_line.gastnrmember

                    glist = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if glist:
                        cust_list_detail.cust_name = glist.name + "," + glist.anredefirma + " " + glist.vorname1
                        cust_list_detail.plz = glist.plz
                        cust_list_detail.land = glist.land
                        cust_list_detail.sales_id = glist.phonetik3
                        cust_list_detail.wohnort = glist.wohnort

                        nation = get_cache (Nation, {"kurzbez": [(eq, glist.land)]})

                        if nation:

                            queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                            if queasy:
                                cust_list_detail.region = queasy.char1
                        else:
                            cust_list_detail.region = "UNKOWN"

                        if cust_list_detail.sales_id == "":
                            cust_list_detail.sales_id = guest.phonetik3


                    else:
                        cust_list_detail.cust_name = guest.name + "," + guest.anredefirma + " " + guest.vorname1
                        cust_list_detail.plz = guest.plz
                        cust_list_detail.land = guest.land
                        cust_list_detail.sales_id = guest.phonetik3
                        cust_list_detail.wohnort = guest.wohnort

                        nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

                        if nation:

                            queasy = get_cache (Queasy, {"key": [(eq, 6)],"number1": [(eq, nation.untergruppe)]})

                            if queasy:
                                cust_list_detail.region = queasy.char1
                        else:
                            cust_list_detail.region = "UNKOWN"
                found = False

                clist = query(clist_data, filters=(lambda clist: clist.gastnr == res_line.gastnr and clist.gname == res_line.name), first=True)

                if clist:

                    if clist.resnr != " ":
                        for loopi in range(1,num_entries(clist.resnr, ";")  + 1) :

                            if entry(loopi - 1, clist.resnr, ";") != " ":

                                if to_int(entry(loopi - 1, clist.resnr, ";")) == res_line.resnr:
                                    found = True


                                    break

                        if not found:
                            clist.resnr = clist.resnr + to_string(res_line.resnr) + ";"

                    elif clist.resnr == " ":
                        clist.resnr = clist.resnr + to_string(res_line.resnr) + ";"

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

                    if curr_resnr != res_line.resnr or curr_reslinnr != res_line.reslinnr:
                        curr_resnr = res_line.resnr
                        curr_reslinnr = res_line.reslinnr

                        if curr_resnr != 0:

                            if ((res_line.ankunft < res_line.abreise) and res_line.abreise != datum) or (res_line.ankunft == res_line.abreise):

                                if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                                    cust_list_detail.count_room = to_string(to_int(cust_list_detail.count_room) + res_line.zimmeranz, ">>,>>>,>>>,>>9")
                                    tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(res_line.zimmeranz)
                                    gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(res_line.zimmeranz)

                        if excl_other == False:

                            for bill in db_session.query(Bill).filter(
                                     (Bill.resnr == res_line.resnr) & (Bill.reslinnr == res_line.reslinnr)).order_by(Bill._recid).all():

                                bill_line_obj_list = {}
                                for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement) & (Artikel.artart == 0)).filter(
                                         (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum == datum)).order_by(Bill_line._recid).all():
                                    if bill_line_obj_list.get(bill_line._recid):
                                        continue
                                    else:
                                        bill_line_obj_list[bill_line._recid] = True


                                    service2 =  to_decimal("0")
                                    vat2 =  to_decimal("0")


                                    service2, vat2, vat22, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, datum))

                                    if currency != " ":
                                        cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + ((bill_line.betrag / (1 + service2 + vat2)) / eexrate) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + ((bill_line.betrag / (1 + service2 + vat2)) / eexrate) , "->>>,>>>,>>>,>>9.99")


                                    else:
                                        cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + bill_line.betrag / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + bill_line.betrag / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")

                    if currency != " ":
                        cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + ((tot_breakfast + tot_lunch + tot_dinner) / eexrate) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + (tot_other / eexrate) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.argtumsatz = to_string(to_decimal(cust_list_detail.argtumsatz) + (net_lodg / eexrate) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + ((net_lodg + tot_breakfast +\
                                tot_lunch + tot_dinner + tot_other) / eexrate) , "->>>,>>>,>>>,>>9.99")


                    else:
                        cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + tot_breakfast + tot_lunch + tot_dinner, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + tot_other, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.argtumsatz = to_string(to_decimal(cust_list_detail.argtumsatz) + net_lodg, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + net_lodg + tot_breakfast +\
                            tot_lunch + tot_dinner + tot_other , "->>>,>>>,>>>,>>9.99")

                    if ((res_line.ankunft < res_line.abreise) and res_line.abreise != datum) or (res_line.ankunft == res_line.abreise):

                        if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                            cust_list_detail.logiernachte = to_string(to_int(cust_list_detail.logiernachte) + 1, ">>>,>>9")

                        elif res_line.resstatus == 11 or res_line.resstatus == 13:
                            cust_list_detail.rm_sharer = "*"

                if ((res_line.ankunft < res_line.abreise) and res_line.abreise != datum) or (res_line.ankunft == res_line.abreise):

                    if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                        cust_list_detail.logiernachte = to_string(to_int(cust_list_detail.logiernachte) * res_line.zimmeranz, ">>>,>>9")

        if excl_other == False:

            for guest_queasy in db_session.query(Guest_queasy).filter(
                     (Guest_queasy.key == ("gast-info").lower()) & (Guest_queasy.date1 >= fdate) & (Guest_queasy.date1 <= tdate)).order_by(Guest_queasy._recid).all():

                res_line = get_cache (Res_line, {"resnr": [(eq, guest_queasy.number2)],"reslinnr": [(eq, guest_queasy.number3)]})

                if res_line:

                    cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == res_line.gastnr and cust_list_detail.resno == res_line.resnr and cust_list_detail.gname == res_line.NAME), first=True)

                    if cust_list_detail:

                        h_bill_line_obj_list = {}
                        for h_bill_line, h_artikel, artikel in db_session.query(H_bill_line, H_artikel, Artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement)).filter(
                                 (H_bill_line.rechnr == to_int(guest_queasy.char1)) & (H_bill_line.departement == guest_queasy.number1)).order_by(H_bill_line._recid).all():
                            if h_bill_line_obj_list.get(h_bill_line._recid):
                                continue
                            else:
                                h_bill_line_obj_list[h_bill_line._recid] = True


                            service2 =  to_decimal("0")
                            vat2 =  to_decimal("0")


                            service2, vat2, vat22, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, guest_queasy.date1))

                            if currency != " ":
                                cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (((guest_queasy.deci1 + guest_queasy.deci2) / (1 + service2 + vat2)) / eexrate) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + ((guest_queasy.deci3 / (1 + service2 + vat2)) / eexrate) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + (((guest_queasy.deci1 + guest_queasy.deci2 +\
                                    guest_queasy.deci3) / (1 + service2 + vat2)) / eexrate) , "->>>,>>>,>>>,>>9.99")


                            else:
                                cust_list_detail.f_b_umsatz = to_string(to_decimal(cust_list_detail.f_b_umsatz) + (guest_queasy.deci1 + guest_queasy.deci2) / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.sonst_umsatz = to_string(to_decimal(cust_list_detail.sonst_umsatz) + guest_queasy.deci3 / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.gesamtumsatz = to_string(to_decimal(cust_list_detail.gesamtumsatz) + (guest_queasy.deci1 + guest_queasy.deci2 +\
                                    guest_queasy.deci3) / (1 + service2 + vat2) , "->>>,>>>,>>>,>>9.99")

        if get_day(fdate) == 29 and get_month(fdate) == 2:
            num_year = get_year(fdate) - 1
            ly_fdate = date_mdy(get_month(fdate) , 28, num_year)
        else:
            num_year = get_year(fdate) - 1
            ly_fdate = date_mdy(get_month(fdate) , get_day(fdate) , num_year)

        if get_day(tdate) == 29 and get_month(tdate) == 2:
            num_year = get_year(tdate) - 1
            ly_tdate = date_mdy(get_month(tdate) , 28, num_year)
        else:
            num_year = get_year(tdate) - 1
            ly_tdate = date_mdy(get_month(tdate) , get_day(tdate) , num_year)

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.gastnrmember, genstat.gastnr, genstat.resnr, genstat.res_int, genstat.res_date, genstat.datum, genstat.res_deci, genstat.logis, genstat.resstatus, genstat._recid, guest.phonetik3, guest.name, guest.anredefirma, guest.vorname1, guest.plz, guest.land, guest.wohnort, guest.anrede1, guest._recid in db_session.query(Genstat.gastnrmember, Genstat.gastnr, Genstat.resnr, Genstat.res_int, Genstat.res_date, Genstat.datum, Genstat.res_deci, Genstat.logis, Genstat.resstatus, Genstat._recid, Guest.phonetik3, Guest.name, Guest.anredefirma, Guest.vorname1, Guest.plz, Guest.land, Guest.wohnort, Guest.anrede1, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                 (Genstat.datum >= ly_fdate) & (Genstat.datum <= ly_tdate) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.gastnr, Guest.land, Genstat.resnr).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            bguest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

            cust_list_detail = query(cust_list_detail_data, filters=(lambda cust_list_detail: cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.resno == genstat.resnr and cust_list_detail.gname == bguest.NAME), first=True)

            if cust_list_detail:

                if currency != " ":

                    exrate = get_cache (Exrate, {"datum": [(eq, genstat.datum)],"artnr": [(eq, exratenr)]})

                    if exrate:
                        cust_list_detail.ly_rev = to_string(to_decimal(cust_list_detail.ly_rev) + ((genstat.logis + genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                else:
                    cust_list_detail.ly_rev = to_string(to_decimal(cust_list_detail.ly_rev) + genstat.logis + genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4], "->>>,>>>,>>>,>>9.99")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 125)]})
    bfast_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    b_list_data.clear()
    create_detail()
    tot_logiernachte =  to_decimal("0")
    tot_argtumsatz =  to_decimal("0")
    tot_fb_umsatz =  to_decimal("0")
    tot_sonst_umsatz =  to_decimal("0")
    tot_ba_umsatz =  to_decimal("0")
    tot_gesamtumsatz =  to_decimal("0")
    tot_stayno =  to_decimal("0")
    tot_lyear =  to_decimal("0")
    tot_nofrm =  to_decimal("0")
    gt_logiernachte =  to_decimal("0")
    gt_argtumsatz =  to_decimal("0")
    gt_fb_umsatz =  to_decimal("0")
    gt_sonst_umsatz =  to_decimal("0")
    gt_ba_umsatz =  to_decimal("0")
    gt_gesamtumsatz =  to_decimal("0")
    gt_lyear =  to_decimal("0")
    gt_nofrm =  to_decimal("0")

    if sort_type == 0:

        for cust_list_detail in query(cust_list_detail_data, sort_by=[("gastnr",False)]):

            guest = get_cache (Guest, {"gastnr": [(eq, cust_list_detail.gastnr)]})

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirma)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = "T O T A L"
                b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
                b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
                b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
                b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
                b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
                b_list.stayno = to_string(tot_stayno, ">>>,>>9")
                b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
                b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")
                tot_logiernachte =  to_decimal("0")
                tot_argtumsatz =  to_decimal("0")
                tot_fb_umsatz =  to_decimal("0")
                tot_sonst_umsatz =  to_decimal("0")
                tot_ba_umsatz =  to_decimal("0")
                tot_gesamtumsatz =  to_decimal("0")
                tot_stayno =  to_decimal("0")
                tot_lyear =  to_decimal("0")
                tot_nofrm =  to_decimal("0")


                b_list = B_list()
                b_list_data.append(b_list)

                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirma)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno =  to_decimal(tot_stayno) + to_decimal(to_int(cust_list_detail.stayno) )
                gt_stayno =  to_decimal(gt_stayno) + to_decimal(to_int(cust_list_detail.stayno) )


            b_list = B_list()
            b_list_data.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte =  to_decimal(tot_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            tot_argtumsatz =  to_decimal(tot_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            tot_fb_umsatz =  to_decimal(tot_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            tot_sonst_umsatz =  to_decimal(tot_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            tot_ba_umsatz =  to_decimal(tot_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            tot_gesamtumsatz =  to_decimal(tot_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            tot_lyear =  to_decimal(tot_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            gt_logiernachte =  to_decimal(gt_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            gt_argtumsatz =  to_decimal(gt_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            gt_fb_umsatz =  to_decimal(gt_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            gt_sonst_umsatz =  to_decimal(gt_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            gt_ba_umsatz =  to_decimal(gt_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            gt_gesamtumsatz =  to_decimal(gt_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            gt_lyear =  to_decimal(gt_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "T O T A L"
            b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(tot_stayno, ">>>,>>9")
            b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")

        if gt_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "G R A N D T O T A L"
            b_list.f_b_umsatz = to_string(gt_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(gt_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(gt_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(gt_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(gt_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(gt_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(gt_stayno, ">>>,>>9")
            b_list.count_room = to_string(gt_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(gt_lyear, "->>>,>>>,>>>,>>9.99")


    elif sort_type == 1:

        for cust_list_detail in query(cust_list_detail_data, sort_by=[("gastnr",False),("gesamtumsatz",True)]):

            guest = get_cache (Guest, {"gastnr": [(eq, cust_list_detail.gastnr)]})

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_data.append(b_list)

                    b_list.cust_name = "T O T A L"
                    b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
                    b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.stayno = to_string(tot_stayno, ">>>,>>9")
                    b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
                    b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")
                    tot_logiernachte =  to_decimal("0")
                    tot_argtumsatz =  to_decimal("0")
                    tot_fb_umsatz =  to_decimal("0")
                    tot_sonst_umsatz =  to_decimal("0")
                    tot_ba_umsatz =  to_decimal("0")
                    tot_gesamtumsatz =  to_decimal("0")
                    tot_stayno =  to_decimal("0")
                    tot_lyear =  to_decimal("0")
                    tot_nofrm =  to_decimal("0")


                b_list = B_list()
                b_list_data.append(b_list)

                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno =  to_decimal(tot_stayno) + to_decimal(to_int(cust_list_detail.stayno) )
                gt_stayno =  to_decimal(gt_stayno) + to_decimal(to_int(cust_list_detail.stayno) )


            b_list = B_list()
            b_list_data.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte =  to_decimal(tot_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            tot_argtumsatz =  to_decimal(tot_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            tot_fb_umsatz =  to_decimal(tot_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            tot_sonst_umsatz =  to_decimal(tot_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            tot_ba_umsatz =  to_decimal(tot_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            tot_gesamtumsatz =  to_decimal(tot_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            tot_lyear =  to_decimal(tot_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            gt_logiernachte =  to_decimal(gt_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            gt_argtumsatz =  to_decimal(gt_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            gt_fb_umsatz =  to_decimal(gt_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            gt_sonst_umsatz =  to_decimal(gt_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            gt_ba_umsatz =  to_decimal(gt_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            gt_gesamtumsatz =  to_decimal(gt_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            gt_lyear =  to_decimal(gt_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "T O T A L"
            b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(tot_stayno, ">>>,>>9")
            b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")

        if gt_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "G R A N D T O T A L"
            b_list.f_b_umsatz = to_string(gt_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(gt_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(gt_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(gt_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(gt_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(gt_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(gt_stayno, ">>>,>>9")
            b_list.count_room = to_string(gt_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(gt_lyear, "->>>,>>>,>>>,>>9.99")


    elif sort_type == 2:

        for cust_list_detail in query(cust_list_detail_data, sort_by=[("gastnr",False),("logiernachte",True)]):

            guest = get_cache (Guest, {"gastnr": [(eq, cust_list_detail.gastnr)]})

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_data.append(b_list)

                    b_list.cust_name = "T O T A L"
                    b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
                    b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.stayno = to_string(tot_stayno, ">>>,>>9")
                    b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
                    b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")
                    tot_logiernachte =  to_decimal("0")
                    tot_argtumsatz =  to_decimal("0")
                    tot_fb_umsatz =  to_decimal("0")
                    tot_sonst_umsatz =  to_decimal("0")
                    tot_ba_umsatz =  to_decimal("0")
                    tot_gesamtumsatz =  to_decimal("0")
                    tot_stayno =  to_decimal("0")
                    tot_lyear =  to_decimal("0")
                    tot_nofrm =  to_decimal("0")


                b_list = B_list()
                b_list_data.append(b_list)

                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno =  to_decimal(tot_stayno) + to_decimal(to_int(cust_list_detail.stayno) )
                gt_stayno =  to_decimal(gt_stayno) + to_decimal(to_int(cust_list_detail.stayno) )


            b_list = B_list()
            b_list_data.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte =  to_decimal(tot_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            tot_argtumsatz =  to_decimal(tot_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            tot_fb_umsatz =  to_decimal(tot_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            tot_sonst_umsatz =  to_decimal(tot_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            tot_ba_umsatz =  to_decimal(tot_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            tot_gesamtumsatz =  to_decimal(tot_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            tot_lyear =  to_decimal(tot_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            gt_logiernachte =  to_decimal(gt_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            gt_argtumsatz =  to_decimal(gt_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            gt_fb_umsatz =  to_decimal(gt_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            gt_sonst_umsatz =  to_decimal(gt_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            gt_ba_umsatz =  to_decimal(gt_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            gt_gesamtumsatz =  to_decimal(gt_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            gt_lyear =  to_decimal(gt_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "T O T A L"
            b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(tot_stayno, ">>>,>>9")
            b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")

        if gt_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "G R A N D T O T A L"
            b_list.f_b_umsatz = to_string(gt_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(gt_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(gt_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(gt_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(gt_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(gt_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(gt_stayno, ">>>,>>9")
            b_list.count_room = to_string(gt_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(gt_lyear, "->>>,>>>,>>>,>>9.99")


    elif sort_type == 3:

        for cust_list_detail in query(cust_list_detail_data, sort_by=[("gastnr",False),("cust_name",False)]):

            guest = get_cache (Guest, {"gastnr": [(eq, cust_list_detail.gastnr)]})

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_data.append(b_list)

                    b_list.cust_name = "T O T A L"
                    b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
                    b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.stayno = to_string(tot_stayno, ">>>,>>9")
                    b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
                    b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")
                    tot_logiernachte =  to_decimal("0")
                    tot_argtumsatz =  to_decimal("0")
                    tot_fb_umsatz =  to_decimal("0")
                    tot_sonst_umsatz =  to_decimal("0")
                    tot_ba_umsatz =  to_decimal("0")
                    tot_gesamtumsatz =  to_decimal("0")
                    tot_stayno =  to_decimal("0")
                    tot_lyear =  to_decimal("0")
                    tot_nofrm =  to_decimal("0")


                b_list = B_list()
                b_list_data.append(b_list)

                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno =  to_decimal(tot_stayno) + to_decimal(to_int(cust_list_detail.stayno) )
                gt_stayno =  to_decimal(gt_stayno) + to_decimal(to_int(cust_list_detail.stayno) )


            b_list = B_list()
            b_list_data.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte =  to_decimal(tot_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            tot_argtumsatz =  to_decimal(tot_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            tot_fb_umsatz =  to_decimal(tot_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            tot_sonst_umsatz =  to_decimal(tot_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            tot_ba_umsatz =  to_decimal(tot_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            tot_gesamtumsatz =  to_decimal(tot_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            tot_lyear =  to_decimal(tot_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            gt_logiernachte =  to_decimal(gt_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            gt_argtumsatz =  to_decimal(gt_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            gt_fb_umsatz =  to_decimal(gt_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            gt_sonst_umsatz =  to_decimal(gt_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            gt_ba_umsatz =  to_decimal(gt_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            gt_gesamtumsatz =  to_decimal(gt_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            gt_lyear =  to_decimal(gt_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "T O T A L"
            b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(tot_stayno, ">>>,>>9")
            b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")

        if gt_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "G R A N D T O T A L"
            b_list.f_b_umsatz = to_string(gt_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(gt_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(gt_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(gt_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(gt_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(gt_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(gt_stayno, ">>>,>>9")
            b_list.count_room = to_string(gt_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(gt_lyear, "->>>,>>>,>>>,>>9.99")


    elif sort_type == 4:

        for cust_list_detail in query(cust_list_detail_data, sort_by=[("gastnr",False),("argtumsatz",True)]):

            guest = get_cache (Guest, {"gastnr": [(eq, cust_list_detail.gastnr)]})

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_data.append(b_list)

                    b_list.cust_name = "T O T A L"
                    b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
                    b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.stayno = to_string(tot_stayno, ">>>,>>9")
                    b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
                    b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")
                    tot_logiernachte =  to_decimal("0")
                    tot_argtumsatz =  to_decimal("0")
                    tot_fb_umsatz =  to_decimal("0")
                    tot_sonst_umsatz =  to_decimal("0")
                    tot_ba_umsatz =  to_decimal("0")
                    tot_gesamtumsatz =  to_decimal("0")
                    tot_stayno =  to_decimal("0")
                    tot_lyear =  to_decimal("0")
                    tot_nofrm =  to_decimal("0")


                b_list = B_list()
                b_list_data.append(b_list)

                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno =  to_decimal(tot_stayno) + to_decimal(to_int(cust_list_detail.stayno) )
                gt_stayno =  to_decimal(gt_stayno) + to_decimal(to_int(cust_list_detail.stayno) )


            b_list = B_list()
            b_list_data.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte =  to_decimal(tot_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            tot_argtumsatz =  to_decimal(tot_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            tot_fb_umsatz =  to_decimal(tot_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            tot_sonst_umsatz =  to_decimal(tot_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            tot_ba_umsatz =  to_decimal(tot_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            tot_gesamtumsatz =  to_decimal(tot_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            tot_lyear =  to_decimal(tot_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            gt_logiernachte =  to_decimal(gt_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            gt_argtumsatz =  to_decimal(gt_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            gt_fb_umsatz =  to_decimal(gt_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            gt_sonst_umsatz =  to_decimal(gt_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            gt_ba_umsatz =  to_decimal(gt_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            gt_gesamtumsatz =  to_decimal(gt_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            gt_lyear =  to_decimal(gt_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "T O T A L"
            b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(tot_stayno, ">>>,>>9")
            b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")

        if gt_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "G R A N D T O T A L"
            b_list.f_b_umsatz = to_string(gt_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(gt_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(gt_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(gt_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(gt_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(gt_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(gt_stayno, ">>>,>>9")
            b_list.count_room = to_string(gt_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(gt_lyear, "->>>,>>>,>>>,>>9.99")


    elif sort_type == 5:

        for cust_list_detail in query(cust_list_detail_data, sort_by=[("gastnr",False),("f_b_umsatz",True)]):

            guest = get_cache (Guest, {"gastnr": [(eq, cust_list_detail.gastnr)]})

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_data.append(b_list)

                    b_list.cust_name = "T O T A L"
                    b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
                    b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.stayno = to_string(tot_stayno, ">>>,>>9")
                    b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
                    b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")
                    tot_logiernachte =  to_decimal("0")
                    tot_argtumsatz =  to_decimal("0")
                    tot_fb_umsatz =  to_decimal("0")
                    tot_sonst_umsatz =  to_decimal("0")
                    tot_ba_umsatz =  to_decimal("0")
                    tot_gesamtumsatz =  to_decimal("0")
                    tot_stayno =  to_decimal("0")
                    tot_lyear =  to_decimal("0")
                    tot_nofrm =  to_decimal("0")


                b_list = B_list()
                b_list_data.append(b_list)

                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno =  to_decimal(tot_stayno) + to_decimal(to_int(cust_list_detail.stayno) )
                gt_stayno =  to_decimal(gt_stayno) + to_decimal(to_int(cust_list_detail.stayno) )


            b_list = B_list()
            b_list_data.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte =  to_decimal(tot_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            tot_argtumsatz =  to_decimal(tot_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            tot_fb_umsatz =  to_decimal(tot_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            tot_sonst_umsatz =  to_decimal(tot_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            tot_ba_umsatz =  to_decimal(tot_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            tot_gesamtumsatz =  to_decimal(tot_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            tot_lyear =  to_decimal(tot_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            gt_logiernachte =  to_decimal(gt_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            gt_argtumsatz =  to_decimal(gt_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            gt_fb_umsatz =  to_decimal(gt_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            gt_sonst_umsatz =  to_decimal(gt_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            gt_ba_umsatz =  to_decimal(gt_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            gt_gesamtumsatz =  to_decimal(gt_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            gt_lyear =  to_decimal(gt_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "T O T A L"
            b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(tot_stayno, ">>>,>>9")
            b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")

        if gt_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "G R A N D T O T A L"
            b_list.f_b_umsatz = to_string(gt_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(gt_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(gt_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(gt_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(gt_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(gt_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(gt_stayno, ">>>,>>9")
            b_list.count_room = to_string(gt_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(gt_lyear, "->>>,>>>,>>>,>>9.99")


    elif sort_type == 6:

        for cust_list_detail in query(cust_list_detail_data, sort_by=[("gastnr",False),("sonst_umsatz",True)]):

            guest = get_cache (Guest, {"gastnr": [(eq, cust_list_detail.gastnr)]})

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_data.append(b_list)

                    b_list.cust_name = "T O T A L"
                    b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
                    b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.stayno = to_string(tot_stayno, ">>>,>>9")
                    b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
                    b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")
                    tot_logiernachte =  to_decimal("0")
                    tot_argtumsatz =  to_decimal("0")
                    tot_fb_umsatz =  to_decimal("0")
                    tot_sonst_umsatz =  to_decimal("0")
                    tot_ba_umsatz =  to_decimal("0")
                    tot_gesamtumsatz =  to_decimal("0")
                    tot_stayno =  to_decimal("0")
                    tot_lyear =  to_decimal("0")
                    tot_nofrm =  to_decimal("0")


                b_list = B_list()
                b_list_data.append(b_list)

                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno =  to_decimal(tot_stayno) + to_decimal(to_int(cust_list_detail.stayno) )
                gt_stayno =  to_decimal(gt_stayno) + to_decimal(to_int(cust_list_detail.stayno) )


            b_list = B_list()
            b_list_data.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte =  to_decimal(tot_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            tot_argtumsatz =  to_decimal(tot_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            tot_fb_umsatz =  to_decimal(tot_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            tot_sonst_umsatz =  to_decimal(tot_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            tot_ba_umsatz =  to_decimal(tot_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            tot_gesamtumsatz =  to_decimal(tot_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            tot_lyear =  to_decimal(tot_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            gt_logiernachte =  to_decimal(gt_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            gt_argtumsatz =  to_decimal(gt_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            gt_fb_umsatz =  to_decimal(gt_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            gt_sonst_umsatz =  to_decimal(gt_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            gt_ba_umsatz =  to_decimal(gt_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            gt_gesamtumsatz =  to_decimal(gt_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            gt_lyear =  to_decimal(gt_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "T O T A L"
            b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(tot_stayno, ">>>,>>9")
            b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")

        if gt_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "G R A N D T O T A L"
            b_list.f_b_umsatz = to_string(gt_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(gt_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(gt_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(gt_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(gt_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(gt_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(gt_stayno, ">>>,>>9")
            b_list.count_room = to_string(gt_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(gt_lyear, "->>>,>>>,>>>,>>9.99")


    elif sort_type == 7:

        for cust_list_detail in query(cust_list_detail_data, sort_by=[("gastnr",False),("wohnort",True)]):

            guest = get_cache (Guest, {"gastnr": [(eq, cust_list_detail.gastnr)]})

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_data.append(b_list)

                    b_list.cust_name = "T O T A L"
                    b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
                    b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.stayno = to_string(tot_stayno, ">>>,>>9")
                    b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
                    b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")
                    tot_logiernachte =  to_decimal("0")
                    tot_argtumsatz =  to_decimal("0")
                    tot_fb_umsatz =  to_decimal("0")
                    tot_sonst_umsatz =  to_decimal("0")
                    tot_ba_umsatz =  to_decimal("0")
                    tot_gesamtumsatz =  to_decimal("0")
                    tot_stayno =  to_decimal("0")
                    tot_lyear =  to_decimal("0")
                    tot_nofrm =  to_decimal("0")


                b_list = B_list()
                b_list_data.append(b_list)

                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno =  to_decimal(tot_stayno) + to_decimal(to_int(cust_list_detail.stayno) )
                gt_stayno =  to_decimal(gt_stayno) + to_decimal(to_int(cust_list_detail.stayno) )


            b_list = B_list()
            b_list_data.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte =  to_decimal(tot_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            tot_argtumsatz =  to_decimal(tot_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            tot_fb_umsatz =  to_decimal(tot_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            tot_sonst_umsatz =  to_decimal(tot_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            tot_ba_umsatz =  to_decimal(tot_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            tot_gesamtumsatz =  to_decimal(tot_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            tot_lyear =  to_decimal(tot_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            gt_logiernachte =  to_decimal(gt_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            gt_argtumsatz =  to_decimal(gt_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            gt_fb_umsatz =  to_decimal(gt_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            gt_sonst_umsatz =  to_decimal(gt_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            gt_ba_umsatz =  to_decimal(gt_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            gt_gesamtumsatz =  to_decimal(gt_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            gt_lyear =  to_decimal(gt_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "T O T A L"
            b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(tot_stayno, ">>>,>>9")
            b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")

        if gt_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "G R A N D T O T A L"
            b_list.f_b_umsatz = to_string(gt_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(gt_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(gt_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(gt_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(gt_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(gt_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(gt_stayno, ">>>,>>9")
            b_list.count_room = to_string(gt_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(gt_lyear, "->>>,>>>,>>>,>>9.99")


    elif sort_type == 8:

        for cust_list_detail in query(cust_list_detail_data, sort_by=[("gastnr",False),("plz",True)]):

            guest = get_cache (Guest, {"gastnr": [(eq, cust_list_detail.gastnr)]})

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_data.append(b_list)

                    b_list.cust_name = "T O T A L"
                    b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
                    b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.stayno = to_string(tot_stayno, ">>>,>>9")
                    b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
                    b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")
                    tot_logiernachte =  to_decimal("0")
                    tot_argtumsatz =  to_decimal("0")
                    tot_fb_umsatz =  to_decimal("0")
                    tot_sonst_umsatz =  to_decimal("0")
                    tot_ba_umsatz =  to_decimal("0")
                    tot_gesamtumsatz =  to_decimal("0")
                    tot_stayno =  to_decimal("0")
                    tot_lyear =  to_decimal("0")
                    tot_nofrm =  to_decimal("0")


                b_list = B_list()
                b_list_data.append(b_list)

                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno =  to_decimal(tot_stayno) + to_decimal(to_int(cust_list_detail.stayno) )
                gt_stayno =  to_decimal(gt_stayno) + to_decimal(to_int(cust_list_detail.stayno) )


            b_list = B_list()
            b_list_data.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte =  to_decimal(tot_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            tot_argtumsatz =  to_decimal(tot_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            tot_fb_umsatz =  to_decimal(tot_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            tot_sonst_umsatz =  to_decimal(tot_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            tot_ba_umsatz =  to_decimal(tot_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            tot_gesamtumsatz =  to_decimal(tot_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            tot_lyear =  to_decimal(tot_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            gt_logiernachte =  to_decimal(gt_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            gt_argtumsatz =  to_decimal(gt_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            gt_fb_umsatz =  to_decimal(gt_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            gt_sonst_umsatz =  to_decimal(gt_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            gt_ba_umsatz =  to_decimal(gt_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            gt_gesamtumsatz =  to_decimal(gt_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            gt_lyear =  to_decimal(gt_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "T O T A L"
            b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(tot_stayno, ">>>,>>9")
            b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")

        if gt_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "G R A N D T O T A L"
            b_list.f_b_umsatz = to_string(gt_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(gt_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(gt_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(gt_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(gt_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(gt_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(gt_stayno, ">>>,>>9")
            b_list.count_room = to_string(gt_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(gt_lyear, "->>>,>>>,>>>,>>9.99")


    elif sort_type == 9:

        for cust_list_detail in query(cust_list_detail_data, sort_by=[("gastnr",False),("land",True)]):

            guest = get_cache (Guest, {"gastnr": [(eq, cust_list_detail.gastnr)]})

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_data.append(b_list)

                    b_list.cust_name = "T O T A L"
                    b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
                    b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.stayno = to_string(tot_stayno, ">>>,>>9")
                    b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
                    b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")
                    tot_logiernachte =  to_decimal("0")
                    tot_argtumsatz =  to_decimal("0")
                    tot_fb_umsatz =  to_decimal("0")
                    tot_sonst_umsatz =  to_decimal("0")
                    tot_ba_umsatz =  to_decimal("0")
                    tot_gesamtumsatz =  to_decimal("0")
                    tot_stayno =  to_decimal("0")
                    tot_lyear =  to_decimal("0")
                    tot_nofrm =  to_decimal("0")


                b_list = B_list()
                b_list_data.append(b_list)

                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno =  to_decimal(tot_stayno) + to_decimal(to_int(cust_list_detail.stayno) )
                gt_stayno =  to_decimal(gt_stayno) + to_decimal(to_int(cust_list_detail.stayno) )


            b_list = B_list()
            b_list_data.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte =  to_decimal(tot_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            tot_argtumsatz =  to_decimal(tot_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            tot_fb_umsatz =  to_decimal(tot_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            tot_sonst_umsatz =  to_decimal(tot_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            tot_ba_umsatz =  to_decimal(tot_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            tot_gesamtumsatz =  to_decimal(tot_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            tot_lyear =  to_decimal(tot_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            gt_logiernachte =  to_decimal(gt_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            gt_argtumsatz =  to_decimal(gt_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            gt_fb_umsatz =  to_decimal(gt_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            gt_sonst_umsatz =  to_decimal(gt_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            gt_ba_umsatz =  to_decimal(gt_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            gt_gesamtumsatz =  to_decimal(gt_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            gt_lyear =  to_decimal(gt_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "T O T A L"
            b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(tot_stayno, ">>>,>>9")
            b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")

        if gt_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "G R A N D T O T A L"
            b_list.f_b_umsatz = to_string(gt_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(gt_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(gt_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(gt_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(gt_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(gt_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(gt_stayno, ">>>,>>9")
            b_list.count_room = to_string(gt_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(gt_lyear, "->>>,>>>,>>>,>>9.99")


    elif sort_type == 10:

        for cust_list_detail in query(cust_list_detail_data, sort_by=[("gastnr",False),("resnr",True)]):

            guest = get_cache (Guest, {"gastnr": [(eq, cust_list_detail.gastnr)]})

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_data.append(b_list)

                    b_list.cust_name = "T O T A L"
                    b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
                    b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.stayno = to_string(tot_stayno, ">>>,>>9")
                    b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
                    b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")
                    tot_logiernachte =  to_decimal("0")
                    tot_argtumsatz =  to_decimal("0")
                    tot_fb_umsatz =  to_decimal("0")
                    tot_sonst_umsatz =  to_decimal("0")
                    tot_ba_umsatz =  to_decimal("0")
                    tot_gesamtumsatz =  to_decimal("0")
                    tot_stayno =  to_decimal("0")
                    tot_lyear =  to_decimal("0")
                    tot_nofrm =  to_decimal("0")


                b_list = B_list()
                b_list_data.append(b_list)

                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno =  to_decimal(tot_stayno) + to_decimal(to_int(cust_list_detail.stayno) )
                gt_stayno =  to_decimal(gt_stayno) + to_decimal(to_int(cust_list_detail.stayno) )


            b_list = B_list()
            b_list_data.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte =  to_decimal(tot_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            tot_argtumsatz =  to_decimal(tot_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            tot_fb_umsatz =  to_decimal(tot_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            tot_sonst_umsatz =  to_decimal(tot_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            tot_ba_umsatz =  to_decimal(tot_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            tot_gesamtumsatz =  to_decimal(tot_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            tot_lyear =  to_decimal(tot_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            gt_logiernachte =  to_decimal(gt_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            gt_argtumsatz =  to_decimal(gt_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            gt_fb_umsatz =  to_decimal(gt_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            gt_sonst_umsatz =  to_decimal(gt_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            gt_ba_umsatz =  to_decimal(gt_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            gt_gesamtumsatz =  to_decimal(gt_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            gt_lyear =  to_decimal(gt_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "T O T A L"
            b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(tot_stayno, ">>>,>>9")
            b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")

        if gt_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "G R A N D T O T A L"
            b_list.f_b_umsatz = to_string(gt_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(gt_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(gt_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(gt_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(gt_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(gt_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(gt_stayno, ">>>,>>9")
            b_list.count_room = to_string(gt_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(gt_lyear, "->>>,>>>,>>>,>>9.99")


    elif sort_type == 11:

        for cust_list_detail in query(cust_list_detail_data, sort_by=[("gastnr",False),("ly_rev",True)]):

            guest = get_cache (Guest, {"gastnr": [(eq, cust_list_detail.gastnr)]})

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_data.append(b_list)

                    b_list.cust_name = "T O T A L"
                    b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
                    b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.stayno = to_string(tot_stayno, ">>>,>>9")
                    b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
                    b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")
                    tot_logiernachte =  to_decimal("0")
                    tot_argtumsatz =  to_decimal("0")
                    tot_fb_umsatz =  to_decimal("0")
                    tot_sonst_umsatz =  to_decimal("0")
                    tot_ba_umsatz =  to_decimal("0")
                    tot_gesamtumsatz =  to_decimal("0")
                    tot_stayno =  to_decimal("0")
                    tot_lyear =  to_decimal("0")
                    tot_nofrm =  to_decimal("0")


                b_list = B_list()
                b_list_data.append(b_list)

                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno =  to_decimal(tot_stayno) + to_decimal(to_int(cust_list_detail.stayno) )
                gt_stayno =  to_decimal(gt_stayno) + to_decimal(to_int(cust_list_detail.stayno) )


            b_list = B_list()
            b_list_data.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte =  to_decimal(tot_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            tot_argtumsatz =  to_decimal(tot_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            tot_fb_umsatz =  to_decimal(tot_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            tot_sonst_umsatz =  to_decimal(tot_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            tot_ba_umsatz =  to_decimal(tot_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            tot_gesamtumsatz =  to_decimal(tot_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            tot_lyear =  to_decimal(tot_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            gt_logiernachte =  to_decimal(gt_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            gt_argtumsatz =  to_decimal(gt_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            gt_fb_umsatz =  to_decimal(gt_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            gt_sonst_umsatz =  to_decimal(gt_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            gt_ba_umsatz =  to_decimal(gt_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            gt_gesamtumsatz =  to_decimal(gt_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            gt_lyear =  to_decimal(gt_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "T O T A L"
            b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(tot_stayno, ">>>,>>9")
            b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")

        if gt_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "G R A N D T O T A L"
            b_list.f_b_umsatz = to_string(gt_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(gt_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(gt_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(gt_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(gt_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(gt_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(gt_stayno, ">>>,>>9")
            b_list.count_room = to_string(gt_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(gt_lyear, "->>>,>>>,>>>,>>9.99")


    elif sort_type == 12:

        for cust_list_detail in query(cust_list_detail_data, sort_by=[("gastnr",False),("count_room",True)]):

            guest = get_cache (Guest, {"gastnr": [(eq, cust_list_detail.gastnr)]})

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_data.append(b_list)

                    b_list.cust_name = "T O T A L"
                    b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
                    b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.stayno = to_string(tot_stayno, ">>>,>>9")
                    b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
                    b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")
                    tot_logiernachte =  to_decimal("0")
                    tot_argtumsatz =  to_decimal("0")
                    tot_fb_umsatz =  to_decimal("0")
                    tot_sonst_umsatz =  to_decimal("0")
                    tot_ba_umsatz =  to_decimal("0")
                    tot_gesamtumsatz =  to_decimal("0")
                    tot_stayno =  to_decimal("0")
                    tot_lyear =  to_decimal("0")
                    tot_nofrm =  to_decimal("0")


                b_list = B_list()
                b_list_data.append(b_list)

                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno =  to_decimal(tot_stayno) + to_decimal(to_int(cust_list_detail.stayno) )
                gt_stayno =  to_decimal(gt_stayno) + to_decimal(to_int(cust_list_detail.stayno) )


            b_list = B_list()
            b_list_data.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte =  to_decimal(tot_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            tot_argtumsatz =  to_decimal(tot_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            tot_fb_umsatz =  to_decimal(tot_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            tot_sonst_umsatz =  to_decimal(tot_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            tot_ba_umsatz =  to_decimal(tot_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            tot_gesamtumsatz =  to_decimal(tot_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            tot_lyear =  to_decimal(tot_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            gt_logiernachte =  to_decimal(gt_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            gt_argtumsatz =  to_decimal(gt_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            gt_fb_umsatz =  to_decimal(gt_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            gt_sonst_umsatz =  to_decimal(gt_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            gt_ba_umsatz =  to_decimal(gt_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            gt_gesamtumsatz =  to_decimal(gt_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            gt_lyear =  to_decimal(gt_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "T O T A L"
            b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(tot_stayno, ">>>,>>9")
            b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")

        if gt_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "G R A N D T O T A L"
            b_list.f_b_umsatz = to_string(gt_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(gt_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(gt_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(gt_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(gt_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(gt_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(gt_stayno, ">>>,>>9")
            b_list.count_room = to_string(gt_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(gt_lyear, "->>>,>>>,>>>,>>9.99")


    elif sort_type == 13:

        for cust_list_detail in query(cust_list_detail_data, sort_by=[("gastnr",False),("region",False)]):

            guest = get_cache (Guest, {"gastnr": [(eq, cust_list_detail.gastnr)]})

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_data.append(b_list)

                    b_list.cust_name = "T O T A L"
                    b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
                    b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.stayno = to_string(tot_stayno, ">>>,>>9")
                    b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
                    b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")
                    tot_logiernachte =  to_decimal("0")
                    tot_argtumsatz =  to_decimal("0")
                    tot_fb_umsatz =  to_decimal("0")
                    tot_sonst_umsatz =  to_decimal("0")
                    tot_ba_umsatz =  to_decimal("0")
                    tot_gesamtumsatz =  to_decimal("0")
                    tot_stayno =  to_decimal("0")
                    tot_lyear =  to_decimal("0")
                    tot_nofrm =  to_decimal("0")


                b_list = B_list()
                b_list_data.append(b_list)

                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno =  to_decimal(tot_stayno) + to_decimal(to_int(cust_list_detail.stayno) )
                gt_stayno =  to_decimal(gt_stayno) + to_decimal(to_int(cust_list_detail.stayno) )


            b_list = B_list()
            b_list_data.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte =  to_decimal(tot_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            tot_argtumsatz =  to_decimal(tot_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            tot_fb_umsatz =  to_decimal(tot_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            tot_sonst_umsatz =  to_decimal(tot_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            tot_ba_umsatz =  to_decimal(tot_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            tot_gesamtumsatz =  to_decimal(tot_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            tot_lyear =  to_decimal(tot_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            gt_logiernachte =  to_decimal(gt_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            gt_argtumsatz =  to_decimal(gt_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            gt_fb_umsatz =  to_decimal(gt_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            gt_sonst_umsatz =  to_decimal(gt_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            gt_ba_umsatz =  to_decimal(gt_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            gt_gesamtumsatz =  to_decimal(gt_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            gt_lyear =  to_decimal(gt_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "T O T A L"
            b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(tot_stayno, ">>>,>>9")
            b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")

        if gt_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "G R A N D T O T A L"
            b_list.f_b_umsatz = to_string(gt_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(gt_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(gt_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(gt_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(gt_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(gt_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(gt_stayno, ">>>,>>9")
            b_list.count_room = to_string(gt_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(gt_lyear, "->>>,>>>,>>>,>>9.99")


    elif sort_type == 14:

        for cust_list_detail in query(cust_list_detail_data, sort_by=[("gastnr",False),("ba_umsatz",True)]):

            guest = get_cache (Guest, {"gastnr": [(eq, cust_list_detail.gastnr)]})

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_data.append(b_list)

                    b_list.cust_name = "T O T A L"
                    b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
                    b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
                    b_list.stayno = to_string(tot_stayno, ">>>,>>9")
                    b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
                    b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")
                    tot_logiernachte =  to_decimal("0")
                    tot_argtumsatz =  to_decimal("0")
                    tot_fb_umsatz =  to_decimal("0")
                    tot_sonst_umsatz =  to_decimal("0")
                    tot_ba_umsatz =  to_decimal("0")
                    tot_gesamtumsatz =  to_decimal("0")
                    tot_stayno =  to_decimal("0")
                    tot_lyear =  to_decimal("0")
                    tot_nofrm =  to_decimal("0")


                b_list = B_list()
                b_list_data.append(b_list)

                b_list = B_list()
                b_list_data.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno =  to_decimal(tot_stayno) + to_decimal(to_int(cust_list_detail.stayno) )
                gt_stayno =  to_decimal(gt_stayno) + to_decimal(to_int(cust_list_detail.stayno) )


            b_list = B_list()
            b_list_data.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte =  to_decimal(tot_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            tot_argtumsatz =  to_decimal(tot_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            tot_fb_umsatz =  to_decimal(tot_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            tot_sonst_umsatz =  to_decimal(tot_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            tot_ba_umsatz =  to_decimal(tot_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            tot_gesamtumsatz =  to_decimal(tot_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            tot_lyear =  to_decimal(tot_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            tot_nofrm =  to_decimal(tot_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            gt_logiernachte =  to_decimal(gt_logiernachte) + to_decimal(to_decimal(cust_list_detail.logiernachte) )
            gt_argtumsatz =  to_decimal(gt_argtumsatz) + to_decimal(to_decimal(cust_list_detail.argtumsatz) )
            gt_fb_umsatz =  to_decimal(gt_fb_umsatz) + to_decimal(to_decimal(cust_list_detail.f_b_umsatz) )
            gt_sonst_umsatz =  to_decimal(gt_sonst_umsatz) + to_decimal(to_decimal(cust_list_detail.sonst_umsatz) )
            gt_ba_umsatz =  to_decimal(gt_ba_umsatz) + to_decimal(to_decimal(cust_list_detail.ba_umsatz) )
            gt_gesamtumsatz =  to_decimal(gt_gesamtumsatz) + to_decimal(to_decimal(cust_list_detail.gesamtumsatz) )
            gt_lyear =  to_decimal(gt_lyear) + to_decimal(to_decimal(cust_list_detail.ly_rev) )
            gt_nofrm =  to_decimal(gt_nofrm) + to_decimal(to_decimal(cust_list_detail.count_room) )
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "T O T A L"
            b_list.f_b_umsatz = to_string(tot_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(tot_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(tot_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(tot_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(tot_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(tot_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(tot_stayno, ">>>,>>9")
            b_list.count_room = to_string(tot_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(tot_lyear, "->>>,>>>,>>>,>>9.99")

        if gt_gesamtumsatz != 0:
            b_list = B_list()
            b_list_data.append(b_list)

            b_list.cust_name = "G R A N D T O T A L"
            b_list.f_b_umsatz = to_string(gt_fb_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.sonst_umsatz = to_string(gt_sonst_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.argtumsatz = to_string(gt_argtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.gesamtumsatz = to_string(gt_gesamtumsatz, "->>>,>>>,>>>,>>9.99")
            b_list.logiernachte = to_string(gt_logiernachte, ">>>,>>9")
            b_list.ba_umsatz = to_string(gt_ba_umsatz, "->>>,>>>,>>>,>>9.99")
            b_list.stayno = to_string(gt_stayno, ">>>,>>9")
            b_list.count_room = to_string(gt_nofrm, ">>,>>>,>>>,>>9")
            b_list.ly_rev = to_string(gt_lyear, "->>>,>>>,>>>,>>9.99")

    return generate_output()