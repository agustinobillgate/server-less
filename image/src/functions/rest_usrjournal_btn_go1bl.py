from functions.additional_functions import *
import decimal
from datetime import date
from functions.rest_usrjournal_btn_gobl import rest_usrjournal_btn_gobl

def rest_usrjournal_btn_go1bl(sumflag:bool, from_date:date, to_date:date, usr_init:str, curr_dept:int, price_decimal:int):
    rest_jour_list_list = []

    output_list = rest_jour_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})
    rest_jour_list_list, Rest_jour_list = create_model("Rest_jour_list", {"datum":date, "tabelno":str, "billno":int, "artno":int, "descr":str, "qty":int, "amount":decimal, "depart":str, "zeit":str, "id":str, "tb":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rest_jour_list_list


        nonlocal output_list, rest_jour_list
        nonlocal output_list_list, rest_jour_list_list
        return {"rest-jour-list": rest_jour_list_list}

    output_list_list = get_output(rest_usrjournal_btn_gobl(sumflag, from_date, to_date, usr_init, curr_dept, price_decimal))

    for rest_jour_list in query(rest_jour_list_list):
        rest_jour_list_list.remove(rest_jour_list)

    for output_list in query(output_list_list):
        rest_jour_list = Rest_jour_list()
        rest_jour_list_list.append(rest_jour_list)

        rest_jour_list.datum = date (substring(STR, 0, 8))
        rest_jour_list.tabelno = substring(STR, 8, 4)
        rest_jour_list.billno = to_int(substring(STR, 12, 9))
        rest_jour_list.artno = to_int(substring(STR, 21, 5))
        rest_jour_list.descr = substring(STR, 26, 28)
        rest_jour_list.qty = to_int(substring(STR, 66, 5))
        rest_jour_list.amount = decimal (substring(STR, 71, 17))
        rest_jour_list.depart = substring(STR, 54, 12)
        rest_jour_list.zeit = substring(STR, 88, 5)
        rest_jour_list.id = substring(STR, 93, 3)
        rest_jour_list.tb = substring(STR, 96, 3)

    return generate_output()