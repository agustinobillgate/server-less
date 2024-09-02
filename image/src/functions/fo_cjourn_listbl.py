from functions.additional_functions import *
import decimal
from datetime import date
from functions.fo_cjournbl import fo_cjournbl

def fo_cjourn_listbl(from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, foreign_flag:bool, long_digit:bool):
    cjourn_list_list = []

    output_list = cjourn_list = None

    output_list_list, Output_list = create_model("Output_list", {"str":str})
    cjourn_list_list, Cjourn_list = create_model("Cjourn_list", {"artnr":int, "bezeich":str, "dept":str, "datum":date, "zinr":str, "rechnr":int, "canc_reason":str, "qty":int, "amount":decimal, "zeit":str, "id":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cjourn_list_list


        nonlocal output_list, cjourn_list
        nonlocal output_list_list, cjourn_list_list
        return {"cjourn-list": cjourn_list_list}

    output_list_list = get_output(fo_cjournbl(from_art, to_art, from_dept, to_dept, from_date, to_date, foreign_flag, long_digit))
    cjourn_list_list.clear()

    for output_list in query(output_list_list):
        cjourn_list = Cjourn_list()
        cjourn_list_list.append(cjourn_list)

        cjourn_list.artnr = to_int(substring(output_list.STR, 39, 5))
        cjourn_list.bezeich = substring(output_list.STR, 44, 24)
        cjourn_list.dept = substring(output_list.STR, 8, 16)
        cjourn_list.datum = date_mdy(substring(output_list.STR, 0, 8))
        cjourn_list.zinr = substring(output_list.STR, 24, 6)
        cjourn_list.rechnr = to_int(substring(output_list.STR, 30, 9))
        cjourn_list.canc_reason = substring(output_list.STR, 68, 24)
        cjourn_list.qty = to_int(substring(output_list.STR, 92, 5))
        cjourn_list.amount = decimal.Decimal(substring(output_list.STR, 97, 17))
        cjourn_list.zeit = substring(output_list.STR, 114, 5)
        cjourn_list.ID = substring(output_list.STR, 119, 3)

    return generate_output()