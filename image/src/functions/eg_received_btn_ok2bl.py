from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Eg_budget, Eg_resources, Res_history

def eg_received_btn_ok2bl(sbudget:[Sbudget], intres:int, fyear:int, user_init:str):
    usrnr:int = 0
    res_nm:str = ""
    month_list:str = ""
    bediener = eg_budget = eg_resources = res_history = None

    tbudget = sbudget = recbudget = usr = None

    tbudget_list, Tbudget = create_model("Tbudget", {"res_nr":int, "year":int, "month":int, "strmonth":str, "amount":decimal})
    sbudget_list, Sbudget = create_model_like(Tbudget)
    recbudget_list, Recbudget = create_model("Recbudget", {"res_nr":int, "year":int, "month":int, "score":int})

    Usr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal usrnr, res_nm, month_list, bediener, eg_budget, eg_resources, res_history
        nonlocal usr


        nonlocal tbudget, sbudget, recbudget, usr
        nonlocal tbudget_list, sbudget_list, recbudget_list
        return {}


    recbudget_list.clear()

    for eg_budget in db_session.query(Eg_budget).filter(
            (Eg_budget.nr == intres) &  (Eg_budget.YEAR == fyear)).all():
        recbudget = Recbudget()
        recbudget_list.append(recbudget)

        recbudget.res_nr = eg_budget.nr
        recbudget.YEAR = eg_budget.YEAR
        recbudget.MONTH = eg_budget.MONTH
        recbudget.score = eg_budget.score


        db_session.delete(eg_budget)

    usr = db_session.query(Usr).filter(
            (func.lower(Usr.userinit) == (user_init).lower())).first()

    if usr:
        usrnr = usr.nr

    for sbudget in query(sbudget_list):

        recbudget = query(recbudget_list, filters=(lambda recbudget :recbudget.MONTH == sbudget.MONTH and recbudget.res_nr == sbudget.res_nr and recbudget.YEAR == sbudget.YEAR), first=True)

        if recbudget:

            if recbudget.score != sbudget.amount:

                eg_resources = db_session.query(Eg_resources).filter(
                        (Eg_resources.nr == sbudget.res_nr)).first()

                if eg_resources:
                    res_nm = eg_resources.bezeich
                else:
                    res_nm = "undefine"
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.Action = "Engineering Budget"
                res_history.aenderung = "Change amount resource " + res_nm + " " +\
                        to_string(recbudget.YEAR) + ", " + month_list[recbudget.MONTH - 1] + to_string(recbudget.score , "->>,>>>,>>>,>>9.99") +\
                        " to " + to_string(sbudget.amount, "->>,>>>,>>>,>>9.99")


        else:
            pass
        eg_budget = Eg_budget()
        db_session.add(eg_budget)

        eg_budget.nr = sbudget.res_nr
        eg_budget.YEAR = sbudget.YEAR
        eg_budget.MONTH = sbudget.MONTH
        eg_budget.score = sbudget.amount


    recbudget_list.clear()

    return generate_output()