#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Eg_budget, Eg_resources, Res_history

tbudget_list, Tbudget = create_model("Tbudget", {"res_nr":int, "year":int, "month":int, "strmonth":string, "amount":Decimal})
sbudget_list, Sbudget = create_model_like(Tbudget)

def eg_received_btn_ok2bl(sbudget_list:[Sbudget], intres:int, fyear:int, user_init:string):

    prepare_cache ([Bediener, Eg_resources, Res_history])

    tbudget_list = []
    usrnr:int = 0
    res_nm:string = ""
    month_list:List[string] = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    bediener = eg_budget = eg_resources = res_history = None

    tbudget = sbudget = recbudget = usr = None

    recbudget_list, Recbudget = create_model("Recbudget", {"res_nr":int, "year":int, "month":int, "score":int})

    Usr = create_buffer("Usr",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tbudget_list, usrnr, res_nm, month_list, bediener, eg_budget, eg_resources, res_history
        nonlocal intres, fyear, user_init
        nonlocal usr


        nonlocal tbudget, sbudget, recbudget, usr
        nonlocal tbudget_list, recbudget_list

        return {}


    recbudget_list.clear()

    for eg_budget in db_session.query(Eg_budget).filter(
             (Eg_budget.nr == intres) & (Eg_budget.year == fyear)).order_by(Eg_budget._recid).all():
        recbudget = Recbudget()
        recbudget_list.append(recbudget)

        recbudget.res_nr = eg_budget.nr
        recbudget.year = eg_budget.year
        recbudget.month = eg_budget.month
        recbudget.score = eg_budget.score


        db_session.delete(eg_budget)

    usr = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if usr:
        usrnr = usr.nr

    for sbudget in query(sbudget_list):

        recbudget = query(recbudget_list, filters=(lambda recbudget: recbudget.month == sbudget.month and recbudget.res_nr == sbudget.res_nr and recbudget.year == sbudget.year), first=True)

        if recbudget:

            if recbudget.score != sbudget.amount:

                eg_resources = get_cache (Eg_resources, {"nr": [(eq, sbudget.res_nr)]})

                if eg_resources:
                    res_nm = eg_resources.bezeich
                else:
                    res_nm = "undefine"
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Engineering Budget"
                res_history.aenderung = "Change amount resource " + res_nm + " " +\
                        to_string(recbudget.year) + ", " + month_list[recbudget.month - 1] + to_string(recbudget.score , "->>,>>>,>>>,>>9.99") +\
                        " to " + to_string(sbudget.amount, "->>,>>>,>>>,>>9.99")


        else:
            pass
        eg_budget = Eg_budget()
        db_session.add(eg_budget)

        eg_budget.nr = sbudget.res_nr
        eg_budget.year = sbudget.year
        eg_budget.month = sbudget.month
        eg_budget.score =  to_decimal(sbudget.amount)


    recbudget_list.clear()

    return generate_output()