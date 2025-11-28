#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added, skip (remark)
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Budget

del_list_data, Del_list = create_model("Del_list", {"int1":int, "int2":int, "date1":date})

def delete_budget_webbl(case_type:int, del_list_data:[Del_list]):
    success_flag = False
    budget = None

    del_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, budget
        nonlocal case_type


        nonlocal del_list

        return {"success_flag": success_flag}

    if case_type == 1:

        for del_list in query(del_list_data, sort_by=[("int1",False)]):

            # budget = get_cache (Budget, {"artnr": [(eq, del_list.int1)],"departement": [(eq, del_list.int2)],"datum": [(eq, del_list.date1)]})
            budget = db_session.query(Budget).filter(
                        (Budget.artnr == del_list.int1) &
                        (Budget.departement == del_list.int2) &
                        (Budget.datum == del_list.date1)
                    ).with_for_update().first()

            if budget:
                db_session.delete(budget)
                pass
                success_flag = True

    return generate_output()