from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Bill_line, Artikel, Bill, Zwkum, Billjournal, Waehrung, Exrate, Hoteldpt, H_journal, H_bill_line, H_artikel

def sum_cashier_listbl(pvilanguage:int, to_date:date, short_flag:bool, foreign_flag:bool):
    msg_str = ""
    sumcsr_list_list = []
    long_digit:bool = False
    curr_dept:int = 0
    price_decimal:int = 0
    curr_bez:str = ""
    foreign_curr:str = ""
    from_date:date = None
    fact1:decimal = 1
    curr_tot_cash:decimal = 0
    lvcarea:str = "sum_cashier"
    htparam = bill_line = artikel = bill = zwkum = billjournal = waehrung = exrate = hoteldpt = h_journal = h_bill_line = h_artikel = None

    sumcsr_list = output_list = cash_list = rechnr_list = art_list = cl_list = bline = h_bline = depobuff = None

    sumcsr_list_list, Sumcsr_list = create_model("Sumcsr_list", {"reihe":int, "flag":int, "artart":int, "dept":str, "cash":str, "rmfobill":str, "card":str, "cl":str, "revenue":str, "compli":str, "mealcou":str, "outstand":str})
    output_list_list, Output_list = create_model("Output_list", {"reihe":int, "flag":int, "artart":int, "str":str})
    cash_list_list, Cash_list = create_model("Cash_list", {"artnr":int, "bezeich":str, "betrag":decimal})
    rechnr_list_list, Rechnr_list = create_model("Rechnr_list", {"rechnr":int})
    art_list_list, Art_list = create_model("Art_list", {"artnr":int, "artart":int, "dept":int, "bezeich":str, "revenue":decimal})
    cl_list_list, Cl_list = create_model("Cl_list", {"begin":bool, "flag":int, "artnr":int, "artart":int, "dept":int, "bezeich":str, "cash":decimal, "room":decimal, "card":decimal, "cl":decimal, "gl":decimal, "revenue":decimal, "compli":decimal, "mcoupon":decimal})

    Bline = Bill_line
    H_bline = Bill_line
    Depobuff = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, sumcsr_list_list, long_digit, curr_dept, price_decimal, curr_bez, foreign_curr, from_date, fact1, curr_tot_cash, lvcarea, htparam, bill_line, artikel, bill, zwkum, billjournal, waehrung, exrate, hoteldpt, h_journal, h_bill_line, h_artikel
        nonlocal bline, h_bline, depobuff


        nonlocal sumcsr_list, output_list, cash_list, rechnr_list, art_list, cl_list, bline, h_bline, depobuff
        nonlocal sumcsr_list_list, output_list_list, cash_list_list, rechnr_list_list, art_list_list, cl_list_list
        return {"msg_str": msg_str, "sumcsr-list": sumcsr_list_list}

    def create_umsatz():

        nonlocal msg_str, sumcsr_list_list, long_digit, curr_dept, price_decimal, curr_bez, foreign_curr, from_date, fact1, curr_tot_cash, lvcarea, htparam, bill_line, artikel, bill, zwkum, billjournal, waehrung, exrate, hoteldpt, h_journal, h_bill_line, h_artikel
        nonlocal bline, h_bline, depobuff


        nonlocal sumcsr_list, output_list, cash_list, rechnr_list, art_list, cl_list, bline, h_bline, depobuff
        nonlocal sumcsr_list_list, output_list_list, cash_list_list, rechnr_list_list, art_list_list, cl_list_list

        cash:decimal = 0
        cc:decimal = 0
        cl:decimal = 0
        compli:decimal = 0
        mcoup:decimal = 0
        rest:decimal = 0
        room:decimal = 0
        i:int = 0
        curr_flag:int = 0
        t1_cash:decimal = 0
        t1_cc:decimal = 0
        t1_cl:decimal = 0
        t1_compli:decimal = 0
        t1_mcoup:decimal = 0
        t1_room:decimal = 0
        t1_revenue:decimal = 0
        t1_gl:decimal = 0
        t2_cash:decimal = 0
        t2_cc:decimal = 0
        t2_cl:decimal = 0
        t2_compli:decimal = 0
        t2_mcoup:decimal = 0
        t2_room:decimal = 0
        t2_revenue:decimal = 0
        t2_gl:decimal = 0
        t_cash:decimal = 0
        t_cc:decimal = 0
        t_cl:decimal = 0
        t_compli:decimal = 0
        t_mcoup:decimal = 0
        t_room:decimal = 0
        t_revenue:decimal = 0
        t_gl:decimal = 0
        do_it:bool = False
        exchg_rate:decimal = 0
        amount:decimal = 0
        deposit_artnr:int = 0
        deposit_baartnr:int = 0
        deposit_bez:str = "Deposit (Rsv)"
        depo_foreign:bool = False
        banquet_dept:int = -1
        deposit_babez:str = "Deposit (Bqt)"
        Bline = Bill_line
        H_bline = Bill_line
        Depobuff = Artikel
        t_cash = 0
        t_cc = 0
        t_cl = 0
        t_compli = 0
        t_mcoup = 0
        t_revenue = 0
        t_room = 0
        t_gl = 0
        t1_cash = 0
        t1_cc = 0
        t1_cl = 0
        t1_compli = 0
        t1_mcoup = 0
        t1_revenue = 0
        t1_room = 0
        t1_gl = 0
        t2_cash = 0
        t2_cc = 0
        t2_cl = 0
        t2_compli = 0
        t2_mcoup = 0
        t2_revenue = 0
        t2_room = 0
        t2_gl = 0


        output_list_list.clear()
        cl_list_list.clear()
        cash_list_list.clear()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 120)).first()
        deposit_artnr = finteger

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == deposit_artnr) &  (Artikel.departement == 0)).first()

        if artikel:
            deposit_bez = artikel.bezeich
            depo_foreign = artikel.pricetab

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 900)).first()

        if htparam.finteger != 0:
            banquet_dept = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 117)).first()
        deposit_baartnr = finteger

        depobuff = db_session.query(Depobuff).filter(
                (Depobuff.artnr == deposit_baartnr) &  (Depobuff.departement == banquet_dept) &  (Depobuff.artart == 5)).first()

        if not depobuff:

            depobuff = db_session.query(Depobuff).filter(
                    (Depobuff.artnr == deposit_baartnr) &  (Depobuff.departement == 0) &  (Depobuff.artart == 5)).first()

        if depobuff:
            deposit_babez = depobuff.bezeich

        bill_obj_list = []
        for bill, bline in db_session.query(Bill, Bline).join(Bline,(Bline.rechnr == Bill.rechnr) &  (Bline.bill_datum == to_date)).filter(
                (((Bill.flag == 0) &  (Bill.datum >= to_date)) |  ((Bill.flag == 1) &  (Bill.datum >= to_date))) &  (Bill.resnr > 0)).all():
            if bill._recid in bill_obj_list:
                continue
            else:
                bill_obj_list.append(bill._recid)


            curr_dept = bill.rechnr

            for bill_line in db_session.query(Bill_line).filter(
                    (Bill_line.rechnr == bill.rechnr) &  (Bill_line.bill_datum == to_date)).all():

                if foreign_flag:
                    amount = bill_line.fremdwbetrag
                else:
                    amount = bill_line.betrag

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == bill_line.departement)).first()

                if not artikel and num_entries(bill_line.bezeich, "*") > 1:

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == 0)).first()

                if not artikel:
                    msg_str = msg_str + "&W" + translateExtended ("Artikel not found:", lvcarea, "") + " " + translateExtended ("Bill No:", lvcarea, "") + " " + to_string(bill.rechnr) + "; " + translateExtended ("Article No:", lvcarea, "") + " " + to_string(bill_line.artnr) + " - " + bill_line.bezeich + " " + trim(to_string(bill_line.betrag, "->>>,>>>,>>9.99"))

                if artikel:

                    if artikel.artart == 0 or artikel.artart == 8 or artikel.artart == 9 or artikel.artart == 5:
                        do_it = True

                        if artikel.artart == 5 and artikel.departement == 0 and bill_line.userinit.lower()  == "$$":
                            do_it = False

                        if do_it:
                            curr_bez = artikel.bezeich

                            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.artnr == artikel.artnr and cl_list.dept == artikel.departement), first=True)

                            if not cl_list:
                                cl_list = Cl_list()
                                cl_list_list.append(cl_list)

                                cl_list.flag = -1
                                cl_list.artart = artikel.umsatzart
                                cl_list.artnr = artikel.artnr
                                cl_list.dept = artikel.departement
                                cl_list.bezeich = to_string(artikel.departement, "99 ") +\
                                        to_string(artikel.bezeich, "x(21)")


                            cl_list.room = cl_list.room + amount / fact1
                            cl_list.revenue = cl_list.revenue + amount / fact1
                            t1_revenue = t1_revenue + amount / fact1
                            t1_room = t1_room + amount / fact1
                            t_room = t_room + amount / fact1

                    elif artikel.artart == 2 or artikel.artart == 6 or artikel.artart == 7 or artikel.artart == 11 or artikel.artart == 12:

                        if artikel.artart == 6:

                            cash_list = query(cash_list_list, filters=(lambda cash_list :cash_list.artnr == artikel.artnr), first=True)

                            if not cash_list:
                                cash_list = Cash_list()
                                cash_list_list.append(cash_list)

                                cash_list.artnr = artikel.artnr
                                cash_list.bezeich = artikel.bezeich


                            cash_list.betrag = cash_list.betrag - amount / fact1

                        cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.artnr == artikel.artnr and cl_list.dept == artikel.departement), first=True)

                        if not cl_list:
                            cl_list = Cl_list()
                            cl_list_list.append(cl_list)

                            cl_list.flag = 200
                            cl_list.artnr = artikel.artnr
                            cl_list.dept = artikel.departement
                            cl_list.bezeich = to_string(artikel.bezeich, "x(19)")
                        cl_list.revenue = cl_list.revenue - amount / fact1
                        t2_revenue = t2_revenue - amount / fact1

                        if artikel.artart == 2:
                            cl_list.cl = cl_list.cl - amount / fact1
                            t2_cl = t2_cl - amount / fact1
                            t_cl = t_cl - amount / fact1

                        elif artikel.artart == 6:
                            cl_list.cash = cl_list.cash - amount / fact1
                            t2_cash = t2_cash - amount / fact1
                            t_cash = t_cash - amount / fact1

                        elif artikel.artart == 7:
                            cl_list.card = cl_list.card - amount / fact1
                            t2_cc = t2_cc - amount / fact1
                            t_cc = t_cc - amount / fact1

                        elif artikel.artart == 11:
                            cl_list.compli = cl_list.compli - amount / fact1
                            t2_compli = t2_compli - amount / fact1
                            t_compli = t_compli - amount / fact1

                        elif artikel.artart == 12:
                            cl_list.mcoup = cl_list.mcoup - amount / fact1
                            t2_mcoup = t2_mcoup - amount / fact1
                            t_mcoup = t_mcoup - amount / fact1

        bill_obj_list = []
        for bill, bline in db_session.query(Bill, Bline).join(Bline,(Bline.rechnr == Bill.rechnr) &  (Bline.bill_datum == to_date)).filter(
                (((Bill.flag == 0) &  (Bill.datum >= to_date)) |  ((Bill.flag == 1) &  (Bill.datum >= to_date))) &  (Bill.resnr == 0)).all():
            if bill._recid in bill_obj_list:
                continue
            else:
                bill_obj_list.append(bill._recid)


            curr_dept = bill.rechnr
            cash = 0
            cc = 0
            cl = 0
            compli = 0
            mcoup = 0
            room = 0
            i = 1

            for bill_line in db_session.query(Bill_line).filter(
                    (Bill_line.rechnr == bill.rechnr) &  (Bill_line.bill_datum == to_date)).all():

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == bill_line.departement)).first()

                if not artikel and num_entries(bill_line.bezeich, "*") > 1:

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == bill_line.departement)).first()

                if not artikel:
                    msg_str = msg_str + "&W" + translateExtended ("Artikel not found:", lvcarea, "") + " " + translateExtended ("Bill No:", lvcarea, "") + " " + to_string(bill.rechnr) + "; " + translateExtended ("Article No:", lvcarea, "") + " " + to_string(bill_line.artnr) + " - " + bill_line.bezeich + " " + trim(to_string(bill_line.betrag, "->>>,>>>,>>9.99"))
                else:

                    zwkum = db_session.query(Zwkum).filter(
                            (Zwkum.zknr == artikel.zwkum) &  (Zwkum.departement == artikel.departement)).first()
                    i = i + 1
                    curr_bez = artikel.bezeich

                    if foreign_flag:
                        amount = bill_line.fremdwbetrag
                    else:
                        amount = bill_line.betrag

                    if artikel.artart == 0 or artikel.artart == 9 or artikel.artart == 8 or artikel.artart == 5:

                        if artikel.departement == 0:
                            do_it = True

                            if artikel.artart == 5 and bill_line.userinit.lower()  == "$$":
                                do_it = False

                            if do_it:

                                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.artnr == artikel.artnr and cl_list.dept == artikel.departement), first=True)

                                if not cl_list:
                                    cl_list = Cl_list()
                                    cl_list_list.append(cl_list)

                                    cl_list.flag = 0
                                    cl_list.artart = artikel.umsatzart
                                    cl_list.artnr = artikel.artnr
                                    cl_list.dept = artikel.departement
                                    cl_list.bezeich = to_string(artikel.departement, "99 ") +\
                                            to_string(artikel.bezeich, "x(21)")


                                cl_list.gl = cl_list.gl + amount / fact1
                                cl_list.revenue = cl_list.revenue + amount / fact1
                                t1_revenue = t1_revenue + amount / fact1

                        elif artikel.departement > 0:

                            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.artnr == zwkum.zknr and cl_list.dept == zwkum.departement), first=True)

                            if not cl_list:
                                cl_list = Cl_list()
                                cl_list_list.append(cl_list)

                                cl_list.flag = 0
                                cl_list.artart = artikel.umsatzart
                                cl_list.artnr = zwkum.zknr
                                cl_list.dept = zwkum.departement
                                cl_list.bezeich = to_string(zwkum.departement, "99 ") +\
                                        to_string(zwkum.bezeich, "x(21)")


                            cl_list.gl = cl_list.gl + amount / fact1
                            cl_list.revenue = cl_list.revenue + amount / fact1
                            t1_revenue = t1_revenue + amount / fact1

                    elif artikel.artart == 2 or artikel.artart == 6 or artikel.artart == 7 or artikel.artart == 11 or artikel.artart == 12:

                        if artikel.artart == 6:

                            cash_list = query(cash_list_list, filters=(lambda cash_list :cash_list.artnr == artikel.artnr), first=True)

                            if not cash_list:
                                cash_list = Cash_list()
                                cash_list_list.append(cash_list)

                                cash_list.artnr = artikel.artnr
                                cash_list.bezeich = artikel.bezeich


                            cash_list.betrag = cash_list.betrag - amount / fact1
                            cash = cash - amount / fact1

                        cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.artnr == artikel.artnr and cl_list.dept == artikel.departement), first=True)

                        if not cl_list:
                            cl_list = Cl_list()
                            cl_list_list.append(cl_list)

                            cl_list.flag = 200
                            cl_list.artnr = artikel.artnr
                            cl_list.dept = artikel.departement
                            cl_list.bezeich = to_string(artikel.bezeich, "x(19)")
                        cl_list.revenue = cl_list.revenue - amount / fact1
                        t2_revenue = t2_revenue - amount / fact1

                        if artikel.artart == 2:
                            cl_list.cl = cl_list.cl - amount / fact1
                            cl = cl - amount / fact1
                            t2_cl = t2_cl - amount / fact1
                            t_cl = t_cl - amount / fact1

                        elif artikel.artart == 6:
                            cl_list.cash = cl_list.cash - amount / fact1
                            t2_cash = t2_cash - amount / fact1
                            t_cash = t_cash - amount / fact1

                        elif artikel.artart == 7:
                            cl_list.card = cl_list.card - amount / fact1
                            cc = cc - amount / fact1
                            t2_cc = t2_cc - amount / fact1
                            t_cc = t_cc - amount / fact1

                        elif artikel.artart == 11:
                            cl_list.compli = cl_list.compli - amount / fact1
                            compli = compli - amount / fact1
                            t2_compli = t2_compli - amount / fact1
                            t_compli = t_compli - amount / fact1

                        elif artikel.artart == 12:
                            cl_list.mcoup = cl_list.mcoup - amount / fact1
                            mcoup = mcoup - amount / fact1
                            t2_mcoup = t2_mcoup - amount / fact1
                            t_mcoup = t_mcoup - amount / fact1

            if cash != 0:

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.bezeich.lower()  == "00 cash"), first=True)

                if not cl_list:
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.bezeich = "00 cash"
                cl_list.cash = cl_list.cash + cash
                t1_cash = t1_cash + cash
                t_cash = t_cash + cash
                cash = 0

            if cc != 0:

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.bezeich.lower()  == "00 Credit Cards"), first=True)

                if not cl_list:
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.bezeich = "00 Credit Cards"
                cl_list.card = cl_list.card + cc
                t1_cc = t1_cc + cc
                t_cc = t_cc + cc
                cc = 0

            if cl != 0:

                cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.bezeich.lower()  == "00 City Ledger"), first=True)

                if not cl_list:
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.bezeich = "00 City Ledger"
                cl_list.cl = cl_list.cl + cl
                t1_cl = t1_cl + cl
                t_cl = t_cl + cl
                cl = 0

        billjournal_obj_list = []
        for billjournal, artikel in db_session.query(Billjournal, Artikel).join(Artikel,(Artikel.artnr == Billjournal.artnr) &  (Artikel.departement == 0) &  (Artikel.artart != 5)).filter(
                (Billjournal.departement == 0) &  (Billjournal.bill_datum == to_date) &  (Billjournal.billjou_ref > 0) &  (Billjournal.anzahl != 0)).all():
            if billjournal._recid in billjournal_obj_list:
                continue
            else:
                billjournal_obj_list.append(billjournal._recid)

            if not depo_foreign:

                if foreign_flag:
                    amount = billjournal.fremdwaehrng
                else:
                    amount = billjournal.betrag
            else:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 110)).first()

                waehrung = db_session.query(Waehrung).filter(
                        (func.lower(Waehrung.wabkurz) == (foreign_curr).lower())).first()

                if to_date < htparam.fdate:

                    exrate = db_session.query(Exrate).filter(
                            (Exrate.datum == to_date) &  (Exrate.artnr == waehrungsnr)).first()

                    if exrate:
                        exchg_rate = exrate.betrag

                if exchg_rate == 0:
                    exchg_rate = waehrung.ankauf / waehrung.einheit
                amount = billjournal.betrag * exchg_rate
            cash = 0
            cc = 0
            cl = 0
            compli = 0
            mcoup = 0

            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.artnr == deposit_artnr and cl_list.dept == 0), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.artnr = deposit_artnr
                cl_list.bezeich = to_string(0, "99 ") + to_string(deposit_bez, "x(21)")
                cl_list.room = 0
            cl_list.revenue = cl_list.revenue - amount / fact1
            t1_revenue = t1_revenue - amount / fact1

            if artikel.artart == 6:

                cash_list = query(cash_list_list, filters=(lambda cash_list :cash_list.artnr == artikel.artnr), first=True)

                if not cash_list:
                    cash_list = Cash_list()
                    cash_list_list.append(cash_list)

                    cash_list.artnr = artikel.artnr
                    cash_list.bezeich = artikel.bezeich


                cash_list.betrag = cash_list.betrag - amount / fact1
                cl_list.cash = cl_list.cash - amount / fact1
                cash = cash - amount / fact1
                t1_cash = t1_cash - amount / fact1
                t_cash = t_cash - amount / fact1

            elif artikel.artart == 7:
                cl_list.card = cl_list.card - amount / fact1
                cc = cc - amount / fact1
                t1_cc = t1_cc - amount / fact1
                t_cc = t_cc - amount / fact1

            elif artikel.artart == 2:
                cl_list.cl = cl_list.cl - amount / fact1
                cl = cl - amount / fact1
                t1_cl = t1_cl - amount / fact1
                t_cl = t_cl - amount / fact1

        for billjournal in db_session.query(Billjournal).filter(
                (Billjournal.artnr == deposit_baartnr) &  (Billjournal.departement == depobuff.departement) &  (Billjournal.bill_datum == to_date) &  (Billjournal.billjou_ref > 0)).all():
            amount = - billjournal.betrag
            cash = 0
            cc = 0
            cl = 0
            compli = 0
            mcoup = 0

            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.artnr == deposit_baartnr and cl_list.dept == banquet_dept), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.dept = banquet_dept
                cl_list.artnr = deposit_baartnr
                cl_list.bezeich = to_string(depobuff.departement, "99 ") +\
                        to_string(deposit_babez, "x(21)")
                cl_list.room = 0


            cl_list.revenue = cl_list.revenue - amount / fact1
            t1_revenue = t1_revenue - amount / fact1

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == billjournal.billjou_ref) &  (Artikel.departement == 0)).first()

            if artikel.artart == 6:

                cash_list = query(cash_list_list, filters=(lambda cash_list :cash_list.artnr == artikel.artnr), first=True)

                if not cash_list:
                    cash_list = Cash_list()
                    cash_list_list.append(cash_list)

                    cash_list.artnr = artikel.artnr
                    cash_list.bezeich = artikel.bezeich


                cash_list.betrag = cash_list.betrag - amount / fact1
                cl_list.cash = cl_list.cash - amount / fact1
                cash = cash - amount / fact1
                t1_cash = t1_cash - amount / fact1
                t_cash = t_cash - amount / fact1

            elif artikel.artart == 7:
                cl_list.card = cl_list.card - amount / fact1
                cc = cc - amount / fact1
                t1_cc = t1_cc - amount / fact1
                t_cc = t_cc - amount / fact1

            elif artikel.artart == 2:
                cl_list.cl = cl_list.cl - amount / fact1
                cl = cl - amount / fact1
                t1_cl = t1_cl - amount / fact1
                t_cl = t_cl - amount / fact1

        for hoteldpt in db_session.query(Hoteldpt).filter(
                (Hoteldpt.num >= 0)).all():
            create_rlist()
            cash = 0
            cc = 0
            cl = 0
            compli = 0
            mcoup = 0
            room = 0
            rest = 0
            curr_dept = hoteldpt.num
            curr_bez = hoteldpt.depart
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.begin = True
            cl_list.flag = hoteldpt.num
            cl_list.dept = hoteldpt.num
            cl_list.bezeich = to_string(hoteldpt.num, "99 ") +\
                    to_string(hoteldpt.depart, "x(21)")

            for rechnr_list in query(rechnr_list_list):
                h_journal = db_session.query(H_journal).filter((H_journal.rechnr == rechnr_list.rechnr) &  (H_journal.departement == hoteldpt.num)).first()
                if not h_journal:
                    continue


                for h_bill_line in db_session.query(H_bill_line).filter(
                        (H_bill_line.bill_datum == to_date) &  (H_bill_line.departement == hoteldpt.num) &  (H_bill_line.rechnr == h_journal.rechnr)).all():

                    if foreign_flag:
                        amount = h_bill_line.fremdwbetrag
                    else:
                        amount = h_bill_line.betrag
                    rest = rest + amount / fact1

                    if h_bill_line.artnr != 0:

                        h_artikel = db_session.query(H_artikel).filter(
                                (H_artikel.artnr == h_bill_line.artnr) &  (H_artikel.departement == h_bill_line.departement)).first()

                        if h_artikel.artart == 0:
                            cl_list.revenue = cl_list.revenue + amount / fact1
                            t1_revenue = t1_revenue + amount / fact1

                        elif h_artikel.artart == 6:
                            cash = cash - amount / fact1

                            artikel = db_session.query(Artikel).filter(
                                    (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == 0)).first()

                            cash_list = query(cash_list_list, filters=(lambda cash_list :cash_list.artnr == artikel.artnr), first=True)

                            if not cash_list:
                                cash_list = Cash_list()
                                cash_list_list.append(cash_list)

                                cash_list.artnr = artikel.artnr
                                cash_list.bezeich = artikel.bezeich


                            cash_list.betrag = cash_list.betrag - amount / fact1

                        elif h_artikel.artart == 7:
                            cc = cc - amount / fact1

                        elif h_artikel.artart == 2:
                            cl = cl - amount / fact1

                        elif h_artikel.artart == 11:
                            compli = compli - amount / fact1
                            cl_list.revenue = cl_list.revenue + amount / fact1
                            t1_revenue = t1_revenue + amount / fact1

                        elif h_artikel.artart == 12:
                            mcoup = mcoup - amount / fact1
                            cl_list.revenue = cl_list.revenue + amount / fact1
                            t1_revenue = t1_revenue + amount / fact1
                    else:
                        room = room - amount / fact1

            if cl_list:
                t1_cash = t1_cash + cash
                t1_cc = t1_cc + cc
                t1_cl = t1_cl + cl
                t1_compli = t1_compli + compli
                t1_mcoup = t1_mcoup + mcoup
                t1_room = t1_room + room
                t1_gl = t1_gl + rest
                t_cash = t_cash + cash
                t_cc = t_cc + cc
                t_cl = t_cl + cl
                t_compli = t_compli + compli
                t_mcoup = t_mcoup + mcoup
                t_room = t_room + room
                t_gl = t_gl + rest
                cl_list.cash = cl_list.cash + cash
                cl_list.card = cl_list.card + cc
                cl_list.cl = cl_list.cl + cl
                cl_list.compli = cl_list.compli + compli
                cl_list.mcoup = cl_list.mcoup + mcoup
                cl_list.room = cl_list.room + room
                cl_list.gl = cl_list.gl + rest


        i = 0
        curr_flag = -1

        for cl_list in query(cl_list_list):

            if cl_list.flag == 200 and curr_flag != cl_list.flag:
                curr_flag = cl_list.flag

                if price_decimal == 0 and not foreign_flag:

                    if not long_digit or short_flag:
                        sumcsr_list = Sumcsr_list()
                        sumcsr_list_list.append(sumcsr_list)

                        sumcsr_list = Sumcsr_list()
                        sumcsr_list_list.append(sumcsr_list)

                        sumcsr_list.dept = "Subtotal"
                        sumcsr_list.cash = to_string(t1_cash, "->>>,>>>,>>>,>>9.99")
                        sumcsr_list.card = to_string(t1_cc, "->>>,>>>,>>>,>>9.99")
                        sumcsr_list.cl = to_string(t1_cl, "->>>,>>>,>>>,>>9.99")
                        sumcsr_list.compli = to_string(t1_compli, "->>>,>>>,>>>,>>9.99")
                        sumcsr_list.mealcou = to_string(t1_mcoup, "->>>,>>>,>>>,>>9.99")
                        sumcsr_list.rmfobill = to_string(t1_room, "->>>,>>>,>>>,>>9.99")
                        sumcsr_list.revenue = to_string(t1_revenue, "->>>,>>>,>>>,>>9.99")
                        sumcsr_list.outstand = to_string(t1_gl, "->>>,>>>,>>>,>>9.99")


                        sumcsr_list = Sumcsr_list()
                        sumcsr_list_list.append(sumcsr_list)

                        sumcsr_list = Sumcsr_list()
                        sumcsr_list_list.append(sumcsr_list)

                else:
                    sumcsr_list = Sumcsr_list()
                    sumcsr_list_list.append(sumcsr_list)

                    sumcsr_list = Sumcsr_list()
                    sumcsr_list_list.append(sumcsr_list)

                    sumcsr_list.dept = "Subtotal"
                    sumcsr_list.cash = to_string(t1_cash, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.card = to_string(t1_cc, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.cl = to_string(t1_cl, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.compli = to_string(t1_compli, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.mealcou = to_string(t1_mcoup, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.rmfobill = to_string(t1_room, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.revenue = to_string(t1_revenue, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.outstand = to_string(t1_gl, "->>>,>>>,>>>,>>9.99")


                    sumcsr_list = Sumcsr_list()
                    sumcsr_list_list.append(sumcsr_list)

                    sumcsr_list = Sumcsr_list()
                    sumcsr_list_list.append(sumcsr_list)

            sumcsr_list = Sumcsr_list()
            sumcsr_list_list.append(sumcsr_list)

            i = i + 1
            sumcsr_list.reihe = i
            sumcsr_list.flag = cl_list.flag
            sumcsr_list.artart = cl_list.artart

            if cl_list.begin and cl_list.dept == 0:
                sumcsr_list.dept = cl_list.bezeich
                sumcsr_list.cash = to_string(cl_list.cash, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.rmfobill = to_string(cl_list.room, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.card = to_string(cl_list.card, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.cl = to_string(cl_list.cl, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.revenue = to_string(cl_list.revenue, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.compli = to_string(cl_list.compli, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.mealcou = to_string(cl_list.mcoupon, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.outstand = to_string(cl_list.gl, "->>>,>>>,>>>,>>9.99")

            elif cl_list.artart >= 0 and price_decimal == 0 and not foreign_flag:

                if not long_digit or short_flag:
                    sumcsr_list.dept = cl_list.bezeich
                    sumcsr_list.cash = to_string(cl_list.cash, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.rmfobill = to_string(cl_list.room, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.card = to_string(cl_list.card, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.cl = to_string(cl_list.cl, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.revenue = to_string(cl_list.revenue, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.compli = to_string(cl_list.compli, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.mealcou = to_string(cl_list.mcoupon, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.outstand = to_string(cl_list.gl, "->>>,>>>,>>>,>>9.99")

            elif cl_list.artart >= 0:
                sumcsr_list.dept = cl_list.bezeich
                sumcsr_list.cash = to_string(cl_list.cash, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.rmfobill = to_string(cl_list.room, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.card = to_string(cl_list.card, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.cl = to_string(cl_list.cl, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.revenue = to_string(cl_list.revenue, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.compli = to_string(cl_list.compli, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.mealcou = to_string(cl_list.mcoupon, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.outstand = to_string(cl_list.gl, "->>>,>>>,>>>,>>9.99")

        cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.flag == 200), first=True)

        if not cl_list:

            if price_decimal == 0 and not foreign_flag:

                if not long_digit or short_flag:
                    sumcsr_list = Sumcsr_list()
                    sumcsr_list_list.append(sumcsr_list)

                    sumcsr_list = Sumcsr_list()
                    sumcsr_list_list.append(sumcsr_list)

                    sumcsr_list.dept = "Subtotal"
                    sumcsr_list.cash = to_string(t1_cash, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.card = to_string(t1_cc, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.cl = to_string(t1_cl, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.compli = to_string(t1_compli, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.mealcou = to_string(t1_mcoup, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.rmfobill = to_string(t1_room, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.revenue = to_string(t1_revenue, "->>>,>>>,>>>,>>9.99")
                    sumcsr_list.outstand = to_string(t1_gl, "->>>,>>>,>>>,>>9.99")


                    sumcsr_list = Sumcsr_list()
                    sumcsr_list_list.append(sumcsr_list)

            else:
                sumcsr_list = Sumcsr_list()
                sumcsr_list_list.append(sumcsr_list)

                sumcsr_list = Sumcsr_list()
                sumcsr_list_list.append(sumcsr_list)

                sumcsr_list.dept = "Subtotal"
                sumcsr_list.cash = to_string(t1_cash, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.card = to_string(t1_cc, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.cl = to_string(t1_cl, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.compli = to_string(t1_compli, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.mealcou = to_string(t1_mcoup, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.rmfobill = to_string(t1_room, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.revenue = to_string(t1_revenue, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.outstand = to_string(t1_gl, "->>>,>>>,>>>,>>9.99")


                sumcsr_list = Sumcsr_list()
                sumcsr_list_list.append(sumcsr_list)


        if price_decimal == 0 and not foreign_flag:

            if not long_digit or short_flag:
                sumcsr_list = Sumcsr_list()
                sumcsr_list_list.append(sumcsr_list)

                sumcsr_list = Sumcsr_list()
                sumcsr_list_list.append(sumcsr_list)

                sumcsr_list.dept = "Subtotal"
                sumcsr_list.cash = to_string(t2_cash, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.card = to_string(t2_cc, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.cl = to_string(t2_cl, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.compli = to_string(t2_compli, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.mealcou = to_string(t2_mcoup, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.rmfobill = to_string(t2_room, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.revenue = to_string(t2_revenue, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.outstand = to_string(t2_gl, "->>>,>>>,>>>,>>9.99")


                sumcsr_list = Sumcsr_list()
                sumcsr_list_list.append(sumcsr_list)

        else:
            sumcsr_list = Sumcsr_list()
            sumcsr_list_list.append(sumcsr_list)

            sumcsr_list = Sumcsr_list()
            sumcsr_list_list.append(sumcsr_list)

            sumcsr_list.dept = "Subtotal"
            sumcsr_list.cash = to_string(t2_cash, "->>>,>>>,>>>,>>9.99")
            sumcsr_list.card = to_string(t2_cc, "->>>,>>>,>>>,>>9.99")
            sumcsr_list.cl = to_string(t2_cl, "->>>,>>>,>>>,>>9.99")
            sumcsr_list.compli = to_string(t2_compli, "->>>,>>>,>>>,>>9.99")
            sumcsr_list.mealcou = to_string(t2_mcoup, "->>>,>>>,>>>,>>9.99")
            sumcsr_list.rmfobill = to_string(t2_room, "->>>,>>>,>>>,>>9.99")
            sumcsr_list.revenue = to_string(t2_revenue, "->>>,>>>,>>>,>>9.99")
            sumcsr_list.outstand = to_string(t2_gl, "->>>,>>>,>>>,>>9.99")


            sumcsr_list = Sumcsr_list()
            sumcsr_list_list.append(sumcsr_list)


        if price_decimal == 0 and not foreign_flag:

            if not long_digit or short_flag:
                sumcsr_list = Sumcsr_list()
                sumcsr_list_list.append(sumcsr_list)

                sumcsr_list.dept = "T O T A L"
                sumcsr_list.cash = to_string(t_cash, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.card = to_string(t_cc, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.cl = to_string(t_cl, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.compli = to_string(t_compli, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.mealcou = to_string(t_mcoup, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.rmfobill = to_string(t_room, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.revenue = to_string(t_revenue, "->>>,>>>,>>>,>>9.99")
                sumcsr_list.outstand = to_string(t_gl, "->>>,>>>,>>>,>>9.99")


                sumcsr_list = Sumcsr_list()
                sumcsr_list_list.append(sumcsr_list)

                sumcsr_list = Sumcsr_list()
                sumcsr_list_list.append(sumcsr_list)

        else:
            sumcsr_list = Sumcsr_list()
            sumcsr_list_list.append(sumcsr_list)

            sumcsr_list.dept = "T O T A L"
            sumcsr_list.cash = to_string(t_cash, "->>>,>>>,>>>,>>9.99")
            sumcsr_list.card = to_string(t_cc, "->>>,>>>,>>>,>>9.99")
            sumcsr_list.cl = to_string(t_cl, "->>>,>>>,>>>,>>9.99")
            sumcsr_list.compli = to_string(t_compli, "->>>,>>>,>>>,>>9.99")
            sumcsr_list.mealcou = to_string(t_mcoup, "->>>,>>>,>>>,>>9.99")
            sumcsr_list.rmfobill = to_string(t_room, "->>>,>>>,>>>,>>9.99")
            sumcsr_list.revenue = to_string(t_revenue, "->>>,>>>,>>>,>>9.99")
            sumcsr_list.outstand = to_string(t_gl, "->>>,>>>,>>>,>>9.99")


            sumcsr_list = Sumcsr_list()
            sumcsr_list_list.append(sumcsr_list)

            sumcsr_list = Sumcsr_list()
            sumcsr_list_list.append(sumcsr_list)

        t_cash = 0

        cash_list = query(cash_list_list, first=True)

        if cash_list:
            sumcsr_list = Sumcsr_list()
            sumcsr_list_list.append(sumcsr_list)

            i = i + 1
            sumcsr_list.reihe = i
            sumcsr_list.dept = "cash Breakdown:"

            for cash_list in query(cash_list_list):
                sumcsr_list = Sumcsr_list()
                sumcsr_list_list.append(sumcsr_list)

                i = i + 1
                t_cash = t_cash + cash_list.betrag
                sumcsr_list.reihe = i

                if price_decimal == 0 and not foreign_flag:
                    sumcsr_list.dept = cash_list.bezeich
                    sumcsr_list.cash = to_string(cash_list.betrag, "->>>,>>>,>>>,>>9.99")


                else:
                    sumcsr_list.dept = cash_list.bezeich
                    sumcsr_list.cash = to_string(cash_list.betrag, "->>>,>>>,>>>,>>9.99")


            sumcsr_list = Sumcsr_list()
            sumcsr_list_list.append(sumcsr_list)

            sumcsr_list = Sumcsr_list()
            sumcsr_list_list.append(sumcsr_list)

            i = i + 1
            sumcsr_list.reihe = i
            sumcsr_list.dept = "Total cash"

            if price_decimal == 0 and not foreign_flag:
                sumcsr_list.cash = to_string(t_cash, "->>>,>>>,>>>,>>9.99")


            else:
                sumcsr_list.cash = to_string(t_cash, "->>>,>>>,>>>,>>9.99")

    def create_rlist():

        nonlocal msg_str, sumcsr_list_list, long_digit, curr_dept, price_decimal, curr_bez, foreign_curr, from_date, fact1, curr_tot_cash, lvcarea, htparam, bill_line, artikel, bill, zwkum, billjournal, waehrung, exrate, hoteldpt, h_journal, h_bill_line, h_artikel
        nonlocal bline, h_bline, depobuff


        nonlocal sumcsr_list, output_list, cash_list, rechnr_list, art_list, cl_list, bline, h_bline, depobuff
        nonlocal sumcsr_list_list, output_list_list, cash_list_list, rechnr_list_list, art_list_list, cl_list_list


        rechnr_list_list.clear()

        for h_journal in db_session.query(H_journal).filter(
                (H_journal.departement == hoteldpt.num) &  (H_journal.bill_datum == to_date)).all():

            rechnr_list = query(rechnr_list_list, filters=(lambda rechnr_list :rechnr_list.rechnr == h_journal.rechnr), first=True)

            if not rechnr_list:
                rechnr_list = Rechnr_list()
                rechnr_list_list.append(rechnr_list)

                rechnr_list.rechnr = h_journal.rechnr


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))


    create_umsatz()

    return generate_output()