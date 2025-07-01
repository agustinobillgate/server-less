#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, Paramtext, Htparam, Parameters, Waehrung, Fa_ordheader, Fa_order, Bediener

def prepare_fa_polistbl():

    prepare_cache ([Paramtext, Htparam, Parameters, Waehrung, Fa_ordheader, Fa_order, Bediener])

    long_digit = False
    billdate = None
    briefnr = 0
    p_464 = 0
    htl_name = ""
    htl_adr = ""
    htl_tel = ""
    cost_list_list = []
    w_list_list = []
    username_list = []
    l_supp_list = []
    l_lieferant = paramtext = htparam = parameters = waehrung = fa_ordheader = fa_order = bediener = None

    cost_list = w_list = username = l_supp = None

    cost_list_list, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":string, "sorting":string})
    w_list_list, W_list = create_model("W_list", {"nr":int, "wabkurz":string})
    username_list, Username = create_model("Username", {"order_nr":string, "create_by":string, "modify_by":string, "close_by":string, "close_date":date, "close_time":string, "last_arrival":date, "total_amount":Decimal})
    l_supp_list, L_supp = create_model_like(L_lieferant)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, billdate, briefnr, p_464, htl_name, htl_adr, htl_tel, cost_list_list, w_list_list, username_list, l_supp_list, l_lieferant, paramtext, htparam, parameters, waehrung, fa_ordheader, fa_order, bediener


        nonlocal cost_list, w_list, username, l_supp
        nonlocal cost_list_list, w_list_list, username_list, l_supp_list

        return {"long_digit": long_digit, "billdate": billdate, "briefnr": briefnr, "p_464": p_464, "htl_name": htl_name, "htl_adr": htl_adr, "htl_tel": htl_tel, "cost-list": cost_list_list, "w-list": w_list_list, "username": username_list, "l-supp": l_supp_list}

    def create_supp():

        nonlocal long_digit, billdate, briefnr, p_464, htl_name, htl_adr, htl_tel, cost_list_list, w_list_list, username_list, l_supp_list, l_lieferant, paramtext, htparam, parameters, waehrung, fa_ordheader, fa_order, bediener


        nonlocal cost_list, w_list, username, l_supp
        nonlocal cost_list_list, w_list_list, username_list, l_supp_list

        for l_lieferant in db_session.query(L_lieferant).order_by(L_lieferant._recid).all():
            l_supp = L_supp()
            l_supp_list.append(l_supp)

            buffer_copy(l_lieferant, l_supp)


    def create_costlist():

        nonlocal long_digit, billdate, briefnr, p_464, htl_name, htl_adr, htl_tel, cost_list_list, w_list_list, username_list, l_supp_list, l_lieferant, paramtext, htparam, parameters, waehrung, fa_ordheader, fa_order, bediener


        nonlocal cost_list, w_list, username, l_supp
        nonlocal cost_list_list, w_list_list, username_list, l_supp_list

        i:int = 0
        m:int = 1
        n:int = 0

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():
            cost_list = Cost_list()
            cost_list_list.append(cost_list)

            cost_list.nr = to_int(parameters.varname)
            cost_list.bezeich = parameters.vstring


    def currency_list():

        nonlocal long_digit, billdate, briefnr, p_464, htl_name, htl_adr, htl_tel, cost_list_list, w_list_list, username_list, l_supp_list, l_lieferant, paramtext, htparam, parameters, waehrung, fa_ordheader, fa_order, bediener


        nonlocal cost_list, w_list, username, l_supp
        nonlocal cost_list_list, w_list_list, username_list, l_supp_list

        local_nr:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            local_nr = waehrung.waehrungsnr
        w_list = W_list()
        w_list_list.append(w_list)


        if local_nr != 0:
            w_list.wabkurz = waehrung.wabkurz

        for waehrung in db_session.query(Waehrung).order_by(Waehrung.wabkurz).all():
            w_list = W_list()
            w_list_list.append(w_list)

            w_list.nr = waehrung.waehrungsnr
            w_list.wabkurz = waehrung.wabkurz


    def create_bediener():

        nonlocal long_digit, billdate, briefnr, p_464, htl_name, htl_adr, htl_tel, cost_list_list, w_list_list, username_list, l_supp_list, l_lieferant, paramtext, htparam, parameters, waehrung, fa_ordheader, fa_order, bediener


        nonlocal cost_list, w_list, username, l_supp
        nonlocal cost_list_list, w_list_list, username_list, l_supp_list

        temp_create:string = ""
        temp_modify:string = ""
        temp_close:string = ""
        temp_date:date = None
        temp_time:string = ""
        last_arrive:date = None
        total_amount:Decimal = to_decimal("0.0")
        username_list.clear()

        for fa_ordheader in db_session.query(Fa_ordheader).order_by(Fa_ordheader._recid).all():

            for fa_order in db_session.query(Fa_order).filter(
                     (Fa_order.order_nr == fa_ordheader.order_nr)).order_by(Fa_order.delivered_date).all():

                if last_arrive == None:
                    last_arrive = fa_order.delivered_date
                else:

                    if last_arrive <= fa_order.delivered_date:
                        last_arrive = fa_order.delivered_date
                    else:
                        last_arrive = last_arrive

            if fa_ordheader.activeflag == 2:

                bediener = get_cache (Bediener, {"userinit": [(eq, fa_ordheader.close_by)]})

                if bediener:
                    temp_close = bediener.username
                else:
                    temp_close = ""

                if fa_ordheader.close_date != None:
                    temp_date = fa_ordheader.close_date
                else:
                    temp_date = None

                if fa_ordheader.close_time != 0:
                    temp_time = to_string(fa_ordheader.close_time , "HH:MM")
                else:
                    temp_time = ""
            else:
                temp_close = ""
                temp_date = None
                temp_time = ""

            bediener = get_cache (Bediener, {"userinit": [(eq, fa_ordheader.created_by)]})

            if bediener:
                temp_create = bediener.username
            else:
                temp_create = ""

            bediener = get_cache (Bediener, {"userinit": [(eq, fa_ordheader.modified_by)]})

            if bediener:
                temp_modify = bediener.username
            else:
                temp_modify = ""

            for fa_order in db_session.query(Fa_order).filter(
                     (Fa_order.order_nr == fa_ordheader.order_nr) & (Fa_order.activeflag == 0)).order_by(Fa_order._recid).all():
                total_amount =  to_decimal(total_amount) + to_decimal(fa_order.order_amount)
            username = Username()
            username_list.append(username)

            username.order_nr = fa_ordheader.order_nr
            username.create_by = temp_create
            username.modify_by = temp_modify
            username.close_by = temp_close
            username.close_date = temp_date
            username.close_time = temp_time
            username.last_arrival = last_arrive
            username.total_amount =  to_decimal(total_amount)
            total_amount =  to_decimal("0")
            temp_create = ""
            temp_modify = ""
            temp_close = ""
            temp_date = None
            temp_time = ""
            last_arrive = None

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
    htl_name = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})
    htl_adr = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})
    htl_tel = paramtext.ptexte

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1093)]})
    briefnr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 464)]})
    p_464 = htparam.finteger
    create_costlist()
    currency_list()
    create_bediener()
    create_supp()

    return generate_output()