#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Artikel, Hoteldpt, Billjournal

def fo_cjournbl(from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, foreign_flag:bool, long_digit:bool):

    prepare_cache ([Htparam, Artikel, Hoteldpt, Billjournal])

    output_list_data = []
    htparam = artikel = hoteldpt = billjournal = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, htparam, artikel, hoteldpt, billjournal
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, foreign_flag, long_digit


        nonlocal output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def journal_list():

        nonlocal output_list_data, htparam, artikel, hoteldpt, billjournal
        nonlocal from_art, to_art, from_dept, to_dept, from_date, to_date, foreign_flag, long_digit


        nonlocal output_list
        nonlocal output_list_data

        qty:int = 0
        sub_tot:Decimal = to_decimal("0.0")
        tot:Decimal = to_decimal("0.0")
        curr_date:date = None
        last_dept:int = -1
        it_exist:bool = False
        ekumnr:int = 0
        amount:Decimal = to_decimal("0.0")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 555)]})
        ekumnr = htparam.finteger
        output_list_data.clear()

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.artnr >= from_art) & (Artikel.artnr <= to_art) & (Artikel.departement >= from_dept) & (Artikel.departement <= to_dept) & (Artikel.endkum != ekumnr)).order_by((Artikel.departement * 10000 + Artikel.artnr)).all():

            if last_dept != artikel.departement:

                hoteldpt = get_cache (Hoteldpt, {"num": [(eq, artikel.departement)]})
            last_dept = artikel.departement
            sub_tot =  to_decimal("0")
            it_exist = False
            qty = 0
            for curr_date in date_range(from_date,to_date) :

                for billjournal in db_session.query(Billjournal).filter(
                         (Billjournal.stornogrund != "") & (Billjournal.departement == hoteldpt.num) & (Billjournal.bill_datum == curr_date) & (Billjournal.artnr == artikel.artnr)).order_by(Billjournal.sysdate, Billjournal.zeit).all():

                    if foreign_flag:
                        amount =  to_decimal(billjournal.fremdwaehrng)
                    else:
                        amount =  to_decimal(billjournal.betrag)
                    it_exist = True
                    output_list = Output_list()
                    output_list_data.append(output_list)


                    if not long_digit:
                        output_list.str = to_string(billjournal.bill_datum) + to_string(hoteldpt.depart, "x(16)") + to_string(billjournal.zinr, "999999") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>>9") + to_string(billjournal.bezeich, "x(24)") + to_string(billjournal.stornogrund, "x(74)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, "->,>>>,>>>,>>9.99") + to_string(billjournal.zeit, "HH:MM") + to_string(billjournal.userinit, "x(3)")
                    else:
                        output_list.str = to_string(billjournal.bill_datum) + to_string(hoteldpt.depart, "x(16)") + to_string(billjournal.zinr, "999999") + to_string(billjournal.rechnr, ">>>>>>>>9") + to_string(billjournal.artnr, ">>>>9") + to_string(billjournal.bezeich, "x(24)") + to_string(billjournal.stornogrund, "x(74)") + to_string(billjournal.anzahl, "-9999") + to_string(amount, " ->>>,>>>,>>>,>>9") + to_string(billjournal.zeit, "HH:MM") + to_string(billjournal.userinit, "x(3)")
                    qty = qty + billjournal.anzahl
                    sub_tot =  to_decimal(sub_tot) + to_decimal(amount)
                    tot =  to_decimal(tot) + to_decimal(amount)

            if it_exist:
                output_list = Output_list()
                output_list_data.append(output_list)


                if not long_digit:
                    output_list.str = to_string("", "x(118)") + to_string("T O T A L ", "x(24)") + to_string(qty, "-9999") + to_string(sub_tot, "->,>>>,>>>,>>9.99")
                else:
                    output_list.str = to_string("", "x(118)") + to_string("T O T A L ", "x(24)") + to_string(qty, "-9999") + to_string(sub_tot, " ->>>,>>>,>>>,>>9")
        output_list = Output_list()
        output_list_data.append(output_list)


        if not long_digit:
            output_list.str = to_string("", "x(118)") + to_string("Grand TOTAL", "x(24)") + to_string(0, ">>>>>") + to_string(tot, "->,>>>,>>>,>>9.99")
        else:
            output_list.str = to_string("", "x(118)") + to_string("Grand TOTAL", "x(24)") + to_string(0, ">>>>>") + to_string(tot, " ->>>,>>>,>>>,>>9")

    journal_list()

    return generate_output()