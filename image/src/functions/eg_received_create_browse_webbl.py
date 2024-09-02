from functions.additional_functions import *
import decimal
from models import Eg_budget

def eg_received_create_browse_webbl(case_type:int, curr_year:int, intres:int, res:[Res], t_eg_budget:[T_eg_budget]):
    tbudget_list = []
    sbudget_list = []
    i:int = 0
    month_list:[str] = ["", "", "", "", "", "", "", "", "", "", "", "", ""]
    eg_budget = None

    t_eg_budget = res = tbudget = sbudget = None

    t_eg_budget_list, T_eg_budget = create_model_like(Eg_budget)
    res_list, Res = create_model("Res", {"res_nr":int, "res_nm":str, "res_selected":bool})
    tbudget_list, Tbudget = create_model("Tbudget", {"res_nr":int, "year":int, "month":int, "strmonth":str, "amount":decimal})
    sbudget_list, Sbudget = create_model("Sbudget", {"res_nr":int, "year":int, "month":int, "strmonth":str, "amount":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tbudget_list, sbudget_list, i, month_list, eg_budget


        nonlocal t_eg_budget, res, tbudget, sbudget
        nonlocal t_eg_budget_list, res_list, tbudget_list, sbudget_list
        return {"tbudget": tbudget_list, "sbudget": sbudget_list}

    def create_budget():

        nonlocal tbudget_list, sbudget_list, i, month_list, eg_budget


        nonlocal t_eg_budget, res, tbudget, sbudget
        nonlocal t_eg_budget_list, res_list, tbudget_list, sbudget_list

        s:int = 0
        tamount:int = 0
        s = curr_year
        tbudget_list.clear()

        if s == None:
            pass
        else:

            for res in query(res_list):
                i = 1
                while i <= 12:

                    t_eg_budget = query(t_eg_budget_list, filters=(lambda t_eg_budget :t_eg_budget.nr == res.res_nr and t_eg_budget.YEAR == s and t_eg_budget.MONTH == i), first=True)

                    if t_eg_budget:
                        tamount = t_eg_budget.score
                    else:
                        tamount = 0
                    tbudget = Tbudget()
                    tbudget_list.append(tbudget)

                    tbudget.res_nr = res.res_nr
                    tbudget.YEAR = s
                    tbudget.MONTH = i
                    tbudget.strMONTH = month_list[i - 1]
                    tbudget.amount = tamount


                    i = i + 1

    def create_get_budget():

        nonlocal tbudget_list, sbudget_list, i, month_list, eg_budget


        nonlocal t_eg_budget, res, tbudget, sbudget
        nonlocal t_eg_budget_list, res_list, tbudget_list, sbudget_list

        samount:int = 0
        sbudget_list.clear()
        i = 1
        while i <= 12:

            t_eg_budget = query(t_eg_budget_list, filters=(lambda t_eg_budget :t_eg_budget.nr == intres and t_eg_budget.YEAR == curr_year and t_eg_budget.MONTH == i), first=True)

            if t_eg_budget:
                samount = t_eg_budget.score
            else:
                samount = 0
            sbudget = Sbudget()
            sbudget_list.append(sbudget)

            sbudget.res_nr = intres
            sbudget.YEAR = curr_year
            sbudget.MONTH = i
            sbudget.strMONTH = month_list[i - 1]
            sbudget.amount = samount


            i = i + 1


    if case_type == 1:
        create_budget()

    elif case_type == 2:
        create_get_budget()

    return generate_output()