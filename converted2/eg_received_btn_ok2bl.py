#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Eg_budget, Eg_resources, Res_history

tbudget_data, Tbudget = create_model("Tbudget", {"res_nr":int, "year":int, "month":int, "strmonth":string, "amount":Decimal})
sbudget_data, Sbudget = create_model_like(Tbudget)

def eg_received_btn_ok2bl(sbudget_data:[Sbudget], intres:int, fyear:int, user_init:string):

    prepare_cache ([Bediener, Eg_resources, Res_history])

    tbudget_data = []
    usrnr:int = 0
    res_nm:string = ""
    month_list:List[string] = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    bediener = eg_budget = eg_resources = res_history = None

    tbudget = sbudget = recbudget = usr = None

    recbudget_data, Recbudget = create_model("Recbudget", {"res_nr":int, "year":int, "month":int, "score":int})

    Usr = create_buffer("Usr",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tbudget_data, usrnr, res_nm, month_list, bediener, eg_budget, eg_resources, res_history
        nonlocal intres, fyear, user_init
        nonlocal usr


        nonlocal tbudget, sbudget, recbudget, usr
        nonlocal tbudget_data, recbudget_data

        return {}


    recbudget_data.clear()

    for eg_budget in db_session.query(Eg_budget).filter(
             (Eg_budget.nr == intres) & (Eg_budget.year == fyear)).order_by(Eg_budget._recid).all():
        recbudget = Recbudget()
        recbudget_data.append(recbudget)

        recbudget.res_nr = eg_budget.nr
        recbudget.year = eg_budget.year
        recbudget.month = eg_budget.month
        recbudget.score = eg_budget.score


        db_session.delete(eg_budget)

    usr = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if usr:
        usrnr = usr.nr

    for sbudget in query(sbudget_data):

        recbudget = query(recbudget_data, filters=(lambda recbudget: recbudget.month == sbudget.month and recbudget.res_nr == sbudget.res_nr and recbudget.year == sbudget.year), first=True)

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


    recbudget_data.clear()

    return generate_output()