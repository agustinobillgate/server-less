from functions.additional_functions import *
import decimal
from datetime import date
from models import Res_line, Reservation, Bresline, Bill, Billhis, Bill_line, Artikel, Arrangement

def co_guest_1bl(case_type:int, pvilanguage:int, fr_date:date, to_date:date, price_decimal:int):
    cl_list_list = []
    tot_rm:int = 0
    tot_deposit:decimal = 0
    tot_cash:decimal = 0
    tot_cc:decimal = 0
    tot_cl:decimal = 0
    tot_amt:decimal = 0
    tot_bb:decimal = 0
    lvcarea:str = "co_guest"
    res_line = reservation = bresline = bill = billhis = bill_line = artikel = arrangement = None

    cl_list = bresline = None

    cl_list_list, Cl_list = create_model("Cl_list", {"flag":int, "reihe":int, "zinr":str, "name":str, "zipreis":decimal, "s_zipreis":str, "rechnr":int, "ankunft":date, "abreise":date, "cotime":str, "deposit":decimal, "s_deposit":str, "cash":decimal, "s_cash":str, "cc":decimal, "s_cc":str, "cl":decimal, "s_cl":str, "tot":decimal, "s_tot":str, "resnr":int, "company":str, "bill_balance":decimal}, {"ankunft": None, "abreise": None})

    Bresline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cl_list_list, tot_rm, tot_deposit, tot_cash, tot_cc, tot_cl, tot_amt, tot_bb, lvcarea, res_line, reservation, bresline, bill, billhis, bill_line, artikel, arrangement
        nonlocal bresline


        nonlocal cl_list, bresline
        nonlocal cl_list_list
        return {"cl-list": cl_list_list}

    def disp_billbalance():

        nonlocal cl_list_list, tot_rm, tot_deposit, tot_cash, tot_cc, tot_cl, tot_amt, tot_bb, lvcarea, res_line, reservation, bresline, bill, billhis, bill_line, artikel, arrangement
        nonlocal bresline


        nonlocal cl_list, bresline
        nonlocal cl_list_list

        gname:str = ""
        curr_zinr:str = ""
        curr_resnr:int = 0
        billno:int = 0
        b_bal:int = 0
        do_it:bool = True
        tot_rm = 0
        tot_deposit = 0
        tot_cash = 0
        tot_cc = 0
        tot_cl = 0
        tot_amt = 0
        cl_list_list.clear()

        res_line_obj_list = []
        for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                (Res_line.active_flag == 2) &  (Res_line.abreise >= fr_date) &  (Res_line.abreise <= to_date) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            do_it = True

            bresline = db_session.query(Bresline).filter(
                    (Bresline.resnr == res_line.resnr) &  (Bresline.reslinnr != res_line.resstatus) &  (Bresline.resstatus != 12)).first()

            if not bresline:
                do_it = False

            if do_it :
                billno = 0
                b_bal = 0

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr)).first()

                if bill:
                    billno = bill.rechnr
                    b_bal = bill.saldo


                else:

                    billhis = db_session.query(Billhis).filter(
                            (Billhis.resnr == res_line.resnr) &  (Billhis.reslinnr == res_line.reslinnr)).first()

                    if billhis:
                        billno = billhis.rechnr

                if curr_zinr != res_line.zinr:
                    curr_zinr = res_line.zinr
                    curr_resnr = res_line.resnr
                    tot_rm = tot_rm + 1

                elif curr_resnr != res_line.resnr:
                    curr_resnr = res_line.resnr
                    tot_rm = tot_rm + 1
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.resnr = reservation.resnr
                cl_list.company = reservation.name
                cl_list.zinr = res_line.zinr
                cl_list.zipreis = res_line.zipreis
                cl_list.ankunft = res_line.ankunft
                cl_list.abreise = res_line.abreise
                cl_list.rechnr = billno
                cl_list.cotime = to_string(res_line.abreisezeit, "HH:MM")
                cl_list.bill_balance = b_bal

                if res_line.resstatus == 12:
                    cl_list.name = translateExtended ("** Extra Bill", lvcarea, "")
                else:
                    cl_list.name = res_line.name

                for bill_line in db_session.query(Bill_line).filter(
                        (Bill_line.rechnr == billno)).all():

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == bill_line.departement)).first()

                    if artikel:

                        if artikel.artart == 2:
                            cl_list.cl = cl_list.cl - bill_line.betrag
                            cl_list.tot = cl_list.tot - bill_line.betrag
                            tot_cl = tot_cl - bill_line.betrag
                            tot_amt = tot_amt - bill_line.betrag

                        if artikel.artart == 5:
                            cl_list.deposit = cl_list.deposit - bill_line.betrag
                            cl_list.tot = cl_list.tot - bill_line.betrag
                            tot_deposit = tot_deposit - bill_line.betrag
                            tot_amt = tot_amt - bill_line.betrag

                        if artikel.artart == 6:
                            cl_list.cash = cl_list.cash - bill_line.betrag
                            cl_list.tot = cl_list.tot - bill_line.betrag
                            tot_cash = tot_cash - bill_line.betrag
                            tot_amt = tot_amt - bill_line.betrag

                        if artikel.artart == 7:
                            cl_list.cc = cl_list.cc - bill_line.betrag
                            cl_list.tot = cl_list.tot - bill_line.betrag
                            tot_cc = tot_cc - bill_line.betrag
                            tot_amt = tot_amt - bill_line.betrag

        for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.flag == 0)):

            if price_decimal == 0:

                if cl_list.zipreis <= 9999999:
                    cl_list.s_zipreis = to_string(cl_list.zipreis, ">,>>>,>>9.99")
                else:
                    cl_list.s_zipreis = to_string(cl_list.zipreis, " >>>,>>>,>>9")
            else:
                cl_list.s_zipreis = to_string(cl_list.zipreis, ">,>>>,>>9.99")
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.reihe = 1
        cl_list.name = translateExtended ("Total C/O Room(s)", lvcarea, "")
        cl_list.s_zipreis = to_string(tot_rm, ">>>>>>>>>>>9")
        cl_list.deposit = tot_deposit
        cl_list.cash = tot_cash
        cl_list.cc = tot_cc
        cl_list.cl = tot_cl
        cl_list.tot = tot_amt

    def disp_dubalance():

        nonlocal cl_list_list, tot_rm, tot_deposit, tot_cash, tot_cc, tot_cl, tot_amt, tot_bb, lvcarea, res_line, reservation, bresline, bill, billhis, bill_line, artikel, arrangement
        nonlocal bresline


        nonlocal cl_list, bresline
        nonlocal cl_list_list

        gname:str = ""
        curr_zinr:str = ""
        curr_resnr:int = 0
        billno:int = 0
        b_bal:int = 0
        do_it:bool = True
        tot_rm = 0
        tot_deposit = 0
        tot_cash = 0
        tot_cc = 0
        tot_cl = 0
        tot_amt = 0
        cl_list_list.clear()

        res_line_obj_list = []
        for res_line, reservation in db_session.query(Res_line, Reservation).join(Reservation,(Reservation.resnr == Res_line.resnr)).filter(
                (Res_line.active_flag == 2) &  (Res_line.ankunft >= fr_date) &  (Res_line.ankunft <= to_date) &  (Res_line.abreise == Res_line.ankunft) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10)).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)


            do_it = True

            bresline = db_session.query(Bresline).filter(
                    (Bresline.resnr == res_line.resnr) &  (Bresline.reslinnr != res_line.resstatus) &  (Bresline.resstatus != 12)).first()

            if not bresline:
                do_it = False

            if do_it :

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == res_line.arrangement)).first()
                billno = 0
                b_bal = 0

                bill = db_session.query(Bill).filter(
                        (Bill.resnr == res_line.resnr) &  (Bill.reslinnr == res_line.reslinnr)).first()

                if bill:
                    billno = bill.rechnr
                    b_bal = bill.saldo


                else:

                    billhis = db_session.query(Billhis).filter(
                            (Billhis.resnr == res_line.resnr) &  (Billhis.reslinnr == res_line.reslinnr)).first()

                    if billhis:
                        billno = billhis.rechnr

                if curr_zinr != res_line.zinr:
                    curr_zinr = res_line.zinr
                    curr_resnr = res_line.resnr
                    tot_rm = tot_rm + 1

                elif curr_resnr != res_line.resnr:
                    curr_resnr = res_line.resnr
                    tot_rm = tot_rm + 1
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.resnr = reservation.resnr
                cl_list.company = reservation.name
                cl_list.zinr = res_line.zinr
                cl_list.zipreis = res_line.zipreis
                cl_list.rechnr = billno
                cl_list.ankunft = res_line.ankunft
                cl_list.abreise = res_line.abreise
                cl_list.cotime = to_string(res_line.abreisezeit, "HH:MM")
                cl_list.bill_balance = b_bal

                bill_line = db_session.query(Bill_line).filter(
                        (Bill_line.departement == 0) &  (Bill_line.artnr == arrangement.argt_artikelnr) &  (Bill_line.bill_datum == res_line.ankunft) &  (Bill_line.massnr == res_line.resnr) &  (Bill_line.billin_nr == res_line.reslinnr)).first()

                if bill_line:
                    cl_list.flag = 1

                if res_line.resstatus == 12:
                    cl_list.name = translateExtended ("** Extra Bill", lvcarea, "")
                else:
                    cl_list.name = res_line.name

                for bill_line in db_session.query(Bill_line).filter(
                        (Bill_line.rechnr == billno)).all():

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == bill_line.departement)).first()

                    if artikel:

                        if artikel.artart == 2:
                            cl_list.cl = cl_list.cl - bill_line.betrag
                            cl_list.tot = cl_list.tot - bill_line.betrag
                            tot_cl = tot_cl - bill_line.betrag
                            tot_amt = tot_amt - bill_line.betrag

                        if artikel.artart == 5:
                            cl_list.deposit = cl_list.deposit - bill_line.betrag
                            cl_list.tot = cl_list.tot - bill_line.betrag
                            tot_deposit = tot_deposit - bill_line.betrag
                            tot_amt = tot_amt - bill_line.betrag

                        if artikel.artart == 6:
                            cl_list.cash = cl_list.cash - bill_line.betrag
                            cl_list.tot = cl_list.tot - bill_line.betrag
                            tot_cash = tot_cash - bill_line.betrag
                            tot_amt = tot_amt - bill_line.betrag

                        if artikel.artart == 7:
                            cl_list.cc = cl_list.cc - bill_line.betrag
                            cl_list.tot = cl_list.tot - bill_line.betrag
                            tot_cc = tot_cc - bill_line.betrag
                            tot_amt = tot_amt - bill_line.betrag

        for cl_list in query(cl_list_list):

            if price_decimal == 0:

                if cl_list.zipreis <= 9999999:
                    cl_list.s_zipreis = to_string(cl_list.zipreis, ">,>>>,>>9.99")
                else:
                    cl_list.s_zipreis = to_string(cl_list.zipreis, " >>>,>>>,>>9")
            else:
                cl_list.s_zipreis = to_string(cl_list.zipreis, ">,>>>,>>9.99")
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = 2
        cl_list.reihe = 1
        cl_list.name = translateExtended ("Total C/O Room(s)", lvcarea, "")
        cl_list.s_zipreis = to_string(tot_rm, ">>>>>>>>>>>9")
        cl_list.deposit = tot_deposit
        cl_list.cash = tot_cash
        cl_list.cc = tot_cc
        cl_list.cl = tot_cl
        cl_list.tot = tot_amt

    if case_type == 1:
        disp_billbalance()
    else:
        disp_dubalance()

    for cl_list in query(cl_list_list):
        cl_list.s_deposit = to_string(cl_list.deposit, "->,>>>,>>>,>>9.99")
        cl_list.s_cc = to_string(cl_list.cc, "->,>>>,>>>,>>9.99")
        cl_list.s_cl = to_string(cl_list.cl, "->,>>>,>>>,>>9.99")
        cl_list.s_cash = to_string(cl_list.cash, "->,>>>,>>>,>>9.99")
        cl_list.s_tot = to_string(cl_list.tot, "->,>>>,>>>,>>9.99")

    return generate_output()