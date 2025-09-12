#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 22/8/2025
# adjust string positions to match gl_jouhislist_create_listbl.py
# add fixed length formatting (Oscar suggestion)
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.gl_jouhislist_create_listbl import gl_jouhislist_create_listbl
import os


def format_fixed_length(text: str, length: int) -> str:
    if len(text) > length:
        return text[:length]   # trim
    else:
        return text.ljust(length)

def gl_jouhislist_create_list_webbl(sorttype:int, from_fibu:string, to_fibu:string, from_dept:int, from_date:date, to_date:date, close_year:date):
    t_ouput_list_data = []
    curr_date:date = None
    scurr_date:string = ""

    output_list = t_ouput_list = None

    output_list_data, Output_list = create_model("Output_list", {"marked":string, "fibukonto":string, "jnr":int, "bemerk":string, "str":string})
    t_ouput_list_data, T_ouput_list = create_model("T_ouput_list", {"marked":string, "fibukonto":string, "jnr":int, "bemerk":string, "datum":string, "refno":string, "bezeich":string, "debit":string, "credit":string, "user_init":string, "created":string, "chgid":string, "chgdate":string, "balance":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_ouput_list_data, curr_date, scurr_date
        nonlocal sorttype, from_fibu, to_fibu, from_dept, from_date, to_date, close_year


        nonlocal output_list, t_ouput_list
        nonlocal output_list_data, t_ouput_list_data

        return {"t-ouput-list": t_ouput_list_data}

    output_list_data = get_output(gl_jouhislist_create_listbl(sorttype, from_fibu, to_fibu, from_dept, from_date, to_date, close_year))

    for output_list in query(output_list_data):
        curr_date = date_mdy(to_int(entry(1, substring(output_list.str, 110, 8) , "/")) , to_int(entry(0, substring(output_list.str, 110, 8) , "/")) , to_int(entry(2, substring(output_list.str, 110, 8) , "/")))
        scurr_date = to_string(curr_date, "99/99/9999")


        t_ouput_list = T_ouput_list()
        t_ouput_list_data.append(t_ouput_list)

        t_ouput_list.marked = output_list.marked
        t_ouput_list.fibukonto = output_list.fibukonto
        t_ouput_list.jnr = output_list.jnr
        t_ouput_list.bemerk = output_list.bemerk.replace("\u0002", "")
        t_ouput_list.datum = substring(output_list.str, 0, 8)
        t_ouput_list.refno = substring(output_list.str, 8, 15)
        t_ouput_list.bezeich = substring(output_list.str, 23, 40)
        t_ouput_list.debit = substring(output_list.str, 62, 22)
        t_ouput_list.credit = substring(output_list.str, 84, 21)
        t_ouput_list.balance = substring(output_list.str, 179, 22)
        t_ouput_list.user_init = substring(output_list.str, 105, 3)
        t_ouput_list.created = substring(output_list.str, 108, 8)
        # t_ouput_list.created = scurr_date
        t_ouput_list.chgid = substring(output_list.str, 116, 3)
        t_ouput_list.chgdate = substring(output_list.str, 119, 8)

        t_ouput_list.debit = format_fixed_length(t_ouput_list.debit.strip(), 22)
        t_ouput_list.credit = format_fixed_length(t_ouput_list.credit.strip(), 21)
        t_ouput_list.balance = format_fixed_length(t_ouput_list.balance.strip(), 22)
        t_ouput_list.user_init = format_fixed_length(t_ouput_list.user_init.strip(), 3)
        t_ouput_list.created = format_fixed_length(t_ouput_list.created.strip(), 8)
        t_ouput_list.chgid = format_fixed_length(t_ouput_list.chgid.strip(), 3)

    return generate_output()