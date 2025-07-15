#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.mbar_report_journal_listbl import mbar_report_journal_listbl

def mbar_report_journal_list_1bl(from_date:date, to_date:date, curr_dept:int, long_digit:bool):
    roomtransreportlist_data = []

    output_list = roomtransreportlist = None

    output_list_data, Output_list = create_model("Output_list", {"rechnr":int, "dept":int, "datum":date, "str":string})
    roomtransreportlist_data, Roomtransreportlist = create_model("Roomtransreportlist", {"rechnr":int, "dept":int, "datum":date, "rmno":string, "gname":string, "bezeich":string, "saldo":Decimal, "foreign":Decimal, "zeit":string, "id":string, "tb":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal roomtransreportlist_data
        nonlocal from_date, to_date, curr_dept, long_digit


        nonlocal output_list, roomtransreportlist
        nonlocal output_list_data, roomtransreportlist_data

        return {"roomtransreportlist": roomtransreportlist_data}

    output_list_data = get_output(mbar_report_journal_listbl(from_date, to_date, curr_dept, long_digit))
    roomtransreportlist_data.clear()

    for output_list in query(output_list_data):
        roomtransreportlist = Roomtransreportlist()
        roomtransreportlist_data.append(roomtransreportlist)

        roomtransreportlist.rechnr = output_list.rechnr
        roomtransreportlist.dept = output_list.dept
        roomtransreportlist.datum = output_list.datum
        roomtransreportlist.rmno = substring(output_list.str, 8, 6)
        roomtransreportlist.gname = substring(output_list.str, 14, 24)
        roomtransreportlist.bezeich = substring(output_list.str, 47, 24)
        roomtransreportlist.saldo = to_decimal(substring(output_list.str, 71, 14))
        roomtransreportlist.foreign = to_decimal(substring(output_list.str, 85, 14))
        roomtransreportlist.zeit = substring(output_list.str, 99, 5)
        roomtransreportlist.id = substring(output_list.str, 104, 3)
        roomtransreportlist.tb = substring(output_list.str, 107, 3)

    return generate_output()