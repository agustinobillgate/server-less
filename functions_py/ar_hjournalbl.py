#using conversion tools version: 1.0.0.117

# ---------------------------------------------------------
# Rulita, 09-09-2025  
# Issue, fixing parsing kolom outlet, qty, amount, time
#     fixing format date 
# ---------------------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, H_journal, H_artikel

# Rulita | For debug
# from functions import log_program

def ar_hjournalbl(from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date):

    prepare_cache ([Hoteldpt, H_journal, H_artikel])

    output_list_data = []
    long_digit:bool = False
    qty:int = 0
    sub_tot:Decimal = to_decimal("0.0")
    tot:Decimal = to_decimal("0.0")
    curr_date:date = None
    last_dept:int = -1
    it_exist:bool = False
    hoteldpt = h_journal = h_artikel = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, long_digit, qty, sub_tot, tot, curr_date, last_dept, it_exist, hoteldpt, h_journal, h_artikel
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date


        nonlocal output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}


    output_list_data.clear()

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
                    output_list_data.append(output_list)
                    
                    # Rulita
                    tmp_depart = hoteldpt.depart[:12].ljust(13)

                    if not long_digit:
                        # Rulita
                        output_list.str =   to_string(h_journal.bill_datum.strftime("%d/%m/%y")) \
                                            + to_string(h_journal.tischnr, "9999") \
                                            + to_string(h_journal.rechnr, "9,999,999") \
                                            + to_string(h_journal.artnr, "99999") \
                                            + to_string(h_journal.bezeich, "x(28)") \
                                            + to_string(tmp_depart, "x(12)") \
                                            + to_string(h_journal.anzahl, "-9999") \
                                            + to_string(h_journal.betrag, "->,>>>,>>>,>>9.99") \
                                            + to_string(h_journal.zeit, "HH:MM:SS") \
                                            + to_string(h_journal.kellner_nr, "999")            
                    else:
                        # Rulita
                        output_list.str =   to_string(h_journal.bill_datum.strftime("%d/%m/%y")) \
                                            + to_string(h_journal.tischnr, "9999") \
                                            + to_string(h_journal.rechnr, "9,999,999") \
                                            + to_string(h_journal.artnr, "99999") \
                                            + to_string(h_journal.bezeich, "x(28)") \
                                            + to_string(tmp_depart, "x(12)") \
                                            + to_string(h_journal.anzahl, "-9999") \
                                            + to_string(h_journal.betrag, " ->>>,>>>,>>>,>>9") \
                                            + to_string(h_journal.zeit, "HH:MM:SS") \
                                            + to_string(h_journal.kellner_nr, "999")

                    qty = qty + h_journal.anzahl
                    sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                    tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

            if it_exist:
                output_list = Output_list()
                output_list_data.append(output_list)

                # Rulita
                tmp_total = "T O T A L "

                if not long_digit:
                    # Rulita
                    output_list.str = to_string("", "x(54)") + to_string(tmp_total.ljust(13) , "x(12)") + to_string(qty, "-9999") + to_string(sub_tot, "->,>>>,>>>,>>9.99")
                else:
                    # Rulita
                    output_list.str = to_string("", "x(54)") + to_string(tmp_total.ljust(13) , "x(12)") + to_string(qty, "-9999") + to_string(sub_tot, " ->>>,>>>,>>>,>>9")

    last_dept = - 1

    h_artikel_obj_list = {}
    h_artikel = H_artikel()
    hoteldpt = Hoteldpt()
    for h_artikel.departement, h_artikel.artnr, h_artikel._recid, hoteldpt.num, hoteldpt.depart, hoteldpt._recid in db_session.query(H_artikel.departement, H_artikel.artnr, H_artikel._recid, Hoteldpt.num, Hoteldpt.depart, Hoteldpt._recid).join(Hoteldpt,(Hoteldpt.num == H_artikel.departement)).filter(
             (H_artikel.artnr >= from_art) & (H_artikel.artnr <= to_art) & ((H_artikel.artart == 2) | (H_artikel.artart == 7)) & (H_artikel.departement >= from_dept) & (H_artikel.departement <= to_dept)).order_by(H_artikel.departement, H_artikel.artnr).all():
        if h_artikel_obj_list.get(h_artikel._recid):
            continue
        else:
            h_artikel_obj_list[h_artikel._recid] = True


        last_dept = h_artikel.departement
        sub_tot =  to_decimal("0")
        it_exist = False
        qty = 0
        for curr_date in date_range(from_date,to_date) :

            for h_journal in db_session.query(H_journal).filter(
                     (H_journal.artnr == h_artikel.artnr) & (H_journal.departement == h_artikel.departement) & (H_journal.bill_datum == curr_date)).order_by(H_journal._recid).all():
                it_exist = True
                output_list = Output_list()
                output_list_data.append(output_list)
                
                # Rulita
                tmp_depart = hoteldpt.depart[:12].ljust(13)

                if not long_digit:
                    # Rulita
                    output_list.str =   to_string(h_journal.bill_datum.strftime("%d/%m/%y")) \
                                        + to_string(h_journal.tischnr, "9999") \
                                        + to_string(h_journal.rechnr, "9,999,999") \
                                        + to_string(h_journal.artnr, "99999") \
                                        + to_string(h_journal.bezeich, "x(28)") \
                                        + to_string(tmp_depart, "x(12)") \
                                        + to_string(h_journal.anzahl, "-9999") \
                                        + to_string(h_journal.betrag, "->,>>>,>>>,>>9.99") \
                                        + to_string(h_journal.zeit, "HH:MM:SS") \
                                        + to_string(h_journal.kellner_nr, "999")
                else:
                    # Rulita
                    output_list.str =   to_string(h_journal.bill_datum.strftime("%d/%m/%y")) \
                                        + to_string(h_journal.tischnr, "9999") \
                                        + to_string(h_journal.rechnr, "9,999,999") \
                                        + to_string(h_journal.artnr, "99999") \
                                        + to_string(h_journal.bezeich, "x(28)") \
                                        + to_string(tmp_depart, "x(12)") \
                                        + to_string(h_journal.anzahl, "-9999") \
                                        + to_string(h_journal.betrag, " ->>>,>>>,>>>,>>9") \
                                        + to_string(h_journal.zeit, "HH:MM:SS") \
                                        + to_string(h_journal.kellner_nr, "999")
                    
                qty = qty + h_journal.anzahl
                sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                tot =  to_decimal(tot) + to_decimal(h_journal.betrag)

        if it_exist:
            output_list = Output_list()
            output_list_data.append(output_list)
            
            # Rulita
            tmp_total = "T O T A L "

            if not long_digit:
                # Rulita
                output_list.str = to_string("", "x(54)") + to_string(tmp_total.ljust(13), "x(12)") + to_string(qty, "-9999") + to_string(sub_tot, "->,>>>,>>>,>>9.99")
            else:
                # Rulita
                output_list.str = to_string("", "x(54)") + to_string(tmp_total.ljust(13), "x(12)") + to_string(qty, "-9999") + to_string(sub_tot, " ->>>,>>>,>>>,>>9")
    output_list = Output_list()
    output_list_data.append(output_list)

    # Rulita
    tmp_gtot = "Grand TOTAL "

    if not long_digit:
        # Rulita
        output_list.str = to_string("", "x(54)") + to_string(tmp_gtot.ljust(13), "x(12)") + to_string(0, "-9999") + to_string(tot, "->,>>>,>>>,>>9.99")
    else:
        # Rulita
        output_list.str = to_string("", "x(54)") + to_string(tmp_gtot.ljust(13), "x(12)") + to_string(0, "-9999") + to_string(tot, " ->>>,>>>,>>>,>>9")

    return generate_output()