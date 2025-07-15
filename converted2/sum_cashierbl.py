#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bill_line, Artikel, Bill, Zwkum, Billjournal, Waehrung, Exrate, Hoteldpt, H_journal, H_bill_line, H_artikel

def sum_cashierbl(pvilanguage:int, to_date:date, short_flag:bool, foreign_flag:bool):

    prepare_cache ([Htparam, Bill_line, Artikel, Bill, Zwkum, Billjournal, Waehrung, Exrate, Hoteldpt, H_journal, H_bill_line, H_artikel])

    msg_str = ""
    output_list_data = []
    long_digit:bool = False
    curr_dept:int = 0
    price_decimal:int = 0
    curr_bez:string = ""
    foreign_curr:string = ""
    from_date:date = None
    fact1:Decimal = 1
    lvcarea:string = "gacct-balance"
    htparam = bill_line = artikel = bill = zwkum = billjournal = waehrung = exrate = hoteldpt = h_journal = h_bill_line = h_artikel = None

    output_list = cash_list = rechnr_list = art_list = cl_list = None

    output_list_data, Output_list = create_model("Output_list", {"reihe":int, "flag":int, "artart":int, "str":string})
    cash_list_data, Cash_list = create_model("Cash_list", {"artnr":int, "bezeich":string, "betrag":Decimal})
    rechnr_list_data, Rechnr_list = create_model("Rechnr_list", {"rechnr":int})
    art_list_data, Art_list = create_model("Art_list", {"artnr":int, "artart":int, "dept":int, "bezeich":string, "revenue":Decimal})
    cl_list_data, Cl_list = create_model("Cl_list", {"begin":bool, "flag":int, "artnr":int, "artart":int, "dept":int, "bezeich":string, "cash":Decimal, "room":Decimal, "card":Decimal, "cl":Decimal, "gl":Decimal, "revenue":Decimal, "compli":Decimal, "mcoupon":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, output_list_data, long_digit, curr_dept, price_decimal, curr_bez, foreign_curr, from_date, fact1, lvcarea, htparam, bill_line, artikel, bill, zwkum, billjournal, waehrung, exrate, hoteldpt, h_journal, h_bill_line, h_artikel
        nonlocal pvilanguage, to_date, short_flag, foreign_flag


        nonlocal output_list, cash_list, rechnr_list, art_list, cl_list
        nonlocal output_list_data, cash_list_data, rechnr_list_data, art_list_data, cl_list_data

        return {"msg_str": msg_str, "output-list": output_list_data}

    def create_umsatz():

        nonlocal msg_str, output_list_data, long_digit, curr_dept, price_decimal, curr_bez, foreign_curr, from_date, fact1, lvcarea, htparam, bill_line, artikel, bill, zwkum, billjournal, waehrung, exrate, hoteldpt, h_journal, h_bill_line, h_artikel
        nonlocal pvilanguage, to_date, short_flag, foreign_flag


        nonlocal output_list, cash_list, rechnr_list, art_list, cl_list
        nonlocal output_list_data, cash_list_data, rechnr_list_data, art_list_data, cl_list_data

        cash:Decimal = to_decimal("0.0")
        cc:Decimal = to_decimal("0.0")
        cl:Decimal = to_decimal("0.0")
        compli:Decimal = to_decimal("0.0")
        mcoup:Decimal = to_decimal("0.0")
        rest:Decimal = to_decimal("0.0")
        room:Decimal = to_decimal("0.0")
        i:int = 0
        curr_flag:int = 0
        t1_cash:Decimal = to_decimal("0.0")
        t1_cc:Decimal = to_decimal("0.0")
        t1_cl:Decimal = to_decimal("0.0")
        t1_compli:Decimal = to_decimal("0.0")
        t1_mcoup:Decimal = to_decimal("0.0")
        t1_room:Decimal = to_decimal("0.0")
        t1_revenue:Decimal = to_decimal("0.0")
        t1_gl:Decimal = to_decimal("0.0")
        t2_cash:Decimal = to_decimal("0.0")
        t2_cc:Decimal = to_decimal("0.0")
        t2_cl:Decimal = to_decimal("0.0")
        t2_compli:Decimal = to_decimal("0.0")
        t2_mcoup:Decimal = to_decimal("0.0")
        t2_room:Decimal = to_decimal("0.0")
        t2_revenue:Decimal = to_decimal("0.0")
        t2_gl:Decimal = to_decimal("0.0")
        t_cash:Decimal = to_decimal("0.0")
        t_cc:Decimal = to_decimal("0.0")
        t_cl:Decimal = to_decimal("0.0")
        t_compli:Decimal = to_decimal("0.0")
        t_mcoup:Decimal = to_decimal("0.0")
        t_room:Decimal = to_decimal("0.0")
        t_revenue:Decimal = to_decimal("0.0")
        t_gl:Decimal = to_decimal("0.0")
        do_it:bool = False
        exchg_rate:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        deposit_artnr:int = 0
        deposit_baartnr:int = 0
        deposit_bez:string = "Deposit (Rsv)"
        depo_foreign:bool = False
        banquet_dept:int = -1
        deposit_babez:string = "Deposit (Bqt)"
        bline = None
        h_bline = None
        depobuff = None
        Bline =  create_buffer("Bline",Bill_line)
        H_bline =  create_buffer("H_bline",Bill_line)
        Depobuff =  create_buffer("Depobuff",Artikel)
        t_cash =  to_decimal("0")
        t_cc =  to_decimal("0")
        t_cl =  to_decimal("0")
        t_compli =  to_decimal("0")
        t_mcoup =  to_decimal("0")
        t_revenue =  to_decimal("0")
        t_room =  to_decimal("0")
        t_gl =  to_decimal("0")
        t1_cash =  to_decimal("0")
        t1_cc =  to_decimal("0")
        t1_cl =  to_decimal("0")
        t1_compli =  to_decimal("0")
        t1_mcoup =  to_decimal("0")
        t1_revenue =  to_decimal("0")
        t1_room =  to_decimal("0")
        t1_gl =  to_decimal("0")
        t2_cash =  to_decimal("0")
        t2_cc =  to_decimal("0")
        t2_cl =  to_decimal("0")
        t2_compli =  to_decimal("0")
        t2_mcoup =  to_decimal("0")
        t2_revenue =  to_decimal("0")
        t2_room =  to_decimal("0")
        t2_gl =  to_decimal("0")


        output_list_data.clear()
        cl_list_data.clear()
        cash_list_data.clear()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})
        deposit_artnr = htparam.finteger

        artikel = get_cache (Artikel, {"artnr": [(eq, deposit_artnr)],"departement": [(eq, 0)]})

        if artikel:
            deposit_bez = artikel.bezeich
            depo_foreign = artikel.pricetab

        htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})

        if htparam.finteger != 0:
            banquet_dept = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 117)]})
        deposit_baartnr = htparam.finteger

        depobuff = get_cache (Artikel, {"artnr": [(eq, deposit_baartnr)],"departement": [(eq, banquet_dept)],"artart": [(eq, 5)]})

        if not depobuff:

            depobuff = get_cache (Artikel, {"artnr": [(eq, deposit_baartnr)],"departement": [(eq, 0)],"artart": [(eq, 5)]})

        if depobuff:
            deposit_babez = depobuff.bezeich

        bill_obj_list = {}
        bill = Bill()
        bline = Bill_line()
        for bill.rechnr, bill._recid, bline.fremdwbetrag, bline.betrag, bline.artnr, bline.departement, bline.bezeich, bline.userinit, bline._recid in db_session.query(Bill.rechnr, Bill._recid, Bline.fremdwbetrag, Bline.betrag, Bline.artnr, Bline.departement, Bline.bezeich, Bline.userinit, Bline._recid).join(Bline,(Bline.rechnr == Bill.rechnr) & (Bline.bill_datum == to_date)).filter(
                 (((Bill.flag == 0) & (Bill.datum >= to_date)) | ((Bill.flag == 1) & (Bill.datum >= to_date))) & (Bill.resnr > 0)).order_by(Bill._recid).all():
            if bill_obj_list.get(bill._recid):
                continue
            else:
                bill_obj_list[bill._recid] = True


            curr_dept = bill.rechnr

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum == to_date)).order_by(Bill_line._recid).all():

                if foreign_flag:
                    amount =  to_decimal(bill_line.fremdwbetrag)
                else:
                    amount =  to_decimal(bill_line.betrag)

                artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

                if not artikel and num_entries(bill_line.bezeich, "*") > 1:

                    artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, 0)]})

                if not artikel:
                    msg_str = msg_str + "&W" + translateExtended ("Artikel not found:", lvcarea, "") + " " + translateExtended ("Bill No:", lvcarea, "") + " " + to_string(bill.rechnr) + "; " + translateExtended ("Article No:", lvcarea, "") + " " + to_string(bill_line.artnr) + " - " + bill_line.bezeich + " " + trim(to_string(bill_line.betrag, "->>>,>>>,>>9.99"))

                if artikel:

                    if artikel.artart == 0 or artikel.artart == 8 or artikel.artart == 9 or artikel.artart == 5:
                        do_it = True

                        if artikel.artart == 5 and artikel.departement == 0 and bill_line.userinit.lower()  == ("$$").lower() :
                            do_it = False

                        if do_it:
                            curr_bez = artikel.bezeich

                            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.artnr == artikel.artnr and cl_list.dept == artikel.departement), first=True)

                            if not cl_list:
                                cl_list = Cl_list()
                                cl_list_data.append(cl_list)

                                cl_list.flag = -1
                                cl_list.artart = artikel.umsatzart
                                cl_list.artnr = artikel.artnr
                                cl_list.dept = artikel.departement
                                cl_list.bezeich = to_string(artikel.departement, "99 ") +\
                                        to_string(artikel.bezeich, "x(21)")


                            cl_list.room =  to_decimal(cl_list.room) + to_decimal(amount) / to_decimal(fact1)
                            cl_list.revenue =  to_decimal(cl_list.revenue) + to_decimal(amount) / to_decimal(fact1)
                            t1_revenue =  to_decimal(t1_revenue) + to_decimal(amount) / to_decimal(fact1)
                            t1_room =  to_decimal(t1_room) + to_decimal(amount) / to_decimal(fact1)
                            t_room =  to_decimal(t_room) + to_decimal(amount) / to_decimal(fact1)

                    elif artikel.artart == 2 or artikel.artart == 6 or artikel.artart == 7 or artikel.artart == 11 or artikel.artart == 12:

                        if artikel.artart == 6:

                            cash_list = query(cash_list_data, filters=(lambda cash_list: cash_list.artnr == artikel.artnr), first=True)

                            if not cash_list:
                                cash_list = Cash_list()
                                cash_list_data.append(cash_list)

                                cash_list.artnr = artikel.artnr
                                cash_list.bezeich = artikel.bezeich


                            cash_list.betrag =  to_decimal(cash_list.betrag) - to_decimal(amount) / to_decimal(fact1)

                        cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.artnr == artikel.artnr and cl_list.dept == artikel.departement), first=True)

                        if not cl_list:
                            cl_list = Cl_list()
                            cl_list_data.append(cl_list)

                            cl_list.flag = 200
                            cl_list.artnr = artikel.artnr
                            cl_list.dept = artikel.departement
                            cl_list.bezeich = to_string(artikel.bezeich, "x(19)")
                        cl_list.revenue =  to_decimal(cl_list.revenue) - to_decimal(amount) / to_decimal(fact1)
                        t2_revenue =  to_decimal(t2_revenue) - to_decimal(amount) / to_decimal(fact1)

                        if artikel.artart == 2:
                            cl_list.cl =  to_decimal(cl_list.cl) - to_decimal(amount) / to_decimal(fact1)
                            t2_cl =  to_decimal(t2_cl) - to_decimal(amount) / to_decimal(fact1)
                            t_cl =  to_decimal(t_cl) - to_decimal(amount) / to_decimal(fact1)

                        elif artikel.artart == 6:
                            cl_list.cash =  to_decimal(cl_list.cash) - to_decimal(amount) / to_decimal(fact1)
                            t2_cash =  to_decimal(t2_cash) - to_decimal(amount) / to_decimal(fact1)
                            t_cash =  to_decimal(t_cash) - to_decimal(amount) / to_decimal(fact1)

                        elif artikel.artart == 7:
                            cl_list.card =  to_decimal(cl_list.card) - to_decimal(amount) / to_decimal(fact1)
                            t2_cc =  to_decimal(t2_cc) - to_decimal(amount) / to_decimal(fact1)
                            t_cc =  to_decimal(t_cc) - to_decimal(amount) / to_decimal(fact1)

                        elif artikel.artart == 11:
                            cl_list.compli =  to_decimal(cl_list.compli) - to_decimal(amount) / to_decimal(fact1)
                            t2_compli =  to_decimal(t2_compli) - to_decimal(amount) / to_decimal(fact1)
                            t_compli =  to_decimal(t_compli) - to_decimal(amount) / to_decimal(fact1)

                        elif artikel.artart == 12:
                            cl_list.mcoup =  to_decimal(cl_list.mcoup) - to_decimal(amount) / to_decimal(fact1)
                            t2_mcoup =  to_decimal(t2_mcoup) - to_decimal(amount) / to_decimal(fact1)
                            t_mcoup =  to_decimal(t_mcoup) - to_decimal(amount) / to_decimal(fact1)

        bill_obj_list = {}
        bill = Bill()
        bline = Bill_line()
        for bill.rechnr, bill._recid, bline.fremdwbetrag, bline.betrag, bline.artnr, bline.departement, bline.bezeich, bline.userinit, bline._recid in db_session.query(Bill.rechnr, Bill._recid, Bline.fremdwbetrag, Bline.betrag, Bline.artnr, Bline.departement, Bline.bezeich, Bline.userinit, Bline._recid).join(Bline,(Bline.rechnr == Bill.rechnr) & (Bline.bill_datum == to_date)).filter(
                 (((Bill.flag == 0) & (Bill.datum >= to_date)) | ((Bill.flag == 1) & (Bill.datum >= to_date))) & (Bill.resnr == 0)).order_by(Bill._recid).all():
            if bill_obj_list.get(bill._recid):
                continue
            else:
                bill_obj_list[bill._recid] = True


            curr_dept = bill.rechnr
            cash =  to_decimal("0")
            cc =  to_decimal("0")
            cl =  to_decimal("0")
            compli =  to_decimal("0")
            mcoup =  to_decimal("0")
            room =  to_decimal("0")
            i = 1

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr) & (Bill_line.bill_datum == to_date)).order_by(Bill_line.sysdate, Bill_line.zeit).all():

                artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

                if not artikel and num_entries(bill_line.bezeich, "*") > 1:

                    artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

                if not artikel:
                    msg_str = msg_str + "&W" + translateExtended ("Artikel not found:", lvcarea, "") + " " + translateExtended ("Bill No:", lvcarea, "") + " " + to_string(bill.rechnr) + "; " + translateExtended ("Article No:", lvcarea, "") + " " + to_string(bill_line.artnr) + " - " + bill_line.bezeich + " " + trim(to_string(bill_line.betrag, "->>>,>>>,>>9.99"))
                else:

                    zwkum = get_cache (Zwkum, {"zknr": [(eq, artikel.zwkum)],"departement": [(eq, artikel.departement)]})
                    i = i + 1
                    curr_bez = artikel.bezeich

                    if foreign_flag:
                        amount =  to_decimal(bill_line.fremdwbetrag)
                    else:
                        amount =  to_decimal(bill_line.betrag)

                    if artikel.artart == 0 or artikel.artart == 9 or artikel.artart == 8 or artikel.artart == 5:

                        if artikel.departement == 0:
                            do_it = True

                            if artikel.artart == 5 and bill_line.userinit.lower()  == ("$$").lower() :
                                do_it = False

                            if do_it:

                                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.artnr == artikel.artnr and cl_list.dept == artikel.departement), first=True)

                                if not cl_list:
                                    cl_list = Cl_list()
                                    cl_list_data.append(cl_list)

                                    cl_list.flag = 0
                                    cl_list.artart = artikel.umsatzart
                                    cl_list.artnr = artikel.artnr
                                    cl_list.dept = artikel.departement
                                    cl_list.bezeich = to_string(artikel.departement, "99 ") +\
                                            to_string(artikel.bezeich, "x(21)")


                                cl_list.gl =  to_decimal(cl_list.gl) + to_decimal(amount) / to_decimal(fact1)
                                cl_list.revenue =  to_decimal(cl_list.revenue) + to_decimal(amount) / to_decimal(fact1)
                                t1_revenue =  to_decimal(t1_revenue) + to_decimal(amount) / to_decimal(fact1)

                        elif artikel.departement > 0:

                            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.artnr == zwkum.zknr and cl_list.dept == zwkum.departement), first=True)

                            if not cl_list:
                                cl_list = Cl_list()
                                cl_list_data.append(cl_list)

                                cl_list.flag = 0
                                cl_list.artart = artikel.umsatzart
                                cl_list.artnr = zwkum.zknr
                                cl_list.dept = zwkum.departement
                                cl_list.bezeich = to_string(zwkum.departement, "99 ") +\
                                        to_string(zwkum.bezeich, "x(21)")


                            cl_list.gl =  to_decimal(cl_list.gl) + to_decimal(amount) / to_decimal(fact1)
                            cl_list.revenue =  to_decimal(cl_list.revenue) + to_decimal(amount) / to_decimal(fact1)
                            t1_revenue =  to_decimal(t1_revenue) + to_decimal(amount) / to_decimal(fact1)

                    elif artikel.artart == 2 or artikel.artart == 6 or artikel.artart == 7 or artikel.artart == 11 or artikel.artart == 12:

                        if artikel.artart == 6:

                            cash_list = query(cash_list_data, filters=(lambda cash_list: cash_list.artnr == artikel.artnr), first=True)

                            if not cash_list:
                                cash_list = Cash_list()
                                cash_list_data.append(cash_list)

                                cash_list.artnr = artikel.artnr
                                cash_list.bezeich = artikel.bezeich


                            cash_list.betrag =  to_decimal(cash_list.betrag) - to_decimal(amount) / to_decimal(fact1)
                            cash =  to_decimal(cash) - to_decimal(amount) / to_decimal(fact1)

                        if artikel.artart == 2:
                            cl =  to_decimal(cl) - to_decimal(amount) / to_decimal(fact1)

                        elif artikel.artart == 6:
                            pass

                        elif artikel.artart == 7:
                            cc =  to_decimal(cc) - to_decimal(amount) / to_decimal(fact1)

                        elif artikel.artart == 11:
                            compli =  to_decimal(compli) - to_decimal(amount) / to_decimal(fact1)

                        elif artikel.artart == 12:
                            mcoup =  to_decimal(mcoup) - to_decimal(amount) / to_decimal(fact1)

            if cash != 0:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.bezeich.lower()  == ("00 cash").lower()), first=True)

                if not cl_list:
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.bezeich = "00 cash"
                cl_list.cash =  to_decimal(cl_list.cash) + to_decimal(cash)
                t1_cash =  to_decimal(t1_cash) + to_decimal(cash)
                t_cash =  to_decimal(t_cash) + to_decimal(cash)
                cash =  to_decimal("0")

            if cc != 0:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.bezeich.lower()  == ("00 Credit Cards").lower()), first=True)

                if not cl_list:
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.bezeich = "00 Credit Cards"
                cl_list.card =  to_decimal(cl_list.card) + to_decimal(cc)
                t1_cc =  to_decimal(t1_cc) + to_decimal(cc)
                t_cc =  to_decimal(t_cc) + to_decimal(cc)
                cc =  to_decimal("0")

            if cl != 0:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.bezeich.lower()  == ("00 City Ledger").lower()), first=True)

                if not cl_list:
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.bezeich = "00 City Ledger"
                cl_list.cl =  to_decimal(cl_list.cl) + to_decimal(cl)
                t1_cl =  to_decimal(t1_cl) + to_decimal(cl)
                t_cl =  to_decimal(t_cl) + to_decimal(cl)
                cl =  to_decimal("0")

        billjournal_obj_list = {}
        billjournal = Billjournal()
        artikel = Artikel()
        for billjournal.fremdwaehrng, billjournal.betrag, billjournal.billjou_ref, billjournal._recid, artikel.bezeich, artikel.pricetab, artikel.artart, artikel.departement, artikel.artnr, artikel.umsatzart, artikel.zwkum, artikel._recid in db_session.query(Billjournal.fremdwaehrng, Billjournal.betrag, Billjournal.billjou_ref, Billjournal._recid, Artikel.bezeich, Artikel.pricetab, Artikel.artart, Artikel.departement, Artikel.artnr, Artikel.umsatzart, Artikel.zwkum, Artikel._recid).join(Artikel,(Artikel.artnr == Billjournal.artnr) & (Artikel.departement == 0) & (Artikel.artart != 5)).filter(
                 (Billjournal.departement == 0) & (Billjournal.bill_datum == to_date) & (Billjournal.billjou_ref > 0) & (Billjournal.anzahl != 0)).order_by(Billjournal._recid).all():
            if billjournal_obj_list.get(billjournal._recid):
                continue
            else:
                billjournal_obj_list[billjournal._recid] = True

            if not depo_foreign:

                if foreign_flag:
                    amount =  to_decimal(billjournal.fremdwaehrng)
                else:
                    amount =  to_decimal(billjournal.betrag)
            else:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

                waehrung = get_cache (Waehrung, {"wabkurz": [(eq, foreign_curr)]})

                if to_date < htparam.fdate:

                    exrate = get_cache (Exrate, {"datum": [(eq, to_date)],"artnr": [(eq, waehrung.waehrungsnr)]})

                    if exrate:
                        exchg_rate =  to_decimal(exrate.betrag)

                if exchg_rate == 0:
                    exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                amount =  to_decimal(billjournal.betrag) * to_decimal(exchg_rate)
            cash =  to_decimal("0")
            cc =  to_decimal("0")
            cl =  to_decimal("0")
            compli =  to_decimal("0")
            mcoup =  to_decimal("0")

            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.artnr == deposit_artnr and cl_list.dept == 0), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.artnr = deposit_artnr
                cl_list.bezeich = to_string(0, "99 ") + to_string(deposit_bez, "x(21)")
                cl_list.room =  to_decimal("0")
            cl_list.revenue =  to_decimal(cl_list.revenue) - to_decimal(amount) / to_decimal(fact1)
            t1_revenue =  to_decimal(t1_revenue) - to_decimal(amount) / to_decimal(fact1)

            if artikel.artart == 6:

                cash_list = query(cash_list_data, filters=(lambda cash_list: cash_list.artnr == artikel.artnr), first=True)

                if not cash_list:
                    cash_list = Cash_list()
                    cash_list_data.append(cash_list)

                    cash_list.artnr = artikel.artnr
                    cash_list.bezeich = artikel.bezeich


                cash_list.betrag =  to_decimal(cash_list.betrag) - to_decimal(amount) / to_decimal(fact1)
                cl_list.cash =  to_decimal(cl_list.cash) - to_decimal(amount) / to_decimal(fact1)
                cash =  to_decimal(cash) - to_decimal(amount) / to_decimal(fact1)
                t1_cash =  to_decimal(t1_cash) - to_decimal(amount) / to_decimal(fact1)
                t_cash =  to_decimal(t_cash) - to_decimal(amount) / to_decimal(fact1)

            elif artikel.artart == 7:
                cl_list.card =  to_decimal(cl_list.card) - to_decimal(amount) / to_decimal(fact1)
                cc =  to_decimal(cc) - to_decimal(amount) / to_decimal(fact1)
                t1_cc =  to_decimal(t1_cc) - to_decimal(amount) / to_decimal(fact1)
                t_cc =  to_decimal(t_cc) - to_decimal(amount) / to_decimal(fact1)

            elif artikel.artart == 2:
                cl_list.cl =  to_decimal(cl_list.cl) - to_decimal(amount) / to_decimal(fact1)
                cl =  to_decimal(cl) - to_decimal(amount) / to_decimal(fact1)
                t1_cl =  to_decimal(t1_cl) - to_decimal(amount) / to_decimal(fact1)
                t_cl =  to_decimal(t_cl) - to_decimal(amount) / to_decimal(fact1)

        for billjournal in db_session.query(Billjournal).filter(
                 (Billjournal.artnr == deposit_baartnr) & (Billjournal.departement == depobuff.departement) & (Billjournal.bill_datum == to_date) & (Billjournal.billjou_ref > 0)).order_by(Billjournal._recid).all():
            amount =  - to_decimal(billjournal.betrag)
            cash =  to_decimal("0")
            cc =  to_decimal("0")
            cl =  to_decimal("0")
            compli =  to_decimal("0")
            mcoup =  to_decimal("0")

            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.artnr == deposit_baartnr and cl_list.dept == banquet_dept), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.dept = banquet_dept
                cl_list.artnr = deposit_baartnr
                cl_list.bezeich = to_string(depobuff.departement, "99 ") +\
                        to_string(deposit_babez, "x(21)")
                cl_list.room =  to_decimal("0")


            cl_list.revenue =  to_decimal(cl_list.revenue) - to_decimal(amount) / to_decimal(fact1)
            t1_revenue =  to_decimal(t1_revenue) - to_decimal(amount) / to_decimal(fact1)

            artikel = get_cache (Artikel, {"artnr": [(eq, billjournal.billjou_ref)],"departement": [(eq, 0)]})

            if artikel.artart == 6:

                cash_list = query(cash_list_data, filters=(lambda cash_list: cash_list.artnr == artikel.artnr), first=True)

                if not cash_list:
                    cash_list = Cash_list()
                    cash_list_data.append(cash_list)

                    cash_list.artnr = artikel.artnr
                    cash_list.bezeich = artikel.bezeich


                cash_list.betrag =  to_decimal(cash_list.betrag) - to_decimal(amount) / to_decimal(fact1)
                cl_list.cash =  to_decimal(cl_list.cash) - to_decimal(amount) / to_decimal(fact1)
                cash =  to_decimal(cash) - to_decimal(amount) / to_decimal(fact1)
                t1_cash =  to_decimal(t1_cash) - to_decimal(amount) / to_decimal(fact1)
                t_cash =  to_decimal(t_cash) - to_decimal(amount) / to_decimal(fact1)

            elif artikel.artart == 7:
                cl_list.card =  to_decimal(cl_list.card) - to_decimal(amount) / to_decimal(fact1)
                cc =  to_decimal(cc) - to_decimal(amount) / to_decimal(fact1)
                t1_cc =  to_decimal(t1_cc) - to_decimal(amount) / to_decimal(fact1)
                t_cc =  to_decimal(t_cc) - to_decimal(amount) / to_decimal(fact1)

            elif artikel.artart == 2:
                cl_list.cl =  to_decimal(cl_list.cl) - to_decimal(amount) / to_decimal(fact1)
                cl =  to_decimal(cl) - to_decimal(amount) / to_decimal(fact1)
                t1_cl =  to_decimal(t1_cl) - to_decimal(amount) / to_decimal(fact1)
                t_cl =  to_decimal(t_cl) - to_decimal(amount) / to_decimal(fact1)

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= 0)).order_by(Hoteldpt.num).all():
            create_rlist()
            cash =  to_decimal("0")
            cc =  to_decimal("0")
            cl =  to_decimal("0")
            compli =  to_decimal("0")
            mcoup =  to_decimal("0")
            room =  to_decimal("0")
            rest =  to_decimal("0")
            curr_dept = hoteldpt.num
            curr_bez = hoteldpt.depart
            cl_list = Cl_list()
            cl_list_data.append(cl_list)

            cl_list.begin = True
            cl_list.flag = hoteldpt.num
            cl_list.dept = hoteldpt.num
            cl_list.bezeich = to_string(hoteldpt.num, "99 ") +\
                    to_string(hoteldpt.depart, "x(21)")

            h_journal_obj_list = {}
            for h_journal in db_session.query(H_journal).filter(
                     ((H_journal.rechnr.in_(list(set([rechnr_list.rechnr for rechnr_list in rechnr_list_data])))) & (H_journal.departement == hoteldpt.num))).order_by(H_journal._recid).all():
                if h_journal_obj_list.get(h_journal._recid):
                    continue
                else:
                    h_journal_obj_list[h_journal._recid] = True

                for h_bill_line in db_session.query(H_bill_line).filter(
                         (H_bill_line.bill_datum == to_date) & (H_bill_line.departement == hoteldpt.num) & (H_bill_line.rechnr == h_journal.rechnr)).order_by(H_bill_line._recid).all():

                    if foreign_flag:
                        amount =  to_decimal(h_bill_line.fremdwbetrag)
                    else:
                        amount =  to_decimal(h_bill_line.betrag)
                    rest =  to_decimal(rest) + to_decimal(amount) / to_decimal(fact1)

                    if h_bill_line.artnr != 0:

                        h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})

                        if h_artikel.artart == 0:
                            cl_list.revenue =  to_decimal(cl_list.revenue) + to_decimal(amount) / to_decimal(fact1)
                            t1_revenue =  to_decimal(t1_revenue) + to_decimal(amount) / to_decimal(fact1)

                        elif h_artikel.artart == 6:
                            cash =  to_decimal(cash) - to_decimal(amount) / to_decimal(fact1)

                            artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, 0)]})

                            cash_list = query(cash_list_data, filters=(lambda cash_list: cash_list.artnr == artikel.artnr), first=True)

                            if not cash_list:
                                cash_list = Cash_list()
                                cash_list_data.append(cash_list)

                                cash_list.artnr = artikel.artnr
                                cash_list.bezeich = artikel.bezeich


                            cash_list.betrag =  to_decimal(cash_list.betrag) - to_decimal(amount) / to_decimal(fact1)

                        elif h_artikel.artart == 7:
                            cc =  to_decimal(cc) - to_decimal(amount) / to_decimal(fact1)

                        elif h_artikel.artart == 2:
                            cl =  to_decimal(cl) - to_decimal(amount) / to_decimal(fact1)

                        elif h_artikel.artart == 11:
                            compli =  to_decimal(compli) - to_decimal(amount) / to_decimal(fact1)
                            cl_list.revenue =  to_decimal(cl_list.revenue) + to_decimal(amount) / to_decimal(fact1)
                            t1_revenue =  to_decimal(t1_revenue) + to_decimal(amount) / to_decimal(fact1)

                        elif h_artikel.artart == 12:
                            mcoup =  to_decimal(mcoup) - to_decimal(amount) / to_decimal(fact1)
                            cl_list.revenue =  to_decimal(cl_list.revenue) + to_decimal(amount) / to_decimal(fact1)
                            t1_revenue =  to_decimal(t1_revenue) + to_decimal(amount) / to_decimal(fact1)
                    else:
                        room =  to_decimal(room) - to_decimal(amount) / to_decimal(fact1)

            if cl_list:
                t1_cash =  to_decimal(t1_cash) + to_decimal(cash)
                t1_cc =  to_decimal(t1_cc) + to_decimal(cc)
                t1_cl =  to_decimal(t1_cl) + to_decimal(cl)
                t1_compli =  to_decimal(t1_compli) + to_decimal(compli)
                t1_mcoup =  to_decimal(t1_mcoup) + to_decimal(mcoup)
                t1_room =  to_decimal(t1_room) + to_decimal(room)
                t1_gl =  to_decimal(t1_gl) + to_decimal(rest)
                t_cash =  to_decimal(t_cash) + to_decimal(cash)
                t_cc =  to_decimal(t_cc) + to_decimal(cc)
                t_cl =  to_decimal(t_cl) + to_decimal(cl)
                t_compli =  to_decimal(t_compli) + to_decimal(compli)
                t_mcoup =  to_decimal(t_mcoup) + to_decimal(mcoup)
                t_room =  to_decimal(t_room) + to_decimal(room)
                t_gl =  to_decimal(t_gl) + to_decimal(rest)
                cl_list.cash =  to_decimal(cl_list.cash) + to_decimal(cash)
                cl_list.card =  to_decimal(cl_list.card) + to_decimal(cc)
                cl_list.cl =  to_decimal(cl_list.cl) + to_decimal(cl)
                cl_list.compli =  to_decimal(cl_list.compli) + to_decimal(compli)
                cl_list.mcoup =  to_decimal(cl_list.mcoup) + to_decimal(mcoup)
                cl_list.room =  to_decimal(cl_list.room) + to_decimal(room)
                cl_list.gl =  to_decimal(cl_list.gl) + to_decimal(rest)


        i = 0
        curr_flag = -1

        for cl_list in query(cl_list_data, sort_by=[("flag",False),("begin",True),("artart",False),("artnr",False)]):

            if cl_list.flag == 200 and curr_flag != cl_list.flag:
                curr_flag = cl_list.flag
                output_list = Output_list()
                output_list_data.append(output_list)

                i = i + 1
                output_list.reihe = i
                output_list.flag = 100
                output_list.str = output_list.str + fill("-", 170)


                output_list = Output_list()
                output_list_data.append(output_list)

                i = i + 1
                output_list.reihe = i
                output_list.flag = 101

                if price_decimal == 0 and not foreign_flag:

                    if not long_digit or short_flag:
                        str = to_string("Sub Total", "x(24)") + to_string(t1_cash, " ->>>,>>>,>>9") + to_string(t1_room, "->>,>>>,>>>,>>>,>>9") + to_string(t1_cc, "->>,>>>,>>>,>>>,>>9") + to_string(t1_cl, "->>,>>>,>>>,>>>,>>9") + to_string(t1_revenue, "->>,>>>,>>>,>>>,>>9") + to_string(t1_compli, " ->>,>>>,>>9") + to_string(t1_mcoup, " ->>,>>>,>>9") + to_string(t1_gl, " ->>,>>>,>>9")
                    else:
                        str = to_string("Sub Total", "x(24)") + to_string(t1_cash, " ->>>>>>>>>>9") + to_string(t1_room, "->>>>>>>>>>>>>>>>>9") + to_string(t1_cc, "->>>>>>>>>>>>>>>>>9") + to_string(t1_cl, "->>>>>>>>>>>>>>>>>9") + to_string(t1_revenue, "->>>>>>>>>>>>>>>>>9") + to_string(t1_compli, " ->>>>>>>>>9") + to_string(t1_mcoup, " ->>>>>>>>>9") + to_string(t1_gl, " ->>>>>>>>>9")
                else:
                    str = to_string("Sub Total", "x(24)") + to_string(t1_cash, " ->>,>>>,>>9.99") + to_string(t1_room, " ->>,>>>,>>>,>>9.99") + to_string(t1_cc, " ->>,>>>,>>>,>>9.99") + to_string(t1_cl, " ->>,>>>,>>>,>>9.99") + to_string(t1_revenue, " ->>,>>>,>>>,>>9.99") + to_string(t1_compli, " ->>,>>>,>>9.99") + to_string(t1_mcoup, " ->>,>>>,>>9.99") + to_string(t1_gl, " ->>,>>>,>>9.99")
                output_list = Output_list()
                output_list_data.append(output_list)

                i = i + 1
                output_list.reihe = i
                output_list.flag = 102
                output_list.str = output_list.str + fill("-", 170)


                output_list = Output_list()
                output_list_data.append(output_list)

                i = i + 1
                output_list.reihe = i
                output_list.flag = 103


                output_list = Output_list()
                output_list_data.append(output_list)

                i = i + 1
                output_list.reihe = i
                output_list.flag = 103


                output_list = Output_list()
                output_list_data.append(output_list)

                i = i + 1
                output_list.reihe = i
                output_list.flag = 104
                output_list.str = output_list.str + fill("-", 170)


            output_list = Output_list()
            output_list_data.append(output_list)

            i = i + 1
            output_list.reihe = i
            output_list.flag = cl_list.flag
            output_list.artart = cl_list.artart

            if cl_list.begin and cl_list.dept == 0:
                str = to_string(cl_list.bezeich, "x(24)") + to_string(cl_list.cash, " ->>>,>>>,>>>") + to_string(cl_list.room, "->>,>>>,>>>,>>>,>>>") + to_string(cl_list.card, "->>,>>>,>>>,>>>,>>>") + to_string(cl_list.cl, "->>,>>>,>>>,>>>,>>>") + to_string(cl_list.revenue, "->>,>>>,>>>,>>>,>>>") + to_string(cl_list.compli, " ->>,>>>,>>>") + to_string(cl_list.mcoup, " ->>,>>>,>>>") + to_string(cl_list.gl, " ->>,>>>,>>>") + to_string(cl_list.artnr, " >>>>>>>>")

            elif cl_list.artart >= 0 and price_decimal == 0 and not foreign_flag:

                if not long_digit or short_flag:
                    str = to_string(cl_list.bezeich, "x(24)") + to_string(cl_list.cash, " ->>>,>>>,>>9") + to_string(cl_list.room, "->>,>>>,>>>,>>>,>>9") + to_string(cl_list.card, "->>,>>>,>>>,>>>,>>9") + to_string(cl_list.cl, "->>,>>>,>>>,>>>,>>9") + to_string(cl_list.revenue, "->>,>>>,>>>,>>>,>>9") + to_string(cl_list.compli, " ->>,>>>,>>9") + to_string(cl_list.mcoup, " ->>,>>>,>>9") + to_string(cl_list.gl, " ->>,>>>,>>9") + to_string(cl_list.artnr, " >>>>>>>>")
                else:
                    str = to_string(cl_list.bezeich, "x(24)") + to_string(cl_list.cash, " ->>>>>>>>>>9") + to_string(cl_list.room, "->>>>>>>>>>>>>>>>>9") + to_string(cl_list.card, "->>>>>>>>>>>>>>>>>9") + to_string(cl_list.cl, "->>>>>>>>>>>>>>>>>9") + to_string(cl_list.revenue, "->>>>>>>>>>>>>>>>>9") + to_string(cl_list.compli, " ->>>>>>>>>9") + to_string(cl_list.mcoup, " ->>>>>>>>>9") + to_string(cl_list.gl, " ->>>>>>>>>9") + to_string(cl_list.artnr, " >>>>>>>>")

            elif cl_list.artart >= 0:
                str = to_string(cl_list.bezeich, "x(24)") + to_string(cl_list.cash, " ->>,>>>,>>9.99") + to_string(cl_list.room, " ->>,>>>,>>>,>>9.99") + to_string(cl_list.card, " ->>,>>>,>>>,>>9.99") + to_string(cl_list.cl, " ->>,>>>,>>>,>>9.99") + to_string(cl_list.revenue, " ->>,>>>,>>>,>>9.99") + to_string(cl_list.compli, " ->>,>>>,>>9.99") + to_string(cl_list.mcoup, " ->>,>>>,>>9.99") + to_string(cl_list.gl, " ->>,>>>,>>9.99") + to_string(cl_list.artnr, " >>>>>>>>")

        cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.flag == 200), first=True)

        if not cl_list:
            output_list = Output_list()
            output_list_data.append(output_list)

            i = i + 1
            output_list.reihe = i
            output_list.flag = 100
            output_list.str = output_list.str + fill("-", 170)


            output_list = Output_list()
            output_list_data.append(output_list)

            i = i + 1
            output_list.reihe = i
            output_list.flag = 101

            if price_decimal == 0 and not foreign_flag:

                if not long_digit or short_flag:
                    str = to_string("Sub Total", "x(24)") + to_string(t1_cash, " ->>>,>>>,>>9") + to_string(t1_room, "->>,>>>,>>>,>>>,>>9") + to_string(t1_cc, "->>,>>>,>>>,>>>,>>9") + to_string(t1_cl, "->>,>>>,>>>,>>>,>>9") + to_string(t1_revenue, "->>,>>>,>>>,>>>,>>9") + to_string(t1_compli, " ->>,>>>,>>9") + to_string(t1_mcoup, " ->>,>>>,>>9") + to_string(t1_gl, " ->>,>>>,>>9")
                else:
                    str = to_string("Sub Total", "x(24)") + to_string(t1_cash, " ->>>>>>>>>>9") + to_string(t1_room, "->>>>>>>>>>>>>>>>>9") + to_string(t1_cc, "->>>>>>>>>>>>>>>>>9") + to_string(t1_cl, "->>>>>>>>>>>>>>>>>9") + to_string(t1_revenue, "->>>>>>>>>>>>>>>>>9") + to_string(t1_compli, " ->>>>>>>>>9") + to_string(t1_mcoup, " ->>>>>>>>>9") + to_string(t1_gl, " ->>>>>>>>>9")
            else:
                str = to_string("Sub Total", "x(24)") + to_string(t1_cash, " ->>,>>>,>>9.99") + to_string(t1_room, " ->>,>>>,>>>,>>9.99") + to_string(t1_cc, " ->>,>>>,>>>,>>9.99") + to_string(t1_cl, " ->>,>>>,>>>,>>9.99") + to_string(t1_revenue, " ->>,>>>,>>>,>>9.99") + to_string(t1_compli, " ->>,>>>,>>9.99") + to_string(t1_mcoup, " ->>,>>>,>>9.99") + to_string(t1_gl, " ->>,>>>,>>9.99")
            output_list = Output_list()
            output_list_data.append(output_list)

            i = i + 1
            output_list.reihe = i
            output_list.flag = 102
            output_list.str = output_list.str + fill("-", 170)


            output_list = Output_list()
            output_list_data.append(output_list)

            i = i + 1
            output_list.reihe = i
            output_list.flag = 103


            output_list = Output_list()
            output_list_data.append(output_list)

            i = i + 1
            output_list.reihe = i
            output_list.flag = 103


        output_list = Output_list()
        output_list_data.append(output_list)

        i = i + 1
        output_list.reihe = i
        output_list.flag = 201
        output_list.str = output_list.str + fill("-", 170)


        output_list = Output_list()
        output_list_data.append(output_list)

        i = i + 1
        output_list.reihe = i
        output_list.flag = 202

        if price_decimal == 0 and not foreign_flag:

            if not long_digit or short_flag:
                str = to_string("Sub Total", "x(24)") + to_string(t2_cash, " ->>>,>>>,>>9") + to_string(t2_room, "->>,>>>,>>>,>>>,>>9") + to_string(t2_cc, "->>,>>>,>>>,>>>,>>9") + to_string(t2_cl, "->>,>>>,>>>,>>>,>>9") + to_string(t2_revenue, "->>,>>>,>>>,>>>,>>9") + to_string(t2_compli, " ->>,>>>,>>9") + to_string(t2_mcoup, " ->>,>>>,>>9") + to_string(t2_gl, " ->>,>>>,>>9")
            else:
                str = to_string("Sub Total", "x(24)") + to_string(t2_cash, " ->>>>>>>>>>9") + to_string(t2_room, "->>>>>>>>>>>>>>>>>9") + to_string(t2_cc, "->>>>>>>>>>>>>>>>>9") + to_string(t2_cl, "->>>>>>>>>>>>>>>>>9") + to_string(t2_revenue, "->>>>>>>>>>>>>>>>>9") + to_string(t2_compli, " ->>>>>>>>>9") + to_string(t2_mcoup, " ->>>>>>>>>9") + to_string(t2_gl, " ->>>>>>>>>9")
        else:
            str = to_string("Sub Total", "x(24)") + to_string(t2_cash, " ->>,>>>,>>9.99") + to_string(t2_room, " ->>,>>>,>>>,>>9.99") + to_string(t2_cc, " ->>,>>>,>>>,>>9.99") + to_string(t2_cl, " ->>,>>>,>>>,>>9.99") + to_string(t2_revenue, " ->>,>>>,>>>,>>9.99") + to_string(t2_compli, " ->>,>>>,>>9.99") + to_string(t2_mcoup, " ->>,>>>,>>9.99") + to_string(t2_gl, " ->>,>>>,>>9.99")
        output_list = Output_list()
        output_list_data.append(output_list)

        i = i + 1
        output_list.reihe = i
        output_list.flag = 203
        output_list.str = output_list.str + fill("-", 170)


        output_list = Output_list()
        output_list_data.append(output_list)

        i = i + 1
        output_list.reihe = i
        output_list.flag = 204

        if price_decimal == 0 and not foreign_flag:

            if not long_digit or short_flag:
                str = to_string("T o t a l", "x(24)") + to_string(t_cash, " ->>>,>>>,>>9") + to_string(t_room, "->>,>>>,>>>,>>>,>>9") + to_string(t_cc, "->>,>>>,>>>,>>>,>>9") + to_string(t_cl, "->>,>>>,>>>,>>>,>>9") + to_string(0, "->>,>>>,>>>,>>>,>>>") + to_string(t_compli, " ->>,>>>,>>9") + to_string(t_mcoup, " ->>,>>>,>>9") + to_string(t_gl, " ->>,>>>,>>9")
            else:
                str = to_string("T o t a l", "x(24)") + to_string(t_cash, " ->>>>>>>>>>9") + to_string(t_room, "->>>>>>>>>>>>>>>>>9") + to_string(t_cc, "->>>>>>>>>>>>>>>>>9") + to_string(t_cl, "->>>>>>>>>>>>>>>>>9") + to_string(0, "->>>>>>>>>>>>>>>>>>") + to_string(t_compli, " ->>>>>>>>>9") + to_string(t_mcoup, " ->>>>>>>>>9") + to_string(t_gl, " ->>>>>>>>>9")
        else:
            str = to_string("T o t a l", "x(24)") + to_string(t_cash, " ->>,>>>,>>9.99") + to_string(t_room, " ->>,>>>,>>>,>>9.99") + to_string(t_cc, " ->>,>>>,>>>,>>9.99") + to_string(t_cl, " ->>,>>>,>>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>>,>>>") + to_string(t_compli, " ->>,>>>,>>9.99") + to_string(t_mcoup, " ->>,>>>,>>9.99") + to_string(t_gl, " ->>,>>>,>>9.99")
        output_list = Output_list()
        output_list_data.append(output_list)

        i = i + 1
        output_list.reihe = i
        output_list.flag = 205
        output_list.str = output_list.str + fill("-", 170)


        t_cash =  to_decimal("0")

        cash_list = query(cash_list_data, first=True)

        if cash_list:
            output_list = Output_list()
            output_list_data.append(output_list)

            i = i + 1
            output_list.reihe = i


            output_list = Output_list()
            output_list_data.append(output_list)

            i = i + 1
            output_list.reihe = i
            output_list.str = translateExtended ("cash Breakdown:", lvcarea, "")

            for cash_list in query(cash_list_data):
                output_list = Output_list()
                output_list_data.append(output_list)

                i = i + 1
                t_cash =  to_decimal(t_cash) + to_decimal(cash_list.betrag)
                output_list.reihe = i

                if price_decimal == 0 and not foreign_flag:
                    output_list.str = to_string(cash_list.bezeich, "x(24)") + to_string(cash_list.betrag, " ->>>,>>>,>>9")
                else:
                    output_list.str = to_string(cash_list.bezeich, "x(24)") + to_string(cash_list.betrag, " ->>,>>>,>>9.99")
            output_list = Output_list()
            output_list_data.append(output_list)

            i = i + 1
            output_list.reihe = i
            output_list.str = output_list.str + fill("-", 170)


            output_list = Output_list()
            output_list_data.append(output_list)

            i = i + 1
            output_list.reihe = i
            output_list.str = to_string(translateExtended ("Total cash", lvcarea, "") , "x(24)")

            if price_decimal == 0 and not foreign_flag:
                output_list.str = output_list.str + to_string(t_cash, " ->>>,>>>,>>9")
            else:
                output_list.str = output_list.str + to_string(t_cash, " ->>,>>>,>>9.99")


    def create_rlist():

        nonlocal msg_str, output_list_data, long_digit, curr_dept, price_decimal, curr_bez, foreign_curr, from_date, fact1, lvcarea, htparam, bill_line, artikel, bill, zwkum, billjournal, waehrung, exrate, hoteldpt, h_journal, h_bill_line, h_artikel
        nonlocal pvilanguage, to_date, short_flag, foreign_flag


        nonlocal output_list, cash_list, rechnr_list, art_list, cl_list
        nonlocal output_list_data, cash_list_data, rechnr_list_data, art_list_data, cl_list_data


        rechnr_list_data.clear()

        for h_journal in db_session.query(H_journal).filter(
                 (H_journal.departement == hoteldpt.num) & (H_journal.bill_datum == to_date)).order_by(H_journal._recid).all():

            rechnr_list = query(rechnr_list_data, filters=(lambda rechnr_list: rechnr_list.rechnr == h_journal.rechnr), first=True)

            if not rechnr_list:
                rechnr_list = Rechnr_list()
                rechnr_list_data.append(rechnr_list)

                rechnr_list.rechnr = h_journal.rechnr


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))


    create_umsatz()

    return generate_output()