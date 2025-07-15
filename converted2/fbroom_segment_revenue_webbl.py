#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.argt_betrag import argt_betrag
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.get_room_breakdown import get_room_breakdown
from models import Htparam, Segment, Queasy, Arrangement, Genstat, Artikel, Argt_line, Reservation, Res_line, Bill, Bill_line, Guest, Guestseg, H_journal, H_bill, H_artikel

t_payload_list_data, T_payload_list = create_model("T_payload_list", {"from_date":date, "to_date":date, "sort_type":int})

def fbroom_segment_revenue_webbl(t_payload_list_data:[T_payload_list]):

    prepare_cache ([Htparam, Segment, Queasy, Arrangement, Genstat, Artikel, Argt_line, Reservation, Res_line, Bill, Bill_line, Guest, H_bill, H_artikel])

    revenue_segmlist_data = []
    curr_date:date = None
    bill_date:date = None
    ci_date:date = None
    from_date:date = None
    to_date:date = None
    htparam = segment = queasy = arrangement = genstat = artikel = argt_line = reservation = res_line = bill = bill_line = guest = guestseg = h_journal = h_bill = h_artikel = None

    t_payload_list = revenue_segmlist = revenue_room_other = None

    revenue_segmlist_data, Revenue_segmlist = create_model("Revenue_segmlist", {"segment_code":int, "segmemt_short_desc":string, "segment_description":string, "segment_group":string, "rsv_segmroom_rev":Decimal, "rsv_segmfood_rev":Decimal, "rsv_segmbev_rev":Decimal, "rsv_segmother_rev":Decimal, "rsv_segmfcost_rev":Decimal, "rsv_segmtotal_rev":Decimal, "outlet_segmfood_rev":Decimal, "outlet_segmbev_rev":Decimal, "outlet_segmother_rev":Decimal, "outlet_segmtotal_rev":Decimal, "grand_total":Decimal})
    revenue_room_other_data, Revenue_room_other = create_model("Revenue_room_other", {"segment_code":int, "segmemt_short_desc":string, "segment_room_other":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal revenue_segmlist_data, curr_date, bill_date, ci_date, from_date, to_date, htparam, segment, queasy, arrangement, genstat, artikel, argt_line, reservation, res_line, bill, bill_line, guest, guestseg, h_journal, h_bill, h_artikel


        nonlocal t_payload_list, revenue_segmlist, revenue_room_other
        nonlocal revenue_segmlist_data, revenue_room_other_data

        return {"revenue-segmlist": revenue_segmlist_data}

    def create_history():

        nonlocal revenue_segmlist_data, curr_date, bill_date, ci_date, from_date, to_date, htparam, segment, queasy, arrangement, genstat, artikel, argt_line, reservation, res_line, bill, bill_line, guest, guestseg, h_journal, h_bill, h_artikel


        nonlocal t_payload_list, revenue_segmlist, revenue_room_other
        nonlocal revenue_segmlist_data, revenue_room_other_data

        ex_rate:Decimal = 1
        argt_betrag:Decimal = to_decimal("0.0")
        nett_betrag:Decimal = to_decimal("0.0")
        vat_art:Decimal = to_decimal("0.0")
        service_art:Decimal = to_decimal("0.0")
        vat2_art:Decimal = to_decimal("0.0")
        fact_art:Decimal = to_decimal("0.0")
        post_it:bool = False

        genstat_obj_list = {}
        genstat = Genstat()
        arrangement = Arrangement()
        for genstat.segmentcode, genstat.logis, genstat.datum, genstat._recid, arrangement.argtnr, arrangement._recid in db_session.query(Genstat.segmentcode, Genstat.logis, Genstat.datum, Genstat._recid, Arrangement.argtnr, Arrangement._recid).join(Arrangement,(Arrangement.arrangement == Genstat.argt)).filter(
                 (Genstat.datum == curr_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.segmentcode).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            revenue_segmlist = query(revenue_segmlist_data, filters=(lambda revenue_segmlist: revenue_segmlist.segment_code == genstat.segmentcode), first=True)

            if revenue_segmlist:
                revenue_segmlist.rsv_segmroom_rev =  to_decimal(revenue_segmlist.rsv_segmroom_rev) + to_decimal(genstat.logis)
                revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(genstat.logis)
                revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(genstat.logis)

                argt_line_obj_list = {}
                argt_line = Argt_line()
                artikel = Artikel()
                for argt_line._recid, artikel.artnr, artikel.departement, artikel.umsatzart, artikel._recid in db_session.query(Argt_line._recid, Artikel.artnr, Artikel.departement, Artikel.umsatzart, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                         (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line._recid).all():
                    if argt_line_obj_list.get(argt_line._recid):
                        continue
                    else:
                        argt_line_obj_list[argt_line._recid] = True


                    argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                    service_art, vat_art, vat2_art, fact_art = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))
                    nett_betrag =  to_decimal(argt_betrag) / to_decimal(fact_art)

                    if (artikel.umsatzart == 3 or artikel.umsatzart == 5):
                        revenue_segmlist.rsv_segmfood_rev =  to_decimal(revenue_segmlist.rsv_segmfood_rev) + to_decimal(argt_betrag)
                        revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(argt_betrag)
                        revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(argt_betrag)

                    elif artikel.umsatzart == 6:
                        revenue_segmlist.rsv_segmbev_rev =  to_decimal(revenue_segmlist.rsv_segmbev_rev) + to_decimal(argt_betrag)
                        revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(argt_betrag)
                        revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(argt_betrag)


                    else:
                        revenue_segmlist.rsv_segmother_rev =  to_decimal(revenue_segmlist.rsv_segmother_rev) + to_decimal(argt_betrag)
                        revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(argt_betrag)
                        revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(argt_betrag)


    def create_forecast():

        nonlocal revenue_segmlist_data, curr_date, bill_date, ci_date, from_date, to_date, htparam, segment, queasy, arrangement, genstat, artikel, argt_line, reservation, res_line, bill, bill_line, guest, guestseg, h_journal, h_bill, h_artikel


        nonlocal t_payload_list, revenue_segmlist, revenue_room_other
        nonlocal revenue_segmlist_data, revenue_room_other_data

        net_lodg:Decimal = to_decimal("0.0")
        fnet_lodg:Decimal = to_decimal("0.0")
        tot_breakfast:Decimal = to_decimal("0.0")
        tot_lunch:Decimal = to_decimal("0.0")
        tot_dinner:Decimal = to_decimal("0.0")
        tot_other:Decimal = to_decimal("0.0")
        tot_rmrev:Decimal = to_decimal("0.0")
        tot_vat:Decimal = to_decimal("0.0")
        tot_service:Decimal = to_decimal("0.0")
        ex_rate:Decimal = 1
        argt_betrag:Decimal = to_decimal("0.0")
        nett_betrag:Decimal = to_decimal("0.0")
        vat_art:Decimal = to_decimal("0.0")
        service_art:Decimal = to_decimal("0.0")
        vat2_art:Decimal = to_decimal("0.0")
        fact_art:Decimal = to_decimal("0.0")
        post_it:bool = False

        res_line_obj_list = {}
        res_line = Res_line()
        reservation = Reservation()
        for res_line._recid, res_line.abreise, res_line.resnr, res_line.gastnrmember, reservation.segmentcode, reservation._recid in db_session.query(Res_line._recid, Res_line.abreise, Res_line.resnr, Res_line.gastnrmember, Reservation.segmentcode, Reservation._recid).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.segmentcode != 0)).filter(
                 ((Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag <= 1) & (Res_line.ankunft >= curr_date) & (Res_line.abreise <= curr_date)) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == ci_date) & (Res_line.abreise == ci_date)) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.gastnr > 0)).order_by(Reservation.segmentcode).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if curr_date == res_line.abreise:
                pass
            else:
                net_lodg =  to_decimal("0")
                tot_breakfast =  to_decimal("0")
                tot_lunch =  to_decimal("0")
                tot_dinner =  to_decimal("0")
                tot_other =  to_decimal("0")


                fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, curr_date, 0, from_date))

                revenue_segmlist = query(revenue_segmlist_data, filters=(lambda revenue_segmlist: revenue_segmlist.segment_code == reservation.segmentcode), first=True)

                if revenue_segmlist:
                    revenue_segmlist.rsv_segmroom_rev =  to_decimal(revenue_segmlist.rsv_segmroom_rev) + to_decimal(net_lodg)
                    revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(net_lodg)
                    revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(net_lodg)

                    argt_line_obj_list = {}
                    argt_line = Argt_line()
                    artikel = Artikel()
                    for argt_line._recid, artikel.artnr, artikel.departement, artikel.umsatzart, artikel._recid in db_session.query(Argt_line._recid, Artikel.artnr, Artikel.departement, Artikel.umsatzart, Artikel._recid).join(Artikel,(Artikel.artnr == Argt_line.argt_artnr) & (Artikel.departement == Argt_line.departement)).filter(
                             (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2) & (Argt_line.kind1)).order_by(Argt_line._recid).all():
                        if argt_line_obj_list.get(argt_line._recid):
                            continue
                        else:
                            argt_line_obj_list[argt_line._recid] = True


                        argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                        service_art, vat_art, vat2_art, fact_art = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))
                        nett_betrag =  to_decimal(argt_betrag) / to_decimal(fact_art)

                        if (artikel.umsatzart == 3 or artikel.umsatzart == 5):
                            revenue_segmlist.rsv_segmfood_rev =  to_decimal(revenue_segmlist.rsv_segmfood_rev) + to_decimal(argt_betrag)
                            revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(argt_betrag)
                            revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(argt_betrag)

                        elif artikel.umsatzart == 6:
                            revenue_segmlist.rsv_segmbev_rev =  to_decimal(revenue_segmlist.rsv_segmbev_rev) + to_decimal(argt_betrag)
                            revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(argt_betrag)
                            revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(argt_betrag)


                        else:
                            revenue_segmlist.rsv_segmother_rev =  to_decimal(revenue_segmlist.rsv_segmother_rev) + to_decimal(argt_betrag)
                            revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(argt_betrag)
                            revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(argt_betrag)


    def create_bill_fo():

        nonlocal revenue_segmlist_data, curr_date, bill_date, ci_date, from_date, to_date, htparam, segment, queasy, arrangement, genstat, artikel, argt_line, reservation, res_line, bill, bill_line, guest, guestseg, h_journal, h_bill, h_artikel


        nonlocal t_payload_list, revenue_segmlist, revenue_room_other
        nonlocal revenue_segmlist_data, revenue_room_other_data

        bill_line_obj_list = {}
        bill_line = Bill_line()
        artikel = Artikel()
        bill = Bill()
        for bill_line.betrag, bill_line._recid, artikel.artnr, artikel.departement, artikel.umsatzart, artikel._recid, bill.resnr, bill.parent_nr, bill.reslinnr, bill.gastnr, bill._recid in db_session.query(Bill_line.betrag, Bill_line._recid, Artikel.artnr, Artikel.departement, Artikel.umsatzart, Artikel._recid, Bill.resnr, Bill.parent_nr, Bill.reslinnr, Bill.gastnr, Bill._recid).join(Artikel,(Artikel.artnr == Bill_line.artnr) & (Artikel.departement == Bill_line.departement)).join(Bill,(Bill.rechnr == Bill_line.rechnr)).filter(
                 (Bill_line.bill_datum >= t_payload_list.from_date) & (Bill_line.bill_datum <= t_payload_list.to_date)).order_by(Bill_line._recid).all():
            if bill_line_obj_list.get(bill_line._recid):
                continue
            else:
                bill_line_obj_list[bill_line._recid] = True

            res_line = db_session.query(Res_line).filter(
                     ((Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)) | ((Res_line.resnr == bill.resnr) & (bill.reslinnr == 0))).first()

            if res_line:

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)],"segmentcode": [(ne, 0)]})

                if reservation:

                    revenue_segmlist = query(revenue_segmlist_data, filters=(lambda revenue_segmlist: revenue_segmlist.segment_code == reservation.segmentcode), first=True)

                    if revenue_segmlist:

                        if (artikel.umsatzart == 3 or artikel.umsatzart == 5):
                            revenue_segmlist.rsv_segmfood_rev =  to_decimal(revenue_segmlist.rsv_segmfood_rev) + to_decimal(bill_line.betrag)
                            revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(bill_line.betrag)
                            revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(bill_line.betrag)

                        elif artikel.umsatzart == 6:
                            revenue_segmlist.rsv_segmbev_rev =  to_decimal(revenue_segmlist.rsv_segmbev_rev) + to_decimal(bill_line.betrag)
                            revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(bill_line.betrag)
                            revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(bill_line.betrag)

                        elif artikel.umsatzart == 4:
                            revenue_segmlist.rsv_segmother_rev =  to_decimal(revenue_segmlist.rsv_segmother_rev) + to_decimal(bill_line.betrag)
                            revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(bill_line.betrag)
                            revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(bill_line.betrag)

            if bill.resnr == 0 and bill.reslinnr != 0 and bill.gastnr != 0:

                guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)],"karteityp": [(ge, 1)]})

                if guest:

                    guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)],"segmentcode": [(ne, 0)]})

                    if guestseg:

                        revenue_segmlist = query(revenue_segmlist_data, filters=(lambda revenue_segmlist: revenue_segmlist.segment_code == reservation.segmentcode), first=True)

                        if revenue_segmlist:

                            if (artikel.umsatzart == 3 or artikel.umsatzart == 5):
                                revenue_segmlist.rsv_segmfood_rev =  to_decimal(revenue_segmlist.rsv_segmfood_rev) + to_decimal(bill_line.betrag)
                                revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(bill_line.betrag)
                                revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(bill_line.betrag)

                            elif artikel.umsatzart == 6:
                                revenue_segmlist.rsv_segmbev_rev =  to_decimal(revenue_segmlist.rsv_segmbev_rev) + to_decimal(bill_line.betrag)
                                revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(bill_line.betrag)
                                revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(bill_line.betrag)

                            elif artikel.umsatzart == 4:
                                revenue_segmlist.rsv_segmother_rev =  to_decimal(revenue_segmlist.rsv_segmother_rev) + to_decimal(bill_line.betrag)
                                revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(bill_line.betrag)
                                revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(bill_line.betrag)


                else:

                    revenue_segmlist = query(revenue_segmlist_data, filters=(lambda revenue_segmlist: revenue_segmlist.segment_code == 9999), first=True)

                    if revenue_segmlist:

                        if (artikel.umsatzart == 3 or artikel.umsatzart == 5):
                            revenue_segmlist.rsv_segmfood_rev =  to_decimal(revenue_segmlist.rsv_segmfood_rev) + to_decimal(bill_line.betrag)
                            revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(bill_line.betrag)
                            revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(bill_line.betrag)

                        elif artikel.umsatzart == 6:
                            revenue_segmlist.rsv_segmbev_rev =  to_decimal(revenue_segmlist.rsv_segmbev_rev) + to_decimal(bill_line.betrag)
                            revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(bill_line.betrag)
                            revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(bill_line.betrag)

                        elif artikel.umsatzart == 4:
                            revenue_segmlist.rsv_segmother_rev =  to_decimal(revenue_segmlist.rsv_segmother_rev) + to_decimal(bill_line.betrag)
                            revenue_segmlist.rsv_segmtotal_rev =  to_decimal(revenue_segmlist.rsv_segmtotal_rev) + to_decimal(bill_line.betrag)
                            revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(bill_line.betrag)


    def create_bill_outlet():

        nonlocal revenue_segmlist_data, curr_date, bill_date, ci_date, from_date, to_date, htparam, segment, queasy, arrangement, genstat, artikel, argt_line, reservation, res_line, bill, bill_line, guest, guestseg, h_journal, h_bill, h_artikel


        nonlocal t_payload_list, revenue_segmlist, revenue_room_other
        nonlocal revenue_segmlist_data, revenue_room_other_data

        guest_no:int = 0

        h_journal = get_cache (H_journal, {"bill_datum": [(ge, t_payload_list.from_date),(le, t_payload_list.to_date)]})
        while None != h_journal:
            guest_no = 0

            h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)],"bilname": [(ne, "")]})

            if h_bill:

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_journal.artnr)],"departement": [(eq, h_journal.departement)],"artart": [(eq, 0)]})

                if h_artikel:

                    artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                    if artikel:

                        if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                            if res_line:
                                guest_no = res_line.gastnrmember

                        elif h_bill.resnr > 0:
                            guest_no = h_bill.resnr

                        if guest_no != 0 and h_bill.segmentcode != 0:

                            revenue_segmlist = query(revenue_segmlist_data, filters=(lambda revenue_segmlist: revenue_segmlist.segment_code == h_bill.segmentcode), first=True)

                            if revenue_segmlist:

                                if (artikel.umsatzart == 3 or artikel.umsatzart == 5):
                                    revenue_segmlist.outlet_segmfood_rev =  to_decimal(revenue_segmlist.outlet_segmfood_rev) + to_decimal(h_journal.betrag)
                                    revenue_segmlist.outlet_segmtotal_rev =  to_decimal(revenue_segmlist.outlet_segmtotal_rev) + to_decimal(h_journal.betrag)
                                    revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(h_journal.betrag)

                                elif artikel.umsatzart == 6:
                                    revenue_segmlist.outlet_segmbev_rev =  to_decimal(revenue_segmlist.outlet_segmbev_rev) + to_decimal(h_journal.betrag)
                                    revenue_segmlist.outlet_segmtotal_rev =  to_decimal(revenue_segmlist.outlet_segmtotal_rev) + to_decimal(h_journal.betrag)
                                    revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(h_journal.betrag)

                                elif artikel.umsatzart == 4:
                                    revenue_segmlist.outlet_segmother_rev =  to_decimal(revenue_segmlist.outlet_segmother_rev) + to_decimal(h_journal.betrag)
                                    revenue_segmlist.outlet_segmtotal_rev =  to_decimal(revenue_segmlist.outlet_segmtotal_rev) + to_decimal(h_journal.betrag)
                                    revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(h_journal.betrag)


                        else:

                            revenue_segmlist = query(revenue_segmlist_data, filters=(lambda revenue_segmlist: revenue_segmlist.segment_code == 9999), first=True)

                            if revenue_segmlist:

                                if (artikel.umsatzart == 3 or artikel.umsatzart == 5):
                                    revenue_segmlist.outlet_segmfood_rev =  to_decimal(revenue_segmlist.outlet_segmfood_rev) + to_decimal(h_journal.betrag)
                                    revenue_segmlist.outlet_segmtotal_rev =  to_decimal(revenue_segmlist.outlet_segmtotal_rev) + to_decimal(h_journal.betrag)
                                    revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(h_journal.betrag)

                                elif artikel.umsatzart == 6:
                                    revenue_segmlist.outlet_segmbev_rev =  to_decimal(revenue_segmlist.outlet_segmbev_rev) + to_decimal(h_journal.betrag)
                                    revenue_segmlist.outlet_segmtotal_rev =  to_decimal(revenue_segmlist.outlet_segmtotal_rev) + to_decimal(h_journal.betrag)
                                    revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(h_journal.betrag)

                                elif artikel.umsatzart == 4:
                                    revenue_segmlist.outlet_segmother_rev =  to_decimal(revenue_segmlist.outlet_segmother_rev) + to_decimal(h_journal.betrag)
                                    revenue_segmlist.outlet_segmtotal_rev =  to_decimal(revenue_segmlist.outlet_segmtotal_rev) + to_decimal(h_journal.betrag)
                                    revenue_segmlist.grand_total =  to_decimal(revenue_segmlist.grand_total) + to_decimal(h_journal.betrag)

            curr_recid = h_journal._recid
            h_journal = db_session.query(H_journal).filter(
                     (H_journal.bill_datum >= t_payload_list.from_date) & (H_journal.bill_datum <= t_payload_list.to_date) & (H_journal._recid > curr_recid)).first()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    t_payload_list = query(t_payload_list_data, first=True)

    for segment in db_session.query(Segment).filter(
             (not_(matches(Segment.bezeich,"*$$0*")))).order_by(Segment._recid).all():
        revenue_segmlist = Revenue_segmlist()
        revenue_segmlist_data.append(revenue_segmlist)

        revenue_segmlist.segment_code = segment.segmentcode
        revenue_segmlist.segmemt_short_desc = segment.bezeich
        revenue_segmlist.segment_description = segment.bemerkung

        queasy = get_cache (Queasy, {"key": [(eq, 26)],"number1": [(eq, segment.segmentgrup)]})

        if queasy:
            revenue_segmlist.segment_group = queasy.char3
    revenue_segmlist = Revenue_segmlist()
    revenue_segmlist_data.append(revenue_segmlist)

    revenue_segmlist.segment_code = 9999
    revenue_segmlist.segmemt_short_desc = "UNKNOWN"


    for curr_date in date_range(t_payload_list.from_date,t_payload_list.to_date) :

        if curr_date < ci_date:
            create_history()
        else:
            create_forecast()
    create_bill_fo()
    create_bill_outlet()

    return generate_output()