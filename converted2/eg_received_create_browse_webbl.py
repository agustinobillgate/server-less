#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_budget

res_data, Res = create_model("Res", {"res_nr":int, "res_nm":string, "res_selected":bool})
t_eg_budget_data, T_eg_budget = create_model_like(Eg_budget)

def eg_received_create_browse_webbl(case_type:int, curr_year:int, intres:int, res_data:[Res], t_eg_budget_data:[T_eg_budget]):
    tbudget_data = []
    sbudget_data = []
    i:int = 0
    month_list:List[string] = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    eg_budget = None

    t_eg_budget = res = tbudget = sbudget = None

    tbudget_data, Tbudget = create_model("Tbudget", {"res_nr":int, "year":int, "month":int, "strmonth":string, "amount":Decimal})
    sbudget_data, Sbudget = create_model("Sbudget", {"res_nr":int, "year":int, "month":int, "strmonth":string, "amount":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tbudget_data, sbudget_data, i, month_list, eg_budget
        nonlocal case_type, curr_year, intres


        nonlocal t_eg_budget, res, tbudget, sbudget
        nonlocal tbudget_data, sbudget_data

        return {"tbudget": tbudget_data, "sbudget": sbudget_data}

    def create_budget():

        nonlocal tbudget_data, sbudget_data, i, month_list, eg_budget
        nonlocal case_type, curr_year, intres


        nonlocal t_eg_budget, res, tbudget, sbudget
        nonlocal tbudget_data, sbudget_data

        s:int = 0
        tamount:int = 0
        s = curr_year
        tbudget_data.clear()

        if s == None:
            pass
        else:

            for res in query(res_data):
                i = 1
                while i <= 12:

                    t_eg_budget = query(t_eg_budget_data, filters=(lambda t_eg_budget: t_eg_budget.nr == res.res_nr and t_eg_budget.year == s and t_eg_budget.month == i), first=True)

                    if t_eg_budget:
                        tamount = t_eg_budget.score
                    else:
                        tamount = 0
                    tbudget = Tbudget()
                    tbudget_data.append(tbudget)

                    tbudget.res_nr = res.res_nr
                    tbudget.year = s
                    tbudget.month = i
                    tbudget.strmonth = month_list[i - 1]
                    tbudget.amount =  to_decimal(tamount)


                    i = i + 1


    def create_get_budget():

        nonlocal tbudget_data, sbudget_data, i, month_list, eg_budget
        nonlocal case_type, curr_year, intres


        nonlocal t_eg_budget, res, tbudget, sbudget
        nonlocal tbudget_data, sbudget_data

        samount:int = 0
        sbudget_data.clear()
        i = 1
        while i <= 12:

            t_eg_budget = query(t_eg_budget_data, filters=(lambda t_eg_budget: t_eg_budget.nr == intres and t_eg_budget.year == curr_year and t_eg_budget.month == i), first=True)

            if t_eg_budget:
                samount = t_eg_budget.score
            else:
                samount = 0
            sbudget = Sbudget()
            sbudget_data.append(sbudget)

            sbudget.res_nr = intres
            sbudget.year = curr_year
            sbudget.month = i
            sbudget.strmonth = month_list[i - 1]
            sbudget.amount =  to_decimal(samount)


            i = i + 1

    if case_type == 1:
        create_budget()

    elif case_type == 2:
        create_get_budget()

    return generate_output()