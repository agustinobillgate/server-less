from functions.additional_functions import *
import decimal
from datetime import date
from models import Exrate

g_list_list, G_list = create_model("G_list", {"monat":int, "wert":decimal, "datum":date})

def budget_exrate_update_exratebl(g_list_list:[G_list]):
    exrate = None

    g_list = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal exrate


        nonlocal g_list
        nonlocal g_list_list
        return {}

    def update_exrate():

        nonlocal exrate


        nonlocal g_list
        nonlocal g_list_list

        i:int = 0
        curr_date:date = None

        for g_list in query(g_list_list):

            exrate = db_session.query(Exrate).filter(
                     (Exrate.artnr == 99998) & (Exrate.datum == g_list.datum)).first()

            if not exrate:
                exrate = Exrate()
                db_session.add(exrate)

                exrate.artnr = 99998
                exrate.datum = g_list.datum
                exrate.betrag =  to_decimal("1")

            if g_list.wert != 0:
                exrate.betrag =  to_decimal(g_list.wert)

    update_exrate()

    return generate_output()