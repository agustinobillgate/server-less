#using conversion tools version: 1.0.0.118

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Uebertrag, Bill_line, Bill, Res_line, Guest, Artikel

def correct_guest_ledgerbl(fdate:date, tdate:date):

    prepare_cache ([Htparam, Uebertrag, Bill_line, Bill, Res_line, Guest, Artikel])

    success_flag = False
    billdate:date = None
    heute:date = None
    ank_flag:bool = False
    sorttype:int = 1
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
    long_digit:bool = False
    fact1:int = 0
    short_flag:bool = False
    outstanding:Decimal = to_decimal("0.0")
    curr_date:date = None
    curr_time:int = 0
    htparam = uebertrag = bill_line = bill = res_line = guest = artikel = None

    output_list = m_list = sum_list = s_list = ns_list = bill_alert = bill_list = None

    output_list_data, Output_list = create_model("Output_list", {"flag":int, "artart":int, "str":string, "ankunft":date, "ankzeit":string})
    m_list_data, M_list = create_model("M_list", {"resnr":int, "zinr":string, "abreise":date})
    sum_list_data, Sum_list = create_model("Sum_list", {"bezeich":string, "debit":Decimal, "credit":Decimal, "balance":Decimal})
    s_list_data, S_list = create_model("S_list", {"i_counter":int, "flag":int, "artnr":int, "dept":int, "gname":string, "zinr":string, "abreise":date, "bill_datum":date, "rechnr":int, "billtyp":string, "billnr":int, "bezeich":string, "prevbal":Decimal, "debit":Decimal, "credit":Decimal, "balance":Decimal, "ankunft":date, "ankzeit":string}, {"abreise": None, "ankunft": None, "ankzeit": ""})
    ns_list_data, Ns_list = create_model("Ns_list", {"rechnr":int, "saldo":Decimal, "prevbal":Decimal})
    bill_alert_data, Bill_alert = create_model("Bill_alert", {"rechnr":int})
    bill_list_data, Bill_list = create_model("Bill_list", {"rechnr":int, "billnr":int, "resnr":int, "reslinnr":int, "ankzeit":int, "ankunft":date, "abreise":date, "first_date":date, "last_date":date, "zinr":string, "gname":string, "billtype":string, "betrag":Decimal}, {"first_date": None, "last_date": None})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, billdate, heute, ank_flag, sorttype, prevbal, debit, credit, balance, current_counter, t_prevbal, t_debit, t_credit, t_balance, tot_bline, curr_rechnr, curr_flag, long_digit, fact1, short_flag, outstanding, curr_date, curr_time, htparam, uebertrag, bill_line, bill, res_line, guest, artikel
        nonlocal fdate, tdate


        nonlocal output_list, m_list, sum_list, s_list, ns_list, bill_alert, bill_list
        nonlocal output_list_data, m_list_data, sum_list_data, s_list_data, ns_list_data, bill_alert_data, bill_list_data

        return {"success_flag": success_flag}

    def create_bill_list():

        nonlocal success_flag, billdate, heute, ank_flag, sorttype, prevbal, debit, credit, balance, current_counter, t_prevbal, t_debit, t_credit, t_balance, tot_bline, curr_rechnr, curr_flag, long_digit, fact1, short_flag, outstanding, curr_date, curr_time, htparam, uebertrag, bill_line, bill, res_line, guest, artikel
        nonlocal fdate, tdate


        nonlocal output_list, m_list, sum_list, s_list, ns_list, bill_alert, bill_list
        nonlocal output_list_data, m_list_data, sum_list_data, s_list_data, ns_list_data, bill_alert_data, bill_list_data

        bline = None
        rbilldate:date = None
        first_date:date = None
        last_date:date = None
        Bline =  create_buffer("Bline",Bill_line)
        bill_list_data.clear()
        rbilldate = billdate - timedelta(days=30)

        for bill in db_session.query(Bill).filter(
                 (Bill.rechnr > 0) & ((Bill.flag == 0) | ((Bill.datum >= rbilldate) & (Bill.flag == 1)))).order_by(Bill.rechnr).all():
            last_date = None
            first_date = None

            if bill.flag == 0:
                last_date = heute

            if bill.flag == 1:

                bill_alert = query(bill_alert_data, filters=(lambda bill_alert: bill_alert.rechnr == bill.rechnr), first=True)

                if bill_alert:
                    last_date = heute

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == bill.rechnr)).order_by(Bill_line.bill_datum).all():
                first_date = bill_line.bill_datum
                break

            if first_date == None:
                continue

            elif first_date > billdate:
                continue

            elif last_date < billdate:
                continue
            bill_list = Bill_list()
            bill_list_data.append(bill_list)

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

            if bill_list.gname == "":

                guest = get_cache (Guest, {"gastnr": [(eq, bill.gastnr)]})

                if guest:
                    bill_list.gname = guest.name


    def create_umsatz():

        nonlocal success_flag, billdate, heute, ank_flag, sorttype, prevbal, debit, credit, balance, current_counter, t_prevbal, t_debit, t_credit, t_balance, tot_bline, curr_rechnr, curr_flag, long_digit, fact1, short_flag, outstanding, curr_date, curr_time, htparam, uebertrag, bill_line, bill, res_line, guest, artikel
        nonlocal fdate, tdate


        nonlocal output_list, m_list, sum_list, s_list, ns_list, bill_alert, bill_list
        nonlocal output_list_data, m_list_data, sum_list_data, s_list_data, ns_list_data, bill_alert_data, bill_list_data

        s:Decimal = to_decimal("0.0")
        ns_list_data.clear()
        s_list_data.clear()
        sum_list_data.clear()
        m_list_data.clear()
        output_list_data.clear()

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
        outstanding =  to_decimal(t_prevbal) + to_decimal(t_debit) - to_decimal(t_credit)


    def create_data2():

        nonlocal success_flag, billdate, heute, ank_flag, sorttype, prevbal, debit, credit, balance, current_counter, t_prevbal, t_debit, t_credit, t_balance, tot_bline, curr_rechnr, curr_flag, long_digit, fact1, short_flag, outstanding, curr_date, curr_time, htparam, uebertrag, bill_line, bill, res_line, guest, artikel
        nonlocal fdate, tdate


        nonlocal output_list, m_list, sum_list, s_list, ns_list, bill_alert, bill_list
        nonlocal output_list_data, m_list_data, sum_list_data, s_list_data, ns_list_data, bill_alert_data, bill_list_data


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


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    curr_date = htparam.fdate

    if not long_digit or not short_flag:
        fact1 = 1
    else:
        fact1 = 1000
    curr_time = get_current_time_in_seconds()


    for billdate in date_range(fdate,tdate) :
        tot_bline = 0
        current_counter = 0
        t_prevbal =  to_decimal("0")
        t_debit =  to_decimal("0")
        t_credit =  to_decimal("0")
        t_balance =  to_decimal("0")
        outstanding =  to_decimal("0")
        heute = billdate


        create_bill_list()
        create_umsatz()

        if outstanding != 0:

            if billdate < curr_date:

                uebertrag = get_cache (Uebertrag, {"datum": [(eq, billdate)]})

                if uebertrag:
                    pass
                    uebertrag.betrag =  to_decimal(outstanding)


                    pass
                    pass
                else:
                    uebertrag = Uebertrag()
                    db_session.add(uebertrag)

                    uebertrag.datum = billdate
                    uebertrag.betrag =  to_decimal(outstanding)


        success_flag = True

    return generate_output()