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
from functions.rest_usrjournal_btn_cldbl import rest_usrjournal_btn_cldbl

log_debug = []
def rest_usrjournal_btn_go1bl(sumflag:bool, from_date:date, to_date:date, usr_init:string, curr_dept:int, price_decimal:int):
    rest_jour_list_data = []
    monthpart:string = ""
    daypart:string = ""
    yearpart:string = ""
    fullyear:int = 0
    date_flag:bool = False

    output_list = rest_jour_list = None

    output_list_data, Output_list = create_model("Output_list", {"bezeich":string, "str":string})
    rest_jour_list_data, Rest_jour_list = create_model("Rest_jour_list", {"datum":date, "tabelno":string, "billno":int, "artno":int, "descr":string, "qty":int, "amount":Decimal, "depart":string, "zeit":string, "id":string, "tb":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rest_jour_list_data, monthpart, daypart, yearpart, fullyear, date_flag
        nonlocal sumflag, from_date, to_date, usr_init, curr_dept, price_decimal


        nonlocal output_list, rest_jour_list
        nonlocal output_list_data, rest_jour_list_data

        return {"log": log_debug, "rest-jour-list": rest_jour_list_data}

    log_debug, output_list_data = get_output(rest_usrjournal_btn_cldbl(sumflag, from_date, to_date, usr_init, curr_dept, price_decimal))

    for rest_jour_list in query(rest_jour_list_data):
        rest_jour_list_data.remove(rest_jour_list)

    for output_list in query(output_list_data):
        monthpart = substring(substring(output_list.str, 0, 8) , 0, 2)
        daypart = substring(substring(output_list.str, 0, 8) , 3, 2)
        yearpart = substring(substring(output_list.str, 0, 8) , 6, 2)

        if monthpart == "" and daypart == "" and yearpart == "":
            date_flag = True

        if to_int(yearpart) < 50:
            fullyear = 2000 + to_int(yearpart)
        else:
            fullyear = 1900 + to_int(yearpart)

        if not date_flag:
            rest_jour_list = Rest_jour_list()
            rest_jour_list_data.append(rest_jour_list)

            rest_jour_list.datum = date_mdy(to_int(monthpart) , to_int(daypart) , fullyear)
            rest_jour_list.tabelno = substring(output_list.str, 8, 6)
            rest_jour_list.billno = to_int(substring(output_list.str, 14, 9))
            rest_jour_list.artno = to_int(substring(output_list.str, 23, 9))
            rest_jour_list.descr = output_list.bezeich
            rest_jour_list.qty = to_int(substring(output_list.str, 72, 5))

            # Rd 21/7/2025
            try:
                rest_jour_list.amount = to_decimal(substring(output_list.str, 77, 17))
            except:
                rest_jour_list.amount = 0
                
            rest_jour_list.depart = substring(output_list.str, 60, 12)
            rest_jour_list.zeit = substring(output_list.str, 94, 5)
            rest_jour_list.id = substring(output_list.str, 99, 5)
            rest_jour_list.tb = substring(output_list.str, 104, 5)


        else:
            rest_jour_list = Rest_jour_list()
            rest_jour_list_data.append(rest_jour_list)

            rest_jour_list.descr = "TOTAL"
            rest_jour_list.qty = to_int(substring(output_list.str, 72, 5))
            rest_jour_list.amount = to_decimal(substring(output_list.str, 77, 17))

    return generate_output()