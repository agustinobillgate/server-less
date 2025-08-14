#using conversion tools version: 1.0.0.117

#Rulita 140825 49F8AD | Modify format date output param datetime_server MM/DD/YY format


from functions.additional_functions import *
from decimal import Decimal
from datetime import date

def load_datetime_serverbl():
    datetime_server = ""
    bill_date:date = None
    curr_zeit:int = 0

    #Rulita 49F8AD
    tmp_dd:string = ""
    tmp_mm:string = ""
    tmp_yy:string = ""

    db_session = local_storage.db_session

    def generate_output():
        nonlocal datetime_server, bill_date, curr_zeit, tmp_dd, tmp_mm, tmp_yy

        return {"datetime_server": datetime_server}

    curr_zeit = get_current_time_in_seconds()

    #Rulita 49F8AD
    tmp_dd = to_string(get_day(get_current_date()) , "99")
    tmp_mm = to_string(get_month(get_current_date()) , "99")
    tmp_yy = substring(to_string(get_year(get_current_date())) , 2)

    #Rulita 49F8AD
    datetime_server = tmp_mm + "/" + tmp_dd + "/" + tmp_yy + " " + to_string(curr_zeit, "HH:MM:SS")

    return generate_output()