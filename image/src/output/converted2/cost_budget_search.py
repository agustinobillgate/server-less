#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Parameters, Gl_acct, L_artikel, Htparam, Costbudget, L_op, L_ophis

def cost_budget_search(deptno:int, artno:int, from_date:date):

    prepare_cache ([Parameters, L_artikel, Htparam, Costbudget, L_op, L_ophis])

    cost_list_list = []
    to_date:date = None
    curr_date:date = None
    inv_close_date:date = None
    parameters = gl_acct = l_artikel = htparam = costbudget = l_op = l_ophis = None

    cost_list = alloc_list = pbuff = cbuff = None

    cost_list_list, Cost_list = create_model("Cost_list", {"month_i":int, "year_i":int, "budget":Decimal, "actual":Decimal, "ytd_budget":Decimal, "ytd_actual":Decimal})
    alloc_list_list, Alloc_list = create_model("Alloc_list", {"fibu":string})

    Pbuff = create_buffer("Pbuff",Parameters)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cost_list_list, to_date, curr_date, inv_close_date, parameters, gl_acct, l_artikel, htparam, costbudget, l_op, l_ophis
        nonlocal deptno, artno, from_date
        nonlocal pbuff


        nonlocal cost_list, alloc_list, pbuff, cbuff
        nonlocal cost_list_list, alloc_list_list

        return {"cost-list": cost_list_list}

    def create_costlist():

        nonlocal cost_list_list, to_date, curr_date, inv_close_date, parameters, gl_acct, l_artikel, htparam, costbudget, l_op, l_ophis
        nonlocal deptno, artno, from_date
        nonlocal pbuff


        nonlocal cost_list, alloc_list, pbuff, cbuff
        nonlocal cost_list_list, alloc_list_list

        fdate:date = None
        tdate:date = None
        cdate:date = None
        htparam.fdate = date_mdy(get_month(curr_date) , 1, get_year(curr_date))
        tdate = tdate + timedelta(days=31)
        tdate = date_mdy(get_month(tdate) , 1, get_year(tdate)) - timedelta(days=1)

        cost_list = query(cost_list_list, filters=(lambda cost_list: cost_list.month_i == get_month(curr_date) and cost_list.year_i == get_year(curr_date)), first=True)

        if not cost_list:
            cost_list = Cost_list()
            cost_list_list.append(cost_list)

            cost_list.month_i = get_month(curr_date)
            cost_list.year_i = get_year(curr_date)


            for cdate in date_range(htparam.fdate,tdate) :

                costbudget = get_cache (Costbudget, {"departement": [(eq, deptno)],"zwkum": [(eq, l_artikel.zwkum)],"artnr": [(eq, artno)],"datum": [(eq, cdate)]})

                if not costbudget:

                    costbudget = get_cache (Costbudget, {"departement": [(eq, deptno)],"zwkum": [(eq, l_artikel.zwkum)],"artnr": [(eq, 0)],"datum": [(eq, cdate)]})

                if costbudget:
                    cost_list.budget =  to_decimal(cost_list.budget) + to_decimal(costbudget.betrag)

        if get_month(curr_date) == get_month(inv_close_date) and get_year(curr_date) == get_year(inv_close_date):

            for l_op in db_session.query(L_op).filter(
                     (L_op.artnr == artno) & (L_op.op_art == 3) & (L_op.datum >= fdate) & (L_op.datum <= to_date) & (L_op.loeschflag <= 1)).order_by(L_op._recid).all():

                alloc_list = query(alloc_list_list, filters=(lambda alloc_list: alloc_list.fibu == l_op.stornogrund), first=True)

                if alloc_list:
                    cost_list.actual =  to_decimal(cost_list.actual) + to_decimal(l_op.warenwert)


        elif curr_date < date_mdy(get_month(inv_close_date) , 1, get_year(inv_close_date)):

            for l_ophis in db_session.query(L_ophis).filter(
                     (L_ophis.artnr == artno) & (L_ophis.op_art == 3) & (L_ophis.datum >= fdate) & (L_ophis.datum <= tdate)).order_by(L_ophis._recid).all():

                alloc_list = query(alloc_list_list, filters=(lambda alloc_list: alloc_list.fibu == l_ophis.fibukonto), first=True)

                if alloc_list:
                    cost_list.actual =  to_decimal(cost_list.actual) + to_decimal(l_ophis.warenwert)

    def calc_ytd():

        nonlocal cost_list_list, to_date, curr_date, inv_close_date, parameters, gl_acct, l_artikel, htparam, costbudget, l_op, l_ophis
        nonlocal deptno, artno, from_date
        nonlocal pbuff


        nonlocal cost_list, alloc_list, pbuff, cbuff
        nonlocal cost_list_list, alloc_list_list


        Cbuff = Cost_list
        cbuff_list = cost_list_list

        for cost_list in query(cost_list_list):

            for cbuff in query(cbuff_list, filters=(lambda cbuff:((cbuff.month_i <= cost_list.month_i) and (cbuff.year_i == cost_list.year_i)) or (cbuff.year_i < cost_list.year_i))):
                cost_list.ytd_budget =  to_decimal(cost_list.ytd_budget) + to_decimal(cbuff.budget)
                cost_list.ytd_actual =  to_decimal(cost_list.ytd_actual) + to_decimal(cbuff.actual)

    parameters = db_session.query(Parameters).filter(
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == deptno)).first()

    if not parameters:

        return generate_output()

    for pbuff in db_session.query(Pbuff).filter(
             (Pbuff.progname == ("CostCenter").lower()) & (Pbuff.section == ("Alloc").lower()) & (Pbuff.varname == parameters.varname)).order_by(Pbuff._recid).all():

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, pbuff.vstring)]})

        if gl_acct:
            alloc_list = Alloc_list()
            alloc_list_list.append(alloc_list)

            alloc_list.fibu = pbuff.vstring

    l_artikel = get_cache (L_artikel, {"artnr": [(eq, artno)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    to_date = htparam.fdate

    if artno <= 2999999:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    inv_close_date = htparam.fdate


    for curr_date in date_range(from_date,to_date) :
        create_costlist()
    calc_ytd()

    return generate_output()