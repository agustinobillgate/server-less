#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 21/7/2025
# gitlab: 385
# add if available
# Rd 16/9/20225, checkbox 'Show as summary' beda output
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, H_bill, H_journal

def rest_usrjournal_btn_cldbl(sumflag:bool, from_date:date, to_date:date, usr_init:string, curr_dept:int, price_decimal:int):

    prepare_cache ([Hoteldpt, H_bill, H_journal])

    output_list_data = []
    hoteldpt = h_bill = h_journal = None

    output_list = sum_list = None

    output_list_data, Output_list = create_model("Output_list", {"bezeich":string, "str":string})
    sum_list_data, Sum_list = create_model("Sum_list", {"datum":date, "artnr":int, "bezeich":string, "anzahl":int, "betrag":Decimal, "usrno":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, hoteldpt, h_bill, h_journal
        nonlocal sumflag, from_date, to_date, usr_init, curr_dept, price_decimal


        nonlocal output_list, sum_list
        nonlocal output_list_data, sum_list_data

        log_debug = []
        for output_list in query(output_list_data):
            log_debug.append(output_list.str)
        return {"log": log_debug, "output-list": output_list_data}

    def journal_list():

        nonlocal output_list_data, hoteldpt, h_bill, h_journal
        nonlocal sumflag, from_date, to_date, usr_init, curr_dept, price_decimal


        nonlocal output_list, sum_list
        nonlocal output_list_data, sum_list_data

        qty:int = 0
        sub_tot:Decimal = to_decimal("0.0")
        tot:Decimal = to_decimal("0.0")
        curr_date:date = None
        h_journal_tischnr:string = ""
        h_journal_rechnr:string = ""
        h_journal_artnr:string = ""
        hoteldpt_depart_journal_list:string = ""
        h_journal_anzahl:string = ""
        h_journal_betrag:string = ""
        h_journal_zeit:string = ""
        h_journal_kellner_nr:string = ""
        h_bill_kellner_nr:string = ""
        h_journal_betrag_no_coma:string = ""
        qty_total:string = ""
        sub_tot_total:string = ""
        sub_tot_total_no_coma:string = ""
        output_list_data.clear()
        for curr_date in date_range(from_date,to_date) :

            h_journal_obj_list = {}
            h_journal = H_journal()
            h_bill = H_bill()
            for h_journal.tischnr, h_journal.rechnr, h_journal.artnr, h_journal.anzahl, h_journal.betrag, h_journal.zeit, h_journal.kellner_nr, h_journal.bill_datum, h_journal.bezeich, h_journal._recid, h_bill.kellner_nr, h_bill._recid in db_session.query(H_journal.tischnr, H_journal.rechnr, H_journal.artnr, H_journal.anzahl, H_journal.betrag, H_journal.zeit, H_journal.kellner_nr, H_journal.bill_datum, H_journal.bezeich, H_journal._recid, H_bill.kellner_nr, H_bill._recid).join(H_bill,(H_bill.rechnr == H_journal.rechnr) & (H_bill.departement == H_journal.departement)).filter(
                     (H_journal.kellner_nr == to_int(usr_init)) & (H_journal.departement == curr_dept) & (H_journal.bill_datum == curr_date)).order_by(H_journal.rechnr, H_journal.sysdate, H_journal.zeit).all():
                if h_journal_obj_list.get(h_journal._recid):
                    continue
                else:
                    h_journal_obj_list[h_journal._recid] = True


                h_journal_tischnr = to_string(h_journal.tischnr, ">>>>>9")
                h_journal_rechnr = to_string(h_journal.rechnr, "9,999,999")
                h_journal_artnr = to_string(h_journal.artnr, ">>>>>>>>>")
                hoteldpt_depart_journal_list = substring(hoteldpt.depart, 0, 12)
                h_journal_anzahl = to_string(h_journal.anzahl, "-9999")
                h_journal_betrag = to_string(h_journal.betrag, "->,>>>,>>>,>>9.99")
                h_journal_zeit = to_string(h_journal.zeit, "HH:MM")
                h_journal_kellner_nr = to_string(h_journal.kellner_nr, "9999")
                h_bill_kellner_nr = to_string(h_bill.kellner_nr, "9999")
                h_journal_betrag_no_coma = to_string(h_journal.betrag, " ->>>,>>>,>>>,>>9")
                output_list = Output_list()
                output_list_data.append(output_list)


                if price_decimal == 2:
                    output_list.str = to_string(h_journal.bill_datum) + to_string(h_journal_tischnr, "x(6)") + to_string(h_journal_rechnr, "x(9)") + to_string(h_journal_artnr, "x(9)") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt_depart_journal_list, "x(12)") + to_string(h_journal_anzahl, "x(5)") + to_string(h_journal_betrag, "x(17)") + h_journal_zeit + to_string(h_journal_kellner_nr, "x(5)") + to_string(h_bill_kellner_nr, "x(5)")
                else:
                    output_list.str = to_string(h_journal.bill_datum) + to_string(h_journal_tischnr, "x(6)") + to_string(h_journal_rechnr, "x(9)") + to_string(h_journal_artnr, "x(9)") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt_depart_journal_list, "x(12)") + to_string(h_journal_anzahl, "x(5)") + to_string(h_journal_betrag_no_coma, "x(17)") + h_journal_zeit + to_string(h_journal_kellner_nr, "x(5)") + to_string(h_bill_kellner_nr, "x(5)")
                output_list.bezeich = h_journal.bezeich


                qty = qty + h_journal.anzahl
                sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
                tot =  to_decimal(tot) + to_decimal(h_journal.betrag)
        qty_total = to_string(qty, "-9999")
        sub_tot_total = to_string(sub_tot, "->,>>>,>>>,>>9.99")
        sub_tot_total_no_coma = to_string(sub_tot, " ->>>,>>>,>>>,>>>")
        output_list = Output_list()
        output_list_data.append(output_list)


        if price_decimal == 2:
            output_list.str = to_string("", "x(33)") + to_string("T O T A L ", "x(27)") + to_string("", "x(11)") + to_string(qty_total, "x(5)") + to_string(sub_tot_total, "x(17)")
        else:
            output_list.str = to_string("", "x(33)") + to_string("T O T A L ", "x(27)") + to_string("", "x(11)") + to_string(qty_total, "x(5)") + to_string(sub_tot_total_no_coma, "x(17)")
        output_list.bezeich = "T O T A L"


    def journal_sumlist():

        nonlocal output_list_data, hoteldpt, h_bill, h_journal
        nonlocal sumflag, from_date, to_date, usr_init, curr_dept, price_decimal


        nonlocal output_list, sum_list
        nonlocal output_list_data, sum_list_data

        qty:int = 0
        sub_tot:Decimal = to_decimal("0.0")
        tot:Decimal = to_decimal("0.0")
        curr_date:date = None
        sum_list_artnr:string = ""
        sum_list_anzahl:string = ""
        sum_list_betrag:string = ""
        sum_list_usrno:string = ""
        sum_list_betrag_no_coma:string = ""
        qty_total:string = ""
        sub_tot_total:string = ""
        sub_tot_total_no_coma:string = ""
        hoteldpt_depart:string = ""
        output_list_data.clear()
        sum_list_data.clear()
        for curr_date in date_range(from_date,to_date) :

            h_journal_obj_list = {}
            h_journal = H_journal()
            h_bill = H_bill()
            for h_journal.tischnr, h_journal.rechnr, h_journal.artnr, h_journal.anzahl, h_journal.betrag, h_journal.zeit, h_journal.kellner_nr, h_journal.bill_datum, h_journal.bezeich, h_journal._recid, h_bill.kellner_nr, h_bill._recid in db_session.query(H_journal.tischnr, H_journal.rechnr, H_journal.artnr, H_journal.anzahl, H_journal.betrag, H_journal.zeit, H_journal.kellner_nr, H_journal.bill_datum, H_journal.bezeich, H_journal._recid, H_bill.kellner_nr, H_bill._recid).join(H_bill,(H_bill.rechnr == H_journal.rechnr) & (H_bill.departement == H_journal.departement)).filter(
                     (H_journal.kellner_nr == to_int(usr_init)) & (H_journal.departement == curr_dept) & (H_journal.bill_datum == curr_date)).order_by(H_journal.rechnr, H_journal.sysdate, H_journal.zeit).all():
                if h_journal_obj_list.get(h_journal._recid):
                    continue
                else:
                    h_journal_obj_list[h_journal._recid] = True

                sum_list = query(sum_list_data, filters=(lambda sum_list: sum_list.artnr == h_journal.artnr and sum_list.bezeich == h_journal.bezeich and sum_list.datum == h_journal.bill_datum), first=True)

                if not sum_list:
                    sum_list = Sum_list()
                    sum_list_data.append(sum_list)

                    sum_list.datum = h_journal.bill_datum
                    sum_list.artnr = h_journal.artnr
                    sum_list.bezeich = h_journal.bezeich
                    sum_list.usrno = h_journal.kellner_nr


                qty = qty + h_journal.anzahl
                sum_list.anzahl = sum_list.anzahl + h_journal.anzahl
                sum_list.betrag =  to_decimal(sum_list.betrag) + to_decimal(h_journal.betrag)

        for sum_list in query(sum_list_data, sort_by=[("datum",False),("artnr",False)]):
            sum_list_artnr = to_string(sum_list.artnr, ">>>>>>>>>")
            sum_list_anzahl = to_string(sum_list.anzahl, "-9999")
            sum_list_betrag = to_string(sum_list.betrag, "->,>>>,>>>,>>9.99")
            sum_list_usrno = to_string(sum_list.usrno, "999")
            sum_list_betrag_no_coma = to_string(sum_list.betrag, " ->>>,>>>,>>>,>>9")
            hoteldpt_depart = substring(hoteldpt.depart, 0, 12)
            output_list = Output_list()
            output_list_data.append(output_list)


            if price_decimal == 2:
                output_list.str = to_string(sum_list.datum) + to_string("", "x(6)") + to_string("", "x(9)") + to_string(sum_list_artnr, "x(9)") + to_string(sum_list.bezeich, "x(28)") + to_string(hoteldpt_depart, "x(12)") + to_string(sum_list_anzahl, "x(5)") + to_string(sum_list_betrag, "x(17)") + to_string("", "x(5)") + to_string(sum_list_usrno, "x(3)") + to_string("", "x(3)")
            else:
                output_list.str = to_string(sum_list.datum) + to_string("", "x(6)") + to_string("", "x(9)") + to_string(sum_list_artnr, "x(9)") + to_string(sum_list.bezeich, "x(28)") + to_string(hoteldpt_depart, "x(12)") + to_string(sum_list_anzahl, "x(5)") + to_string(sum_list_betrag_no_coma, "x(17)") + to_string("", "x(5)") + to_string(sum_list_usrno, "x(3)") + to_string("", "x(3)")
            output_list.bezeich = sum_list.bezeich


            sub_tot =  to_decimal(sub_tot) + to_decimal(sum_list.betrag)
            tot =  to_decimal(tot) + to_decimal(sum_list.betrag)
        qty_total = to_string(qty, "-9999")
        sub_tot_total = to_string(sub_tot, "->,>>>,>>>,>>9.99")
        sub_tot_total_no_coma = to_string(sub_tot, " ->>>,>>>,>>>,>>>")
        output_list = Output_list()
        output_list_data.append(output_list)


        if price_decimal == 2:
            output_list.str = to_string("", "x(33)") + to_string("T O T A L   ", "x(27)") + to_string("", "x(11)") + to_string(qty_total, "x(5)") + to_string(sub_tot_total, "x(17)")
        else:
            output_list.str = to_string("", "x(33)") + to_string("T O T A L   ", "x(27)") + to_string("", "x(11)") + to_string(qty_total, "x(5)") + to_string(sub_tot_total_no_coma, "x(17)")
        output_list.bezeich = "T O T A L"

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})

    if not sumflag:
        journal_list()
    else:
        journal_sumlist()

    return generate_output()