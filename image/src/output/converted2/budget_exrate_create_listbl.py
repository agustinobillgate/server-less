from functions.additional_functions import *
import decimal
from datetime import date
from models import Exrate

def budget_exrate_create_listbl(curr_year:int):
    g_list_list = []
    exrate = None

    g_list = None

    g_list_list, G_list = create_model("G_list", {"monat":int, "wert":decimal, "datum":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal g_list_list, exrate
        nonlocal curr_year


        nonlocal g_list
        nonlocal g_list_list
        return {"g-list": g_list_list}

    def create_list():

        nonlocal g_list_list, exrate
        nonlocal curr_year


        nonlocal g_list
        nonlocal g_list_list

        i:int = 0
        curr_date:date = None
        g_list_list.clear()
        for i in range(1,12 + 1) :
            curr_date = date_mdy(i, 1, curr_year) + timedelta(days=35)
            curr_date = date_mdy(get_month(curr_date) , 1, curr_year) - timedelta(days=1)


            g_list = G_list()
            g_list_list.append(g_list)

            g_list.monat = i
            g_list.wert =  to_decimal("1")
            g_list.datum = curr_date

            exrate = db_session.query(Exrate).filter(
                     (Exrate.artnr == 99998) & (Exrate.datum == curr_date)).first()

            if exrate:
                g_list.wert =  to_decimal(exrate.betrag)

    create_list()

    return generate_output()