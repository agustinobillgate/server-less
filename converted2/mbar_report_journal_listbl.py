#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from models import H_journal, H_bill, Bill, Res_line

def mbar_report_journal_listbl(from_date:date, to_date:date, curr_dept:int, long_digit:bool):

    prepare_cache ([H_journal, Bill, Res_line])

    output_list_data = []
    h_journal = h_bill = bill = res_line = None

    output_list = None

    output_list_data, Output_list = create_model("Output_list", {"rechnr":int, "dept":int, "datum":date, "str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, h_journal, h_bill, bill, res_line
        nonlocal from_date, to_date, curr_dept, long_digit


        nonlocal output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def journal_list():

        nonlocal output_list_data, h_journal, h_bill, bill, res_line
        nonlocal from_date, to_date, curr_dept, long_digit


        nonlocal output_list
        nonlocal output_list_data

        qty:int = 0
        tot:Decimal = to_decimal("0.0")
        tot_foreign:Decimal = to_decimal("0.0")
        curr_date:date = None
        rmno:string = ""
        billno:int = 0
        gname:string = ""
        rm_flag:bool = False
        ct:string = ""
        deci_place:int = 0
        h_journal_rechnr:string = ""
        h_journal_fremdwaehrng:string = ""
        h_journal_kellner_nr:string = ""
        h_journal_tischnr:string = ""
        tmp_betrag:string = ""
        tmp_tot:string = ""
        tmp_tot_foreign:string = ""
        deci_place = get_output(htpint(491))
        output_list_data.clear()
        for curr_date in date_range(from_date,to_date) :

            for h_journal in db_session.query(H_journal).filter(
                     (H_journal.departement == curr_dept) & (H_journal.bill_datum == curr_date)).order_by(H_journal.artnr, H_journal.sysdate, H_journal.zeit).all():

                h_bill = get_cache (H_bill, {"rechnr": [(eq, h_journal.rechnr)],"departement": [(eq, h_journal.departement)]})
                rm_flag = False

                if substring(h_journal.bezeich, 0, 4) == ("rmno").lower() :
                    rm_flag = True
                    ct = substring(h_journal.bezeich, 5)
                    rmno = trim(entry(0, ct, "*"))
                    billno = to_int(trim(entry(1, ct, "*")))

                elif substring(h_journal.bezeich, 6, 4) == ("rmno").lower() :
                    rm_flag = True
                    rmno = trim(substring(h_journal.bezeich, 11, 4))

                    if substring(rmno, 3, 1) == ("*").lower()  or length(rmno) == 3:
                        rmno = substring(rmno, 0, 3)
                        billno = to_int(substring(h_journal.bezeich, 15, 10))
                    else:
                        billno = to_int(substring(h_journal.bezeich, 16, 10))

                if h_journal.artnr == 0 and rm_flag:

                    bill = get_cache (Bill, {"rechnr": [(eq, billno)]})

                    if bill:

                        res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

                    if res_line:
                        gname = res_line.name
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    output_list.rechnr = h_journal.rechnr
                    output_list.dept = h_journal.departement
                    output_list.datum = h_journal.bill_datum

                    if deci_place == 0:
                        h_journal_rechnr = to_string(h_journal.rechnr, ">,>>>,>>9")
                        tmp_betrag = to_string(- betrag, "->,>>>,>>>,>>9")
                        h_journal_fremdwaehrng = to_string(- h_journal.fremdwaehrng, "->>,>>>,>>9.99")
                        h_journal_kellner_nr = to_string(h_journal.kellner_nr, "999")
                        h_journal_tischnr = to_string(h_journal.tischnr, ">>>>>9")
                        output_list.str = to_string(bill_datum) + to_string(rmno, "x(6)") + to_string(gname, "x(24)") + to_string(h_journal_rechnr, "x(9)") + to_string(h_journal.bezeich, "x(24)") + to_string(tmp_betrag, "x(14)") + to_string(h_journal_fremdwaehrng, "x(14)") + to_string(zeit, "HH:MM") + to_string(h_journal_kellner_nr, "x(3)") + to_string(h_journal_tischnr, "x(6)")
                    else:
                        h_journal_rechnr = to_string(h_journal.rechnr, ">,>>>,>>9")
                        tmp_betrag = to_string(- betrag, "->>,>>>,>>9.99")
                        h_journal_fremdwaehrng = to_string(- h_journal.fremdwaehrng, "->>,>>>,>>9.99")
                        h_journal_kellner_nr = to_string(h_journal.kellner_nr, "999")
                        h_journal_tischnr = to_string(h_journal.tischnr, ">>>>>9")
                        output_list.str = to_string(bill_datum) + to_string(rmno, "x(6)") + to_string(gname, "x(24)") + to_string(h_journal_rechnr, "x(9)") + to_string(h_journal.bezeich, "x(24)") + to_string(tmp_betrag, "x(14)") + to_string(h_journal_fremdwaehrng, "x(14)") + to_string(zeit, "HH:MM") + to_string(h_journal_kellner_nr, "x(3)") + to_string(h_journal_tischnr, "x(6)")
                        qty = qty + h_journal.anzahl
                        tot =  to_decimal(tot) - to_decimal(h_journal.betrag)
                        tot_foreign =  to_decimal(tot_foreign) - to_decimal(h_journal.fremdwaehrng)
        output_list = Output_list()
        output_list_data.append(output_list)


        if deci_place == 0:
            tmp_tot = to_string(tot, "->,>>>,>>>,>>9")
            tmp_tot_foreign = to_string(tot_foreign, "->>,>>>,>>9.99")
            output_list.str = to_string("", "x(47)") + to_string("T O T A L ", "x(24)") + to_string(tmp_tot, "x(14)") + to_string(tmp_tot_foreign, "x(14)")
        else:
            tmp_tot = to_string(tot, "->>,>>>,>>9.99")
            tmp_tot_foreign = to_string(tot_foreign, "->>,>>>,>>9.99")
            output_list.str = to_string("", "x(47)") + to_string("T O T A L ", "x(24)") + to_string(tmp_tot, "x(14)") + to_string(tmp_tot_foreign, "x(14)")

    journal_list()

    return generate_output()