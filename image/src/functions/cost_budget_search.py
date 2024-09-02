from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Parameters, Gl_acct, L_artikel, Htparam, Costbudget, L_op, L_ophis

def cost_budget_search(deptno:int, artno:int, from_date:date):
    cost_list_list = []
    to_date:date = None
    curr_date:date = None
    inv_close_date:date = None
    parameters = gl_acct = l_artikel = htparam = costbudget = l_op = l_ophis = None

    cost_list = alloc_list = pbuff = cbuff = None

    cost_list_list, Cost_list = create_model("Cost_list", {"month_i":int, "year_i":int, "budget":decimal, "actual":decimal, "ytd_budget":decimal, "ytd_actual":decimal})
    alloc_list_list, Alloc_list = create_model("Alloc_list", {"fibu":str})

    Pbuff = Parameters
    Cbuff = Cost_list
    cbuff_list = cost_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_list_list, to_date, curr_date, inv_close_date, parameters, gl_acct, l_artikel, htparam, costbudget, l_op, l_ophis
        nonlocal pbuff, cbuff


        nonlocal cost_list, alloc_list, pbuff, cbuff
        nonlocal cost_list_list, alloc_list_list
        return {"cost-list": cost_list_list}

    def create_costlist():

        nonlocal cost_list_list, to_date, curr_date, inv_close_date, parameters, gl_acct, l_artikel, htparam, costbudget, l_op, l_ophis
        nonlocal pbuff, cbuff


        nonlocal cost_list, alloc_list, pbuff, cbuff
        nonlocal cost_list_list, alloc_list_list

        fdate:date = None
        tdate:date = None
        cdate:date = None
        fdate = date_mdy(get_month(curr_date) , 1, get_year(curr_date))
        tdate = tdate + 31
        tdate = date_mdy(get_month(tdate) , 1, get_year(tdate)) - 1

        cost_list = query(cost_list_list, filters=(lambda cost_list :cost_list.month_i == get_month(curr_date) and cost_list.year_i == get_year(curr_date)), first=True)

        if not cost_list:
            cost_list = Cost_list()
            cost_list_list.append(cost_list)

            cost_list.month_i = get_month(curr_date)
            cost_list.year_i = get_year(curr_date)


            for cdate in range(fdate,tdate + 1) :

                costbudget = db_session.query(Costbudget).filter(
                        (Costbudget.departement == deptno) &  (Costbudget.zwkum == l_artikel.zwkum) &  (Costbudget.artnr == artno) &  (Costbudget.datum == cdate)).first()

                if not costbudget:

                    costbudget = db_session.query(Costbudget).filter(
                            (Costbudget.departement == deptno) &  (Costbudget.zwkum == l_artikel.zwkum) &  (Costbudget.artnr == 0) &  (Costbudget.datum == cdate)).first()

                if costbudget:
                    cost_list.budget = cost_list.budget + costbudget.betrag

        if get_month(curr_date) == get_month(inv_close_date) and get_year(curr_date) == get_year(inv_close_date):

            for l_op in db_session.query(L_op).filter(
                    (L_op.artnr == artno) &  (L_op.op_art == 3) &  (L_op.datum >= fdate) &  (L_op.datum <= to_date) &  (L_op.loeschflag <= 1)).all():

                alloc_list = query(alloc_list_list, filters=(lambda alloc_list :alloc_list.fibu == l_op.stornogrund), first=True)

                if alloc_list:
                    cost_list.actual = cost_list.actual + l_op.warenwert


        elif curr_date < date_mdy(get_month(inv_close_date) , 1, get_year(inv_close_date)):

            for l_ophis in db_session.query(L_ophis).filter(
                    (L_ophis.artnr == artno) &  (L_ophis.op_art == 3) &  (L_ophis.datum >= fdate) &  (L_ophis.datum <= tdate)).all():

                alloc_list = query(alloc_list_list, filters=(lambda alloc_list :alloc_list.fibu == l_ophis.fibukonto), first=True)

                if alloc_list:
                    cost_list.actual = cost_list.actual + l_ophis.warenwert


    def calc_ytd():

        nonlocal cost_list_list, to_date, curr_date, inv_close_date, parameters, gl_acct, l_artikel, htparam, costbudget, l_op, l_ophis
        nonlocal pbuff, cbuff


        nonlocal cost_list, alloc_list, pbuff, cbuff
        nonlocal cost_list_list, alloc_list_list


        Cbuff = Cost_list

        for cost_list in query(cost_list_list):

            for cbuff in query(cbuff_list, filters=(lambda cbuff :((cbuff.month_i <= cost_list.month_i) and (cbuff.year_i == cost_list.year_i)) or (cbuff.year_i < cost_list.year_i))):
                cost_list.ytd_budget = cost_list.ytd_budget + cbuff.budget
                cost_list.ytd_actual = cost_list.ytd_actual + cbuff.actual


    parameters = db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (to_int(Parameters.varname) == deptno)).first()

    if not parameters:

        return generate_output()

    for pbuff in db_session.query(Pbuff).filter(
            (func.lower(Pbuff.progname) == "CostCenter") &  (func.lower(Pbuff.section) == "Alloc") &  (Pbuff.varname == parameters.varname)).all():

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == pbuff.vstring)).first()

        if gl_acct:
            alloc_list = Alloc_list()
            alloc_list_list.append(alloc_list)

            alloc_list.fibu = pbuff.vstring

    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == artno)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    to_date = htparam.fdate

    if artno <= 2999999:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 224)).first()
    else:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 221)).first()
    inv_close_date = htparam.fdate


    for curr_date in range(from_date,to_date + 1) :
        create_costlist()
    calc_ytd()

    return generate_output()