#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Queasy, Hoteldpt, H_journal, H_bill, Res_line, Guest, H_artikel

def rest_journal_btn_go2webbl(od_taker:string, from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, sorttype:int, long_digit:bool):

    prepare_cache ([Htparam, Queasy, Hoteldpt, H_journal, Res_line, Guest, H_artikel])

    output_list_data = []
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    curr_time:int = 0
    counter:int = 0
    counter2:int = 0
    htparam = queasy = hoteldpt = h_journal = h_bill = res_line = guest = h_artikel = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"date1":date, "tableno":int, "billno":int, "artno":int, "bezeich":string, "depart":string, "qty":int, "amount":string, "zeit":int, "id":string, "guestname":string, "h_recid":int, "order_taker":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, disc_art1, disc_art2, disc_art3, curr_time, counter, counter2, htparam, queasy, hoteldpt, h_journal, h_bill, res_line, guest, h_artikel
        nonlocal od_taker, from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, long_digit


        nonlocal output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def journal_list():

        nonlocal output_list_data, disc_art1, disc_art2, disc_art3, counter, counter2, htparam, queasy, hoteldpt, h_journal, h_bill, res_line, guest, h_artikel
        nonlocal od_taker, from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, long_digit


        nonlocal output_list
        nonlocal output_list_data

        last_dept:int = -1
        qty:int = 0
        takernum:int = 0
        sub_tot:Decimal = to_decimal("0.0")
        tot:Decimal = to_decimal("0.0")
        curr_date:date = None
        it_exist:bool = False
        do_it:bool = False
        curr_guest:string = ""
        tot_qty:int = 0
        order_taker:string = ""
        hotel_num:int = 0
        curr_time:int = 0
        curr_artikel:int = 0
        output_list_data.clear()

        if od_taker != "":

            queasy = get_cache (Queasy, {"key": [(eq, 10)],"char2": [(eq, od_taker)]})

            if queasy:
                takernum = queasy.number1

        if from_art == 0:
            sub_tot =  to_decimal("0")
            it_exist = False
            qty = 0

            if sorttype == 0:

                h_journal_obj_list = {}
                h_journal = H_journal()
                hoteldpt = Hoteldpt()
                for h_journal.rechnr, h_journal.tischnr, h_journal.departement, h_journal.artnr, h_journal.betrag, h_journal._recid, h_journal.bill_datum, h_journal.bezeich, h_journal.anzahl, h_journal.zeit, h_journal.kellner_nr, hoteldpt.num, hoteldpt.depart, hoteldpt._recid in db_session.query(H_journal.rechnr, H_journal.tischnr, H_journal.departement, H_journal.artnr, H_journal.betrag, H_journal._recid, H_journal.bill_datum, H_journal.bezeich, H_journal.anzahl, H_journal.zeit, H_journal.kellner_nr, Hoteldpt.num, Hoteldpt.depart, Hoteldpt._recid).join(Hoteldpt,(Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).filter(
                         (H_journal.artnr == 0) & (H_journal.departement == hoteldpt.num) & (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date) & (H_journal.artnr > 0) & (H_journal.anzahl != 0)).order_by(Hoteldpt.num).all():
                    if h_journal_obj_list.get(h_journal._recid):
                        continue
                    else:
                        h_journal_obj_list[h_journal._recid] = True

                    if hotel_num != 0 and hotel_num != hoteldpt.num:

                        if it_exist:
                            output_list = Output_list()
                            output_list_data.append(output_list)


                            if long_digit == False:
                                output_list.bezeich = "T O T A L "
                                output_list.qty = qty
                                output_list.amount = to_string(sub_tot, "->,>>>,>>>,>>9.99")
                            else:
                                output_list.bezeich = "T O T A L "
                                output_list.qty = qty
                                output_list.amount = to_string(sub_tot, " ->>>,>>>,>>>,>>9")
                        sub_tot =  to_decimal("0")
                        it_exist = False
                        qty = 0
                        hotel_num = 0


                    hotel_num = hoteldpt.num


                    order_taker = search_ot(h_journal.rechnr, h_journal.tischnr)
                    curr_guest = ""

                    h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})

                    if h_bill:

                        if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                            if res_line:
                                curr_guest = res_line.name

                        elif h_bill.resnr > 0:

                            guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                            if guest:
                                curr_guest = guest.name + "," + guest.vorname1

                        elif h_bill.resnr == 0:
                            curr_guest = h_bill.bilname

                    if takernum == 0:
                        do_it = True
                    else:
                        do_it = None != h_bill and (h_bill.betriebsnr == takernum)

                    if (h_journal.artnr == disc_art1 or h_journal.artnr == disc_art2 or h_journal.artnr == disc_art2) and h_journal.betrag == 0:
                        it_exist = True
                        do_it = False

                    if do_it:
                        it_exist = True
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.guestname = curr_guest
                        output_list.h_recid = h_journal._recid

                        if not long_digit:
                            output_list.date1 = h_journal.bill_datum
                            output_list.tableno = h_journal.tischnr
                            output_list.billno = h_journal.rechnr
                            output_list.artno = h_journal.artnr
                            output_list.bezeich = h_journal.bezeich
                            output_list.depart = hoteldpt.depart
                            output_list.qty = h_journal.anzahl
                            output_list.amount = to_string(h_journal.betrag, "->,>>>,>>>,>>9.99")
                            output_list.zeit = h_journal.zeit
                            output_list.id = to_string(h_journal.kellner_nr, "9999")
                            output_list.order_taker = order_taker
                        else:
                            output_list.date1 = h_journal.bill_datum
                            output_list.tableno = h_journal.tischnr
                            output_list.billno = h_journal.rechnr
                            output_list.artno = h_journal.artnr
                            output_list.bezeich = h_journal.bezeich
                            output_list.depart = hoteldpt.depart
                            output_list.qty = h_journal.anzahl
                            output_list.amount = to_string(h_journal.betrag, "->,>>>,>>>,>>9.99")
                            output_list.zeit = h_journal.zeit
                            output_list.id = to_string(h_journal.kellner_nr, "9999")
                            output_list.order_taker = order_taker
                        qty = qty + h_journal.anzahl
                        sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                        tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

            elif sorttype == 1:
                curr_time = get_current_time_in_seconds()

                h_journal_obj_list = {}
                h_journal = H_journal()
                hoteldpt = Hoteldpt()
                for h_journal.rechnr, h_journal.tischnr, h_journal.departement, h_journal.artnr, h_journal.betrag, h_journal._recid, h_journal.bill_datum, h_journal.bezeich, h_journal.anzahl, h_journal.zeit, h_journal.kellner_nr, hoteldpt.num, hoteldpt.depart, hoteldpt._recid in db_session.query(H_journal.rechnr, H_journal.tischnr, H_journal.departement, H_journal.artnr, H_journal.betrag, H_journal._recid, H_journal.bill_datum, H_journal.bezeich, H_journal.anzahl, H_journal.zeit, H_journal.kellner_nr, Hoteldpt.num, Hoteldpt.depart, Hoteldpt._recid).join(Hoteldpt,(Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).filter(
                         (H_journal.artnr == 0) & (H_journal.departement == hoteldpt.num) & (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date)).order_by(Hoteldpt.num).all():
                    if h_journal_obj_list.get(h_journal._recid):
                        continue
                    else:
                        h_journal_obj_list[h_journal._recid] = True

                    if hotel_num != 0 and hotel_num != hoteldpt.num:

                        if it_exist:
                            output_list = Output_list()
                            output_list_data.append(output_list)


                            if long_digit == False:
                                output_list.bezeich = "T O T A L "
                                output_list.qty = qty
                                output_list.amount = to_string(sub_tot, "->,>>>,>>>,>>9.99")
                            else:
                                output_list.bezeich = "T O T A L "
                                output_list.qty = qty
                                output_list.amount = to_string(sub_tot, " ->>>,>>>,>>>,>>9")
                        sub_tot =  to_decimal("0")
                        it_exist = False
                        qty = 0
                        hotel_num = 0


                    hotel_num = hoteldpt.num


                    order_taker = search_ot(h_journal.rechnr, h_journal.tischnr)
                    curr_guest = ""

                    h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})

                    if h_bill:

                        if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                            if res_line:
                                curr_guest = res_line.name

                        elif h_bill.resnr > 0:

                            guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                            if guest:
                                curr_guest = guest.name + "," + guest.vorname1

                        elif h_bill.resnr == 0:
                            curr_guest = h_bill.bilname

                    if takernum == 0:
                        do_it = True
                    else:
                        do_it = None != h_bill and (h_bill.betriebsnr == takernum)

                    if (h_journal.artnr == disc_art1 or h_journal.artnr == disc_art2 or h_journal.artnr == disc_art2) and h_journal.betrag == 0:
                        it_exist = True
                        do_it = False

                    if do_it:
                        it_exist = True
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.guestname = curr_guest
                        output_list.h_recid = h_journal._recid

                        if long_digit == False:
                            output_list.date1 = h_journal.bill_datum
                            output_list.tableno = h_journal.tischnr
                            output_list.billno = h_journal.rechnr
                            output_list.artno = h_journal.artnr
                            output_list.bezeich = h_journal.bezeich
                            output_list.depart = hoteldpt.depart
                            output_list.qty = h_journal.anzahl
                            output_list.amount = to_string(h_journal.betrag, "->,>>>,>>>,>>9.99")
                            output_list.zeit = h_journal.zeit
                            output_list.id = to_string(h_journal.kellner_nr, "9999")
                            output_list.order_taker = order_taker
                        else:
                            output_list.date1 = h_journal.bill_datum
                            output_list.tableno = h_journal.tischnr
                            output_list.billno = h_journal.rechnr
                            output_list.artno = h_journal.artnr
                            output_list.bezeich = h_journal.bezeich
                            output_list.depart = hoteldpt.depart
                            output_list.qty = h_journal.anzahl
                            output_list.amount = to_string(h_journal.betrag, "->>>,>>>,>>>,>>9")
                            output_list.zeit = h_journal.zeit
                            output_list.id = to_string(h_journal.kellner_nr, "9999")
                            output_list.order_taker = order_taker
                        qty = qty + h_journal.anzahl
                        sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                        tot =  to_decimal(tot) + to_decimal(h_journal.betrag)
                    counter = counter + 1
            else:
                curr_time = get_current_time_in_seconds()

                h_journal_obj_list = {}
                h_journal = H_journal()
                hoteldpt = Hoteldpt()
                for h_journal.rechnr, h_journal.tischnr, h_journal.departement, h_journal.artnr, h_journal.betrag, h_journal._recid, h_journal.bill_datum, h_journal.bezeich, h_journal.anzahl, h_journal.zeit, h_journal.kellner_nr, hoteldpt.num, hoteldpt.depart, hoteldpt._recid in db_session.query(H_journal.rechnr, H_journal.tischnr, H_journal.departement, H_journal.artnr, H_journal.betrag, H_journal._recid, H_journal.bill_datum, H_journal.bezeich, H_journal.anzahl, H_journal.zeit, H_journal.kellner_nr, Hoteldpt.num, Hoteldpt.depart, Hoteldpt._recid).join(Hoteldpt,(Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).filter(
                         (H_journal.artnr == 0) & (H_journal.departement == hoteldpt.num) & (H_journal.bill_datum == from_date) & (H_journal.bill_datum == to_date) & (H_journal.artnr == 0)).order_by(Hoteldpt.num).all():
                    if h_journal_obj_list.get(h_journal._recid):
                        continue
                    else:
                        h_journal_obj_list[h_journal._recid] = True

                    if hotel_num != 0 and hotel_num != hoteldpt.num:

                        if it_exist:
                            output_list = Output_list()
                            output_list_data.append(output_list)


                            if long_digit == False:
                                output_list.bezeich = "T O T A L "
                                output_list.qty = qty
                                output_list.amount = to_string(sub_tot, "->,>>>,>>>,>>9.99")
                            else:
                                output_list.bezeich = "T O T A L "
                                output_list.qty = qty
                                output_list.amount = to_string(sub_tot, " ->>>,>>>,>>>,>>9")
                        sub_tot =  to_decimal("0")
                        it_exist = False
                        qty = 0
                        hotel_num = 0


                    hotel_num = hoteldpt.num


                    order_taker = search_ot(h_journal.rechnr, h_journal.tischnr)
                    curr_guest = ""

                    h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})

                    if h_bill:

                        if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                            res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                            if res_line:
                                curr_guest = res_line.name

                        elif h_bill.resnr > 0:

                            guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                            if guest:
                                curr_guest = guest.name + "," + guest.vorname1

                        elif h_bill.resnr == 0:
                            curr_guest = h_bill.bilname

                    if takernum == 0:
                        do_it = True
                    else:
                        do_it = None != h_bill and (h_bill.betriebsnr == takernum)

                    if (h_journal.artnr == disc_art1 or h_journal.artnr == disc_art2 or h_journal.artnr == disc_art2) and h_journal.betrag == 0:
                        it_exist = True
                        do_it = False

                    if do_it:
                        it_exist = True
                        output_list = Output_list()
                        output_list_data.append(output_list)

                        output_list.guestname = curr_guest
                        output_list.h_recid = h_journal._recid

                        if long_digit == False:
                            output_list.date1 = h_journal.bill_datum
                            output_list.tableno = h_journal.tischnr
                            output_list.billno = h_journal.rechnr
                            output_list.artno = h_journal.artnr
                            output_list.bezeich = h_journal.bezeich
                            output_list.depart = hoteldpt.depart
                            output_list.qty = h_journal.anzahl
                            output_list.amount = to_string(h_journal.betrag, "->,>>>,>>>,>>9.99")
                            output_list.zeit = h_journal.zeit
                            output_list.id = to_string(h_journal.kellner_nr, "9999")
                            output_list.order_taker = order_taker
                        else:
                            output_list.date1 = h_journal.bill_datum
                            output_list.tableno = h_journal.tischnr
                            output_list.billno = h_journal.rechnr
                            output_list.artno = h_journal.artnr
                            output_list.bezeich = h_journal.bezeich
                            output_list.depart = hoteldpt.depart
                            output_list.qty = h_journal.anzahl
                            output_list.amount = to_string(h_journal.betrag, "->>>,>>>,>>>,>>9")
                            output_list.zeit = h_journal.zeit
                            output_list.id = to_string(h_journal.kellner_nr, "9999")
                            output_list.order_taker = order_taker
                        qty = qty + h_journal.anzahl
                        sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                        tot =  to_decimal(tot) + to_decimal(h_journal.betrag)
                    counter = counter + 1

            if it_exist:
                output_list = Output_list()
                output_list_data.append(output_list)


                if long_digit == False:
                    output_list.bezeich = "T O T A L "
                    output_list.qty = qty
                    output_list.amount = to_string(sub_tot, "->,>>>,>>>,>>9.99")
                else:
                    output_list.bezeich = "T O T A L "
                    output_list.qty = qty
                    output_list.amount = to_string(sub_tot, " ->>>,>>>,>>>,>>9")
        curr_time = get_current_time_in_seconds()


        last_dept = - 1
        sub_tot =  to_decimal("0")
        it_exist = False
        qty = 0

        if sorttype == 0:

            h_journal_obj_list = {}
            for h_journal, h_artikel, h_bill, hoteldpt in db_session.query(H_journal, H_artikel, H_bill, Hoteldpt).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == H_journal.departement) & (H_artikel.artnr >= from_art) & (H_artikel.artnr <= to_art) & (H_artikel.departement >= from_dept) & (H_artikel.departement <= to_dept)).join(H_bill,(H_bill.rechnr == H_journal.rechnr) & (H_bill.tischnr == H_journal.tischnr) & (H_bill.departement == H_journal.departement)).join(Hoteldpt,(Hoteldpt.num == H_artikel.departement)).filter(
                     (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date) & (H_journal.artnr > 0) & (H_journal.anzahl != 0)).order_by(H_artikel.departement, H_artikel.artnr).all():
                if h_journal_obj_list.get(h_journal._recid):
                    continue
                else:
                    h_journal_obj_list[h_journal._recid] = True

                if curr_artikel != 0 and curr_artikel != h_artikel.artnr:

                    if it_exist:
                        tot_qty = qty + tot_qty
                        output_list = Output_list()
                        output_list_data.append(output_list)


                        if long_digit == False:
                            output_list.bezeich = "T O T A L "
                            output_list.qty = qty
                            output_list.amount = to_string(sub_tot, "->,>>>,>>>,>>9.99")
                        else:
                            output_list.bezeich = "T O T A L "
                            output_list.qty = qty
                            output_list.amount = to_string(sub_tot, "->>>,>>>,>>>,>>9")
                    sub_tot =  to_decimal("0")
                    it_exist = False
                    qty = 0


                last_dept = h_artikel.departement
                curr_artikel = h_artikel.artnr

                queasy = get_cache (Queasy, {"key": [(eq, 10)],"number1": [(eq, h_bill.betriebsnr)]})

                if queasy:
                    order_taker = queasy.char2

                if not queasy:
                    order_taker = ""
                curr_guest = ""

                if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                    if res_line:
                        curr_guest = res_line.name

                elif h_bill.resnr > 0:

                    guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                    if guest:
                        curr_guest = guest.name + "," + guest.vorname1

                elif h_bill.resnr == 0:
                    curr_guest = h_bill.bilname

                if takernum == 0:
                    do_it = True
                else:
                    do_it = None != h_bill and (h_bill.betriebsnr == takernum)

                if (h_journal.artnr == disc_art1 or h_journal.artnr == disc_art2 or h_journal.artnr == disc_art2) and h_journal.betrag == 0:
                    it_exist = True
                    do_it = False

                if do_it:
                    it_exist = True
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.guestname = curr_guest
                    output_list.h_recid = h_journal._recid

                    if long_digit == False:
                        output_list.date1 = h_journal.bill_datum
                        output_list.tableno = h_journal.tischnr
                        output_list.billno = h_journal.rechnr
                        output_list.artno = h_journal.artnr
                        output_list.bezeich = h_journal.bezeich
                        output_list.depart = hoteldpt.depart
                        output_list.qty = h_journal.anzahl
                        output_list.amount = to_string(h_journal.betrag, "->,>>>,>>>,>>9.99")
                        output_list.zeit = h_journal.zeit
                        output_list.id = to_string(h_journal.kellner_nr, "9999")
                        output_list.order_taker = order_taker
                    else:
                        output_list.date1 = h_journal.bill_datum
                        output_list.tableno = h_journal.tischnr
                        output_list.billno = h_journal.rechnr
                        output_list.artno = h_journal.artnr
                        output_list.bezeich = h_journal.bezeich
                        output_list.depart = hoteldpt.depart
                        output_list.qty = h_journal.anzahl
                        output_list.amount = to_string(h_journal.betrag, "->>>,>>>,>>>,>>9")
                        output_list.zeit = h_journal.zeit
                        output_list.id = to_string(h_journal.kellner_nr, "9999")
                        output_list.order_taker = order_taker
                    qty = qty + h_journal.anzahl
                    sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                    tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

        elif sorttype == 1:

            h_journal_obj_list = {}
            for h_journal, h_artikel, h_bill, hoteldpt in db_session.query(H_journal, H_artikel, H_bill, Hoteldpt).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == H_journal.departement) & (H_artikel.artnr >= from_art) & (H_artikel.artnr <= to_art) & (H_artikel.departement >= from_dept) & (H_artikel.departement <= to_dept)).join(H_bill,(H_bill.rechnr == H_journal.rechnr) & (H_bill.tischnr == H_journal.tischnr) & (H_bill.departement == H_journal.departement)).join(Hoteldpt,(Hoteldpt.num == H_artikel.departement)).filter(
                     (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date)).order_by(H_artikel.departement, H_artikel.artnr).all():
                if h_journal_obj_list.get(h_journal._recid):
                    continue
                else:
                    h_journal_obj_list[h_journal._recid] = True

                if curr_artikel != 0 and curr_artikel != h_artikel.artnr:

                    if it_exist:
                        tot_qty = qty + tot_qty
                        output_list = Output_list()
                        output_list_data.append(output_list)


                        if long_digit == False:
                            output_list.bezeich = "T O T A L "
                            output_list.qty = qty
                            output_list.amount = to_string(sub_tot, "->,>>>,>>>,>>9.99")
                        else:
                            output_list.bezeich = "T O T A L "
                            output_list.qty = qty
                            output_list.amount = to_string(sub_tot, "->>>,>>>,>>>,>>9")
                    sub_tot =  to_decimal("0")
                    it_exist = False
                    qty = 0


                last_dept = h_artikel.departement
                curr_artikel = h_artikel.artnr

                queasy = get_cache (Queasy, {"key": [(eq, 10)],"number1": [(eq, h_bill.betriebsnr)]})

                if queasy:
                    order_taker = queasy.char2

                if not queasy:
                    order_taker = ""
                curr_guest = ""

                if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                    if res_line:
                        curr_guest = res_line.name

                elif h_bill.resnr > 0:

                    guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                    if guest:
                        curr_guest = guest.name + "," + guest.vorname1

                elif h_bill.resnr == 0:
                    curr_guest = h_bill.bilname

                if takernum == 0:
                    do_it = True
                else:
                    do_it = None != h_bill and (h_bill.betriebsnr == takernum)

                if (h_journal.artnr == disc_art1 or h_journal.artnr == disc_art2 or h_journal.artnr == disc_art2) and h_journal.betrag == 0:
                    it_exist = True
                    do_it = False

                if do_it:
                    it_exist = True
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.guestname = curr_guest
                    output_list.h_recid = h_journal._recid

                    if long_digit == False:
                        output_list.date1 = h_journal.bill_datum
                        output_list.tableno = h_journal.tischnr
                        output_list.billno = h_journal.rechnr
                        output_list.artno = h_journal.artnr
                        output_list.bezeich = h_journal.bezeich
                        output_list.depart = hoteldpt.depart
                        output_list.qty = h_journal.anzahl
                        output_list.amount = to_string(h_journal.betrag, "->,>>>,>>>,>>9.99")
                        output_list.zeit = h_journal.zeit
                        output_list.id = to_string(h_journal.kellner_nr, "9999")
                        output_list.order_taker = order_taker
                    else:
                        output_list.date1 = h_journal.bill_datum
                        output_list.tableno = h_journal.tischnr
                        output_list.billno = h_journal.rechnr
                        output_list.artno = h_journal.artnr
                        output_list.bezeich = h_journal.bezeich
                        output_list.depart = hoteldpt.depart
                        output_list.qty = h_journal.anzahl
                        output_list.amount = to_string(h_journal.betrag, "->>>,>>>,>>>,>>9")
                        output_list.zeit = h_journal.zeit
                        output_list.id = to_string(h_journal.kellner_nr, "9999")
                        output_list.order_taker = order_taker
                    qty = qty + h_journal.anzahl
                    sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                    tot =  to_decimal(tot) + to_decimal(h_journal.betrag)
        else:

            h_journal_obj_list = {}
            for h_journal, h_artikel, h_bill, hoteldpt in db_session.query(H_journal, H_artikel, H_bill, Hoteldpt).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == H_journal.departement) & (H_artikel.artnr >= from_art) & (H_artikel.artnr <= to_art) & (H_artikel.departement >= from_dept) & (H_artikel.departement <= to_dept)).join(H_bill,(H_bill.rechnr == H_journal.rechnr) & (H_bill.tischnr == H_journal.tischnr) & (H_bill.departement == H_journal.departement)).join(Hoteldpt,(Hoteldpt.num == H_artikel.departement)).filter(
                     (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date) & (H_journal.artnr == 0)).order_by(H_artikel.departement, H_artikel.artnr).all():
                if h_journal_obj_list.get(h_journal._recid):
                    continue
                else:
                    h_journal_obj_list[h_journal._recid] = True

                if curr_artikel != 0 and curr_artikel != h_artikel.artnr:

                    if it_exist:
                        tot_qty = qty + tot_qty
                        output_list = Output_list()
                        output_list_data.append(output_list)


                        if long_digit == False:
                            output_list.bezeich = "T O T A L "
                            output_list.qty = qty
                            output_list.amount = to_string(sub_tot, "->,>>>,>>>,>>9.99")
                        else:
                            output_list.bezeich = "T O T A L "
                            output_list.qty = qty
                            output_list.amount = to_string(sub_tot, "->>>,>>>,>>>,>>9")
                    sub_tot =  to_decimal("0")
                    it_exist = False
                    qty = 0


                last_dept = h_artikel.departement
                curr_artikel = h_artikel.artnr

                queasy = get_cache (Queasy, {"key": [(eq, 10)],"number1": [(eq, h_bill.betriebsnr)]})

                if queasy:
                    order_taker = queasy.char2

                if not queasy:
                    order_taker = ""
                curr_guest = ""

                if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                    res_line = get_cache (Res_line, {"resnr": [(eq, h_bill.resnr)],"reslinnr": [(eq, h_bill.reslinnr)]})

                    if res_line:
                        curr_guest = res_line.name

                elif h_bill.resnr > 0:

                    guest = get_cache (Guest, {"gastnr": [(eq, h_bill.resnr)]})

                    if guest:
                        curr_guest = guest.name + "," + guest.vorname1

                elif h_bill.resnr == 0:
                    curr_guest = h_bill.bilname

                if takernum == 0:
                    do_it = True
                else:
                    do_it = None != h_bill and (h_bill.betriebsnr == takernum)

                if (h_journal.artnr == disc_art1 or h_journal.artnr == disc_art2 or h_journal.artnr == disc_art2) and h_journal.betrag == 0:
                    it_exist = True
                    do_it = False

                if do_it:
                    it_exist = True
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.guestname = curr_guest
                    output_list.h_recid = h_journal._recid

                    if long_digit == False:
                        output_list.date1 = h_journal.bill_datum
                        output_list.tableno = h_journal.tischnr
                        output_list.billno = h_journal.rechnr
                        output_list.artno = h_journal.artnr
                        output_list.bezeich = h_journal.bezeich
                        output_list.depart = hoteldpt.depart
                        output_list.qty = h_journal.anzahl
                        output_list.amount = to_string(h_journal.betrag, "->,>>>,>>>,>>9.99")
                        output_list.zeit = h_journal.zeit
                        output_list.id = to_string(h_journal.kellner_nr, "9999")
                        output_list.order_taker = order_taker
                    else:
                        output_list.date1 = h_journal.bill_datum
                        output_list.tableno = h_journal.tischnr
                        output_list.billno = h_journal.rechnr
                        output_list.artno = h_journal.artnr
                        output_list.bezeich = h_journal.bezeich
                        output_list.depart = hoteldpt.depart
                        output_list.qty = h_journal.anzahl
                        output_list.amount = to_string(h_journal.betrag, "->>>,>>>,>>>,>>9")
                        output_list.zeit = h_journal.zeit
                        output_list.id = to_string(h_journal.kellner_nr, "9999")
                        output_list.order_taker = order_taker
                    qty = qty + h_journal.anzahl
                    sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                    tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

        if it_exist:
            tot_qty = qty + tot_qty
            output_list = Output_list()
            output_list_data.append(output_list)


            if long_digit == False:
                output_list.bezeich = "T O T A L "
                output_list.qty = qty
                output_list.amount = to_string(sub_tot, "->,>>>,>>>,>>9.99")
            else:
                output_list.bezeich = "T O T A L "
                output_list.qty = qty
                output_list.amount = to_string(sub_tot, "->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)


        if not long_digit:
            output_list.bezeich = "GRAND TOTAL "
            output_list.qty = tot_qty
            output_list.amount = to_string(tot, "->,>>>,>>>,>>9.99")
        else:
            output_list.bezeich = "GRAND TOTAL"
            output_list.qty = tot_qty
            output_list.amount = to_string(tot, "->>>,>>>,>>>,>>9")


    def search_ot(r_nr:int, t_nr:int):

        nonlocal output_list_data, disc_art1, disc_art2, disc_art3, curr_time, counter, counter2, htparam, queasy, hoteldpt, h_journal, h_bill, res_line, guest, h_artikel
        nonlocal od_taker, from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, long_digit


        nonlocal output_list
        nonlocal output_list_data

        order_taker = ""

        def generate_inner_output():
            return (order_taker)


        h_bill = get_cache (H_bill, {"rechnr": [(eq, r_nr)],"tischnr": [(eq, t_nr)]})

        if h_bill:

            queasy = get_cache (Queasy, {"key": [(eq, 10)],"number1": [(eq, h_bill.betriebsnr)]})

        if queasy:
            order_taker = queasy.char2

        return generate_inner_output()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
    disc_art1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})
    disc_art2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})
    disc_art3 = htparam.finteger
    journal_list()

    return generate_output()