from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Hoteldpt, H_journal, H_bill, Res_line, H_artikel, Artikel, Guest

def rest_journal_btn_go_3bl(od_taker:str, from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, sorttype:int, long_digit:bool, mc_sort:str):
    output_list_list = []
    queasy = hoteldpt = h_journal = h_bill = res_line = h_artikel = artikel = guest = None

    output_list = toutput_list = out_list = None

    output_list_list, Output_list = create_model("Output_list", {"h_recid":int, "str":str, "gname":str, "fart_bez":str, "bill_datum":date, "tischnr":int, "rechnr":int, "artnr":int, "bezeich":str, "dept_bez":str, "anzahl":int, "betrag":decimal, "zeit":int, "kellner_nr":int, "order_taker":str, "zinr":str, "counter":int})
    toutput_list_list, Toutput_list = create_model_like(Output_list)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, queasy, hoteldpt, h_journal, h_bill, res_line, h_artikel, artikel, guest
        nonlocal od_taker, from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, long_digit, mc_sort


        nonlocal output_list, toutput_list, out_list
        nonlocal output_list_list, toutput_list_list
        return {"output-list": output_list_list}

    def journal_list():

        nonlocal output_list_list, queasy, hoteldpt, h_journal, h_bill, res_line, h_artikel, artikel, guest
        nonlocal od_taker, from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, long_digit, mc_sort


        nonlocal output_list, toutput_list, out_list
        nonlocal output_list_list, toutput_list_list

        last_dept:int = -1
        qty:int = 0
        takernum:int = 0
        sub_tot:decimal = to_decimal("0.0")
        tot:decimal = to_decimal("0.0")
        curr_date:date = None
        it_exist:bool = False
        do_it:bool = False
        curr_guest:str = ""
        curr_room:str = ""
        tot_qty:int = 0
        order_taker:str = ""
        dept:int = 0
        curr_artnr:int = 0
        temp_dept:int = 0
        output_list_list.clear()

        if od_taker != "":

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 10) & (func.lower(Queasy.char2) == (od_taker).lower())).first()

            if queasy:
                takernum = queasy.number1

        if sorttype == 0:

            h_journal_obj_list = []
            for h_journal, hoteldpt in db_session.query(H_journal, Hoteldpt).join(Hoteldpt,(Hoteldpt.num == H_journal.departement)).filter(
                     (H_journal.artnr >= from_art) & (H_journal.artnr <= to_art) & (H_journal.departement >= from_dept) & (H_journal.departement <= to_dept) & (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date) & (H_journal.artnr > 0) & (H_journal.anzahl != 0)).order_by(H_journal._recid).all():
                if h_journal._recid in h_journal_obj_list:
                    continue
                else:
                    h_journal_obj_list.append(h_journal._recid)


                order_taker = search_ot(h_journal.rechnr, h_journal.tischnr)
                curr_guest = ""
                curr_room = ""

                h_bill = db_session.query(H_bill).filter(
                         (H_bill.rechnr == h_journal.rechnr) & (H_bill.departement == h_journal.departement)).first()

                if h_bill:

                    if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == h_bill.resnr) & (Res_line.reslinnr == h_bill.reslinnr)).first()

                        if res_line:
                            curr_guest = res_line.name
                            curr_room = res_line.zinr


                    else:
                        curr_guest = h_bill.bilname

                if takernum == 0:
                    do_it = True
                else:
                    do_it = None != h_bill and (h_bill.betriebsnr == takernum)

                if do_it:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.gname = curr_guest
                    output_list.h_recid = h_journal._recid
                    output_list.bill_datum = h_journal.bill_datum
                    output_list.tischnr = h_journal.tischnr
                    output_list.rechnr = h_journal.rechnr
                    output_list.artnr = h_journal.artnr
                    output_list.bezeich = h_journal.bezeich
                    output_list.dept_bez = hoteldpt.depart
                    output_list.anzahl = h_journal.anzahl
                    output_list.betrag =  to_decimal(h_journal.betrag)
                    output_list.zeit = h_journal.zeit
                    output_list.kellner_nr = h_journal.kellner_nr
                    output_list.order_taker = order_taker
                    output_list.zinr = curr_room

                    h_artikel = db_session.query(H_artikel).filter(
                             (H_artikel.artnr == h_journal.artnr) & (H_artikel.departement == h_journal.departement)).first()

                    if h_artikel:

                        if h_artikel.artart <= 1:
                            temp_dept = h_artikel.departement
                        else:
                            temp_dept = 0

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == temp_dept)).first()

                        if artikel:
                            output_list.fart_bez = artikel.bezeich

                    if not long_digit:
                        str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>>>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, "->>>,>>>,>>>,>>9.99") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
                    else:
                        str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>>>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, "->>,>>>,>>>,>>>,>>9") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room

        elif sorttype == 1:

            h_journal_obj_list = []
            for h_journal, hoteldpt in db_session.query(H_journal, Hoteldpt).join(Hoteldpt,(Hoteldpt.num == H_journal.departement)).filter(
                     (((H_journal.artnr >= from_art) & (H_journal.artnr <= to_art)) | (H_journal.artnr == 0)) & (H_journal.departement >= from_dept) & (H_journal.departement <= to_dept) & (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date)).order_by(H_journal._recid).all():
                if h_journal._recid in h_journal_obj_list:
                    continue
                else:
                    h_journal_obj_list.append(h_journal._recid)


                order_taker = search_ot(h_journal.rechnr, h_journal.tischnr)
                curr_guest = ""
                curr_room = ""

                h_bill = db_session.query(H_bill).filter(
                         (H_bill.rechnr == h_journal.rechnr) & (H_bill.departement == h_journal.departement)).first()

                if h_bill:

                    if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == h_bill.resnr) & (Res_line.reslinnr == h_bill.reslinnr)).first()

                        if res_line:
                            curr_guest = res_line.name
                            curr_room = res_line.zinr

                    elif h_bill.resnr > 0:

                        guest = db_session.query(Guest).filter(
                                 (Guest.resnr == Guest.gastnr)).first()

                        if guest:
                            curr_guest = guest.name + "," + guest.vorname1

                    elif h_bill.resnr == 0:
                        curr_guest = h_bill.bilname

                if takernum == 0:
                    do_it = True
                else:
                    do_it = None != h_bill and (h_bill.betriebsnr == takernum)

                if do_it:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.gname = curr_guest
                    output_list.h_recid = h_journal._recid
                    output_list.bill_datum = h_journal.bill_datum
                    output_list.tischnr = h_journal.tischnr
                    output_list.rechnr = h_journal.rechnr
                    output_list.artnr = h_journal.artnr
                    output_list.bezeich = h_journal.bezeich
                    output_list.dept_bez = hoteldpt.depart
                    output_list.anzahl = h_journal.anzahl
                    output_list.betrag =  to_decimal(h_journal.betrag)
                    output_list.zeit = h_journal.zeit
                    output_list.kellner_nr = h_journal.kellner_nr
                    output_list.order_taker = order_taker
                    output_list.zinr = curr_room

                    h_artikel = db_session.query(H_artikel).filter(
                             (H_artikel.artnr == h_journal.artnr) & (H_artikel.departement == h_journal.departement)).first()

                    if h_artikel:

                        if h_artikel.artart <= 1:
                            temp_dept = h_artikel.departement
                        else:
                            temp_dept = 0

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == temp_dept)).first()

                        if artikel:
                            output_list.fart_bez = artikel.bezeich

                    if not long_digit:
                        str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>>>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, "->>>,>>>,>>>,>>9.99") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
                    else:
                        str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>>>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, "->>,>>>,>>>,>>>,>>9") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
        else:

            h_journal_obj_list = []
            for h_journal, hoteldpt in db_session.query(H_journal, Hoteldpt).join(Hoteldpt,(Hoteldpt.num == H_journal.departement)).filter(
                     (H_journal.artnr == 0) & (H_journal.departement >= from_dept) & (H_journal.departement <= to_dept) & (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date) & (H_journal.anzahl == 0)).order_by(H_journal._recid).all():
                if h_journal._recid in h_journal_obj_list:
                    continue
                else:
                    h_journal_obj_list.append(h_journal._recid)


                order_taker = search_ot(h_journal.rechnr, h_journal.tischnr)
                curr_guest = ""
                curr_room = ""

                h_bill = db_session.query(H_bill).filter(
                         (H_bill.rechnr == h_journal.rechnr) & (H_bill.departement == h_journal.departement)).first()

                if h_bill:

                    if h_bill.resnr > 0 and h_bill.reslinnr > 0:

                        res_line = db_session.query(Res_line).filter(
                                 (Res_line.resnr == h_bill.resnr) & (Res_line.reslinnr == h_bill.reslinnr)).first()

                        if res_line:
                            curr_guest = res_line.name
                            curr_room = res_line.zinr

                    elif h_bill.resnr > 0:

                        guest = db_session.query(Guest).filter(
                                 (Guest.resnr == Guest.gastnr)).first()

                        if guest:
                            curr_guest = guest.name + "," + guest.vorname1

                    elif h_bill.resnr == 0:
                        curr_guest = h_bill.bilname

                if takernum == 0:
                    do_it = True
                else:
                    do_it = None != h_bill and (h_bill.betriebsnr == takernum)

                if do_it:
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.gname = curr_guest
                    output_list.h_recid = h_journal._recid
                    output_list.bill_datum = h_journal.bill_datum
                    output_list.tischnr = h_journal.tischnr
                    output_list.rechnr = h_journal.rechnr
                    output_list.artnr = h_journal.artnr
                    output_list.bezeich = h_journal.bezeich
                    output_list.dept_bez = hoteldpt.depart
                    output_list.anzahl = h_journal.anzahl
                    output_list.betrag =  to_decimal(h_journal.betrag)
                    output_list.zeit = h_journal.zeit
                    output_list.kellner_nr = h_journal.kellner_nr
                    output_list.order_taker = order_taker
                    output_list.zinr = curr_room

                    h_artikel = db_session.query(H_artikel).filter(
                             (H_artikel.artnr == h_journal.artnr) & (H_artikel.departement == h_journal.departement)).first()

                    if h_artikel:

                        if h_artikel.artart <= 1:
                            temp_dept = h_artikel.departement
                        else:
                            temp_dept = 0

                        artikel = db_session.query(Artikel).filter(
                                 (Artikel.artnr == h_artikel.artnrfront) & (Artikel.departement == temp_dept)).first()

                        if artikel:
                            output_list.fart_bez = artikel.bezeich

                    if not long_digit:
                        str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>>>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, "->>>,>>>,>>>,>>9.99") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room
                    else:
                        str = to_string(h_journal.bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>>>>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(h_journal.betrag, "->>,>>>,>>>,>>>,>>9") + to_string(h_journal.zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999") + to_string(order_taker, "x(8)") + "|" + curr_room


    def create_total():

        nonlocal output_list_list, queasy, hoteldpt, h_journal, h_bill, res_line, h_artikel, artikel, guest
        nonlocal od_taker, from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, long_digit, mc_sort


        nonlocal output_list, toutput_list, out_list
        nonlocal output_list_list, toutput_list_list

        curr_artnr:int = 0
        curr_deptbez:str = ""
        qty:int = 0
        tot_qty:int = 0
        sub_tot:decimal = to_decimal("0.0")
        tot:decimal = to_decimal("0.0")
        counter:int = 0
        Out_list = Output_list
        out_list_list = output_list_list

        if mc_sort == 'sart':

            for output_list in query(output_list_list, sort_by=[("fart_bez",False),("artnr",False),("bill_datum",False),("zeit",False),("dept_bez",False)]):

                if output_list.artnr != 0:

                    if curr_artnr != 0 and curr_artnr != output_list.artnr:
                        out_list = Out_list()
                        out_list_list.append(out_list)


                        if not long_digit:
                            out_list.str = to_string("", "x(61)") + to_string("T O T A L ", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, "->>>,>>>,>>>,>>9.99")
                        else:
                            out_list.str = to_string("", "x(56)") + to_string("T O T A L ", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, "->>,>>>,>>>,>>>,>>9")
                        sub_tot =  to_decimal("0")
                        qty = 0
                        curr_artnr = 0
                        curr_deptbez = ""
                        counter = counter + 1
                        out_list.counter = counter
                    counter = counter + 1
                    output_list.counter = counter
                    qty = qty + output_list.anzahl
                    tot_qty = tot_qty + output_list.anzahl
                    sub_tot =  to_decimal(sub_tot) + to_decimal(output_list.betrag)
                    tot =  to_decimal(tot) + to_decimal(output_list.betrag)
                    curr_artnr = output_list.artnr
                    curr_deptbez = output_list.dept_bez
                else:

                    if curr_deptbez != "" and curr_deptbez != output_list.dept_bez:
                        out_list = Out_list()
                        out_list_list.append(out_list)


                        if not long_digit:
                            out_list.str = to_string("", "x(61)") + to_string("T O T A L ", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, "->>>,>>>,>>>,>>9.99")
                        else:
                            out_list.str = to_string("", "x(56)") + to_string("T O T A L ", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, "->>,>>>,>>>,>>>,>>9")
                        sub_tot =  to_decimal("0")
                        qty = 0
                        curr_deptbez = ""
                        counter = counter + 1
                        out_list.counter = counter
                    counter = counter + 1
                    output_list.counter = counter
                    qty = qty + output_list.anzahl
                    tot_qty = tot_qty + output_list.anzahl
                    sub_tot =  to_decimal(sub_tot) + to_decimal(output_list.betrag)
                    tot =  to_decimal(tot) + to_decimal(output_list.betrag)
                    curr_deptbez = output_list.dept_bez
        else:

            for output_list in query(output_list_list, sort_by=[("dept_bez",False),("artnr",False),("bill_datum",False),("zeit",False)]):

                if output_list.artnr != 0:

                    if curr_deptbez != "" and curr_deptbez != output_list.dept_bez:
                        out_list = Out_list()
                        out_list_list.append(out_list)


                        if not long_digit:
                            out_list.str = to_string("", "x(61)") + to_string("T O T A L ", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, "->>>,>>>,>>>,>>9.99")
                        else:
                            out_list.str = to_string("", "x(56)") + to_string("T O T A L ", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, "->>,>>>,>>>,>>>,>>9")
                        sub_tot =  to_decimal("0")
                        qty = 0
                        curr_artnr = 0
                        curr_deptbez = ""
                        counter = counter + 1
                        out_list.counter = counter
                    counter = counter + 1
                    output_list.counter = counter
                    qty = qty + output_list.anzahl
                    tot_qty = tot_qty + output_list.anzahl
                    sub_tot =  to_decimal(sub_tot) + to_decimal(output_list.betrag)
                    tot =  to_decimal(tot) + to_decimal(output_list.betrag)
                    curr_artnr = output_list.artnr
                    curr_deptbez = output_list.dept_bez
                else:

                    if curr_deptbez != "" and curr_deptbez != output_list.dept_bez:
                        out_list = Out_list()
                        out_list_list.append(out_list)


                        if not long_digit:
                            out_list.str = to_string("", "x(61)") + to_string("T O T A L ", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, "->>>,>>>,>>>,>>9.99")
                        else:
                            out_list.str = to_string("", "x(56)") + to_string("T O T A L ", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, "->>,>>>,>>>,>>>,>>9")
                        sub_tot =  to_decimal("0")
                        qty = 0
                        curr_artnr = 0
                        curr_deptbez = ""
                        counter = counter + 1
                        out_list.counter = counter
                    counter = counter + 1
                    output_list.counter = counter
                    qty = qty + output_list.anzahl
                    tot_qty = tot_qty + output_list.anzahl
                    sub_tot =  to_decimal(sub_tot) + to_decimal(output_list.betrag)
                    tot =  to_decimal(tot) + to_decimal(output_list.betrag)
                    curr_artnr = output_list.artnr
                    curr_deptbez = output_list.dept_bez
        out_list = Out_list()
        out_list_list.append(out_list)


        if not long_digit:
            out_list.str = to_string("", "x(61)") + to_string("T O T A L ", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, "->,>>>,>>>,>>9.99")
        else:
            out_list.str = to_string("", "x(56)") + to_string("T O T A L ", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, "->>,>>>,>>>,>>>,>>9")
        counter = counter + 1
        out_list.counter = counter
        out_list = Out_list()
        out_list_list.append(out_list)


        if not long_digit:
            out_list.str = to_string("", "x(61)") + to_string("Grand TOTAL ", "x(20)") + to_string(tot_qty, "->>>9") + to_string(tot, "->>>,>>>,>>>,>>9.99")
        else:
            out_list.str = to_string("", "x(61)") + to_string("Grand TOTAL ", "x(20)") + to_string(tot_qty, "->>>9") + to_string(tot, " ->>>,>>>,>>>,>>9")
        counter = counter + 1
        out_list.counter = counter


    def search_ot(r_nr:int, t_nr:int):

        nonlocal output_list_list, queasy, hoteldpt, h_journal, h_bill, res_line, h_artikel, artikel, guest
        nonlocal od_taker, from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, long_digit, mc_sort


        nonlocal output_list, toutput_list, out_list
        nonlocal output_list_list, toutput_list_list

        order_taker = ""

        def generate_inner_output():
            return (order_taker)


        h_bill = db_session.query(H_bill).filter(
                 (H_bill.rechnr == r_nr) & (H_bill.tischnr == t_nr)).first()

        if h_bill:

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 10) & (Queasy.number1 == h_bill.betriebsnr)).first()

        if queasy:
            order_taker = queasy.char2

        return generate_inner_output()


    journal_list()
    create_total()

    return generate_output()