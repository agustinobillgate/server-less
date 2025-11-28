#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added, skip (remark)
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Budget

def delete_budgetbl(case_type:int, int1:int, int2:int, date1:date):
    success_flag = False
    budget = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, budget
        nonlocal case_type, int1, int2, date1

        return {"success_flag": success_flag}


    if case_type == 1:

        # budget = get_cache (Budget, {"artnr": [(eq, int1)],"departement": [(eq, int2)],"datum": [(eq, date1)]})
        budget = db_session.query(Budget).filter(
                    (Budget.artnr == int1) &
                    (Budget.departement == int2) &
                    (Budget.datum == date1)
                ).with_for_update().first()

        if budget:
            db_session.delete(budget)
            pass
            success_flag = True

    return generate_output()