from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Artikel, Hoteldpt, Billjournal

def fo_cjournbl(from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, foreign_flag:bool, long_digit:bool):
    output_list_list = []
    htparam = artikel = hoteldpt = billjournal = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, htparam, artikel, hoteldpt, billjournal


        nonlocal output_list
        nonlocal output_list_list
        return {"output-list": output_list_list}

    def journal_list():

        nonlocal output_list_list, htparam, artikel, hoteldpt, billjournal


        nonlocal output_list
        nonlocal output_list_list

        qty:int = 0
        sub_tot:decimal = 0
        tot:decimal = 0
        curr_date:date = None
        last_dept:int = -1
        it_exist:bool = False
        ekumnr:int = 0
        amount:decimal = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 555)).first()
        ekumnr = finteger
        output_list_list.clear()

        for artikel in db_session.query(Artikel).filter(
                (Artikel.artnr >= from_art) &  (Artikel.artnr <= to_art) &  (Artikel.departement >= from_dept) &  (Artikel.departement <= to_dept) &  (Artikel.endkum != ekumnr)).all():

            if last_dept != artikel.departement:

                hoteldpt = db_session.query(Hoteldpt).filter(
                        (Hoteldpt.num == artikel.departement)).first()
            last_dept = artikel.departement
            sub_tot = 0
            it_exist = False
            qty = 0
            for curr_date in range(from_date,to_date + 1) :

                for billjournal in db_session.query(Billjournal).filter(
                        (Billjournal.stornogrund != "") &  (Billjournal.departement == hoteldpt.num) &  (Billjournal.bill_datum == curr_date) &  (Billjournal.artnr == artikel.artnr)).all():

                    if foreign_flag:
                        amount = billjournal.fremdwaehrng
                    else:
                        amount = billjournal.betrag
                    it_exist = True
                    output_list = Output_list()
                    output_list_list.append(output_list)


                    if not long_digit:
                        STR = to_string(bill_datum) + to_string(hoteldpt.depart, "x(16)") + to_string(billjournal.zinr, "999999") + to_string(rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>>9") + to_string(billjournal.bezeich, "x(24)") + to_string(billjournal.stornogrund, "x(74)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>9.99") + to_string(zeit, "HH:MM") + to_string(billjournal.userinit, "x(3)")
                    else:
                        STR = to_string(bill_datum) + to_string(hoteldpt.depart, "x(16)") + to_string(billjournal.zinr, "999999") + to_string(rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>>9") + to_string(billjournal.bezeich, "x(24)") + to_string(billjournal.stornogrund, "x(74)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, " ->>>,>>>,>>>,>>9") + to_string(zeit, "HH:MM") + to_string(billjournal.userinit, "x(3)")
                    qty = qty + billjournal.anzahl
                    sub_tot = sub_tot + amount
                    tot = tot + amount

            if it_exist:
                output_list = Output_list()
                output_list_list.append(output_list)


                if not long_digit:
                    STR = to_string("", "x(118)") + to_string("T O T A L   ", "x(24)") + to_string(qty, "-9999") + to_string(sub_tot, "->,>>>,>>>,>>9.99")
                else:
                    STR = to_string("", "x(118)") + to_string("T O T A L   ", "x(24)") + to_string(qty, "-9999") + to_string(sub_tot, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_list.append(output_list)


        if not long_digit:
            STR = to_string("", "x(118)") + to_string("Grand TOTAL", "x(24)") + to_string(0, ">>>>>") + to_string(tot, "->,>>>,>>>,>>9.99")
        else:
            STR = to_string("", "x(118)") + to_string("Grand TOTAL", "x(24)") + to_string(0, ">>>>>") + to_string(tot, " ->>>,>>>,>>>,>>9")


    journal_list()

    return generate_output()