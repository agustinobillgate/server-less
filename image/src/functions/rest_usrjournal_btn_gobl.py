from functions.additional_functions import *
import decimal
from datetime import date
from models import Hoteldpt, H_bill, H_journal

def rest_usrjournal_btn_gobl(sumflag:bool, from_date:date, to_date:date, usr_init:str, curr_dept:int, price_decimal:int):
    output_list_list = []
    hoteldpt = h_bill = h_journal = None

    output_list = sum_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})
    sum_list_list, Sum_list = create_model("Sum_list", {"datum":date, "artnr":int, "bezeich":str, "anzahl":int, "betrag":decimal, "usrno":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, hoteldpt, h_bill, h_journal


        nonlocal output_list, sum_list
        nonlocal output_list_list, sum_list_list
        return {"output-list": output_list_list}

    def journal_list():

        nonlocal output_list_list, hoteldpt, h_bill, h_journal


        nonlocal output_list, sum_list
        nonlocal output_list_list, sum_list_list

        qty:int = 0
        sub_tot:decimal = 0
        tot:decimal = 0
        curr_date:date = None
        output_list_list.clear()
        for curr_date in range(from_date,to_date + 1) :

            h_journal_obj_list = []
            for h_journal, h_bill in db_session.query(H_journal, H_bill).join(H_bill,(H_bill.rechnr == H_journal.rechnr) &  (H_bill.departement == H_journal.departement)).filter(
                    (H_journal.kellner_nr == to_int(usr_init)) &  (H_journal.departement == curr_dept) &  (H_journal.bill_datum == curr_date)).all():
                if h_journal._recid in h_journal_obj_list:
                    continue
                else:
                    h_journal_obj_list.append(h_journal._recid)


                output_list = Output_list()
                output_list_list.append(output_list)


                if price_decimal == 2:
                    STR = to_string(bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, "9,999,999") + to_string(h_journal.artnr, ">>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(12)") + to_string(h_journal.anzahl, "-9999") + to_string(betrag, "->,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM") + to_string(h_journal.kellner_nr, "999") + to_string(h_bill.kellner_nr, "999")
                else:
                    STR = to_string(bill_datum) + to_string(h_journal.tischnr, ">>>>>9") + to_string(h_journal.rechnr, "9,999,999") + to_string(h_journal.artnr, ">>>>>") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(12)") + to_string(h_journal.anzahl, "-9999") + to_string(betrag, " ->>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM") + to_string(h_journal.kellner_nr, "999") + to_string(h_bill.kellner_nr, "999")
                qty = qty + h_journal.anzahl
                sub_tot = sub_tot + h_journal.betrag
                tot = tot + h_journal.betrag
        output_list = Output_list()
        output_list_list.append(output_list)


        if price_decimal == 2:
            STR = to_string("", "x(29)") + to_string("T O T A L   ", "x(27)") + to_string("", "x(11)") + to_string(qty, "-9999") + to_string(sub_tot, "->,>>>,>>>,>>9.99")
        else:
            STR = to_string("", "x(29)") + to_string("T O T A L   ", "x(27)") + to_string("", "x(11)") + to_string(qty, "-9999") + to_string(sub_tot, " ->>>,>>>,>>>,>>>")

    def journal_sumlist():

        nonlocal output_list_list, hoteldpt, h_bill, h_journal


        nonlocal output_list, sum_list
        nonlocal output_list_list, sum_list_list

        qty:int = 0
        sub_tot:decimal = 0
        tot:decimal = 0
        curr_date:date = None
        output_list_list.clear()
        sum_list_list.clear()
        for curr_date in range(from_date,to_date + 1) :

            h_journal_obj_list = []
            for h_journal, h_bill in db_session.query(H_journal, H_bill).join(H_bill,(H_bill.rechnr == H_journal.rechnr) &  (H_bill.departement == H_journal.departement)).filter(
                    (H_journal.kellner_nr == to_int(usr_init)) &  (H_journal.departement == curr_dept) &  (H_journal.bill_datum == curr_date)).all():
                if h_journal._recid in h_journal_obj_list:
                    continue
                else:
                    h_journal_obj_list.append(h_journal._recid)

                sum_list = query(sum_list_list, filters=(lambda sum_list :sum_list.artnr == h_journal.artnr and sum_list.bezeich == h_journal.bezeich and sum_list.datum == h_journal.bill_datum), first=True)

                if not sum_list:
                    sum_list = Sum_list()
                    sum_list_list.append(sum_list)

                    sum_list.datum = h_journal.bill_datum
                    sum_list.artnr = h_journal.artnr
                    sum_list.bezeich = h_journal.bezeich
                    sum_list.usrNo = h_journal.kellner_nr


                qty = qty + h_journal.anzahl
                sum_list.anzahl = sum_list.anzahl + h_journal.anzahl
                sum_list.betrag = sum_list.betrag + h_journal.betrag

        for sum_list in query(sum_list_list):
            output_list = Output_list()
            output_list_list.append(output_list)


            if price_decimal == 2:
                STR = to_string(sum_list.datum) + to_string("", "x(6)") + to_string("", "x(9)") + to_string(sum_list.artnr, ">>>>>") + to_string(sum_list.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(12)") + to_string(sum_list.anzahl, "-9999") + to_string(sum_list.betrag, "->,>>>,>>>,>>9.99") + to_string("", "x(5)") + to_string(sum_list.usrNo, "999") + to_string("", "x(3)")
            else:
                STR = to_string(sum_list.datum) + to_string("", "x(6)") + to_string("", "x(9)") + to_string(sum_list.artnr, ">>>>>") + to_string(sum_list.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(12)") + to_string(sum_list.anzahl, "-9999") + to_string(sum_list.betrag, " ->>>,>>>,>>>,>>9") + to_string("", "x(5)") + to_string(sum_list.usrNo, "999") + to_string("", "x(3)")
            sub_tot = sub_tot + sum_list.betrag
            tot = tot + sum_list.betrag
        output_list = Output_list()
        output_list_list.append(output_list)


        if price_decimal == 2:
            STR = to_string("", "x(29)") + to_string("T O T A L   ", "x(27)") + to_string("", "x(11)") + to_string(qty, "-9999") + to_string(sub_tot, "->,>>>,>>>,>>9.99")
        else:
            STR = to_string("", "x(29)") + to_string("T O T A L   ", "x(27)") + to_string("", "x(11)") + to_string(qty, "-9999") + to_string(sub_tot, " ->>>,>>>,>>>,>>>")


    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == curr_dept)).first()

    if not sumflag:
        journal_list()
    else:
        journal_sumlist()

    return generate_output()