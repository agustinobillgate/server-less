from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.get_room_breakdown import get_room_breakdown
from models import Genstat, Guest, Bill_line, Bill, Htparam, Waehrung, Nation, Queasy, exrate, Res_line, Artikel, Guest_queasy, Reservation, Sourccod, Segment, Arrangement, Zimmer

def cust_turnover_sorting_detail_1bl(cardtype:int, sort_type:int, fdate:date, tdate:date, check_ftd:bool, currency:str, excl_other:bool, curr_sort2:int):
    b_list_list = []
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
    curr_gname:str = ""
    curr_gastnr2:int = 0
    t_logiernachte:decimal = 0
    t_argtumsatz:decimal = 0
    t_fb_umsatz:decimal = 0
    t_sonst_umsatz:decimal = 0
    t_ba_umsatz:decimal = 0
    t_gesamtumsatz:decimal = 0
    t_lyear:decimal = 0
    t_nofrm:decimal = 0
    tot_logiernachte:decimal = 0
    tot_argtumsatz:decimal = 0
    tot_fb_umsatz:decimal = 0
    tot_sonst_umsatz:decimal = 0
    tot_ba_umsatz:decimal = 0
    tot_gesamtumsatz:decimal = 0
    tot_stayno:decimal = 0
    tot_lyear:decimal = 0
    tot_nofrm:decimal = 0
    gt_logiernachte:decimal = 0
    gt_argtumsatz:decimal = 0
    gt_fb_umsatz:decimal = 0
    gt_sonst_umsatz:decimal = 0
    gt_ba_umsatz:decimal = 0
    gt_gesamtumsatz:decimal = 0
    gt_stayno:decimal = 0
    gt_lyear:decimal = 0
    gt_nofrm:decimal = 0
    curr_resnr1:int = 0
    curr_reslinnr1:int = 0
    found1:bool = False
    loopj:int = 0
    exratenr:int = 0
    exrate:decimal = 0
    genstat = guest = bill_line = bill = htparam = waehrung = nation = queasy = exrate = res_line = artikel = guest_queasy = reservation = sourccod = segment = arrangement = zimmer = None

    cust_list_detail = b_list = t_genstat = blist = glist = bguest = clist = bline = bbuf = None

    cust_list_detail_list, Cust_list_detail = create_model("Cust_list_detail", {"gastnr":int, "cust_name":str, "gname":str, "gesamtumsatz":str, "logiernachte":str, "argtumsatz":str, "f_b_umsatz":str, "sonst_umsatz":str, "wohnort":str, "plz":str, "land":str, "sales_id":str, "ba_umsatz":str, "ly_rev":str, "region":str, "region1":str, "stayno":str, "resnr":str, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int, "count_room":str, "rm_sharer":str, "arrival":date, "depart":date})
    b_list_list, B_list = create_model("B_list", {"gastnr":int, "cust_name":str, "gname":str, "gesamtumsatz":str, "logiernachte":str, "argtumsatz":str, "f_b_umsatz":str, "sonst_umsatz":str, "wohnort":str, "plz":str, "land":str, "sales_id":str, "ba_umsatz":str, "ly_rev":str, "region":str, "region1":str, "stayno":str, "resnr":str, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int, "count_room":str, "rm_sharer":str, "arrival":date, "depart":date})

    T_genstat = Genstat
    Blist = Cust_list_detail
    blist_list = cust_list_detail_list

    Glist = Guest
    Bguest = Guest
    Clist = Cust_list_detail
    clist_list = cust_list_detail_list

    Bline = Bill_line
    Bbuf = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b_list_list, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_resnr, curr_reslinnr, curr_gname, curr_gastnr2, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, t_lyear, t_nofrm, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, tot_lyear, tot_nofrm, gt_logiernachte, gt_argtumsatz, gt_fb_umsatz, gt_sonst_umsatz, gt_ba_umsatz, gt_gesamtumsatz, gt_stayno, gt_lyear, gt_nofrm, curr_resnr1, curr_reslinnr1, found1, loopj, exratenr, exrate, genstat, guest, bill_line, bill, htparam, waehrung, nation, queasy, exrate, res_line, artikel, guest_queasy, reservation, sourccod, segment, arrangement, zimmer
        nonlocal t_genstat, blist, glist, bguest, clist, bline, bbuf


        nonlocal cust_list_detail, b_list, t_genstat, blist, glist, bguest, clist, bline, bbuf
        nonlocal cust_list_detail_list, b_list_list
        return {"b-list": b_list_list}

    def create_detail():

        nonlocal b_list_list, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_resnr, curr_reslinnr, curr_gname, curr_gastnr2, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, t_lyear, t_nofrm, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, tot_lyear, tot_nofrm, gt_logiernachte, gt_argtumsatz, gt_fb_umsatz, gt_sonst_umsatz, gt_ba_umsatz, gt_gesamtumsatz, gt_stayno, gt_lyear, gt_nofrm, curr_resnr1, curr_reslinnr1, found1, loopj, exratenr, exrate, genstat, guest, bill_line, bill, htparam, waehrung, nation, queasy, exrate, res_line, artikel, guest_queasy, reservation, sourccod, segment, arrangement, zimmer
        nonlocal t_genstat, blist, glist, bguest, clist, bline, bbuf


        nonlocal cust_list_detail, b_list, t_genstat, blist, glist, bguest, clist, bline, bbuf
        nonlocal cust_list_detail_list, b_list_list

        if currency != "":

            waehrung = db_session.query(Waehrung).filter(
                    (func.lower(Waehrung.wabkurz) == (currency).lower())).first()

            if waehrung:
                exratenr = waehrungsnr
                exrate = waehrung.ankauf

        if cardtype == 3:

            if not check_ftd:

                genstat_obj_list = []
                for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                        (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                    if genstat._recid in genstat_obj_list:
                        continue
                    else:
                        genstat_obj_list.append(genstat._recid)

                    bguest = db_session.query(Bguest).filter(
                            (Bguest.gastnr == genstat.gastnrmember)).first()

                    cust_list_detail = query(cust_list_detail_list, filters=(lambda cust_list_detail :cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gname == bguest.name), first=True)

                    if not cust_list_detail:
                        cust_list_detail = Cust_list_detail()
                        cust_list_detail_list.append(cust_list_detail)

                        cust_list_detail.gastnr = genstat.gastnr
                        cust_list_detail.resno = genstat.resnr
                        cust_list_detail.reslinnr = genstat.res_int[0]
                        cust_list_detail.gname = bguest.name
                        cust_list_detail.arrival = genstat.res_date[0]
                        cust_list_detail.depart = genstat.res_date[1]

                        glist = db_session.query(Glist).filter(
                                (Glist.gastnr == genstat.gastnrmember)).first()

                        if glist:
                            cust_list_detail.cust_name = glist.name + "," + glist.anredefirma + " " + glist.vorname1
                            cust_list_detail.plz = glist.plz
                            cust_list_detail.land = glist.land
                            cust_list_detail.sales_id = glist.phonetik3
                            cust_list_detail.wohnort = glist.wohnort

                            nation = db_session.query(Nation).filter(
                                    (Nation.kurzbez == glist.land)).first()

                            if nation:

                                queasy = db_session.query(Queasy).filter(
                                        (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                                if queasy:
                                    cust_list_detail.region = queasy.char1
                            else:
                                cust_list_detail.region = "UNKOWN"
                        else:
                            cust_list_detail.cust_name = guest.name + "," + guest.anredefirma + " " + guest.vorname1
                            cust_list_detail.plz = guest.plz
                            cust_list_detail.land = guest.land
                            cust_list_detail.sales_id = guest.phonetik3
                            cust_list_detail.wohnort = guest.wohnort

                            nation = db_session.query(Nation).filter(
                                    (Nation.kurzbez == guest.land)).first()

                            if nation:

                                queasy = db_session.query(Queasy).filter(
                                        (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                                if queasy:
                                    cust_list_detail.region = queasy.char1
                            else:
                                cust_list_detail.region = "UNKOWN"
                    found1 = False

                    clist = query(clist_list, filters=(lambda clist :clist.gastnr == genstat.gastnr and clist.gname == bguest.name), first=True)

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

                        exrate = db_session.query(exrate).filter(
                                (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                        if exrate:
                            cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + ((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (genstat.res_deci[4] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.argtumsatz = to_string(decimal.Decimal(cust_list_detail.argtumsatz) + (genstat.logis / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + ((genstat.logis + genstat.res_deci[1] +\
                                    genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.ba_umsatz = to_string(decimal.Decimal(cust_list_detail.ba_umsatz) + (genstat.res_deci[6] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                    else:
                        cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + (genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + genstat.res_deci[4], "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.argtumsatz = to_string(decimal.Decimal(cust_list_detail.argtumsatz) + genstat.logis, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + genstat.logis + genstat.res_deci[1] +\
                                genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4] , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.ba_umsatz = to_string(decimal.Decimal(cust_list_detail.ba_umsatz) + genstat.res_deci[6], "->>>,>>>,>>>,>>9.99")

                    if genstat.resstatus != 13:
                        cust_list_detail.logiernachte = to_string(to_int(cust_list_detail.logiernachte) + 1, ">>>,>>9")


                    else:
                        cust_list_detail.rm_sharer = "*"

                    if curr_resnr1 != genstat.resnr or curr_reslinnr1 != genstat.res_int[0]:
                        curr_resnr1 = genstat.resnr
                        curr_reslinnr1 = genstat.res_int[0]

                        if genstat.resstatus == 6:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                            if res_line:
                                cust_list_detail.count_room = to_string(to_int(cust_list_detail.count_room) + res_line.zimmeranz, ">>,>>>,>>>,>>9")

                        if excl_other == False:

                            for bill in db_session.query(Bill).filter(
                                    (Bill.resnr == genstat.resnr) &  (Bill.reslinnr == genstat.res_int[0])).all():

                                bill_line_obj_list = []
                                for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) &  (Artikel.departement == Bill_line.departement) &  (Artikel.artart == 0)).filter(
                                        (Bill_line.rechnr == bill.rechnr) &  (Bill_line.bill_datum == genstat.datum)).all():
                                    if bill_line._recid in bill_line_obj_list:
                                        continue
                                    else:
                                        bill_line_obj_list.append(bill_line._recid)

                                    if currency != " ":

                                        exrate = db_session.query(exrate).filter(
                                                (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                        if exrate:
                                            cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (bill_line.betrag / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                            cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + (bill_line.betrag / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                                    else:
                                        cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + bill_line.betrag, "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + bill_line.betrag, "->>>,>>>,>>>,>>9.99")

                if excl_other == False:

                    for guest_queasy in db_session.query(Guest_queasy).filter(
                            (func.lower(Guest_queasy.key) == "gast_info") &  (Guest_queasy.date1 >= fdate) &  (Guest_queasy.date1 <= tdate)).all():

                        genstat = db_session.query(Genstat).filter(
                                (Genstat.resnr == guest_queasy.number2) &  (Genstat.res_int[0] == guest_queasy.number3) &  (Genstat.datum == guest_queasy.date1) &  (Genstat.res_logic[1])).first()

                        if genstat:

                            bguest = db_session.query(Bguest).filter(
                                    (Bguest.gastnr == genstat.gastnrmember)).first()

                            cust_list_detail = query(cust_list_detail_list, filters=(lambda cust_list_detail :cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gname == bguest.name), first=True)

                            if cust_list_detail:

                                if currency != " ":

                                    exrate = db_session.query(exrate).filter(
                                            (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                    if exrate:
                                        cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + ((guest_queasy.deci1 + guest_queasy.deci2) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (guest_queasy.deci3 / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + ((guest_queasy.deci1 + guest_queasy.deci2 +\
                                            guest_queasy.deci3) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                                else:
                                    cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + guest_queasy.deci1 + guest_queasy.deci2, "->>>,>>>,>>>,>>9.99")
                                    cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + guest_queasy.deci3, "->>>,>>>,>>>,>>9.99")
                                    cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + guest_queasy.deci1 + guest_queasy.deci2 +\
                                        guest_queasy.deci3, "->>>,>>>,>>>,>>9.99")


            else:
                cr_ftd1()

            if tdate != None and tdate >= ci_date and check_ftd:
                create_forecast1()
        else:

            if not check_ftd:

                genstat_obj_list = []
                for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr) &  (Guest.karteityp == cardtype)).filter(
                        (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
                    if genstat._recid in genstat_obj_list:
                        continue
                    else:
                        genstat_obj_list.append(genstat._recid)

                    bguest = db_session.query(Bguest).filter(
                            (Bguest.gastnr == genstat.gastnrmember)).first()

                    cust_list_detail = query(cust_list_detail_list, filters=(lambda cust_list_detail :cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gname == bguest.name), first=True)

                    if not cust_list_detail:
                        cust_list_detail = Cust_list_detail()
                        cust_list_detail_list.append(cust_list_detail)

                        cust_list_detail.gastnr = genstat.gastnr
                        cust_list_detail.resno = genstat.resnr
                        cust_list_detail.reslinnr = genstat.res_int[0]
                        cust_list_detail.gname = bguest.name

                        glist = db_session.query(Glist).filter(
                                (Glist.gastnr == genstat.gastnrmember)).first()

                        if glist:
                            cust_list_detail.cust_name = glist.name + "," + glist.anredefirma + " " + glist.vorname1
                            cust_list_detail.plz = glist.plz
                            cust_list_detail.land = glist.land
                            cust_list_detail.sales_id = glist.phonetik3
                            cust_list_detail.wohnort = glist.wohnort

                            nation = db_session.query(Nation).filter(
                                    (Nation.kurzbez == glist.land)).first()

                            if nation:

                                queasy = db_session.query(Queasy).filter(
                                        (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                                if queasy:
                                    cust_list_detail.region = queasy.char1
                            else:
                                cust_list_detail.region = "UNKOWN"
                        else:
                            cust_list_detail.cust_name = guest.name + "," + guest.anredefirma + " " + guest.vorname1
                            cust_list_detail.plz = guest.plz
                            cust_list_detail.land = guest.land
                            cust_list_detail.sales_id = guest.phonetik3
                            cust_list_detail.wohnort = guest.wohnort

                            nation = db_session.query(Nation).filter(
                                    (Nation.kurzbez == guest.land)).first()

                            if nation:

                                queasy = db_session.query(Queasy).filter(
                                        (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                                if queasy:
                                    cust_list_detail.region = queasy.char1
                            else:
                                cust_list_detail.region = "UNKOWN"
                    found1 = False

                    clist = query(clist_list, filters=(lambda clist :clist.gastnr == genstat.gastnr and clist.gname == bguest.name), first=True)

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

                        exrate = db_session.query(exrate).filter(
                                (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                        if exrate:
                            cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + ((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (genstat.res_deci[4] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.argtumsatz = to_string(decimal.Decimal(cust_list_detail.argtumsatz) + (genstat.logis / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + ((genstat.logis + genstat.res_deci[1] +\
                                    genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.ba_umsatz = to_string(decimal.Decimal(cust_list_detail.ba_umsatz) + (genstat.res_deci[6] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                    else:
                        cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + (genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + genstat.res_deci[4], "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.argtumsatz = to_string(decimal.Decimal(cust_list_detail.argtumsatz) + genstat.logis, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + genstat.logis + genstat.res_deci[1] +\
                                genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4] , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.ba_umsatz = to_string(decimal.Decimal(cust_list_detail.ba_umsatz) + genstat.res_deci[6], "->>>,>>>,>>>,>>9.99")

                    if genstat.resstatus != 13:
                        cust_list_detail.logiernachte = to_string(to_int(cust_list_detail.logiernachte) + 1, ">>>,>>9")


                    else:
                        cust_list_detail.rm_sharer = "*"

                    if curr_resnr1 != genstat.resnr or curr_reslinnr1 != genstat.res_int[0]:
                        curr_resnr1 = genstat.resnr
                        curr_reslinnr1 = genstat.res_int[0]

                        if genstat.resstatus == 6:

                            res_line = db_session.query(Res_line).filter(
                                    (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                            if res_line:
                                cust_list_detail.count_room = to_string(to_int(cust_list_detail.count_room) + res_line.zimmeranz, ">>,>>>,>>>,>>9")

                        if excl_other == False:

                            for bill in db_session.query(Bill).filter(
                                    (Bill.resnr == genstat.resnr) &  (Bill.reslinnr == genstat.res_int[0])).all():

                                bill_line_obj_list = []
                                for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) &  (Artikel.departement == Bill_line.departement) &  (Artikel.artart == 0)).filter(
                                        (Bill_line.rechnr == bill.rechnr) &  (Bill_line.bill_datum == genstat.datum)).all():
                                    if bill_line._recid in bill_line_obj_list:
                                        continue
                                    else:
                                        bill_line_obj_list.append(bill_line._recid)

                                    if currency != " ":

                                        exrate = db_session.query(exrate).filter(
                                                (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                        if exrate:
                                            cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (bill_line.betrag / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                            cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + (bill_line.betrag / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                                    else:
                                        cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + bill_line.betrag, "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + bill_line.betrag, "->>>,>>>,>>>,>>9.99")

                if excl_other == False:

                    for guest_queasy in db_session.query(Guest_queasy).filter(
                            (func.lower(Guest_queasy.key) == "gast_info") &  (Guest_queasy.date1 >= fdate) &  (Guest_queasy.date1 <= tdate)).all():

                        genstat = db_session.query(Genstat).filter(
                                (Genstat.resnr == guest_queasy.number2) &  (Genstat.res_int[0] == guest_queasy.number3) &  (Genstat.datum == guest_queasy.date1) &  (Genstat.res_logic[1])).first()

                        if genstat:

                            bguest = db_session.query(Bguest).filter(
                                    (Bguest.gastnr == genstat.gastnrmember)).first()

                            cust_list_detail = query(cust_list_detail_list, filters=(lambda cust_list_detail :cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gname == bguest.name), first=True)

                            if cust_list_detail:

                                if currency != " ":

                                    exrate = db_session.query(exrate).filter(
                                            (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                    if exrate:
                                        cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + ((guest_queasy.deci1 + guest_queasy.deci2) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (guest_queasy.deci3 / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + ((guest_queasy.deci1 + guest_queasy.deci2 +\
                                            guest_queasy.deci3) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                                else:
                                    cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + guest_queasy.deci1 + guest_queasy.deci2, "->>>,>>>,>>>,>>9.99")
                                    cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + guest_queasy.deci3, "->>>,>>>,>>>,>>9.99")
                                    cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + guest_queasy.deci1 + guest_queasy.deci2 +\
                                        guest_queasy.deci3, "->>>,>>>,>>>,>>9.99")


            else:
                cr_ftd()

            if tdate != None and tdate >= ci_date and check_ftd:
                create_forecast()

    def cr_ftd():

        nonlocal b_list_list, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_resnr, curr_reslinnr, curr_gname, curr_gastnr2, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, t_lyear, t_nofrm, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, tot_lyear, tot_nofrm, gt_logiernachte, gt_argtumsatz, gt_fb_umsatz, gt_sonst_umsatz, gt_ba_umsatz, gt_gesamtumsatz, gt_stayno, gt_lyear, gt_nofrm, curr_resnr1, curr_reslinnr1, found1, loopj, exratenr, exrate, genstat, guest, bill_line, bill, htparam, waehrung, nation, queasy, exrate, res_line, artikel, guest_queasy, reservation, sourccod, segment, arrangement, zimmer
        nonlocal t_genstat, blist, glist, bguest, clist, bline, bbuf


        nonlocal cust_list_detail, b_list, t_genstat, blist, glist, bguest, clist, bline, bbuf
        nonlocal cust_list_detail_list, b_list_list

        t_argtumsatz:int = 0
        rate:decimal = 1
        frate:decimal = 1
        rmnite:int = 0
        curr_resnr:int = 0
        curr_reslinnr:int = 0
        loopi:int = 0
        found:bool = False
        Clist = Cust_list_detail

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr) &  (Guest.karteityp == cardtype)).filter(
                (Genstat.datum >= fdate) &  (Genstat.datum <= tdate) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            bguest = db_session.query(Bguest).filter(
                    (Bguest.gastnr == genstat.gastnrmember)).first()

            cust_list_detail = query(cust_list_detail_list, filters=(lambda cust_list_detail :cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gname == bguest.name), first=True)

            if not cust_list_detail:
                cust_list_detail = Cust_list_detail()
                cust_list_detail_list.append(cust_list_detail)

                cust_list_detail.gastnr = genstat.gastnr
                cust_list_detail.resno = genstat.resnr
                cust_list_detail.reslinnr = genstat.res_int[0]
                cust_list_detail.gname = bguest.name
                cust_list_detail.arrival = genstat.res_date[0]
                cust_list_detail.depart = genstat.res_date[1]

                glist = db_session.query(Glist).filter(
                        (Glist.gastnr == genstat.gastnrmember)).first()

                if glist:
                    cust_list_detail.cust_name = glist.name + "," + glist.anredefirma + " " + glist.vorname1
                    cust_list_detail.plz = glist.plz
                    cust_list_detail.land = glist.land
                    cust_list_detail.sales_id = glist.phonetik3
                    cust_list_detail.wohnort = glist.wohnort

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == glist.land)).first()

                    if nation:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                        if queasy:
                            cust_list_detail.region = queasy.char1
                    else:
                        cust_list_detail.region = "UNKOWN"
                else:
                    cust_list_detail.cust_name = guest.name + "," + guest.anredefirma + " " + guest.vorname1
                    cust_list_detail.plz = guest.plz
                    cust_list_detail.land = guest.land
                    cust_list_detail.sales_id = guest.phonetik3
                    cust_list_detail.wohnort = guest.wohnort

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == guest.land)).first()

                    if nation:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                        if queasy:
                            cust_list_detail.region = queasy.char1
                    else:
                        cust_list_detail.region = "UNKOWN"
            found = False

            clist = query(clist_list, filters=(lambda clist :clist.gastnr == genstat.gastnr and clist.gname == bguest.name), first=True)

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

                exrate = db_session.query(exrate).filter(
                        (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                if exrate:
                    cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + ((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (genstat.res_deci[4] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.argtumsatz = to_string(decimal.Decimal(cust_list_detail.argtumsatz) + (genstat.logis / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + ((genstat.logis + genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.ba_umsatz = to_string(decimal.Decimal(cust_list_detail.ba_umsatz) + (genstat.res_deci[6] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


            else:
                cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + (genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) , "->>>,>>>,>>>,>>9.99")
                cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + genstat.res_deci[4], "->>>,>>>,>>>,>>9.99")
                cust_list_detail.argtumsatz = to_string(decimal.Decimal(cust_list_detail.argtumsatz) + genstat.logis, "->>>,>>>,>>>,>>9.99")
                cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + genstat.logis + genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4] , "->>>,>>>,>>>,>>9.99")
                cust_list_detail.ba_umsatz = to_string(decimal.Decimal(cust_list_detail.ba_umsatz) + genstat.res_deci[6], "->>>,>>>,>>>,>>9.99")

            if genstat.resstatus != 13:
                cust_list_detail.logiernachte = to_string(to_int(cust_list_detail.logiernachte) + 1, ">>>,>>9")


            else:
                cust_list_detail.rm_sharer = "*"

            if curr_resnr != genstat.resnr or curr_reslinnr != genstat.res_int[0]:
                curr_resnr = genstat.resnr
                curr_reslinnr = genstat.res_int[0]

                if genstat.resstatus == 6:

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                    if res_line:
                        cust_list_detail.count_room = to_string(to_int(cust_list_detail.count_room) + res_line.zimmeranz, ">>,>>>,>>>,>>9")

                if excl_other == False:

                    for bill in db_session.query(Bill).filter(
                            (Bill.resnr == genstat.resnr) &  (Bill.reslinnr == genstat.res_int[0])).all():

                        bill_line_obj_list = []
                        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) &  (Artikel.departement == Bill_line.departement) &  (Artikel.artart == 0)).filter(
                                (Bill_line.rechnr == bill.rechnr) &  (Bill_line.bill_datum == genstat.datum)).all():
                            if bill_line._recid in bill_line_obj_list:
                                continue
                            else:
                                bill_line_obj_list.append(bill_line._recid)

                            if currency != " ":

                                exrate = db_session.query(exrate).filter(
                                        (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                if exrate:
                                    cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (bill_line.betrag / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                    cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + (bill_line.betrag / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                            else:
                                cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + bill_line.betrag, "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + bill_line.betrag, "->>>,>>>,>>>,>>9.99")

        if excl_other == False:

            for guest_queasy in db_session.query(Guest_queasy).filter(
                    (func.lower(Guest_queasy.key) == "gast_info") &  (Guest_queasy.date1 >= fdate) &  (Guest_queasy.date1 <= tdate)).all():

                genstat = db_session.query(Genstat).filter(
                        (Genstat.resnr == guest_queasy.number2) &  (Genstat.res_int[0] == guest_queasy.number3) &  (Genstat.datum == guest_queasy.date1) &  (Genstat.res_logic[1])).first()

                if genstat:

                    bguest = db_session.query(Bguest).filter(
                            (Bguest.gastnr == genstat.gastnrmember)).first()

                    cust_list_detail = query(cust_list_detail_list, filters=(lambda cust_list_detail :cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gname == bguest.name), first=True)

                    if cust_list_detail:

                        if currency != " ":

                            exrate = db_session.query(exrate).filter(
                                    (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                            if exrate:
                                cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + ((guest_queasy.deci1 + guest_queasy.deci2) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (guest_queasy.deci3 / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + ((guest_queasy.deci1 + guest_queasy.deci2 +\
                                    guest_queasy.deci3) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                        else:
                            cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + guest_queasy.deci1 + guest_queasy.deci2, "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + guest_queasy.deci3, "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + guest_queasy.deci1 + guest_queasy.deci2 +\
                                guest_queasy.deci3, "->>>,>>>,>>>,>>9.99")

    def create_forecast():

        nonlocal b_list_list, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_resnr, curr_reslinnr, curr_gname, curr_gastnr2, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, t_lyear, t_nofrm, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, tot_lyear, tot_nofrm, gt_logiernachte, gt_argtumsatz, gt_fb_umsatz, gt_sonst_umsatz, gt_ba_umsatz, gt_gesamtumsatz, gt_stayno, gt_lyear, gt_nofrm, curr_resnr1, curr_reslinnr1, found1, loopj, exratenr, exrate, genstat, guest, bill_line, bill, htparam, waehrung, nation, queasy, exrate, res_line, artikel, guest_queasy, reservation, sourccod, segment, arrangement, zimmer
        nonlocal t_genstat, blist, glist, bguest, clist, bline, bbuf


        nonlocal cust_list_detail, b_list, t_genstat, blist, glist, bguest, clist, bline, bbuf
        nonlocal cust_list_detail_list, b_list_list

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

                cust_list_detail = query(cust_list_detail_list, filters=(lambda cust_list_detail :cust_list_detail.gastnr == res_line.gastnr and cust_list_detail.gname == res_line.name), first=True)

                if not cust_list_detail:
                    cust_list_detail = Cust_list_detail()
                    cust_list_detail_list.append(cust_list_detail)

                    cust_list_detail.gastnr = res_line.gastnr
                    cust_list_detail.resno = res_line.resnr
                    cust_list_detail.reslinnr = res_line.reslinnr
                    cust_list_detail.gname = res_line.name
                    cust_list_detail.arrival = res_line.ankunft
                    cust_list_detail.depart = res_line.abreise

                    glist = db_session.query(Glist).filter(
                            (Glist.gastnr == res_line.gastnrmember)).first()

                    if glist:
                        cust_list_detail.cust_name = glist.name + "," + glist.anredefirma + " " + glist.vorname1
                        cust_list_detail.plz = glist.plz
                        cust_list_detail.land = glist.land
                        cust_list_detail.sales_id = glist.phonetik3
                        cust_list_detail.wohnort = glist.wohnort

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == glist.land)).first()

                        if nation:

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                            if queasy:
                                cust_list_detail.region = queasy.char1
                        else:
                            cust_list_detail.region = "UNKOWN"
                    else:
                        cust_list_detail.cust_name = guest.name + "," + guest.anredefirma + " " + guest.vorname1
                        cust_list_detail.plz = guest.plz
                        cust_list_detail.land = guest.land
                        cust_list_detail.sales_id = guest.phonetik3
                        cust_list_detail.wohnort = guest.wohnort

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == guest.land)).first()

                        if nation:

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                            if queasy:
                                cust_list_detail.region = queasy.char1
                        else:
                            cust_list_detail.region = "UNKOWN"
                found = False

                clist = query(clist_list, filters=(lambda clist :clist.gastnr == res_line.gastnr and clist.gname == res_line.name), first=True)

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

                    if curr_resnr != res_line.resnr or curr_reslinnr != res_line.reslinnr:
                        curr_resnr = res_line.resnr
                        curr_reslinnr = res_line.reslinnr

                        if curr_resnr != 0:

                            if ((res_line.ankunft < res_line.abreise) and res_line.abreise != datum) or (res_line.ankunft == res_line.abreise):

                                if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                                    cust_list_detail.count_room = to_string(to_int(cust_list_detail.count_room) + res_line.zimmeranz, ">>,>>>,>>>,>>9")
                                    tot_nofrm = tot_nofrm + res_line.zimmeranz
                                    gt_nofrm = gt_nofrm + res_line.zimmeranz

                        if excl_other == False:

                            for bill in db_session.query(Bill).filter(
                                    (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr)).all():

                                bill_line_obj_list = []
                                for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) &  (Artikel.departement == Bill_line.departement) &  (Artikel.artart == 0)).filter(
                                        (Bill_line.rechnr == bill.rechnr) &  (Bill_line.bill_datum == datum)).all():
                                    if bill_line._recid in bill_line_obj_list:
                                        continue
                                    else:
                                        bill_line_obj_list.append(bill_line._recid)

                                    if currency != " ":
                                        cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (bill_line.betrag / exrate) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + (bill_line.betrag / exrate) , "->>>,>>>,>>>,>>9.99")


                                    else:
                                        cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + bill_line.betrag, "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + bill_line.betrag, "->>>,>>>,>>>,>>9.99")

                    if currency != " ":
                        cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + ((tot_breakfast + tot_lunch + tot_dinner) / exrate) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (tot_other / exrate) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.argtumsatz = to_string(decimal.Decimal(cust_list_detail.argtumsatz) + (net_lodg / exrate) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + ((net_lodg + tot_breakfast +\
                            tot_lunch + tot_dinner + tot_other) / exrate) , "->>>,>>>,>>>,>>9.99")


                    else:
                        cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + tot_breakfast + tot_lunch + tot_dinner, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + tot_other, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.argtumsatz = to_string(decimal.Decimal(cust_list_detail.argtumsatz) + net_lodg, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + net_lodg + tot_breakfast +\
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
                    (func.lower(Guest_queasy.key) == "gast_info") &  (Guest_queasy.date1 >= fdate) &  (Guest_queasy.date1 <= tdate)).all():

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == guest_queasy.number2) &  (Res_line.reslinnr == guest_queasy.number3)).first()

                if res_line:

                    cust_list_detail = query(cust_list_detail_list, filters=(lambda cust_list_detail :cust_list_detail.gastnr == res_line.gastnr and cust_list_detail.resno == res_line.resnr and cust_list_detail.gname == res_line.name), first=True)

                    if cust_list_detail:

                        if currency != " ":
                            cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + ((guest_queasy.deci1 + guest_queasy.deci2) / exrate) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (guest_queasy.deci3 / exrate) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + ((guest_queasy.deci1 + guest_queasy.deci2 +\
                                guest_queasy.deci3) / exrate) , "->>>,>>>,>>>,>>9.99")


                        else:
                            cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + guest_queasy.deci1 + guest_queasy.deci2, "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + guest_queasy.deci3, "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + guest_queasy.deci1 + guest_queasy.deci2 +\
                                guest_queasy.deci3, "->>>,>>>,>>>,>>9.99")

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

            bguest = db_session.query(Bguest).filter(
                    (Bguest.gastnr == genstat.gastnrmember)).first()

            cust_list_detail = query(cust_list_detail_list, filters=(lambda cust_list_detail :cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.resno == genstat.resnr and cust_list_detail.gname == bguest.name), first=True)

            if cust_list_detail:

                if currency != " ":

                    exrate = db_session.query(exrate).filter(
                            (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                    if exrate:
                        cust_list_detail.ly_rev = to_string(decimal.Decimal(cust_list_detail.ly_rev) + ((genstat.logis + genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                else:
                    cust_list_detail.ly_rev = to_string(decimal.Decimal(cust_list_detail.ly_rev) + genstat.logis + genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4], "->>>,>>>,>>>,>>9.99")

    def cr_ftd1():

        nonlocal b_list_list, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_resnr, curr_reslinnr, curr_gname, curr_gastnr2, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, t_lyear, t_nofrm, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, tot_lyear, tot_nofrm, gt_logiernachte, gt_argtumsatz, gt_fb_umsatz, gt_sonst_umsatz, gt_ba_umsatz, gt_gesamtumsatz, gt_stayno, gt_lyear, gt_nofrm, curr_resnr1, curr_reslinnr1, found1, loopj, exratenr, exrate, genstat, guest, bill_line, bill, htparam, waehrung, nation, queasy, exrate, res_line, artikel, guest_queasy, reservation, sourccod, segment, arrangement, zimmer
        nonlocal t_genstat, blist, glist, bguest, clist, bline, bbuf


        nonlocal cust_list_detail, b_list, t_genstat, blist, glist, bguest, clist, bline, bbuf
        nonlocal cust_list_detail_list, b_list_list

        t_argtumsatz:int = 0
        rate:decimal = 1
        frate:decimal = 1
        rmnite:int = 0
        curr_resnr:int = 0
        curr_reslinnr:int = 0
        loopi:int = 0
        found:bool = False
        Clist = Cust_list_detail

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                (Genstat.datum >= fdate) &  (Genstat.datum <= tdate) &  (Genstat.segmentcode != 0) &  (Genstat.nationnr != 0) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)

            bguest = db_session.query(Bguest).filter(
                    (Bguest.gastnr == genstat.gastnrmember)).first()

            cust_list_detail = query(cust_list_detail_list, filters=(lambda cust_list_detail :cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gname == bguest.name), first=True)

            if not cust_list_detail:
                cust_list_detail = Cust_list_detail()
                cust_list_detail_list.append(cust_list_detail)

                cust_list_detail.gastnr = genstat.gastnr
                cust_list_detail.resno = genstat.resnr
                cust_list_detail.reslinnr = genstat.res_int[0]
                cust_list_detail.gname = bguest.name
                cust_list_detail.arrival = genstat.res_date[0]
                cust_list_detail.depart = genstat.res_date[1]

                glist = db_session.query(Glist).filter(
                        (Glist.gastnr == genstat.gastnrmember)).first()

                if glist:
                    cust_list_detail.cust_name = glist.name + "," + glist.anredefirma + " " + glist.vorname1
                    cust_list_detail.plz = glist.plz
                    cust_list_detail.land = glist.land
                    cust_list_detail.sales_id = glist.phonetik3
                    cust_list_detail.wohnort = glist.wohnort

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == glist.land)).first()

                    if nation:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                        if queasy:
                            cust_list_detail.region = queasy.char1
                    else:
                        cust_list_detail.region = "UNKOWN"
                else:
                    cust_list_detail.cust_name = guest.name + "," + guest.anredefirma + " " + guest.vorname1
                    cust_list_detail.plz = guest.plz
                    cust_list_detail.land = guest.land
                    cust_list_detail.sales_id = guest.phonetik3
                    cust_list_detail.wohnort = guest.wohnort

                    nation = db_session.query(Nation).filter(
                            (Nation.kurzbez == guest.land)).first()

                    if nation:

                        queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                        if queasy:
                            cust_list_detail.region = queasy.char1
                    else:
                        cust_list_detail.region = "UNKOWN"
            found = False

            clist = query(clist_list, filters=(lambda clist :clist.gastnr == genstat.gastnr and clist.gname == bguest.name), first=True)

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

                exrate = db_session.query(exrate).filter(
                        (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                if exrate:
                    cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + ((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (genstat.res_deci[4] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.argtumsatz = to_string(decimal.Decimal(cust_list_detail.argtumsatz) + (genstat.logis / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + ((genstat.logis + genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                    cust_list_detail.ba_umsatz = to_string(decimal.Decimal(cust_list_detail.ba_umsatz) + (genstat.res_deci[6] / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


            else:
                cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + (genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) , "->>>,>>>,>>>,>>9.99")
                cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + genstat.res_deci[4], "->>>,>>>,>>>,>>9.99")
                cust_list_detail.argtumsatz = to_string(decimal.Decimal(cust_list_detail.argtumsatz) + genstat.logis, "->>>,>>>,>>>,>>9.99")
                cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + genstat.logis + genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4] , "->>>,>>>,>>>,>>9.99")
                cust_list_detail.ba_umsatz = to_string(decimal.Decimal(cust_list_detail.ba_umsatz) + genstat.res_deci[6], "->>>,>>>,>>>,>>9.99")

            if genstat.resstatus != 13:
                cust_list_detail.logiernachte = to_string(to_int(cust_list_detail.logiernachte) + 1, ">>>,>>9")


            else:
                cust_list_detail.rm_sharer = "*"

            if curr_resnr != genstat.resnr or curr_reslinnr != genstat.res_int[0]:
                curr_resnr = genstat.resnr
                curr_reslinnr = genstat.res_int[0]

                if genstat.resstatus == 6:

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == genstat.resnr) &  (Res_line.reslinnr == genstat.res_int[0])).first()

                    if res_line:
                        cust_list_detail.count_room = to_string(to_int(cust_list_detail.count_room) + res_line.zimmeranz, ">>,>>>,>>>,>>9")

                if excl_other == False:

                    for bill in db_session.query(Bill).filter(
                            (Bill.resnr == genstat.resnr) &  (Bill.reslinnr == genstat.res_int[0])).all():

                        bill_line_obj_list = []
                        for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) &  (Artikel.departement == Bill_line.departement) &  (Artikel.artart == 0)).filter(
                                (Bill_line.rechnr == bill.rechnr) &  (Bill_line.bill_datum == genstat.datum)).all():
                            if bill_line._recid in bill_line_obj_list:
                                continue
                            else:
                                bill_line_obj_list.append(bill_line._recid)

                            if currency != " ":

                                exrate = db_session.query(exrate).filter(
                                        (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                                if exrate:
                                    cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (bill_line.betrag / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                    cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + (bill_line.betrag / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                            else:
                                cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + bill_line.betrag, "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + bill_line.betrag, "->>>,>>>,>>>,>>9.99")

        if excl_other == False:

            for guest_queasy in db_session.query(Guest_queasy).filter(
                    (func.lower(Guest_queasy.key) == "gast_info") &  (Guest_queasy.date1 >= fdate) &  (Guest_queasy.date1 <= tdate)).all():

                genstat = db_session.query(Genstat).filter(
                        (Genstat.resnr == guest_queasy.number2) &  (Genstat.res_int[0] == guest_queasy.number3) &  (Genstat.datum == guest_queasy.date1) &  (Genstat.res_logic[1])).first()

                if genstat:

                    bguest = db_session.query(Bguest).filter(
                            (Bguest.gastnr == genstat.gastnrmember)).first()

                    cust_list_detail = query(cust_list_detail_list, filters=(lambda cust_list_detail :cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.gname == bguest.name), first=True)

                    if cust_list_detail:

                        if currency != " ":

                            exrate = db_session.query(exrate).filter(
                                    (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                            if exrate:
                                cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + ((guest_queasy.deci1 + guest_queasy.deci2) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (guest_queasy.deci3 / exrate.betrag) , "->>>,>>>,>>>,>>9.99")
                                cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + ((guest_queasy.deci1 + guest_queasy.deci2 +\
                                    guest_queasy.deci3) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                        else:
                            cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + guest_queasy.deci1 + guest_queasy.deci2, "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + guest_queasy.deci3, "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + guest_queasy.deci1 + guest_queasy.deci2 +\
                                guest_queasy.deci3, "->>>,>>>,>>>,>>9.99")

    def create_forecast1():

        nonlocal b_list_list, bfast_art, lunch_art, dinner_art, lundin_art, service, vat, datum, end_date, net_lodg, fnet_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service, curr_i, i, found, ly_fdate, ly_tdate, ci_date, pos, curr_gastnr, curr_resnr, curr_reslinnr, curr_gname, curr_gastnr2, t_logiernachte, t_argtumsatz, t_fb_umsatz, t_sonst_umsatz, t_ba_umsatz, t_gesamtumsatz, t_lyear, t_nofrm, tot_logiernachte, tot_argtumsatz, tot_fb_umsatz, tot_sonst_umsatz, tot_ba_umsatz, tot_gesamtumsatz, tot_stayno, tot_lyear, tot_nofrm, gt_logiernachte, gt_argtumsatz, gt_fb_umsatz, gt_sonst_umsatz, gt_ba_umsatz, gt_gesamtumsatz, gt_stayno, gt_lyear, gt_nofrm, curr_resnr1, curr_reslinnr1, found1, loopj, exratenr, exrate, genstat, guest, bill_line, bill, htparam, waehrung, nation, queasy, exrate, res_line, artikel, guest_queasy, reservation, sourccod, segment, arrangement, zimmer
        nonlocal t_genstat, blist, glist, bguest, clist, bline, bbuf


        nonlocal cust_list_detail, b_list, t_genstat, blist, glist, bguest, clist, bline, bbuf
        nonlocal cust_list_detail_list, b_list_list

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

                cust_list_detail = query(cust_list_detail_list, filters=(lambda cust_list_detail :cust_list_detail.gastnr == res_line.gastnr and cust_list_detail.gname == res_line.name), first=True)

                if not cust_list_detail:
                    cust_list_detail = Cust_list_detail()
                    cust_list_detail_list.append(cust_list_detail)

                    cust_list_detail.gastnr = res_line.gastnr
                    cust_list_detail.resno = res_line.resnr
                    cust_list_detail.reslinnr = res_line.reslinnr
                    cust_list_detail.gname = res_line.name
                    cust_list_detail.arrival = res_line.ankunft
                    cust_list_detail.depart = res_line.abreise

                    glist = db_session.query(Glist).filter(
                            (Glist.gastnr == res_line.gastnrmember)).first()

                    if glist:
                        cust_list_detail.cust_name = glist.name + "," + glist.anredefirma + " " + glist.vorname1
                        cust_list_detail.plz = glist.plz
                        cust_list_detail.land = glist.land
                        cust_list_detail.sales_id = glist.phonetik3
                        cust_list_detail.wohnort = glist.wohnort

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == glist.land)).first()

                        if nation:

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                            if queasy:
                                cust_list_detail.region = queasy.char1
                        else:
                            cust_list_detail.region = "UNKOWN"
                    else:
                        cust_list_detail.cust_name = guest.name + "," + guest.anredefirma + " " + guest.vorname1
                        cust_list_detail.plz = guest.plz
                        cust_list_detail.land = guest.land
                        cust_list_detail.sales_id = guest.phonetik3
                        cust_list_detail.wohnort = guest.wohnort

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == guest.land)).first()

                        if nation:

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 6) &  (Queasy.number1 == nation.untergruppe)).first()

                            if queasy:
                                cust_list_detail.region = queasy.char1
                        else:
                            cust_list_detail.region = "UNKOWN"
                found = False

                clist = query(clist_list, filters=(lambda clist :clist.gastnr == res_line.gastnr and clist.gname == res_line.name), first=True)

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

                    if curr_resnr != res_line.resnr or curr_reslinnr != res_line.reslinnr:
                        curr_resnr = res_line.resnr
                        curr_reslinnr = res_line.reslinnr

                        if curr_resnr != 0:

                            if ((res_line.ankunft < res_line.abreise) and res_line.abreise != datum) or (res_line.ankunft == res_line.abreise):

                                if res_line.resstatus != 11 and res_line.resstatus != 13 and not res_line.zimmerfix:
                                    cust_list_detail.count_room = to_string(to_int(cust_list_detail.count_room) + res_line.zimmeranz, ">>,>>>,>>>,>>9")
                                    tot_nofrm = tot_nofrm + res_line.zimmeranz
                                    gt_nofrm = gt_nofrm + res_line.zimmeranz

                        if excl_other == False:

                            for bill in db_session.query(Bill).filter(
                                    (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr)).all():

                                bill_line_obj_list = []
                                for bill_line, artikel in db_session.query(Bill_line, Artikel).join(Artikel,(Artikel.artnr == Bill_line.artnr) &  (Artikel.departement == Bill_line.departement) &  (Artikel.artart == 0)).filter(
                                        (Bill_line.rechnr == bill.rechnr) &  (Bill_line.bill_datum == datum)).all():
                                    if bill_line._recid in bill_line_obj_list:
                                        continue
                                    else:
                                        bill_line_obj_list.append(bill_line._recid)

                                    if currency != " ":
                                        cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (bill_line.betrag / exrate) , "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + (bill_line.betrag / exrate) , "->>>,>>>,>>>,>>9.99")


                                    else:
                                        cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + bill_line.betrag, "->>>,>>>,>>>,>>9.99")
                                        cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + bill_line.betrag, "->>>,>>>,>>>,>>9.99")

                    if currency != " ":
                        cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + ((tot_breakfast + tot_lunch + tot_dinner) / exrate) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (tot_other / exrate) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.argtumsatz = to_string(decimal.Decimal(cust_list_detail.argtumsatz) + (net_lodg / exrate) , "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + ((net_lodg + tot_breakfast +\
                                tot_lunch + tot_dinner + tot_other) / exrate) , "->>>,>>>,>>>,>>9.99")


                    else:
                        cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + tot_breakfast + tot_lunch + tot_dinner, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + tot_other, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.argtumsatz = to_string(decimal.Decimal(cust_list_detail.argtumsatz) + net_lodg, "->>>,>>>,>>>,>>9.99")
                        cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + net_lodg + tot_breakfast +\
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
                    (func.lower(Guest_queasy.key) == "gast_info") &  (Guest_queasy.date1 >= fdate) &  (Guest_queasy.date1 <= tdate)).all():

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == guest_queasy.number2) &  (Res_line.reslinnr == guest_queasy.number3)).first()

                if res_line:

                    cust_list_detail = query(cust_list_detail_list, filters=(lambda cust_list_detail :cust_list_detail.gastnr == res_line.gastnr and cust_list_detail.resno == res_line.resnr and cust_list_detail.gname == res_line.name), first=True)

                    if cust_list_detail:

                        if currency != " ":
                            cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + ((guest_queasy.deci1 + guest_queasy.deci2) / exrate) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + (guest_queasy.deci3 / exrate) , "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + ((guest_queasy.deci1 + guest_queasy.deci2 +\
                                guest_queasy.deci3) / exrate) , "->>>,>>>,>>>,>>9.99")


                        else:
                            cust_list_detail.f_b_umsatz = to_string(decimal.Decimal(cust_list_detail.f_b_umsatz) + guest_queasy.deci1 + guest_queasy.deci2, "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.sonst_umsatz = to_string(decimal.Decimal(cust_list_detail.sonst_umsatz) + guest_queasy.deci3, "->>>,>>>,>>>,>>9.99")
                            cust_list_detail.gesamtumsatz = to_string(decimal.Decimal(cust_list_detail.gesamtumsatz) + guest_queasy.deci1 + guest_queasy.deci2 +\
                                guest_queasy.deci3, "->>>,>>>,>>>,>>9.99")

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

            bguest = db_session.query(Bguest).filter(
                    (Bguest.gastnr == genstat.gastnrmember)).first()

            cust_list_detail = query(cust_list_detail_list, filters=(lambda cust_list_detail :cust_list_detail.gastnr == genstat.gastnr and cust_list_detail.resno == genstat.resnr and cust_list_detail.gname == bguest.name), first=True)

            if cust_list_detail:

                if currency != " ":

                    exrate = db_session.query(exrate).filter(
                            (exrate.datum == genstat.datum) &  (exrate.artnr == exratenr)).first()

                    if exrate:
                        cust_list_detail.ly_rev = to_string(decimal.Decimal(cust_list_detail.ly_rev) + ((genstat.logis + genstat.res_deci[1] +\
                            genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4]) / exrate.betrag) , "->>>,>>>,>>>,>>9.99")


                else:
                    cust_list_detail.ly_rev = to_string(decimal.Decimal(cust_list_detail.ly_rev) + genstat.logis + genstat.res_deci[1] +\
                        genstat.res_deci[2] + genstat.res_deci[3] + genstat.res_deci[4], "->>>,>>>,>>>,>>9.99")


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 125)).first()
    bfast_art = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    b_list_list.clear()
    create_detail()
    tot_logiernachte = 0
    tot_argtumsatz = 0
    tot_fb_umsatz = 0
    tot_sonst_umsatz = 0
    tot_ba_umsatz = 0
    tot_gesamtumsatz = 0
    tot_stayno = 0
    tot_lyear = 0
    tot_nofrm = 0
    gt_logiernachte = 0
    gt_argtumsatz = 0
    gt_fb_umsatz = 0
    gt_sonst_umsatz = 0
    gt_ba_umsatz = 0
    gt_gesamtumsatz = 0
    gt_lyear = 0
    gt_nofrm = 0

    if sort_type == 0:

        for cust_list_detail in query(cust_list_detail_list):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == cust_list_detail.gastnr)).first()

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:
                b_list = B_list()
                b_list_list.append(b_list)

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
                tot_logiernachte = 0
                tot_argtumsatz = 0
                tot_fb_umsatz = 0
                tot_sonst_umsatz = 0
                tot_ba_umsatz = 0
                tot_gesamtumsatz = 0
                tot_stayno = 0
                tot_lyear = 0
                tot_nofrm = 0


                b_list = B_list()
                b_list_list.append(b_list)

                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno = tot_stayno + to_int(cust_list_detail.stayno)
                gt_stayno = gt_stayno + to_int(cust_list_detail.stayno)


            b_list = B_list()
            b_list_list.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte = tot_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            tot_argtumsatz = tot_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            tot_fb_umsatz = tot_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            tot_sonst_umsatz = tot_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            tot_ba_umsatz = tot_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            tot_gesamtumsatz = tot_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            tot_lyear = tot_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            tot_nofrm = tot_nofrm + decimal.Decimal(cust_list_detail.count_room)
            gt_logiernachte = gt_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            gt_argtumsatz = gt_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            gt_fb_umsatz = gt_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            gt_sonst_umsatz = gt_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            gt_ba_umsatz = gt_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            gt_gesamtumsatz = gt_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            gt_lyear = gt_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            gt_nofrm = gt_nofrm + decimal.Decimal(cust_list_detail.count_room)
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_list.append(b_list)

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
            b_list_list.append(b_list)

            b_list.cust_name = "G R A N D  T O T A L"
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

        for cust_list_detail in query(cust_list_detail_list):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == cust_list_detail.gastnr)).first()

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_list.append(b_list)

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
                    tot_logiernachte = 0
                    tot_argtumsatz = 0
                    tot_fb_umsatz = 0
                    tot_sonst_umsatz = 0
                    tot_ba_umsatz = 0
                    tot_gesamtumsatz = 0
                    tot_stayno = 0
                    tot_lyear = 0
                    tot_nofrm = 0


                b_list = B_list()
                b_list_list.append(b_list)

                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno = tot_stayno + to_int(cust_list_detail.stayno)
                gt_stayno = gt_stayno + to_int(cust_list_detail.stayno)


            b_list = B_list()
            b_list_list.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte = tot_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            tot_argtumsatz = tot_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            tot_fb_umsatz = tot_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            tot_sonst_umsatz = tot_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            tot_ba_umsatz = tot_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            tot_gesamtumsatz = tot_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            tot_lyear = tot_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            tot_nofrm = tot_nofrm + decimal.Decimal(cust_list_detail.count_room)
            gt_logiernachte = gt_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            gt_argtumsatz = gt_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            gt_fb_umsatz = gt_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            gt_sonst_umsatz = gt_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            gt_ba_umsatz = gt_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            gt_gesamtumsatz = gt_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            gt_lyear = gt_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            gt_nofrm = gt_nofrm + decimal.Decimal(cust_list_detail.count_room)
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_list.append(b_list)

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
            b_list_list.append(b_list)

            b_list.cust_name = "G R A N D  T O T A L"
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

        for cust_list_detail in query(cust_list_detail_list):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == cust_list_detail.gastnr)).first()

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_list.append(b_list)

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
                    tot_logiernachte = 0
                    tot_argtumsatz = 0
                    tot_fb_umsatz = 0
                    tot_sonst_umsatz = 0
                    tot_ba_umsatz = 0
                    tot_gesamtumsatz = 0
                    tot_stayno = 0
                    tot_lyear = 0
                    tot_nofrm = 0


                b_list = B_list()
                b_list_list.append(b_list)

                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno = tot_stayno + to_int(cust_list_detail.stayno)
                gt_stayno = gt_stayno + to_int(cust_list_detail.stayno)


            b_list = B_list()
            b_list_list.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte = tot_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            tot_argtumsatz = tot_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            tot_fb_umsatz = tot_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            tot_sonst_umsatz = tot_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            tot_ba_umsatz = tot_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            tot_gesamtumsatz = tot_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            tot_lyear = tot_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            tot_nofrm = tot_nofrm + decimal.Decimal(cust_list_detail.count_room)
            gt_logiernachte = gt_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            gt_argtumsatz = gt_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            gt_fb_umsatz = gt_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            gt_sonst_umsatz = gt_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            gt_ba_umsatz = gt_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            gt_gesamtumsatz = gt_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            gt_lyear = gt_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            gt_nofrm = gt_nofrm + decimal.Decimal(cust_list_detail.count_room)
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_list.append(b_list)

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
            b_list_list.append(b_list)

            b_list.cust_name = "G R A N D  T O T A L"
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

        for cust_list_detail in query(cust_list_detail_list):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == cust_list_detail.gastnr)).first()

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_list.append(b_list)

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
                    tot_logiernachte = 0
                    tot_argtumsatz = 0
                    tot_fb_umsatz = 0
                    tot_sonst_umsatz = 0
                    tot_ba_umsatz = 0
                    tot_gesamtumsatz = 0
                    tot_stayno = 0
                    tot_lyear = 0
                    tot_nofrm = 0


                b_list = B_list()
                b_list_list.append(b_list)

                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno = tot_stayno + to_int(cust_list_detail.stayno)
                gt_stayno = gt_stayno + to_int(cust_list_detail.stayno)


            b_list = B_list()
            b_list_list.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte = tot_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            tot_argtumsatz = tot_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            tot_fb_umsatz = tot_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            tot_sonst_umsatz = tot_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            tot_ba_umsatz = tot_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            tot_gesamtumsatz = tot_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            tot_lyear = tot_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            tot_nofrm = tot_nofrm + decimal.Decimal(cust_list_detail.count_room)
            gt_logiernachte = gt_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            gt_argtumsatz = gt_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            gt_fb_umsatz = gt_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            gt_sonst_umsatz = gt_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            gt_ba_umsatz = gt_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            gt_gesamtumsatz = gt_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            gt_lyear = gt_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            gt_nofrm = gt_nofrm + decimal.Decimal(cust_list_detail.count_room)
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_list.append(b_list)

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
            b_list_list.append(b_list)

            b_list.cust_name = "G R A N D  T O T A L"
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

        for cust_list_detail in query(cust_list_detail_list):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == cust_list_detail.gastnr)).first()

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_list.append(b_list)

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
                    tot_logiernachte = 0
                    tot_argtumsatz = 0
                    tot_fb_umsatz = 0
                    tot_sonst_umsatz = 0
                    tot_ba_umsatz = 0
                    tot_gesamtumsatz = 0
                    tot_stayno = 0
                    tot_lyear = 0
                    tot_nofrm = 0


                b_list = B_list()
                b_list_list.append(b_list)

                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno = tot_stayno + to_int(cust_list_detail.stayno)
                gt_stayno = gt_stayno + to_int(cust_list_detail.stayno)


            b_list = B_list()
            b_list_list.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte = tot_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            tot_argtumsatz = tot_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            tot_fb_umsatz = tot_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            tot_sonst_umsatz = tot_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            tot_ba_umsatz = tot_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            tot_gesamtumsatz = tot_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            tot_lyear = tot_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            tot_nofrm = tot_nofrm + decimal.Decimal(cust_list_detail.count_room)
            gt_logiernachte = gt_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            gt_argtumsatz = gt_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            gt_fb_umsatz = gt_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            gt_sonst_umsatz = gt_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            gt_ba_umsatz = gt_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            gt_gesamtumsatz = gt_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            gt_lyear = gt_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            gt_nofrm = gt_nofrm + decimal.Decimal(cust_list_detail.count_room)
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_list.append(b_list)

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
            b_list_list.append(b_list)

            b_list.cust_name = "G R A N D  T O T A L"
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

        for cust_list_detail in query(cust_list_detail_list):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == cust_list_detail.gastnr)).first()

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_list.append(b_list)

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
                    tot_logiernachte = 0
                    tot_argtumsatz = 0
                    tot_fb_umsatz = 0
                    tot_sonst_umsatz = 0
                    tot_ba_umsatz = 0
                    tot_gesamtumsatz = 0
                    tot_stayno = 0
                    tot_lyear = 0
                    tot_nofrm = 0


                b_list = B_list()
                b_list_list.append(b_list)

                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno = tot_stayno + to_int(cust_list_detail.stayno)
                gt_stayno = gt_stayno + to_int(cust_list_detail.stayno)


            b_list = B_list()
            b_list_list.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte = tot_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            tot_argtumsatz = tot_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            tot_fb_umsatz = tot_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            tot_sonst_umsatz = tot_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            tot_ba_umsatz = tot_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            tot_gesamtumsatz = tot_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            tot_lyear = tot_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            tot_nofrm = tot_nofrm + decimal.Decimal(cust_list_detail.count_room)
            gt_logiernachte = gt_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            gt_argtumsatz = gt_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            gt_fb_umsatz = gt_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            gt_sonst_umsatz = gt_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            gt_ba_umsatz = gt_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            gt_gesamtumsatz = gt_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            gt_lyear = gt_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            gt_nofrm = gt_nofrm + decimal.Decimal(cust_list_detail.count_room)
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_list.append(b_list)

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
            b_list_list.append(b_list)

            b_list.cust_name = "G R A N D  T O T A L"
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

        for cust_list_detail in query(cust_list_detail_list):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == cust_list_detail.gastnr)).first()

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_list.append(b_list)

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
                    tot_logiernachte = 0
                    tot_argtumsatz = 0
                    tot_fb_umsatz = 0
                    tot_sonst_umsatz = 0
                    tot_ba_umsatz = 0
                    tot_gesamtumsatz = 0
                    tot_stayno = 0
                    tot_lyear = 0
                    tot_nofrm = 0


                b_list = B_list()
                b_list_list.append(b_list)

                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno = tot_stayno + to_int(cust_list_detail.stayno)
                gt_stayno = gt_stayno + to_int(cust_list_detail.stayno)


            b_list = B_list()
            b_list_list.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte = tot_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            tot_argtumsatz = tot_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            tot_fb_umsatz = tot_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            tot_sonst_umsatz = tot_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            tot_ba_umsatz = tot_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            tot_gesamtumsatz = tot_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            tot_lyear = tot_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            tot_nofrm = tot_nofrm + decimal.Decimal(cust_list_detail.count_room)
            gt_logiernachte = gt_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            gt_argtumsatz = gt_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            gt_fb_umsatz = gt_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            gt_sonst_umsatz = gt_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            gt_ba_umsatz = gt_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            gt_gesamtumsatz = gt_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            gt_lyear = gt_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            gt_nofrm = gt_nofrm + decimal.Decimal(cust_list_detail.count_room)
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_list.append(b_list)

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
            b_list_list.append(b_list)

            b_list.cust_name = "G R A N D  T O T A L"
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

        for cust_list_detail in query(cust_list_detail_list):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == cust_list_detail.gastnr)).first()

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_list.append(b_list)

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
                    tot_logiernachte = 0
                    tot_argtumsatz = 0
                    tot_fb_umsatz = 0
                    tot_sonst_umsatz = 0
                    tot_ba_umsatz = 0
                    tot_gesamtumsatz = 0
                    tot_stayno = 0
                    tot_lyear = 0
                    tot_nofrm = 0


                b_list = B_list()
                b_list_list.append(b_list)

                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno = tot_stayno + to_int(cust_list_detail.stayno)
                gt_stayno = gt_stayno + to_int(cust_list_detail.stayno)


            b_list = B_list()
            b_list_list.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte = tot_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            tot_argtumsatz = tot_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            tot_fb_umsatz = tot_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            tot_sonst_umsatz = tot_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            tot_ba_umsatz = tot_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            tot_gesamtumsatz = tot_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            tot_lyear = tot_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            tot_nofrm = tot_nofrm + decimal.Decimal(cust_list_detail.count_room)
            gt_logiernachte = gt_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            gt_argtumsatz = gt_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            gt_fb_umsatz = gt_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            gt_sonst_umsatz = gt_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            gt_ba_umsatz = gt_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            gt_gesamtumsatz = gt_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            gt_lyear = gt_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            gt_nofrm = gt_nofrm + decimal.Decimal(cust_list_detail.count_room)
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_list.append(b_list)

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
            b_list_list.append(b_list)

            b_list.cust_name = "G R A N D  T O T A L"
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

        for cust_list_detail in query(cust_list_detail_list):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == cust_list_detail.gastnr)).first()

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_list.append(b_list)

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
                    tot_logiernachte = 0
                    tot_argtumsatz = 0
                    tot_fb_umsatz = 0
                    tot_sonst_umsatz = 0
                    tot_ba_umsatz = 0
                    tot_gesamtumsatz = 0
                    tot_stayno = 0
                    tot_lyear = 0
                    tot_nofrm = 0


                b_list = B_list()
                b_list_list.append(b_list)

                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno = tot_stayno + to_int(cust_list_detail.stayno)
                gt_stayno = gt_stayno + to_int(cust_list_detail.stayno)


            b_list = B_list()
            b_list_list.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte = tot_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            tot_argtumsatz = tot_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            tot_fb_umsatz = tot_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            tot_sonst_umsatz = tot_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            tot_ba_umsatz = tot_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            tot_gesamtumsatz = tot_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            tot_lyear = tot_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            tot_nofrm = tot_nofrm + decimal.Decimal(cust_list_detail.count_room)
            gt_logiernachte = gt_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            gt_argtumsatz = gt_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            gt_fb_umsatz = gt_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            gt_sonst_umsatz = gt_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            gt_ba_umsatz = gt_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            gt_gesamtumsatz = gt_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            gt_lyear = gt_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            gt_nofrm = gt_nofrm + decimal.Decimal(cust_list_detail.count_room)
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_list.append(b_list)

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
            b_list_list.append(b_list)

            b_list.cust_name = "G R A N D  T O T A L"
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

        for cust_list_detail in query(cust_list_detail_list):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == cust_list_detail.gastnr)).first()

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_list.append(b_list)

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
                    tot_logiernachte = 0
                    tot_argtumsatz = 0
                    tot_fb_umsatz = 0
                    tot_sonst_umsatz = 0
                    tot_ba_umsatz = 0
                    tot_gesamtumsatz = 0
                    tot_stayno = 0
                    tot_lyear = 0
                    tot_nofrm = 0


                b_list = B_list()
                b_list_list.append(b_list)

                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno = tot_stayno + to_int(cust_list_detail.stayno)
                gt_stayno = gt_stayno + to_int(cust_list_detail.stayno)


            b_list = B_list()
            b_list_list.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte = tot_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            tot_argtumsatz = tot_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            tot_fb_umsatz = tot_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            tot_sonst_umsatz = tot_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            tot_ba_umsatz = tot_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            tot_gesamtumsatz = tot_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            tot_lyear = tot_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            tot_nofrm = tot_nofrm + decimal.Decimal(cust_list_detail.count_room)
            gt_logiernachte = gt_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            gt_argtumsatz = gt_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            gt_fb_umsatz = gt_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            gt_sonst_umsatz = gt_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            gt_ba_umsatz = gt_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            gt_gesamtumsatz = gt_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            gt_lyear = gt_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            gt_nofrm = gt_nofrm + decimal.Decimal(cust_list_detail.count_room)
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_list.append(b_list)

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
            b_list_list.append(b_list)

            b_list.cust_name = "G R A N D  T O T A L"
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

        for cust_list_detail in query(cust_list_detail_list):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == cust_list_detail.gastnr)).first()

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_list.append(b_list)

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
                    tot_logiernachte = 0
                    tot_argtumsatz = 0
                    tot_fb_umsatz = 0
                    tot_sonst_umsatz = 0
                    tot_ba_umsatz = 0
                    tot_gesamtumsatz = 0
                    tot_stayno = 0
                    tot_lyear = 0
                    tot_nofrm = 0


                b_list = B_list()
                b_list_list.append(b_list)

                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno = tot_stayno + to_int(cust_list_detail.stayno)
                gt_stayno = gt_stayno + to_int(cust_list_detail.stayno)


            b_list = B_list()
            b_list_list.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte = tot_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            tot_argtumsatz = tot_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            tot_fb_umsatz = tot_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            tot_sonst_umsatz = tot_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            tot_ba_umsatz = tot_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            tot_gesamtumsatz = tot_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            tot_lyear = tot_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            tot_nofrm = tot_nofrm + decimal.Decimal(cust_list_detail.count_room)
            gt_logiernachte = gt_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            gt_argtumsatz = gt_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            gt_fb_umsatz = gt_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            gt_sonst_umsatz = gt_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            gt_ba_umsatz = gt_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            gt_gesamtumsatz = gt_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            gt_lyear = gt_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            gt_nofrm = gt_nofrm + decimal.Decimal(cust_list_detail.count_room)
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_list.append(b_list)

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
            b_list_list.append(b_list)

            b_list.cust_name = "G R A N D  T O T A L"
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

        for cust_list_detail in query(cust_list_detail_list):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == cust_list_detail.gastnr)).first()

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_list.append(b_list)

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
                    tot_logiernachte = 0
                    tot_argtumsatz = 0
                    tot_fb_umsatz = 0
                    tot_sonst_umsatz = 0
                    tot_ba_umsatz = 0
                    tot_gesamtumsatz = 0
                    tot_stayno = 0
                    tot_lyear = 0
                    tot_nofrm = 0


                b_list = B_list()
                b_list_list.append(b_list)

                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno = tot_stayno + to_int(cust_list_detail.stayno)
                gt_stayno = gt_stayno + to_int(cust_list_detail.stayno)


            b_list = B_list()
            b_list_list.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte = tot_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            tot_argtumsatz = tot_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            tot_fb_umsatz = tot_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            tot_sonst_umsatz = tot_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            tot_ba_umsatz = tot_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            tot_gesamtumsatz = tot_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            tot_lyear = tot_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            tot_nofrm = tot_nofrm + decimal.Decimal(cust_list_detail.count_room)
            gt_logiernachte = gt_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            gt_argtumsatz = gt_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            gt_fb_umsatz = gt_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            gt_sonst_umsatz = gt_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            gt_ba_umsatz = gt_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            gt_gesamtumsatz = gt_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            gt_lyear = gt_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            gt_nofrm = gt_nofrm + decimal.Decimal(cust_list_detail.count_room)
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_list.append(b_list)

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
            b_list_list.append(b_list)

            b_list.cust_name = "G R A N D  T O T A L"
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

        for cust_list_detail in query(cust_list_detail_list):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == cust_list_detail.gastnr)).first()

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_list.append(b_list)

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
                    tot_logiernachte = 0
                    tot_argtumsatz = 0
                    tot_fb_umsatz = 0
                    tot_sonst_umsatz = 0
                    tot_ba_umsatz = 0
                    tot_gesamtumsatz = 0
                    tot_stayno = 0
                    tot_lyear = 0
                    tot_nofrm = 0


                b_list = B_list()
                b_list_list.append(b_list)

                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno = tot_stayno + to_int(cust_list_detail.stayno)
                gt_stayno = gt_stayno + to_int(cust_list_detail.stayno)


            b_list = B_list()
            b_list_list.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte = tot_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            tot_argtumsatz = tot_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            tot_fb_umsatz = tot_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            tot_sonst_umsatz = tot_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            tot_ba_umsatz = tot_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            tot_gesamtumsatz = tot_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            tot_lyear = tot_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            tot_nofrm = tot_nofrm + decimal.Decimal(cust_list_detail.count_room)
            gt_logiernachte = gt_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            gt_argtumsatz = gt_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            gt_fb_umsatz = gt_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            gt_sonst_umsatz = gt_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            gt_ba_umsatz = gt_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            gt_gesamtumsatz = gt_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            gt_lyear = gt_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            gt_nofrm = gt_nofrm + decimal.Decimal(cust_list_detail.count_room)
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_list.append(b_list)

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
            b_list_list.append(b_list)

            b_list.cust_name = "G R A N D  T O T A L"
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

        for cust_list_detail in query(cust_list_detail_list):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == cust_list_detail.gastnr)).first()

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_list.append(b_list)

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
                    tot_logiernachte = 0
                    tot_argtumsatz = 0
                    tot_fb_umsatz = 0
                    tot_sonst_umsatz = 0
                    tot_ba_umsatz = 0
                    tot_gesamtumsatz = 0
                    tot_stayno = 0
                    tot_lyear = 0
                    tot_nofrm = 0


                b_list = B_list()
                b_list_list.append(b_list)

                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno = tot_stayno + to_int(cust_list_detail.stayno)
                gt_stayno = gt_stayno + to_int(cust_list_detail.stayno)


            b_list = B_list()
            b_list_list.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte = tot_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            tot_argtumsatz = tot_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            tot_fb_umsatz = tot_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            tot_sonst_umsatz = tot_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            tot_ba_umsatz = tot_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            tot_gesamtumsatz = tot_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            tot_lyear = tot_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            tot_nofrm = tot_nofrm + decimal.Decimal(cust_list_detail.count_room)
            gt_logiernachte = gt_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            gt_argtumsatz = gt_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            gt_fb_umsatz = gt_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            gt_sonst_umsatz = gt_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            gt_ba_umsatz = gt_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            gt_gesamtumsatz = gt_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            gt_lyear = gt_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            gt_nofrm = gt_nofrm + decimal.Decimal(cust_list_detail.count_room)
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_list.append(b_list)

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
            b_list_list.append(b_list)

            b_list.cust_name = "G R A N D  T O T A L"
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

        for cust_list_detail in query(cust_list_detail_list):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == cust_list_detail.gastnr)).first()

            if curr_gastnr == 0:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if curr_gastnr != 0 and curr_gastnr != cust_list_detail.gastnr:

                if tot_gesamtumsatz != 0:
                    b_list = B_list()
                    b_list_list.append(b_list)

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
                    tot_logiernachte = 0
                    tot_argtumsatz = 0
                    tot_fb_umsatz = 0
                    tot_sonst_umsatz = 0
                    tot_ba_umsatz = 0
                    tot_gesamtumsatz = 0
                    tot_stayno = 0
                    tot_lyear = 0
                    tot_nofrm = 0


                b_list = B_list()
                b_list_list.append(b_list)

                b_list = B_list()
                b_list_list.append(b_list)

                b_list.cust_name = (guest.name + ", " + guest.vorname1 + " " + guest.anrede1 +\
                        guest.anredefirm)

            if cust_list_detail.resnr != "":
                cust_list_detail.stayno = to_string(num_entries(cust_list_detail.resnr, ";") - 1, ">>>,>>9")
                tot_stayno = tot_stayno + to_int(cust_list_detail.stayno)
                gt_stayno = gt_stayno + to_int(cust_list_detail.stayno)


            b_list = B_list()
            b_list_list.append(b_list)

            buffer_copy(cust_list_detail, b_list)

            if b_list.ly_rev == " ":
                b_list.ly_rev = to_string(0, "->>>,>>>,>>>,>>9.99")

            if b_list.ba_umsatz == " ":
                b_list.ba_umsatz = to_string(0, "->>>,>>>,>>>,>>9.99")


            tot_logiernachte = tot_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            tot_argtumsatz = tot_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            tot_fb_umsatz = tot_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            tot_sonst_umsatz = tot_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            tot_ba_umsatz = tot_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            tot_gesamtumsatz = tot_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            tot_lyear = tot_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            tot_nofrm = tot_nofrm + decimal.Decimal(cust_list_detail.count_room)
            gt_logiernachte = gt_logiernachte + decimal.Decimal(cust_list_detail.logiernachte)
            gt_argtumsatz = gt_argtumsatz + decimal.Decimal(cust_list_detail.argtumsatz)
            gt_fb_umsatz = gt_fb_umsatz + decimal.Decimal(cust_list_detail.f_b_umsatz)
            gt_sonst_umsatz = gt_sonst_umsatz + decimal.Decimal(cust_list_detail.sonst_umsatz)
            gt_ba_umsatz = gt_ba_umsatz + decimal.Decimal(cust_list_detail.ba_umsatz)
            gt_gesamtumsatz = gt_gesamtumsatz + decimal.Decimal(cust_list_detail.gesamtumsatz)
            gt_lyear = gt_lyear + decimal.Decimal(cust_list_detail.ly_rev)
            gt_nofrm = gt_nofrm + decimal.Decimal(cust_list_detail.count_room)
            curr_gastnr = cust_list_detail.gastnr

        if tot_gesamtumsatz != 0:
            b_list = B_list()
            b_list_list.append(b_list)

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
            b_list_list.append(b_list)

            b_list.cust_name = "G R A N D  T O T A L"
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