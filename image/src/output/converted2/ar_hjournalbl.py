from functions.additional_functions import *
import decimal
from datetime import date
from models import Hoteldpt, H_journal, H_artikel

def ar_hjournalbl(from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date):
    output_list_list = []
    long_digit:bool = False
    qty:int = 0
    sub_tot:decimal = to_decimal("0.0")
    tot:decimal = to_decimal("0.0")
    curr_date:date = None
    last_dept:int = -1
    it_exist:bool = False
    hoteldpt = h_journal = h_artikel = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, long_digit, qty, sub_tot, tot, curr_date, last_dept, it_exist, hoteldpt, h_journal, h_artikel
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date


        nonlocal output_list
        nonlocal output_list_list
        return {"output-list": output_list_list}


    output_list_list.clear()

    if from_art == 0:

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= from_dept) & (Hoteldpt.num <= to_dept)).order_by(Hoteldpt.num).all():
            sub_tot =  to_decimal("0")
            it_exist = False
            qty = 0
            for curr_date in date_range(from_date,to_date) :

                for h_journal in db_session.query(H_journal).filter(
                         (H_journal.artnr == 0) & (H_journal.departement == hoteldpt.num) & (H_journal.bill_datum == curr_date)).order_by(H_journal._recid).all():
                    it_exist = True
                    output_list = Output_list()
                    output_list_list.append(output_list)


                    if not long_digit:
                        str = to_string(bill_datum) + to_string(h_journal.tischnr, "9999") + to_string(rechnr, "9,999,999") + to_string(h_journal.artnr, "99999") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(12)") + to_string(h_journal.anzahl, "-9999") + to_string(betrag, "->,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999")
                    else:
                        str = to_string(bill_datum) + to_string(h_journal.tischnr, "9999") + to_string(rechnr, "9,999,999") + to_string(h_journal.artnr, "99999") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(12)") + to_string(h_journal.anzahl, "-9999") + to_string(betrag, " ->>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999")
                    qty = qty + h_journal.anzahl
                    sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                    tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

            if it_exist:
                output_list = Output_list()
                output_list_list.append(output_list)


                if not long_digit:
                    str = to_string("", "x(54)") + to_string("T O T A L ", "x(12)") + to_string(qty, "-9999") + to_string(sub_tot, "->,>>>,>>>,>>9.99")
                else:
                    str = to_string("", "x(54)") + to_string("T O T A L ", "x(12)") + to_string(qty, "-9999") + to_string(sub_tot, " ->>>,>>>,>>>,>>9")

    last_dept = - 1

    h_artikel_obj_list = []
    for h_artikel, hoteldpt in db_session.query(H_artikel, Hoteldpt).join(Hoteldpt,(Hoteldpt.num == H_artikel.departement)).filter(
             (H_artikel.artnr >= from_art) & (H_artikel.artnr <= to_art) & ((H_artikel.artart == 2) | (H_artikel.artart == 7)) & (H_artikel.departement >= from_dept) & (H_artikel.departement <= to_dept)).order_by(H_artikel.departement, H_artikel.artnr).all():
        if h_artikel._recid in h_artikel_obj_list:
            continue
        else:
            h_artikel_obj_list.append(h_artikel._recid)


        last_dept = h_artikel.departement
        sub_tot =  to_decimal("0")
        it_exist = False
        qty = 0
        for curr_date in date_range(from_date,to_date) :

            for h_journal in db_session.query(H_journal).filter(
                     (H_journal.artnr == h_artikel.artnr) & (H_journal.departement == h_artikel.departement) & (H_journal.bill_datum == curr_date)).order_by(H_journal._recid).all():
                it_exist = True
                output_list = Output_list()
                output_list_list.append(output_list)


                if not long_digit:
                    str = to_string(bill_datum) + to_string(h_journal.tischnr, "9999") + to_string(rechnr, "9,999,999") + to_string(h_journal.artnr, "99999") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(12)") + to_string(h_journal.anzahl, "-9999") + to_string(betrag, "->,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999")
                else:
                    str = to_string(bill_datum) + to_string(h_journal.tischnr, "9999") + to_string(rechnr, "9,999,999") + to_string(h_journal.artnr, "99999") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(12)") + to_string(h_journal.anzahl, "-9999") + to_string(betrag, " ->>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM:SS") + to_string(h_journal.kellner_nr, "999")
                qty = qty + h_journal.anzahl
                sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

        if it_exist:
            output_list = Output_list()
            output_list_list.append(output_list)


            if not long_digit:
                str = to_string("", "x(54)") + to_string("T O T A L ", "x(12)") + to_string(qty, "-9999") + to_string(sub_tot, "->,>>>,>>>,>>9.99")
            else:
                str = to_string("", "x(54)") + to_string("T O T A L ", "x(12)") + to_string(qty, "-9999") + to_string(sub_tot, " ->>>,>>>,>>>,>>9")
    output_list = Output_list()
    output_list_list.append(output_list)


    if not long_digit:
        str = to_string("", "x(54)") + to_string("Grand TOTAL ", "x(12)") + to_string(0, "-9999") + to_string(tot, "->,>>>,>>>,>>9.99")
    else:
        str = to_string("", "x(54)") + to_string("Grand TOTAL ", "x(12)") + to_string(0, "-9999") + to_string(tot, " ->>>,>>>,>>>,>>9")

    return generate_output()