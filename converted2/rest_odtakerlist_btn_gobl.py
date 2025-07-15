from functions.additional_functions import *
import decimal
from datetime import date
from models import H_artikel, H_bill, H_journal, Hoteldpt

def rest_odtakerlist_btn_gobl(from_date:date, to_date:date, usr_nr:int, long_digit:bool):
    output_list_list = []
    h_artikel = h_bill = h_journal = hoteldpt = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, h_artikel, h_bill, h_journal, hoteldpt
        nonlocal from_date, to_date, usr_nr, long_digit


        nonlocal output_list
        nonlocal output_list_list
        return {"output-list": output_list_list}

    def journal_list():

        nonlocal output_list_list, h_artikel, h_bill, h_journal, hoteldpt
        nonlocal from_date, to_date, usr_nr, long_digit


        nonlocal output_list
        nonlocal output_list_list

        qty:int = 0
        sub_tot:decimal = to_decimal("0.0")
        tot:decimal = to_decimal("0.0")
        curr_date:date = None
        output_list_list.clear()

        h_journal_obj_list = []
        for h_journal, h_artikel, h_bill in db_session.query(H_journal, H_artikel, H_bill).join(H_artikel,(H_artikel.artnr == H_journal.artnr) & (H_artikel.departement == H_journal.departement) & (H_artikel.artart == 0)).join(H_bill,(H_bill.rechnr == H_journal.rechnr) & (H_bill.departement == H_journal.departement) & (H_bill.betriebsnr == usr_nr)).filter(
                 (H_journal.bill_datum >= from_date) & (H_journal.bill_datum <= to_date)).order_by(H_journal.rechnr, H_journal.sysdate, H_journal.zeit).all():
            if h_journal._recid in h_journal_obj_list:
                continue
            else:
                h_journal_obj_list.append(h_journal._recid)

            hoteldpt = db_session.query(Hoteldpt).filter(
                     (Hoteldpt.num == h_journal.departement)).first()
            output_list = Output_list()
            output_list_list.append(output_list)


            if not long_digit:
                str = to_string(bill_datum) + to_string(h_journal.tischnr, ">>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>9") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(betrag, "->,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM") + to_string(h_journal.kellner_nr, "999") + to_string(h_journal.tischnr, ">>>9")
            else:
                str = to_string(bill_datum) + to_string(h_journal.tischnr, ">>>9") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.artnr, ">>>>9") + to_string(h_journal.bezeich, "x(28)") + to_string(hoteldpt.depart, "x(20)") + to_string(h_journal.anzahl, "->>>9") + to_string(betrag, " ->>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM") + to_string(h_journal.kellner_nr, "999") + to_string(h_journal.tischnr, ">>>9")
            qty = qty + h_journal.anzahl
            sub_tot =  to_decimal(sub_tot) + to_decimal(h_journal.betrag)
            tot =  to_decimal(tot) + to_decimal(h_journal.betrag)
        output_list = Output_list()
        output_list_list.append(output_list)


        if not long_digit:
            str = to_string("", "x(26)") + to_string("T O T A L ", "x(28)") + to_string("", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, "->,>>>,>>>,>>9.99")
        else:
            str = to_string("", "x(26)") + to_string("T O T A L ", "x(28)") + to_string("", "x(20)") + to_string(qty, "->>>9") + to_string(sub_tot, " ->>>,>>>,>>>,>>9")

    journal_list()

    return generate_output()