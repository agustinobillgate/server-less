from functions.additional_functions import *
import decimal
from datetime import date
from functions.gl_jouhislist_create_listbl import gl_jouhislist_create_listbl

def gl_jouhislist_create_list_webbl(sorttype:int, from_fibu:str, to_fibu:str, from_dept:int, from_date:date, to_date:date, close_year:date):
    t_ouput_list_list = []
    curr_date:date = None
    scurr_date:str = ""

    output_list = t_ouput_list = None

    output_list_list, Output_list = create_model("Output_list", {"marked":str, "fibukonto":str, "jnr":int, "bemerk":str, "str":str})
    t_ouput_list_list, T_ouput_list = create_model("T_ouput_list", {"marked":str, "fibukonto":str, "jnr":int, "bemerk":str, "datum":str, "refno":str, "bezeich":str, "debit":str, "credit":str, "user_init":str, "created":str, "chgid":str, "chgdate":str, "balance":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_ouput_list_list, curr_date, scurr_date
        nonlocal sorttype, from_fibu, to_fibu, from_dept, from_date, to_date, close_year


        nonlocal output_list, t_ouput_list
        nonlocal output_list_list, t_ouput_list_list

        return {"t-ouput-list": t_ouput_list_list}

    output_list_list = get_output(gl_jouhislist_create_listbl(sorttype, from_fibu, to_fibu, from_dept, from_date, to_date, close_year))

    for output_list in query(output_list_list):
        curr_date = date_mdy(to_int(entry(1, substring(output_list.str, 110, 8) , "/")) , to_int(entry(0, substring(output_list.str, 110, 8) , "/")) , to_int(entry(2, substring(output_list.str, 110, 8) , "/")))
        scurr_date = to_string(curr_date, "99/99/9999")


        t_ouput_list = T_ouput_list()
        t_ouput_list_list.append(t_ouput_list)

        t_ouput_list.marked = output_list.marked
        t_ouput_list.fibukonto = output_list.fibukonto
        t_ouput_list.jnr = output_list.jnr
        t_ouput_list.bemerk = output_list.bemerk
        t_ouput_list.datum = substring(output_list.str, 0, 8)
        t_ouput_list.refno = substring(output_list.str, 8, 15)
        t_ouput_list.bezeich = substring(output_list.str, 23, 40)
        t_ouput_list.debit = substring(output_list.str, 63, 22)
        t_ouput_list.credit = substring(output_list.str, 85, 22)
        t_ouput_list.balance = substring(output_list.str, 179, 22)
        t_ouput_list.user_init = substring(output_list.str, 107, 3)
        t_ouput_list.created = scurr_date
        t_ouput_list.chgid = substring(output_list.str, 118, 3)
        t_ouput_list.chgdate = substring(output_list.str, 121, 8)

    return generate_output()