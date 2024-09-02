from functions.additional_functions import *
import decimal
from datetime import date
from models import Budget

def delete_budgetbl(case_type:int, int1:int, int2:int, date1:date):
    success_flag = False
    budget = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, budget


        return {"success_flag": success_flag}


    if case_type == 1:

        budget = db_session.query(Budget).filter(
                (Budget.artnr == int1) &  (Budget.departement == int2) &  (Budget.datum == date1)).first()

        if budget:
            db_session.delete(budget)

            success_flag = True

    return generate_output()