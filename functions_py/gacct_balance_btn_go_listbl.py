#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 29/7/2025
# msg-str tidak ada, sblm update dari Fitria
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bill, Res_line, Guest, Bill_line, Artikel, Uebertrag

bill_alert_data, Bill_alert = create_model("Bill_alert", {"rechnr":int})

def gacct_balance_btn_go_listbl(pvilanguage:int, bill_alert_data:[Bill_alert], heute:date, billdate:date, ank_flag:bool, sorttype:int, fact1:int, price_decimal:int, short_flag:bool):

    prepare_cache ([Res_line, Guest, Bill_line, Artikel, Uebertrag])

    msg_str = ""
    msg_str2 = ""
    gacct_balance_list_data = []
    i:int = 0
    prevbal:Decimal = to_decimal("0.0")
    debit:Decimal = to_decimal("0.0")
    credit:Decimal = to_decimal("0.0")
    balance:Decimal = to_decimal("0.0")
    current_counter:int = 0
    t_prevbal:Decimal = to_decimal("0.0")
    t_debit:Decimal = to_decimal("0.0")
    t_credit:Decimal = to_decimal("0.0")
    t_balance:Decimal = to_decimal("0.0")
    tot_bline:int = 0
    curr_rechnr:int = 0
    curr_flag:int = 0
    jl:int = 0
    lvcarea:string = "gacct-balance"
    bill = res_line = guest = bill_line = artikel = uebertrag = None

    output_list = m_list = sum_list = gacct_balance_list = s_list = ns_list = bill_alert = bill_list = None

    output_list_data, Output_list = create_model("Output_list", {"flag":int, "artart":int, "str":string, "ankunft":date, "ankzeit":string})
    m_list_data, M_list = create_model("M_list", {"resnr":int, "zinr":string, "abreise":date})
    sum_list_data, Sum_list = create_model("Sum_list", {"bezeich":string, "debit":Decimal, "credit":Decimal, "balance":Decimal})
    gacct_balance_list_data, Gacct_balance_list = create_model("Gacct_balance_list", {"i_counter":int, "flag":int, "artnr":int, "dept":int, "ankunft":date, "ankzeit":string, "typebill":string, "billdatum":date, "guest":string, "roomno":string, "billno":int, "billnr":int, "bezeich":string, "prevbala":Decimal, "debit":Decimal, "credit":Decimal, "balance":Decimal, "depart":date})
    s_list_data, S_list = create_model("S_list", {"i_counter":int, "flag":int, "artnr":int, "dept":int, "gname":string, "zinr":string, "abreise":date, "bill_datum":date, "rechnr":int, "billtyp":string, "billnr":int, "bezeich":string, "prevbal":Decimal, "debit":Decimal, "credit":Decimal, "balance":Decimal, "ankunft":date, "ankzeit":string}, {"abreise": None, "ankunft": None, "ankzeit": ""})
    ns_list_data, Ns_list = create_model("Ns_list", {"rechnr":int, "saldo":Decimal, "prevbal":Decimal})
    bill_list_data, Bill_list = create_model("Bill_list", {"rechnr":int, "billnr":int, "resnr":int, "reslinnr":int, "ankzeit":int, "ankunft":date, "abreise":date, "first_date":date, "last_date":date, "zinr":string, "gname":string, "billtype":string, "betrag":Decimal}, {"first_date": None, "last_date": None})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_str2, gacct_balance_list_data, i, prevbal, debit, credit, balance, current_counter, t_prevbal, t_debit, t_credit, t_balance, tot_bline, curr_rechnr, curr_flag, jl, lvcarea, bill, res_line, guest, bill_line, artikel, uebertrag
        nonlocal pvilanguage, heute, billdate, ank_flag, sorttype, fact1, price_decimal, short_flag


        nonlocal output_list, m_list, sum_list, gacct_balance_list, s_list, ns_list, bill_alert, bill_list
        nonlocal output_list_data, m_list_data, sum_list_data, gacct_balance_list_data, s_list_data, ns_list_data, bill_list_data

        return {"msg_str": msg_str, "msg_str2": msg_str2, "gacct-balance-list": gacct_balance_list_data}

    def create_bill_list():

        nonlocal msg_str, msg_str2, gacct_balance_list_data, i, prevbal, debit, credit, balance, current_counter, t_prevbal, t_debit, t_credit, t_balance, tot_bline, curr_rechnr, curr_flag, jl, lvcarea, bill, res_line, guest, bill_line, artikel, uebertrag
        nonlocal pvilanguage, heute, billdate, ank_flag, sorttype, fact1, price_decimal, short_flag


        nonlocal output_list, m_list, sum_list, gacct_balance_list, s_list, ns_list, bill_alert, bill_list
        nonlocal output_list_data, m_list_data, sum_list_data, gacct_balance_list_data, s_list_data, ns_list_data, bill_list_data


        bill_list_data.clear()

        # Rd 29/7/2025
        # optimize 
        print("Billdate:", billdate)
        bills = db_session.query(Bill).filter(
            (Bill.rechnr > 0) & (Bill.datum == billdate)
        ).all()
        for bill in bills:
            bill_list = Bill_list()
            bill_list_data.append(bill_list)
            print("Rechnr:", bill.rechnr, bill.datum)
            
            bill_list.resnr = bill.resnr
            bill_list.zinr = bill.zinr
            bill_list.rechnr = bill.rechnr
            bill_list.billnr = bill.billnr

            if bill.resnr > 0 and bill.reslinnr > 0:

                res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})
                bill_list.billtype = "G"

                if res_line:
                    bill_list.resnr = res_line.resnr
                    bill_list.reslinnr = res_line.reslinnr
                    bill_list.ankunft = res_line.ankunft
                    bill_list.abreise = res_line.abreise
                    bill_list.ankzeit = res_line.ankzeit
                    bill_list.zinr = res_line.zinr
                    bill_list.gname = res_line.name

            elif bill.resnr > 0:
                bill_list.billtype = "M"


            else:
                bill_list.billtype = "N"

            if bill.flag == 0:
                bill_list.last_date = heute

            if bill_list.gname == "":

                guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

                if guest:
                    bill_list.gname = guest.name

            if bill.flag == 1:

                bill_alert = query(bill_alert_data, filters=(lambda bill_alert: bill_alert.rechnr == bill.rechnr), first=True)

                if bill_alert:
                    bill_list.last_date = heute

            bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill_list.rechnr)]})

            if bill_line:
                bill_list.first_date = bill_line.bill_datum
                bill_list.betrag =  to_decimal(bill_line.betrag)

                if bill.flag == 1 and bill_list.last_date == None:

                    bill_line = db_session.query(Bill_line).filter(
                             (Bill_line.rechnr == bill_list.rechnr)).order_by(Bill_line._recid.desc()).first()

                    if bill_line:
                        bill_list.last_date = bill_line.bill_datum

            if bill_list.first_date == None:
                bill_list_data.remove(bill_list)

            elif bill_list.first_date > billdate:
                bill_list_data.remove(bill_list)

            elif bill_list.last_date < billdate:
                bill_list_data.remove(bill_list)

            curr_recid = bill._recid
            # bill = db_session.query(Bill).filter(
            #          (Bill.rechnr > 0) & (Bill._recid > curr_recid)).first()


    def create_data2():

        nonlocal msg_str, msg_str2, gacct_balance_list_data, i, prevbal, debit, credit, balance, current_counter, t_prevbal, t_debit, t_credit, t_balance, tot_bline, curr_rechnr, curr_flag, jl, lvcarea, bill, res_line, guest, bill_line, artikel, uebertrag
        nonlocal pvilanguage, heute, billdate, ank_flag, sorttype, fact1, price_decimal, short_flag


        nonlocal output_list, m_list, sum_list, gacct_balance_list, s_list, ns_list, bill_alert, bill_list
        nonlocal output_list_data, m_list_data, sum_list_data, gacct_balance_list_data, s_list_data, ns_list_data, bill_list_data


        prevbal =  to_decimal("0")
        debit =  to_decimal("0")
        credit =  to_decimal("0")
        balance =  to_decimal("0")

        for bill_line in db_session.query(Bill_line).filter(
                 (Bill_line.rechnr == bill_list.rechnr) & (Bill_line.bill_datum <= billdate)).order_by(Bill_line.bezeich, Bill_line.bill_datum, Bill_line.zeit).all():
            tot_bline = tot_bline + 1

            s_list = query(s_list_data, filters=(lambda s_list: s_list.artnr == bill_line.artnr and s_list.dept == bill_line.departement and s_list.rechnr == bill_line.rechnr), first=True)

            if not s_list:

                artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

                if not artikel and num_entries(bill_line.bezeich, "*") > 1:

                    artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, 0)]})

                if not artikel:
                    pass
                s_list = S_list()
                s_list_data.append(s_list)

                current_counter = current_counter + 1
                s_list.i_counter = current_counter
                s_list.gname = bill_list.gname
                s_list.flag = 0
                s_list.artnr = bill_line.artnr
                s_list.dept = bill_line.departement
                s_list.zinr = bill_list.zinr
                s_list.abreise = bill_list.abreise
                s_list.bill_datum = bill_line.bill_datum
                s_list.rechnr = bill_list.rechnr
                s_list.billtyp = " "
                s_list.prevbal =  to_decimal("0")
                s_list.balance =  to_decimal("0")
                s_list.billnr = bill_list.billnr
                s_list.ankunft = bill_list.ankunft
                s_list.ankzeit = to_string(bill_list.ankzeit, "HH:MM:SS")

                if artikel:
                    s_list.bezeich = artikel.bezeich
                else:
                    s_list.bezeich = bill_line.bezeich

            if bill_line.bill_datum < billdate:
                s_list.prevbal =  to_decimal(s_list.prevbal) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                prevbal =  to_decimal(prevbal) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                t_prevbal =  to_decimal(t_prevbal) + to_decimal(bill_line.betrag) / to_decimal(fact1)
            else:

                if bill_line.betrag > 0:
                    s_list.debit =  to_decimal(s_list.debit) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                    debit =  to_decimal(debit) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                    t_debit =  to_decimal(t_debit) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                else:
                    s_list.credit =  to_decimal(s_list.credit) - to_decimal(bill_line.betrag) / to_decimal(fact1)
                    credit =  to_decimal(credit) - to_decimal(bill_line.betrag) / to_decimal(fact1)
                    t_credit =  to_decimal(t_credit) - to_decimal(bill_line.betrag) / to_decimal(fact1)
            balance =  to_decimal(balance) + to_decimal(bill_line.betrag) / to_decimal(fact1)
            t_balance =  to_decimal(t_balance) + to_decimal(bill_line.betrag) / to_decimal(fact1)
            s_list.balance =  to_decimal(balance)


    def create_umsatz():

        nonlocal msg_str, msg_str2, gacct_balance_list_data, i, prevbal, debit, credit, balance, current_counter, t_prevbal, t_debit, t_credit, t_balance, tot_bline, curr_rechnr, curr_flag, jl, lvcarea, bill, res_line, guest, bill_line, artikel, uebertrag
        nonlocal pvilanguage, heute, billdate, ank_flag, sorttype, fact1, price_decimal, short_flag


        nonlocal output_list, m_list, sum_list, gacct_balance_list, s_list, ns_list, bill_alert, bill_list
        nonlocal output_list_data, m_list_data, sum_list_data, gacct_balance_list_data, s_list_data, ns_list_data, bill_list_data

        s:Decimal = to_decimal("0.0")
        ns_list_data.clear()
        s_list_data.clear()
        sum_list_data.clear()
        m_list_data.clear()
        output_list_data.clear()

        for gacct_balance_list in query(gacct_balance_list_data):
            gacct_balance_list_data.remove(gacct_balance_list)

        if ank_flag:

            if sorttype == 1:

                for bill_list in query(bill_list_data, filters=(lambda bill_list: bill_list.billtype.lower()  == ("G").lower()), sort_by=[("ankunft",False),("ankzeit",False),("gname",False),("zinr",False),("billnr",False)]):
                    create_data2()

            else:

                for bill_list in query(bill_list_data, filters=(lambda bill_list: bill_list.billtype.lower()  == ("G").lower()), sort_by=[("ankunft",False),("ankzeit",False),("zinr",False),("gname",False),("billnr",False)]):
                    create_data2()


        elif not ank_flag:

            if sorttype == 1:

                for bill_list in query(bill_list_data, filters=(lambda bill_list: bill_list.billtype.lower()  == ("G").lower()), sort_by=[("gname",False),("zinr",False),("billnr",False)]):
                    create_data2()

            else:

                for bill_list in query(bill_list_data, filters=(lambda bill_list: bill_list.billtype.lower()  == ("G").lower()), sort_by=[("zinr",False),("gname",False),("billnr",False)]):
                    create_data2()


        for bill_list in query(bill_list_data, filters=(lambda bill_list: bill_list.billtype.lower()  == ("M").lower()), sort_by=[("rechnr",False)]):

            res_line = get_cache (Res_line, {"resnr": [(eq, bill_list.resnr)],"zinr": [(ne, "")],"resstatus": [(ne, 12)]})
            m_list = M_list()
            m_list_data.append(m_list)

            m_list.resnr = bill_list.resnr

            if res_line:
                m_list.zinr = res_line.zinr
                m_list.abreise = res_line.abreise


            prevbal =  to_decimal("0")
            debit =  to_decimal("0")
            credit =  to_decimal("0")
            balance =  to_decimal("0")

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill_list.rechnr) & (Bill_line.bill_datum <= billdate)).order_by(Bill_line.bezeich).all():

                s_list = query(s_list_data, filters=(lambda s_list: s_list.artnr == bill_line.artnr and s_list.dept == bill_line.departement and s_list.rechnr == bill_line.rechnr), first=True)

                if not s_list:

                    artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

                    if not artikel and num_entries(bill_line.bezeich, "*") > 1:

                        artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, 0)]})

                    if not artikel:
                        pass
                    s_list = S_list()
                    s_list_data.append(s_list)

                    current_counter = current_counter + 1
                    s_list.i_counter = current_counter
                    s_list.gname = bill_list.gname
                    s_list.flag = 1
                    s_list.artnr = bill_line.artnr
                    s_list.dept = bill_line.departement
                    s_list.abreise = m_list.abreise
                    s_list.bill_datum = bill_line.bill_datum
                    s_list.zinr = m_list.zinr
                    s_list.rechnr = bill_list.rechnr
                    s_list.billtyp = "M"
                    s_list.billnr = 1
                    s_list.prevbal =  to_decimal("0")
                    s_list.balance =  to_decimal(balance)

                    if artikel:
                        s_list.bezeich = artikel.bezeich
                    else:
                        s_list.bezeich = bill_line.bezeich

                if bill_line.bill_datum < billdate:
                    s_list.prevbal =  to_decimal(s_list.prevbal) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                    prevbal =  to_decimal(prevbal) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                    s_list.balance =  to_decimal(s_list.balance) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                    t_prevbal =  to_decimal(t_prevbal) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                else:

                    if bill_line.betrag > 0:
                        s_list.debit =  to_decimal(s_list.debit) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                        debit =  to_decimal(debit) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                        t_debit =  to_decimal(t_debit) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                    else:
                        s_list.credit =  to_decimal(s_list.credit) - to_decimal(bill_line.betrag) / to_decimal(fact1)
                        credit =  to_decimal(credit) - to_decimal(bill_line.betrag) / to_decimal(fact1)
                        t_credit =  to_decimal(t_credit) - to_decimal(bill_line.betrag) / to_decimal(fact1)
                    s_list.balance =  to_decimal(s_list.balance) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                balance =  to_decimal(balance) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                t_balance =  to_decimal(t_balance) + to_decimal(bill_line.betrag) / to_decimal(fact1)

        for bill_list in query(bill_list_data, filters=(lambda bill_list: bill_list.billtype.lower()  == ("N").lower()), sort_by=[("gname",False)]):
            prevbal =  to_decimal("0")
            debit =  to_decimal("0")
            credit =  to_decimal("0")
            balance =  to_decimal("0")

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill_list.rechnr) & (Bill_line.bill_datum <= billdate)).order_by(Bill_line.bill_datum, Bill_line.artnr, Bill_line.departement).all():
                tot_bline = tot_bline + 1

                artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, bill_line.departement)]})

                if not artikel:

                    artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)],"departement": [(eq, 0)]})

                s_list = query(s_list_data, filters=(lambda s_list: s_list.artnr == artikel.artnr and s_list.dept == artikel.departement and s_list.rechnr == bill_line.rechnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    current_counter = current_counter + 1
                    s_list.i_counter = current_counter
                    s_list.gname = bill_list.gname
                    s_list.flag = 2
                    s_list.artnr = bill_line.artnr
                    s_list.dept = bill_line.departement
                    s_list.rechnr = bill_list.rechnr
                    s_list.billtyp = "NS"
                    s_list.billnr = bill_list.billnr
                    s_list.prevbal =  to_decimal("0")
                    s_list.balance =  to_decimal("0")
                    s_list.bill_datum = bill_line.bill_datum

                    if artikel:
                        s_list.bezeich = artikel.bezeich
                    else:
                        s_list.bezeich = "[!] " + bill_line.bezeich

                if bill_line.bill_datum < billdate:
                    s_list.prevbal =  to_decimal(s_list.prevbal) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                    prevbal =  to_decimal(prevbal) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                    t_prevbal =  to_decimal(t_prevbal) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                    s_list.balance =  to_decimal(s_list.balance) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                else:

                    if bill_line.betrag > 0:
                        s_list.debit =  to_decimal(s_list.debit) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                        debit =  to_decimal(debit) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                        t_debit =  to_decimal(t_debit) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                    else:
                        s_list.credit =  to_decimal(s_list.credit) - to_decimal(bill_line.betrag) / to_decimal(fact1)
                        credit =  to_decimal(credit) - to_decimal(bill_line.betrag) / to_decimal(fact1)
                        t_credit =  to_decimal(t_credit) - to_decimal(bill_line.betrag) / to_decimal(fact1)
                    s_list.balance =  to_decimal(s_list.balance) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                balance =  to_decimal(balance) + to_decimal(bill_line.betrag) / to_decimal(fact1)
                t_balance =  to_decimal(t_balance) + to_decimal(bill_line.betrag) / to_decimal(fact1)
        curr_rechnr = 0
        curr_flag = 0
        balance =  to_decimal("0")

        for s_list in query(s_list_data, sort_by=[("i_counter",False)]):

            if s_list.debit != 0 or s_list.credit != 0:

                sum_list = query(sum_list_data, filters=(lambda sum_list: sum_list.bezeich == s_list.bezeich), first=True)

                if not sum_list:
                    sum_list = Sum_list()
                    sum_list_data.append(sum_list)

                    sum_list.bezeich = s_list.bezeich
                sum_list.debit =  to_decimal(sum_list.debit) + to_decimal(s_list.debit)
                sum_list.credit =  to_decimal(sum_list.credit) + to_decimal(s_list.credit)
                sum_list.balance =  to_decimal(sum_list.balance) + to_decimal(s_list.debit) - to_decimal(s_list.credit)

            if curr_rechnr != s_list.rechnr:
                balance =  to_decimal(s_list.prevbal) + to_decimal(s_list.debit) - to_decimal(s_list.credit)
                s_list.balance =  to_decimal(balance)

                if curr_rechnr != 0:
                    gacct_balance_list = Gacct_balance_list()
                    gacct_balance_list_data.append(gacct_balance_list)

                gacct_balance_list = Gacct_balance_list()
                gacct_balance_list_data.append(gacct_balance_list)

                gacct_balance_list.ankunft = s_list.ankunft
                gacct_balance_list.ankzeit = s_list.ankzeit
                gacct_balance_list.depart = s_list.abreise
                gacct_balance_list.typebill = s_list.billtyp
                gacct_balance_list.guest = s_list.gname
                gacct_balance_list.roomno = s_list.zinr
                gacct_balance_list.billno = s_list.rechnr

                if price_decimal == 0:

                    if short_flag:
                        gacct_balance_list.bezeich = s_list.bezeich
                        gacct_balance_list.prevbala =  to_decimal(s_list.prevbal)
                        gacct_balance_list.debit =  to_decimal(s_list.debit)
                        gacct_balance_list.credit =  to_decimal(s_list.credit)
                        gacct_balance_list.balance =  to_decimal(s_list.balance)


                    else:
                        gacct_balance_list.bezeich = s_list.bezeich
                        gacct_balance_list.prevbala =  to_decimal(s_list.prevbal)
                        gacct_balance_list.debit =  to_decimal(s_list.debit)
                        gacct_balance_list.credit =  to_decimal(s_list.credit)
                        gacct_balance_list.balance =  to_decimal(s_list.balance)


                else:
                    gacct_balance_list.bezeich = s_list.bezeich
                    gacct_balance_list.prevbala =  to_decimal(s_list.prevbal)
                    gacct_balance_list.debit =  to_decimal(s_list.debit)
                    gacct_balance_list.credit =  to_decimal(s_list.credit)
                    gacct_balance_list.balance =  to_decimal(s_list.balance)


                curr_rechnr = gacct_balance_list.billno
            else:
                balance =  to_decimal(balance) + to_decimal(s_list.prevbal) + to_decimal(s_list.debit) - to_decimal(s_list.credit)
                s_list.balance =  to_decimal(balance)


                gacct_balance_list = Gacct_balance_list()
                gacct_balance_list_data.append(gacct_balance_list)

                gacct_balance_list.ankunft = s_list.ankunft
                gacct_balance_list.ankzeit = s_list.ankzeit

                if price_decimal == 0:

                    if short_flag:
                        gacct_balance_list.bezeich = s_list.bezeich
                        gacct_balance_list.prevbala =  to_decimal(s_list.prevbal)
                        gacct_balance_list.debit =  to_decimal(s_list.debit)
                        gacct_balance_list.credit =  to_decimal(s_list.credit)
                        gacct_balance_list.balance =  to_decimal(s_list.balance)


                    else:
                        gacct_balance_list.bezeich = s_list.bezeich
                        gacct_balance_list.prevbala =  to_decimal(s_list.prevbal)
                        gacct_balance_list.debit =  to_decimal(s_list.debit)
                        gacct_balance_list.credit =  to_decimal(s_list.credit)
                        gacct_balance_list.balance =  to_decimal(s_list.balance)


                else:
                    gacct_balance_list.bezeich = s_list.bezeich
                    gacct_balance_list.prevbala =  to_decimal(s_list.prevbal)
                    gacct_balance_list.debit =  to_decimal(s_list.debit)
                    gacct_balance_list.credit =  to_decimal(s_list.credit)
                    gacct_balance_list.balance =  to_decimal(s_list.balance)


        gacct_balance_list = Gacct_balance_list()
        gacct_balance_list_data.append(gacct_balance_list)


        if price_decimal == 0:

            if short_flag:
                gacct_balance_list.bezeich = "T O T A L"
                gacct_balance_list.prevbala =  to_decimal(t_prevbal)
                gacct_balance_list.debit =  to_decimal(t_debit)
                gacct_balance_list.credit =  to_decimal(t_credit)
                gacct_balance_list.balance =  to_decimal(t_balance)


            else:
                gacct_balance_list.bezeich = "T O T A L"
                gacct_balance_list.prevbala =  to_decimal(t_prevbal)
                gacct_balance_list.debit =  to_decimal(t_debit)
                gacct_balance_list.credit =  to_decimal(t_credit)
                gacct_balance_list.balance =  to_decimal(t_balance)


        else:
            gacct_balance_list.bezeich = "T O T A L"
            gacct_balance_list.prevbala =  to_decimal(t_prevbal)
            gacct_balance_list.debit =  to_decimal(t_debit)
            gacct_balance_list.credit =  to_decimal(t_credit)
            gacct_balance_list.balance =  to_decimal(t_balance)


        gacct_balance_list = Gacct_balance_list()
        gacct_balance_list_data.append(gacct_balance_list)

        gacct_balance_list = Gacct_balance_list()
        gacct_balance_list_data.append(gacct_balance_list)


        uebertrag = get_cache (Uebertrag, {"datum": [(eq, billdate)]})

        if price_decimal == 0:
            gacct_balance_list.bezeich = "Outstanding"
            gacct_balance_list.balance =  to_decimal(t_prevbal) + to_decimal(t_debit) - to_decimal(t_credit)

            if uebertrag:
                gacct_balance_list = Gacct_balance_list()
                gacct_balance_list_data.append(gacct_balance_list)

                gacct_balance_list.bezeich = "Stored Guest Ledger Amount:"
                gacct_balance_list.balance =  to_decimal(uebertrag.betrag)


        else:
            gacct_balance_list.bezeich = "Outstanding"
            gacct_balance_list.balance =  to_decimal(t_prevbal) + to_decimal(t_debit) - to_decimal(t_credit)

            if uebertrag:
                gacct_balance_list = Gacct_balance_list()
                gacct_balance_list_data.append(gacct_balance_list)

                gacct_balance_list.bezeich = "Stored Guest Ledger Amount:"
                gacct_balance_list.balance =  to_decimal(uebertrag.betrag)


        gacct_balance_list = Gacct_balance_list()
        gacct_balance_list_data.append(gacct_balance_list)

        gacct_balance_list = Gacct_balance_list()
        gacct_balance_list_data.append(gacct_balance_list)

        gacct_balance_list.guest = "Summary of Transaction"
        t_debit =  to_decimal("0")
        t_credit =  to_decimal("0")
        t_balance =  to_decimal("0")

        for sum_list in query(sum_list_data, sort_by=[("bezeich",False)]):
            gacct_balance_list = Gacct_balance_list()
            gacct_balance_list_data.append(gacct_balance_list)

            gacct_balance_list.guest = sum_list.bezeich

            if price_decimal == 0:

                if short_flag:
                    gacct_balance_list.debit =  to_decimal(sum_list.debit)
                    gacct_balance_list.credit =  to_decimal(sum_list.credit)
                    gacct_balance_list.balance =  to_decimal(sum_list.balance)


                else:
                    gacct_balance_list.debit =  to_decimal(sum_list.debit)
                    gacct_balance_list.credit =  to_decimal(sum_list.credit)
                    gacct_balance_list.balance =  to_decimal(sum_list.balance)


            else:
                gacct_balance_list.debit =  to_decimal(sum_list.debit)
                gacct_balance_list.credit =  to_decimal(sum_list.credit)
                gacct_balance_list.balance =  to_decimal(sum_list.balance)


            t_debit =  to_decimal(t_debit) + to_decimal(sum_list.debit)
            t_credit =  to_decimal(t_credit) + to_decimal(sum_list.credit)
        t_balance =  to_decimal(t_debit) - to_decimal(t_credit)
        gacct_balance_list = Gacct_balance_list()
        gacct_balance_list_data.append(gacct_balance_list)

        gacct_balance_list.guest = "T o t a l"

        if price_decimal == 0:

            if short_flag:
                gacct_balance_list.debit =  to_decimal(t_debit)
                gacct_balance_list.credit =  to_decimal(t_credit)
                gacct_balance_list.balance =  to_decimal(t_balance)


            else:
                gacct_balance_list.debit =  to_decimal(t_debit)
                gacct_balance_list.credit =  to_decimal(t_credit)
                gacct_balance_list.balance =  to_decimal(t_balance)


        else:
            gacct_balance_list.debit =  to_decimal(t_debit)
            gacct_balance_list.credit =  to_decimal(t_credit)
            gacct_balance_list.balance =  to_decimal(t_balance)


    tot_bline = 0
    current_counter = 0
    t_prevbal =  to_decimal("0")
    t_debit =  to_decimal("0")
    t_credit =  to_decimal("0")
    t_balance =  to_decimal("0")


    create_bill_list()
    create_umsatz()

    return generate_output()