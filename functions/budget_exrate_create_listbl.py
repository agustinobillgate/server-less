#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Exrate

def budget_exrate_create_listbl(curr_year:int):

    prepare_cache ([Exrate])

    g_list_data = []
    exrate = None

    g_list = None

    g_list_data, G_list = create_model("G_list", {"monat":int, "wert":Decimal, "datum":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal g_list_data, exrate
        nonlocal curr_year


        nonlocal g_list
        nonlocal g_list_data

        return {"g-list": g_list_data}

    def create_list():

        nonlocal g_list_data, exrate
        nonlocal curr_year


        nonlocal g_list
        nonlocal g_list_data

        i:int = 0
        curr_date:date = None
        g_list_data.clear()
        for i in range(1,12 + 1) :
            curr_date = date_mdy(i, 1, curr_year) + timedelta(days=35)
            curr_date = date_mdy(get_month(curr_date) , 1, curr_year) - timedelta(days=1)


            g_list = G_list()
            g_list_data.append(g_list)

            g_list.monat = i
            g_list.wert =  to_decimal("1")
            g_list.datum = curr_date

            exrate = get_cache (Exrate, {"artnr": [(eq, 99998)],"datum": [(eq, curr_date)]})

            if exrate:
                g_list.wert =  to_decimal(exrate.betrag)

    create_list()

    return generate_output()