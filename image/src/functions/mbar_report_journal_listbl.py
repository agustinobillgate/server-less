from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from models import H_journal, H_bill, Bill, Res_line

def mbar_report_journal_listbl(from_date:date, to_date:date, curr_dept:int, long_digit:bool):
    output_list_list = []
    h_journal = h_bill = bill = res_line = None

    output_list = None

    output_list_list, Output_list = create_model("Output_list", {"rechnr":int, "dept":int, "datum":date, "str":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, h_journal, h_bill, bill, res_line


        nonlocal output_list
        nonlocal output_list_list
        return {"output-list": output_list_list}

    def journal_list():

        nonlocal output_list_list, h_journal, h_bill, bill, res_line


        nonlocal output_list
        nonlocal output_list_list

        qty:int = 0
        tot:decimal = 0
        tot_foreign:decimal = 0
        curr_date:date = None
        rmno:str = ""
        billno:int = 0
        gname:str = ""
        rm_flag:bool = False
        ct:str = ""
        deci_place:int = 0
        deci_place = get_output(htpint(491))
        output_list_list.clear()
        for curr_date in range(from_date,to_date + 1) :

            for h_journal in db_session.query(H_journal).filter(
                    (H_journal.departement == curr_dept) &  (H_journal.bill_datum == curr_date)).all():

                h_bill = db_session.query(H_bill).filter(
                        (H_bill.rechnr == h_journal.rechnr) &  (H_bill.departement == h_journal.departement)).first()
                rm_flag = False

                if substring(h_journal.bezeich, 0, 4) == "rmno":
                    rm_flag = True
                    ct = substring(h_journal.bezeich, 5)
                    rmno = trim(entry(0, ct, "*"))
                    billno = to_int(trim(entry(1, ct, "*")))

                elif substring(h_journal.bezeich, 6, 4) == "rmno":
                    rm_flag = True
                    rmno = trim(substring(h_journal.bezeich, 11, 4))

                    if substring(rmno, 3, 1) == "*" or len(rmno) == 3:
                        rmno = substring(rmno, 0, 3)
                        billno = to_int(substring(h_journal.bezeich, 15, 10))
                    else:
                        billno = to_int(substring(h_journal.bezeich, 16, 10))

                if h_journal.artnr == 0 and rm_flag:

                    bill = db_session.query(Bill).filter(
                            (Bill.rechnr == billno)).first()

                    if bill:

                        res_line = db_session.query(Res_line).filter(
                                (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr)).first()

                    if res_line:
                        gname = res_line.name
                    output_list = Output_list()
                    output_list_list.append(output_list)

                    output_list.rechnr = h_journal.rechnr
                    output_list.dept = h_journal.departement
                    output_list.datum = h_journal.bill_datum

                    if deci_place == 0:
                        STR = to_string(bill_datum) + to_string(rmno, "x(6)") + to_string(gname, "x(24)") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.bezeich, "x(24)") + to_string(- betrag, "->,>>>,>>>,>>9") + to_string(- h_journal.fremdwaehrng, "->>,>>>,>>9.99") + to_string(zeit, "HH:MM") + to_string(h_journal.kellner_nr, "999") + to_string(h_journal.tischnr, ">>>>>9")
                    else:
                        STR = to_string(bill_datum) + to_string(rmno, "x(6)") + to_string(gname, "x(24)") + to_string(h_journal.rechnr, ">,>>>,>>9") + to_string(h_journal.bezeich, "x(24)") + to_string(- betrag, "->>,>>>,>>9.99") + to_string(- h_journal.fremdwaehrng, "->>,>>>,>>9.99") + to_string(zeit, "HH:MM") + to_string(h_journal.kellner_nr, "999") + to_string(h_journal.tischnr, ">>>>>9")
                    qty = qty + h_journal.anzahl
                    tot = tot - h_journal.betrag
                    tot_foreign = tot_foreign - h_journal.fremdwaehrng
        output_list = Output_list()
        output_list_list.append(output_list)


        if deci_place == 0:
            STR = to_string("", "x(47)") + to_string("T O T A L   ", "x(24)") + to_string(tot, "->,>>>,>>>,>>9") + to_string(tot_foreign, "->>,>>>,>>9.99")
        else:
            STR = to_string("", "x(47)") + to_string("T O T A L   ", "x(24)") + to_string(tot, "->>,>>>,>>9.99") + to_string(tot_foreign, "->>,>>>,>>9.99")


    journal_list()

    return generate_output()