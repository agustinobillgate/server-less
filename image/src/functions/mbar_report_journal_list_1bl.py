from functions.additional_functions import *
import decimal
from datetime import date
from functions.mbar_report_journal_listbl import mbar_report_journal_listbl

def mbar_report_journal_list_1bl(from_date:date, to_date:date, curr_dept:int, long_digit:bool):
    roomtransreportlist_list = []

    output_list = roomtransreportlist = None

    output_list_list, Output_list = create_model("Output_list", {"rechnr":int, "dept":int, "datum":date, "str":str})
    roomtransreportlist_list, Roomtransreportlist = create_model("Roomtransreportlist", {"rechnr":int, "dept":int, "datum":date, "rmno":str, "gname":str, "bezeich":str, "saldo":decimal, "foreign":decimal, "zeit":str, "id":str, "tb":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal roomtransreportlist_list


        nonlocal output_list, roomtransreportlist
        nonlocal output_list_list, roomtransreportlist_list
        return {"roomtransreportlist": roomtransreportlist_list}

    output_list_list = get_output(mbar_report_journal_listbl(from_date, to_date, curr_dept, long_digit))
    roomtransreportlist._list.clear()

    for output_list in query(output_list_list):
        roomtransreportlist = Roomtransreportlist()
        roomtransreportlist_list.append(roomtransreportlist)

        roomtransreportlist.rechnr = output_list.rechnr
        roomtransreportlist.dept = output_list.dept
        roomtransreportlist.datum = output_list.datum
        roomtransreportlist.rmno = substring(output_list.str, 8, 6)
        roomtransreportlist.gname = substring(output_list.str, 14, 24)
        roomtransreportlist.bezeich = substring(output_list.str, 47, 24)
        roomtransreportlist.saldo = decimal.Decimal(substring(output_list.str, 71, 14))
        roomtransreportlist.foreign = decimal.Decimal(substring(output_list.str, 85, 14))
        roomtransreportlist.zeit = substring(output_list.str, 99, 5)
        roomtransreportlist.id = substring(output_list.str, 104, 3)
        roomtransreportlist.tb = substring(output_list.str, 107, 3)

    return generate_output()