#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill_line, H_artikel, Guest, Mc_guest, Queasy, Hoteldpt, H_journal, H_bill, Res_line, Artikel

def rest_journal_v2bl(od_taker:string, from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, sorttype:int, long_digit:bool, mc_sort:string):

    prepare_cache ([H_bill_line, H_artikel, Guest, Mc_guest, Queasy, Hoteldpt, H_journal, Res_line, Artikel])

    output_list_list = []
    billnumber:int = 0
    total_bill:Decimal = to_decimal("0.0")
    total_amt:Decimal = to_decimal("0.0")
    total_billextns:Decimal = to_decimal("0.0")
    total_qty:Decimal = to_decimal("0.0")
    dept_str:string = ""
    grandtotal_bill:Decimal = to_decimal("0.0")
    grandtotal_afterdisc:Decimal = to_decimal("0.0")
    grandtotal_amt:Decimal = to_decimal("0.0")
    grandtotal_afterdisc_extns:Decimal = to_decimal("0.0")
    gtotal_bill:Decimal = to_decimal("0.0")
    gtotal_afterdisc:Decimal = to_decimal("0.0")
    gtotal_amt:Decimal = to_decimal("0.0")
    gtotal_afterdisc_extns:Decimal = to_decimal("0.0")
    total_amtincltns:Decimal = to_decimal("0.0")
    guestno:int = 0
    h_bill_line = h_artikel = guest = mc_guest = queasy = hoteldpt = h_journal = h_bill = res_line = artikel = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"h_recid":int, "str":string, "gname":string, "fart_bez":string, "total_trans":Decimal, "total_afterdisc":Decimal, "total_afterdisc_extns":Decimal, "member_code":string, "member_email":string, "department":string, "art_amount":Decimal, "gastno":int, "deptno":int, "payment":string, "datum":string, "tableno":string, "bill_no":int, "art_no":int, "descr":string, "qty":int, "time_str":string, "id_str":string, "order_taker":string, "room_no":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, billnumber, total_bill, total_amt, total_billextns, total_qty, dept_str, grandtotal_bill, grandtotal_afterdisc, grandtotal_amt, grandtotal_afterdisc_extns, gtotal_bill, gtotal_afterdisc, gtotal_amt, gtotal_afterdisc_extns, total_amtincltns, guestno, h_bill_line, h_artikel, guest, mc_guest, queasy, hoteldpt, h_journal, h_bill, res_line, artikel
        nonlocal od_taker, from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, long_digit, mc_sort


        nonlocal output_list
        nonlocal output_list_list

        return {"output-list": output_list_list}

    def journal_list():

        nonlocal output_list_list, billnumber, total_bill, total_amt, total_billextns, total_qty, dept_str, grandtotal_bill, grandtotal_afterdisc, grandtotal_amt, grandtotal_afterdisc_extns, gtotal_bill, gtotal_afterdisc, gtotal_amt, gtotal_afterdisc_extns, total_amtincltns, guestno, h_bill_line, h_artikel, guest, mc_guest, queasy, hoteldpt, h_journal, h_bill, res_line, artikel
        nonlocal od_taker, from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, long_digit, mc_sort


        nonlocal output_list
        nonlocal output_list_list

        last_dept:int = -1
        qty:int = 0
        takernum:int = 0
        sub_tot:Decimal = to_decimal("0.0")
        tot:Decimal = to_decimal("0.0")
        curr_date:date = None
        it_exist:bool = False
        do_it:bool = False
        curr_guest:string = ""
        curr_gastnr:int = 0
        curr_room:string = ""
        membercode:string = ""
        guest_mail:string = ""
        tot_qty:int = 0
        order_taker:string = ""
        dept:int = 0
        output_list_list.clear()

        if od_taker != "":

            queasy = get_cache (Queasy, {"key": [(eq, 10)],"char2": [(eq, od_taker)]})

            if queasy:
                takernum = queasy.number1

        if mc_sort == 'sart':
            last_dept = - 1

            h_artikel_obj_list = {}
            h_artikel = H_artikel()
            hoteldpt = Hoteldpt()
            for h_artikel.departement, h_artikel.artnr, h_artikel.artnrfront, h_artikel.bezeich, h_artikel.artart, h_artikel._recid, hoteldpt.depart, hoteldpt._recid in db_session.query(H_artikel.departement, H_artikel.artnr, H_artikel.artnrfront, H_artikel.bezeich, H_artikel.artart, H_artikel._recid, Hoteldpt.depart, Hoteldpt._recid).join(Hoteldpt,(Hoteldpt.num == H_artikel.departement)).filter(
                     (H_artikel.artnr >= from_art) & (H_artikel.artnr <= to_art) & (H_artikel.departement >= from_dept) & (H_artikel.departement <= to_dept)).order_by(artikel.bezeich, H_artikel.departement, H_artikel.artnr).all():
                if h_artikel_obj_list.get(h_artikel._recid):
                    continue
                else:
                    h_artikel_obj_list[h_artikel._recid] = True


                last_dept = h_artikel.departement
                sub_tot =  to_decimal("0")
                it_exist = False
                qty = 0

                if h_artikel.artart <= 1:
                    dept = h_artikel.departement
                else:
                    dept = 0
                for curr_date in date_range(from_date,to_date) :

                    if sorttype == 0:

                        for h_journal in db_session.query(H_journal).filter(
                                 (H_journal.artnr == h_artikel.artnr) & (H_journal.departement == h_artikel.departement) & (H_journal.bill_datum == curr_date) & (H_journal.artnr > 0) & (H_journal.anzahl != 0)).order_by(H_journal._recid).all():
                            order_taker = search_ot(h_journal.rechnr, h_journal.tischnr)
                            curr_guest = ""
                            curr_room = ""
                            membercode = ""
                            guest_mail = ""
                            curr_gastnr = 0

                            h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})

                            if h_bill:

                                if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                                    if res_line:
                                        curr_guest = res_line.name
                                        curr_room = res_line.zinr


                                    curr_gastnr = res_line.gastnrmember

                                elif h_bill.resnr > 0:

                                    guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                    if guest:
                                        curr_guest = guest.name + "," + guest.vorname1
                                        curr_gastnr = guest.gastnr

                                elif h_bill.resnr == 0:
                                    curr_guest = h_bill.bilname

                            if takernum == 0:
                                do_it = True
                            else:
                                do_it = None != h_bill and (h_bill.betriebsnr == takernum)

                            if do_it:
                                it_exist = True
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.gname = curr_guest
                                output_list.h_recid = h_journal._recid
                                output_list.gastno = curr_gastnr
                                output_list.deptno = h_artikel.departement

                                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, dept)]})

                                if artikel:
                                    output_list.fart_bez = artikel.bezeich

                                if not long_digit:
                                    str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, "->,>>>,>>>,>>9.99") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
                                else:
                                    str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, " ->>>,>>>,>>>,>>9") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
                                qty = qty + h_journal.anzahl
                                sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                                tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

                    elif sorttype == 1:

                        for h_journal in db_session.query(H_journal).filter(
                                 (H_journal.artnr == h_artikel.artnr) & (H_journal.departement == h_artikel.departement) & (H_journal.bill_datum == curr_date)).order_by(H_journal._recid).all():
                            order_taker = search_ot(h_journal.rechnr, h_journal.tischnr)
                            curr_guest = ""
                            curr_room = ""
                            curr_gastnr = 0

                            h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})

                            if h_bill:

                                if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                                    if res_line:
                                        curr_guest = res_line.name
                                        curr_room = res_line.zinr


                                    curr_gastnr = res_line.gastnrmember

                                elif h_bill.resnr > 0:

                                    guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                    if guest:
                                        curr_guest = guest.name + "," + guest.vorname1
                                        curr_gastnr = guest.gastnr

                                elif h_bill.resnr == 0:
                                    curr_guest = h_bill.bilname

                            if takernum == 0:
                                do_it = True
                            else:
                                do_it = None != h_bill and (h_bill.betriebsnr == takernum)

                            if do_it:
                                it_exist = True
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.gname = curr_guest
                                output_list.h_recid = h_journal._recid
                                output_list.gastno = curr_gastnr
                                output_list.deptno = h_artikel.departement

                                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, dept)]})

                                if artikel:
                                    output_list.fart_bez = artikel.bezeich

                                if not long_digit:
                                    str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, "->,>>>,>>>,>>9.99") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
                                else:
                                    str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, " ->>>,>>>,>>>,>>9") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
                                qty = qty + h_journal.anzahl
                                sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                                tot =  to_decimal(tot) + to_decimal(h_journal.betrag)
                    else:

                        for h_journal in db_session.query(H_journal).filter(
                                 (H_journal.artnr == h_artikel.artnr) & (H_journal.departement == h_artikel.departement) & (H_journal.bill_datum == curr_date) & (H_journal.anzahl == 0) & (H_journal.artnr == 0)).order_by(H_journal._recid).all():
                            order_taker = search_ot(h_journal.rechnr, h_journal.tischnr)
                            curr_guest = ""
                            curr_room = ""
                            curr_gastnr = 0

                            h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})

                            if h_bill:

                                if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                                    if res_line:
                                        curr_guest = res_line.name
                                        curr_room = res_line.zinr


                                    curr_gastnr = res_line.gastnrmember

                                elif h_bill.resnr > 0:

                                    guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                    if guest:
                                        curr_guest = guest.name + "," + guest.vorname1
                                        curr_gastnr = guest.gastnr

                                elif h_bill.resnr == 0:
                                    curr_guest = h_bill.bilname

                            if takernum == 0:
                                do_it = True
                            else:
                                do_it = None != h_bill and (h_bill.betriebsnr == takernum)

                            if do_it:
                                it_exist = True
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.gname = curr_guest
                                output_list.h_recid = h_journal._recid
                                output_list.gastno = curr_gastnr
                                output_list.deptno = h_artikel.departement

                                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, dept)]})

                                if artikel:
                                    output_list.fart_bez = artikel.bezeich

                                if not long_digit:
                                    str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, "->,>>>,>>>,>>9.99") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
                                else:
                                    str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, " ->>>,>>>,>>>,>>9") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
                                qty = qty + h_journal.anzahl
                                sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                                tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

                if it_exist:
                    tot_qty = qty + tot_qty
                    output_list = Output_list()
                    output_list_list.append(output_list)


                    if not long_digit:
                        str = to_string("", "x(56)") + to_string("T O T A L ", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(56)") + to_string("T O T A L ", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, " ->>>,>>>,>>>,>>9")

        elif mc_sort == 'sdept':
            last_dept = - 1

            h_artikel_obj_list = {}
            h_artikel = H_artikel()
            hoteldpt = Hoteldpt()
            for h_artikel.departement, h_artikel.artnr, h_artikel.artnrfront, h_artikel.bezeich, h_artikel.artart, h_artikel._recid, hoteldpt.depart, hoteldpt._recid in db_session.query(H_artikel.departement, H_artikel.artnr, H_artikel.artnrfront, H_artikel.bezeich, H_artikel.artart, H_artikel._recid, Hoteldpt.depart, Hoteldpt._recid).join(Hoteldpt,(Hoteldpt.num == H_artikel.departement)).filter(
                     (H_artikel.artnr >= from_art) & (H_artikel.artnr <= to_art) & (H_artikel.departement >= from_dept) & (H_artikel.departement <= to_dept)).order_by(H_artikel.departement, H_artikel.artnr).all():
                if h_artikel_obj_list.get(h_artikel._recid):
                    continue
                else:
                    h_artikel_obj_list[h_artikel._recid] = True


                last_dept = h_artikel.departement
                sub_tot =  to_decimal("0")
                it_exist = False
                qty = 0

                if h_artikel.artart <= 1:
                    dept = h_artikel.departement
                else:
                    dept = 0
                for curr_date in date_range(from_date,to_date) :

                    if sorttype == 0:

                        for h_journal in db_session.query(H_journal).filter(
                                 (H_journal.artnr == h_artikel.artnr) & (H_journal.departement == h_artikel.departement) & (H_journal.bill_datum == curr_date) & (H_journal.artnr > 0) & (H_journal.anzahl != 0)).order_by(H_journal._recid).all():
                            order_taker = search_ot(h_journal.rechnr, h_journal.tischnr)
                            curr_guest = ""
                            curr_room = ""
                            curr_gastnr = 0

                            h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})

                            if h_bill:

                                if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                                    if res_line:
                                        curr_guest = res_line.name
                                        curr_room = res_line.zinr


                                    curr_gastnr = res_line.gastnrmember

                                elif h_bill.resnr > 0:

                                    guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                    if guest:
                                        curr_guest = guest.name + "," + guest.vorname1
                                        curr_gastnr = guest.gastnr

                                elif h_bill.resnr == 0:
                                    curr_guest = h_bill.bilname

                            if takernum == 0:
                                do_it = True
                            else:
                                do_it = None != h_bill and (h_bill.betriebsnr == takernum)

                            if do_it:
                                it_exist = True
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.gname = curr_guest
                                output_list.h_recid = h_journal._recid
                                output_list.gastno = curr_gastnr
                                output_list.deptno = h_artikel.departement

                                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, dept)]})

                                if artikel:
                                    output_list.fart_bez = artikel.bezeich

                                if not long_digit:
                                    str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, "->,>>>,>>>,>>9.99") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
                                else:
                                    str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, " ->>>,>>>,>>>,>>9") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
                                qty = qty + h_journal.anzahl
                                sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                                tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

                    elif sorttype == 1:

                        for h_journal in db_session.query(H_journal).filter(
                                 (H_journal.artnr == h_artikel.artnr) & (H_journal.departement == h_artikel.departement) & (H_journal.bill_datum == curr_date)).order_by(H_journal._recid).all():
                            order_taker = search_ot(h_journal.rechnr, h_journal.tischnr)
                            curr_guest = ""
                            curr_room = ""
                            curr_gastnr = 0

                            h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})

                            if h_bill:

                                if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                                    if res_line:
                                        curr_guest = res_line.name
                                        curr_room = res_line.zinr


                                    curr_gastnr = res_line.gastnrmember

                                elif h_bill.resnr > 0:

                                    guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                    if guest:
                                        curr_guest = guest.name + "," + guest.vorname1
                                        curr_gastnr = guest.gastnr

                                elif h_bill.resnr == 0:
                                    curr_guest = h_bill.bilname

                            if takernum == 0:
                                do_it = True
                            else:
                                do_it = None != h_bill and (h_bill.betriebsnr == takernum)

                            if do_it:
                                it_exist = True
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.gname = curr_guest
                                output_list.h_recid = h_journal._recid
                                output_list.gastno = curr_gastnr
                                output_list.deptno = h_artikel.departement

                                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, dept)]})

                                if artikel:
                                    output_list.fart_bez = artikel.bezeich

                                if not long_digit:
                                    str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, "->,>>>,>>>,>>9.99") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
                                else:
                                    str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, " ->>>,>>>,>>>,>>9") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
                                qty = qty + h_journal.anzahl
                                sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                                tot =  to_decimal(tot) + to_decimal(h_journal.betrag)
                    else:

                        for h_journal in db_session.query(H_journal).filter(
                                 (H_journal.artnr == h_artikel.artnr) & (H_journal.departement == h_artikel.departement) & (H_journal.bill_datum == curr_date) & (H_journal.anzahl == 0) & (H_journal.artnr == 0)).order_by(H_journal._recid).all():
                            order_taker = search_ot(h_journal.rechnr, h_journal.tischnr)
                            curr_guest = ""
                            curr_room = ""
                            curr_gastnr = 0

                            h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})

                            if h_bill:

                                if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                                    if res_line:
                                        curr_guest = res_line.name
                                        curr_room = res_line.zinr


                                    curr_gastnr = res_line.gastnrmember

                                elif h_bill.resnr > 0:

                                    guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                                    if guest:
                                        curr_guest = guest.name + "," + guest.vorname1
                                        curr_gastnr = guest.gastnr

                                elif h_bill.resnr == 0:
                                    curr_guest = h_bill.bilname

                            if takernum == 0:
                                do_it = True
                            else:
                                do_it = None != h_bill and (h_bill.betriebsnr == takernum)

                            if do_it:
                                it_exist = True
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.gname = curr_guest
                                output_list.h_recid = h_journal._recid
                                output_list.gastno = curr_gastnr
                                output_list.deptno = h_artikel.departement

                                artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, dept)]})

                                if artikel:
                                    output_list.fart_bez = artikel.bezeich

                                if not long_digit:
                                    str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, "->,>>>,>>>,>>9.99") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
                                else:
                                    str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, " ->>>,>>>,>>>,>>9") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
                                qty = qty + h_journal.anzahl
                                sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                                tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

                if it_exist:
                    tot_qty = qty + tot_qty
                    output_list = Output_list()
                    output_list_list.append(output_list)


                    if not long_digit:
                        str = to_string("", "x(56)") + to_string("T O T A L ", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, "->,>>>,>>>,>>9.99")
                    else:
                        str = to_string("", "x(56)") + to_string("T O T A L ", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)


        if not long_digit:
            str = to_string("", "x(56)") + to_string("Grand TOTAL ", "x(20)") + to_string(tot_qty, "->>>9") + to_string(tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(56)") + to_string("Grand TOTAL ", "x(20)") + to_string(tot_qty, "->>>9") + to_string(tot, " ->>>,>>>,>>>,>>9")


    def search_ot(r_nr:int, t_nr:int):

        nonlocal output_list_list, billnumber, total_bill, total_amt, total_billextns, total_qty, dept_str, grandtotal_bill, grandtotal_afterdisc, grandtotal_amt, grandtotal_afterdisc_extns, gtotal_bill, gtotal_afterdisc, gtotal_amt, gtotal_afterdisc_extns, total_amtincltns, guestno, h_bill_line, h_artikel, guest, mc_guest, queasy, hoteldpt, h_journal, h_bill, res_line, artikel
        nonlocal od_taker, from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, long_digit, mc_sort


        nonlocal output_list
        nonlocal output_list_list

        order_taker = ""

        def generate_inner_output():
            return (order_taker)


        h_bill = get_cache (H_bill, {"rechnr": [(eq, r_nr)],"tischnr": [(eq, t_nr)]})

        if h_bill:

            queasy = get_cache (Queasy, {"key": [(eq, 10)],"number1": [(eq, h_bill.betriebsnr)]})

        if queasy:
            order_taker = queasy.char2

        return generate_inner_output()

    journal_list()

    for output_list in query(output_list_list):
        output_list.datum = substring(output_list.str, 0, 8)
        output_list.tableno = substring(output_list.str, 8, 6)
        output_list.bill_no = to_int(substring(output_list.str, 14, 9))
        output_list.art_no = to_int(substring(output_list.str, 23, 5))
        output_list.descr = substring(output_list.str, 28, 28)
        output_list.qty = to_int(substring(output_list.str, 76, 5))
        output_list.time_str = substring(output_list.str, 98, 8)
        output_list.id_str = substring(output_list.str, 106, 3)
        output_list.order_taker = substring(output_list.str, 109, 8)
        output_list.room_no = substring(output_list.str, 118, 8)
        dept_str = substring(output_list.str, 56, 20)

        if matches(substring(output_list.str, 56, 20),r"*T O T A L*"):
            output_list.department = "T O T A L"
            output_list.total_trans =  to_decimal(grandtotal_bill)
            output_list.total_afterdisc =  to_decimal(grandtotal_afterdisc)
            output_list.total_afterdisc_extns =  to_decimal(grandtotal_afterdisc_extns)
            output_list.art_amount =  to_decimal(grandtotal_amt)


            gtotal_bill =  to_decimal(gtotal_bill) + to_decimal(grandtotal_bill)
            gtotal_afterdisc =  to_decimal(gtotal_afterdisc) + to_decimal(grandtotal_afterdisc)
            gtotal_amt =  to_decimal(gtotal_amt) + to_decimal(grandtotal_amt)
            gtotal_afterdisc_extns =  to_decimal(gtotal_afterdisc_extns) + to_decimal(grandtotal_afterdisc_extns)
            grandtotal_bill =  to_decimal("0")
            grandtotal_afterdisc =  to_decimal("0")
            grandtotal_afterdisc_extns =  to_decimal("0")
            grandtotal_amt =  to_decimal("0")

        elif matches(substring(output_list.str, 56, 20),r"*TOTAL*"):
            output_list.department = "GRAND T O T A L"
            output_list.total_trans =  to_decimal(gtotal_bill)
            output_list.total_afterdisc =  to_decimal(gtotal_afterdisc)
            output_list.total_afterdisc_extns =  to_decimal(gtotal_afterdisc_extns)
            output_list.art_amount =  to_decimal(gtotal_amt)


            gtotal_bill =  to_decimal("0")
            gtotal_afterdisc =  to_decimal("0")
            gtotal_amt =  to_decimal("0")
            gtotal_afterdisc_extns =  to_decimal("0")
        else:
            output_list.department = substring(output_list.str, 56, 20)
            output_list.art_amount = to_decimal(substring(output_list.str, 81, 17))
            billnumber = to_int(substring(output_list.str, 14, 9))
            total_bill =  to_decimal("0")
            total_billextns =  to_decimal("0")
            total_qty =  to_decimal("0")
            total_amt =  to_decimal("0")
            total_amtincltns =  to_decimal("0")

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.departemen == output_list.deptno) & (H_bill_line.rechnr == billnumber) & (H_bill_line.artnr != 8911)).order_by(H_bill_line._recid).all():

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departemen)],"artart": [(ne, 2),(ne, 7),(ne, 6),(ne, 11),(ne, 12)]})

                if h_artikel:
                    total_bill =  to_decimal(total_bill) + to_decimal(h_bill_line.betrag)
                    total_billextns =  to_decimal(total_billextns) + to_decimal((h_bill_line.epreis) * to_decimal(h_bill_line.anzahl))

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.departemen == output_list.deptno) & (H_bill_line.rechnr == billnumber) & (H_bill_line.artnr >= 8911) & (H_bill_line.artnr <= 8912) & (H_bill_line.epreis < 0)).order_by(H_bill_line._recid).all():
                total_amt =  to_decimal(total_amt) + to_decimal(h_bill_line.epreis)
                total_amtincltns =  to_decimal(total_amtincltns) + to_decimal(h_bill_line.betrag)

            for h_bill_line in db_session.query(H_bill_line).filter(
                     (H_bill_line.departemen == output_list.deptno) & (H_bill_line.rechnr == billnumber)).order_by(H_bill_line._recid).all():

                if h_bill_line.artnr == 0:
                    output_list.payment = h_bill_line.bezeich
                else:

                    h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departemen)],"artart": [(ne, 0)]})

                    if h_artikel and h_bill_line.betrag < 0:
                        output_list.payment = to_string(h_artikel.artnr) + "-" + h_artikel.bezeich
            output_list.total_trans =  to_decimal(total_bill)
            output_list.total_afterdisc =  to_decimal(total_bill) + to_decimal(total_amtincltns)
            output_list.total_afterdisc_extns =  to_decimal(total_billextns) + to_decimal(total_amt)

            if dept_str != substring(output_list.str, 56, 20):
                dept_str = substring(output_list.str, 56, 20)
                grandtotal_bill =  to_decimal("0")
                grandtotal_afterdisc =  to_decimal("0")
                grandtotal_afterdisc_extns =  to_decimal("0")
                grandtotal_amt =  to_decimal("0")
            else:
                grandtotal_bill =  to_decimal(grandtotal_bill) + to_decimal(output_list.total_trans)
                grandtotal_afterdisc =  to_decimal(grandtotal_afterdisc) + to_decimal(output_list.total_afterdisc)
                grandtotal_afterdisc_extns =  to_decimal(grandtotal_afterdisc_extns) + to_decimal(output_list.total_afterdisc_extns)
                grandtotal_amt =  to_decimal(grandtotal_amt) + to_decimal(output_list.art_amount)

        if output_list.gastno != 0:

            guest = get_cache (Guest, {"gastnr": [(eq, output_list.gastno)]})

            if guest:
                output_list.member_email = guest.email_adr

            mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, output_list.gastno)]})

            if mc_guest:
                output_list.member_code = mc_guest.cardnum

    output_list = query(output_list_list, first=True)
    while None != output_list:

        output_list = query(output_list_list, next=True)

    return generate_output()