from functions.additional_functions import *
import decimal
from datetime import date
from models import Bill, Res_line, Guest, Bill_line, Artikel, Uebertrag

def gacct_balance_btn_go_listbl(pvilanguage:int, bill_alert:[Bill_alert], heute:date, billdate:date, ank_flag:bool, sorttype:int, fact1:int, price_decimal:int, short_flag:bool):
    msg_str = ""
    msg_str2 = ""
    gacct_balance_list_list = []
    i:int = 0
    prevbal:decimal = 0
    debit:decimal = 0
    credit:decimal = 0
    balance:decimal = 0
    current_counter:int = 0
    t_prevbal:decimal = 0
    t_debit:decimal = 0
    t_credit:decimal = 0
    t_balance:decimal = 0
    tot_bline:int = 0
    curr_rechnr:int = 0
    curr_flag:int = 0
    lvcarea:str = "gacct_balance"
    bill = res_line = guest = bill_line = artikel = uebertrag = None

    output_list = m_list = sum_list = gacct_balance_list = s_list = ns_list = bill_alert = bill_list = None

    output_list_list, Output_list = create_model("Output_list", {"flag":int, "artart":int, "str":str, "ankunft":date, "ankzeit":str})
    m_list_list, M_list = create_model("M_list", {"resnr":int, "zinr":str, "abreise":date})
    sum_list_list, Sum_list = create_model("Sum_list", {"bezeich":str, "debit":decimal, "credit":decimal, "balance":decimal})
    gacct_balance_list_list, Gacct_balance_list = create_model("Gacct_balance_list", {"i_counter":int, "flag":int, "artnr":int, "dept":int, "ankunft":date, "ankzeit":str, "typebill":str, "billdatum":date, "guest":str, "roomno":str, "billno":int, "billnr":int, "bezeich":str, "prevbala":decimal, "debit":decimal, "credit":decimal, "balance":decimal, "depart":date})
    s_list_list, S_list = create_model("S_list", {"i_counter":int, "flag":int, "artnr":int, "dept":int, "gname":str, "zinr":str, "abreise":date, "bill_datum":date, "rechnr":int, "billtyp":str, "billnr":int, "bezeich":str, "prevbal":decimal, "debit":decimal, "credit":decimal, "balance":decimal, "ankunft":date, "ankzeit":str}, {"abreise": None, "ankunft": None, "ankzeit": ""})
    ns_list_list, Ns_list = create_model("Ns_list", {"rechnr":int, "saldo":decimal, "prevbal":decimal})
    bill_alert_list, Bill_alert = create_model("Bill_alert", {"rechnr":int})
    bill_list_list, Bill_list = create_model("Bill_list", {"rechnr":int, "billnr":int, "resnr":int, "reslinnr":int, "ankzeit":int, "ankunft":date, "abreise":date, "first_date":date, "last_date":date, "zinr":str, "gname":str, "billtype":str, "betrag":decimal}, {"first_date": None, "last_date": None})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_str2, gacct_balance_list_list, i, prevbal, debit, credit, balance, current_counter, t_prevbal, t_debit, t_credit, t_balance, tot_bline, curr_rechnr, curr_flag, lvcarea, bill, res_line, guest, bill_line, artikel, uebertrag


        nonlocal output_list, m_list, sum_list, gacct_balance_list, s_list, ns_list, bill_alert, bill_list
        nonlocal output_list_list, m_list_list, sum_list_list, gacct_balance_list_list, s_list_list, ns_list_list, bill_alert_list, bill_list_list
        return {"msg_str": msg_str, "msg_str2": msg_str2, "gacct-balance-list": gacct_balance_list_list}

    def create_bill_list():

        nonlocal msg_str, msg_str2, gacct_balance_list_list, i, prevbal, debit, credit, balance, current_counter, t_prevbal, t_debit, t_credit, t_balance, tot_bline, curr_rechnr, curr_flag, lvcarea, bill, res_line, guest, bill_line, artikel, uebertrag


        nonlocal output_list, m_list, sum_list, gacct_balance_list, s_list, ns_list, bill_alert, bill_list
        nonlocal output_list_list, m_list_list, sum_list_list, gacct_balance_list_list, s_list_list, ns_list_list, bill_alert_list, bill_list_list


        bill_list_list.clear()

        for bill in db_session.query(Bill).filter(
                (Bill.rechnr > 0)).all():
            bill_list = Bill_list()
            bill_list_list.append(bill_list)

            bill_list.resnr = bill.resnr
            bill_list.zinr = bill.zinr
            bill_list.rechnr = bill.rechnr
            bill_list.billnr = billnr

            if bill.resnr > 0 and bill.reslinnr > 0:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()
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

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == bill.gastnr)).first()

                if guest:
                    bill_list.gname = guest.name

            if bill.flag == 1:

                bill_alert = query(bill_alert_list, filters=(lambda bill_alert :bill_alert.rechnr == bill.rechnr), first=True)

                if bill_alert:
                    bill_list.last_date = heute

            bill_line = db_session.query(Bill_line).filter(
                    (Bill_line.rechnr == bill_list.rechnr)).first()

            if bill_line:
                bill_list.first_date = bill_line.bill_datum
                bill_list.betrag = bill_line.betrag

                if bill.flag == 1 and bill_list.last_date == None:

                    bill_line = db_session.query(Bill_line).filter(
                            (Bill_line.rechnr == bill_list.rechnr)).first()

                    if bill_line:
                        bill_list.last_date = bill_line.bill_datum

        for bill_list in query(bill_list_list):

            if bill_list.first_date == None:
                bill_list_list.remove(bill_list)

            elif bill_list.first_date > billdate:
                bill_list_list.remove(bill_list)

            elif bill_list.last_date < billdate:
                bill_list_list.remove(bill_list)

    def create_data2():

        nonlocal msg_str, msg_str2, gacct_balance_list_list, i, prevbal, debit, credit, balance, current_counter, t_prevbal, t_debit, t_credit, t_balance, tot_bline, curr_rechnr, curr_flag, lvcarea, bill, res_line, guest, bill_line, artikel, uebertrag


        nonlocal output_list, m_list, sum_list, gacct_balance_list, s_list, ns_list, bill_alert, bill_list
        nonlocal output_list_list, m_list_list, sum_list_list, gacct_balance_list_list, s_list_list, ns_list_list, bill_alert_list, bill_list_list


        prevbal = 0
        debit = 0
        credit = 0
        balance = 0

        for bill_line in db_session.query(Bill_line).filter(
                (Bill_line.rechnr == bill_list.rechnr) &  (Bill_line.bill_datum <= billdate)).all():
            tot_bline = tot_bline + 1

            s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == bill_line.artnr and s_list.dept == bill_line.departement and s_list.rechnr == bill_line.rechnr), first=True)

            if not s_list:

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == bill_line.departement)).first()

                if not artikel and num_entries(bill_line.bezeich, "*") > 1:

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == 0)).first()

                if not artikel:
                s_list = S_list()
                s_list_list.append(s_list)

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
                s_list.billtyp = "  "
                s_list.prevbal = 0
                s_list.balance = 0
                s_list.billnr = bill_list.billnr
                s_list.ankunft = bill_list.ankunft
                s_list.ankzeit = to_string(bill_list.ankzeit, "HH:MM:SS")

                if artikel:
                    s_list.bezeich = artikel.bezeich
                else:
                    s_list.bezeich = bill_line.bezeich

            if bill_line.bill_datum < billdate:
                s_list.prevbal = s_list.prevbal + bill_line.betrag / fact1
                prevbal = prevbal + bill_line.betrag / fact1
                t_prevbal = t_prevbal + bill_line.betrag / fact1
            else:

                if bill_line.betrag > 0:
                    s_list.debit = s_list.debit + bill_line.betrag / fact1
                    debit = debit + bill_line.betrag / fact1
                    t_debit = t_debit + bill_line.betrag / fact1
                else:
                    s_list.credit = s_list.credit - bill_line.betrag / fact1
                    credit = credit - bill_line.betrag / fact1
                    t_credit = t_credit - bill_line.betrag / fact1
            balance = balance + bill_line.betrag / fact1
            t_balance = t_balance + bill_line.betrag / fact1
            s_list.balance = balance

    def create_umsatz():

        nonlocal msg_str, msg_str2, gacct_balance_list_list, i, prevbal, debit, credit, balance, current_counter, t_prevbal, t_debit, t_credit, t_balance, tot_bline, curr_rechnr, curr_flag, lvcarea, bill, res_line, guest, bill_line, artikel, uebertrag


        nonlocal output_list, m_list, sum_list, gacct_balance_list, s_list, ns_list, bill_alert, bill_list
        nonlocal output_list_list, m_list_list, sum_list_list, gacct_balance_list_list, s_list_list, ns_list_list, bill_alert_list, bill_list_list

        s:decimal = 0
        ns_list_list.clear()
        s_list_list.clear()
        sum_list_list.clear()
        m_list_list.clear()
        output_list_list.clear()

        for gacct_balance_list in query(gacct_balance_list_list):
            gacct_balance_list_list.remove(gacct_balance_list)

        if ank_flag:

            if sorttype == 1:

                for bill_list in query(bill_list_list, filters=(lambda bill_list :bill_list.billtype.lower()  == "G")):
                    create_data2()

            else:

                for bill_list in query(bill_list_list, filters=(lambda bill_list :bill_list.billtype.lower()  == "G")):
                    create_data2()


        elif not ank_flag:

            if sorttype == 1:

                for bill_list in query(bill_list_list, filters=(lambda bill_list :bill_list.billtype.lower()  == "G")):
                    create_data2()

            else:

                for bill_list in query(bill_list_list, filters=(lambda bill_list :bill_list.billtype.lower()  == "G")):
                    create_data2()


        for bill_list in query(bill_list_list, filters=(lambda bill_list :bill_list.billtype.lower()  == "M")):

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == bill_list.resnr) &  (Res_line.zinr != "") &  (Res_line.resstatus != 12)).first()
            m_list = M_list()
            m_list_list.append(m_list)

            m_list.resnr = bill_list.resnr

            if res_line:
                m_list.zinr = res_line.zinr
                m_list.abreise = res_line.abreise


            prevbal = 0
            debit = 0
            credit = 0
            balance = 0

            for bill_line in db_session.query(Bill_line).filter(
                    (Bill_line.rechnr == bill_list.rechnr) &  (Bill_line.bill_datum <= billdate)).all():

                s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == bill_line.artnr and s_list.dept == bill_line.departement and s_list.rechnr == bill_line.rechnr), first=True)

                if not s_list:

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == bill_line.departement)).first()

                    if not artikel and num_entries(bill_line.bezeich, "*") > 1:

                        artikel = db_session.query(Artikel).filter(
                                (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == 0)).first()

                    if not artikel:
                    s_list = S_list()
                    s_list_list.append(s_list)

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
                    s_list.prevbal = 0
                    s_list.balance = balance

                    if artikel:
                        s_list.bezeich = artikel.bezeich
                    else:
                        s_list.bezeich = bill_line.bezeich

                if bill_line.bill_datum < billdate:
                    s_list.prevbal = s_list.prevbal + bill_line.betrag / fact1
                    prevbal = prevbal + bill_line.betrag / fact1
                    s_list.balance = s_list.balance + bill_line.betrag / fact1
                    t_prevbal = t_prevbal + bill_line.betrag / fact1
                else:

                    if bill_line.betrag > 0:
                        s_list.debit = s_list.debit + bill_line.betrag / fact1
                        debit = debit + bill_line.betrag / fact1
                        t_debit = t_debit + bill_line.betrag / fact1
                    else:
                        s_list.credit = s_list.credit - bill_line.betrag / fact1
                        credit = credit - bill_line.betrag / fact1
                        t_credit = t_credit - bill_line.betrag / fact1
                    s_list.balance = s_list.balance + bill_line.betrag / fact1
                balance = balance + bill_line.betrag / fact1
                t_balance = t_balance + bill_line.betrag / fact1

        for bill_list in query(bill_list_list, filters=(lambda bill_list :bill_list.billtype.lower()  == "N")):
            prevbal = 0
            debit = 0
            credit = 0
            balance = 0

            for bill_line in db_session.query(Bill_line).filter(
                    (Bill_line.rechnr == bill_list.rechnr) &  (Bill_line.bill_datum <= billdate)).all():
                tot_bline = tot_bline + 1

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == bill_line.departement)).first()

                if not artikel:

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == 0)).first()

                s_list = query(s_list_list, filters=(lambda s_list :s_list.artnr == artikel.artnr and s_list.dept == artikel.departement and s_list.rechnr == bill_line.rechnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    current_counter = current_counter + 1
                    s_list.i_counter = current_counter
                    s_list.gname = bill_list.gname
                    s_list.flag = 2
                    s_list.artnr = bill_line.artnr
                    s_list.dept = bill_line.departement
                    s_list.rechnr = bill_list.rechnr
                    s_list.billtyp = "NS"
                    s_list.billnr = bill_list.billnr
                    s_list.prevbal = 0
                    s_list.balance = 0
                    s_list.bill_datum = bill_line.bill_datum

                    if artikel:
                        s_list.bezeich = artikel.bezeich
                    else:
                        s_list.bezeich = "[!] " + bill_line.bezeich

                if bill_line.bill_datum < billdate:
                    s_list.prevbal = s_list.prevbal + bill_line.betrag / fact1
                    prevbal = prevbal + bill_line.betrag / fact1
                    t_prevbal = t_prevbal + bill_line.betrag / fact1
                    s_list.balance = s_list.balance + bill_line.betrag / fact1
                else:

                    if bill_line.betrag > 0:
                        s_list.debit = s_list.debit + bill_line.betrag / fact1
                        debit = debit + bill_line.betrag / fact1
                        t_debit = t_debit + bill_line.betrag / fact1
                    else:
                        s_list.credit = s_list.credit - bill_line.betrag / fact1
                        credit = credit - bill_line.betrag / fact1
                        t_credit = t_credit - bill_line.betrag / fact1
                    s_list.balance = s_list.balance + bill_line.betrag / fact1
                balance = balance + bill_line.betrag / fact1
                t_balance = t_balance + bill_line.betrag / fact1
        curr_rechnr = 0
        curr_flag = 0
        balance = 0

        for s_list in query(s_list_list):

            if s_list.debit != 0 or s_list.credit != 0:

                sum_list = query(sum_list_list, filters=(lambda sum_list :sum_list.bezeich == s_list.bezeich), first=True)

                if not sum_list:
                    sum_list = Sum_list()
                    sum_list_list.append(sum_list)

                    sum_list.bezeich = s_list.bezeich
                sum_list.debit = sum_list.debit + s_list.debit
                sum_list.credit = sum_list.credit + s_list.credit
                sum_list.balance = sum_list.balance + s_list.debit - s_list.credit

            if curr_rechnr != s_list.rechnr:
                balance = s_list.prevbal + s_list.debit - s_list.credit
                s_list.balance = balance

                if curr_rechnr != 0:
                    gacct_balance_list = Gacct_balance_list()
                gacct_balance_list_list.append(gacct_balance_list)

                gacct_balance_list = Gacct_balance_list()
                gacct_balance_list_list.append(gacct_balance_list)

                gacct_balance_list.ankunft = s_list.ankunft
                gacct_balance_list.ankzeit = s_list.ankzeit
                gacct_balance_list.depart = s_list.abreise
                gacct_balance_list.typeBill = s_list.billtyp
                gacct_balance_list.guest = s_list.gname
                gacct_balance_list.roomNo = s_list.zinr
                gacct_balance_list.billNo = s_list.rechnr

                if price_decimal == 0:

                    if short_flag:
                        gacct_balance_list.bezeich = s_list.bezeich
                        gacct_balance_list.prevBala = s_list.prevbal
                        gacct_balance_list.debit = s_list.debit
                        gacct_balance_list.credit = s_list.credit
                        gacct_balance_list.balance = s_list.balance


                    else:
                        gacct_balance_list.bezeich = s_list.bezeich
                        gacct_balance_list.prevBala = s_list.prevbal
                        gacct_balance_list.debit = s_list.debit
                        gacct_balance_list.credit = s_list.credit
                        gacct_balance_list.balance = s_list.balance


                else:
                    gacct_balance_list.bezeich = s_list.bezeich
                    gacct_balance_list.prevBala = s_list.prevbal
                    gacct_balance_list.debit = s_list.debit
                    gacct_balance_list.credit = s_list.credit
                    gacct_balance_list.balance = s_list.balance


                curr_rechnr = gacct_balance_list.billNo
            else:
                balance = balance + s_list.prevbal + s_list.debit - s_list.credit
                s_list.balance = balance


                gacct_balance_list = Gacct_balance_list()
                gacct_balance_list_list.append(gacct_balance_list)

                gacct_balance_list.ankunft = s_list.ankunft
                gacct_balance_list.ankzeit = s_list.ankzeit

                if price_decimal == 0:

                    if short_flag:
                        gacct_balance_list.bezeich = s_list.bezeich
                        gacct_balance_list.prevBala = s_list.prevbal
                        gacct_balance_list.debit = s_list.debit
                        gacct_balance_list.credit = s_list.credit
                        gacct_balance_list.balance = s_list.balance


                    else:
                        gacct_balance_list.bezeich = s_list.bezeich
                        gacct_balance_list.prevBala = s_list.prevbal
                        gacct_balance_list.debit = s_list.debit
                        gacct_balance_list.credit = s_list.credit
                        gacct_balance_list.balance = s_list.balance


                else:
                    gacct_balance_list.bezeich = s_list.bezeich
                    gacct_balance_list.prevBala = s_list.prevbal
                    gacct_balance_list.debit = s_list.debit
                    gacct_balance_list.credit = s_list.credit
                    gacct_balance_list.balance = s_list.balance


        gacct_balance_list = Gacct_balance_list()
        gacct_balance_list_list.append(gacct_balance_list)


        if price_decimal == 0:

            if short_flag:
                gacct_balance_list.bezeich = "T O T A L"
                gacct_balance_list.prevBala = t_prevbal
                gacct_balance_list.debit = t_debit
                gacct_balance_list.credit = t_credit
                gacct_balance_list.balance = t_balance


            else:
                gacct_balance_list.bezeich = "T O T A L"
                gacct_balance_list.prevBala = t_prevbal
                gacct_balance_list.debit = t_debit
                gacct_balance_list.credit = t_credit
                gacct_balance_list.balance = t_balance


        else:
            gacct_balance_list.bezeich = "T O T A L"
            gacct_balance_list.prevBala = t_prevbal
            gacct_balance_list.debit = t_debit
            gacct_balance_list.credit = t_credit
            gacct_balance_list.balance = t_balance


        gacct_balance_list = Gacct_balance_list()
        gacct_balance_list_list.append(gacct_balance_list)

        gacct_balance_list = Gacct_balance_list()
        gacct_balance_list_list.append(gacct_balance_list)


        uebertrag = db_session.query(Uebertrag).filter(
                (Uebertrag.datum == billdate)).first()

        if price_decimal == 0:
            gacct_balance_list.bezeich = "Outstanding"
            gacct_balance_list.balance = t_prevbal + t_debit - t_credit

            if uebertrag:
                gacct_balance_list = Gacct_balance_list()
                gacct_balance_list_list.append(gacct_balance_list)

                gacct_balance_list.bezeich = "Stored Guest Ledger Amount:"
                gacct_balance_list.balance = uebertrag.betrag


        else:
            gacct_balance_list.bezeich = "Outstanding"
            gacct_balance_list.balance = t_prevbal + t_debit - t_credit

            if uebertrag:
                gacct_balance_list = Gacct_balance_list()
                gacct_balance_list_list.append(gacct_balance_list)

                gacct_balance_list.bezeich = "Stored Guest Ledger Amount:"
                gacct_balance_list.balance = uebertrag.betrag


        gacct_balance_list = Gacct_balance_list()
        gacct_balance_list_list.append(gacct_balance_list)

        gacct_balance_list = Gacct_balance_list()
        gacct_balance_list_list.append(gacct_balance_list)

        gacct_balance_list.guest = "Summary of Transaction"
        t_debit = 0
        t_credit = 0
        t_balance = 0

        for sum_list in query(sum_list_list):
            gacct_balance_list = Gacct_balance_list()
            gacct_balance_list_list.append(gacct_balance_list)

            gacct_balance_list.guest = sum_list.bezeich

            if price_decimal == 0:

                if short_flag:
                    gacct_balance_list.debit = sum_list.debit
                    gacct_balance_list.credit = sum_list.credit
                    gacct_balance_list.balance = sum_list.balance


                else:
                    gacct_balance_list.debit = sum_list.debit
                    gacct_balance_list.credit = sum_list.credit
                    gacct_balance_list.balance = sum_list.balance


            else:
                gacct_balance_list.debit = sum_list.debit
                gacct_balance_list.credit = sum_list.credit
                gacct_balance_list.balance = sum_list.balance


            t_debit = t_debit + sum_list.debit
            t_credit = t_credit + sum_list.credit
        t_balance = t_debit - t_credit
        gacct_balance_list = Gacct_balance_list()
        gacct_balance_list_list.append(gacct_balance_list)

        gacct_balance_list.guest = "T o t a l"

        if price_decimal == 0:

            if short_flag:
                gacct_balance_list.debit = t_debit
                gacct_balance_list.credit = t_credit
                gacct_balance_list.balance = t_balance


            else:
                gacct_balance_list.debit = t_debit
                gacct_balance_list.credit = t_credit
                gacct_balance_list.balance = t_balance


        else:
            gacct_balance_list.debit = t_debit
            gacct_balance_list.credit = t_credit
            gacct_balance_list.balance = t_balance

    tot_bline = 0
    current_counter = 0
    t_prevbal = 0
    t_debit = 0
    t_credit = 0
    t_balance = 0


    create_bill_list()
    create_umsatz()

    return generate_output()