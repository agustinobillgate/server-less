#using conversion tools version: 1.0.0.117
#--------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#--------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Exrate

g_list_data, G_list = create_model("G_list", {"monat":int, "wert":Decimal, "datum":date})

def budget_exrate_update_exratebl(g_list_data:[G_list]):

    prepare_cache ([Exrate])
    exrate = None
    g_list = None
    db_session = local_storage.db_session

    def generate_output():
        nonlocal exrate
        nonlocal g_list

        return {}

    def update_exrate():
        nonlocal exrate
        nonlocal g_list

        i:int = 0
        curr_date:date = None

        for g_list in query(g_list_data):
            # Rd, 24/11/2025, get exrate dengan for update
            # exrate = get_cache (Exrate, {"artnr": [(eq, 99998)],"datum": [(eq, g_list.datum)]})
            exrate = db_session.query(Exrate).filter(
                         (Exrate.artnr == 99998) &
                         (Exrate.datum == g_list.datum)).with_for_update().first()

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