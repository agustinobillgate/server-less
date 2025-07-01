#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_ordheader, L_lieferant, Fa_order, Htparam, Bediener, Parameters, Waehrung, Mathis

def prepare_fa_recpobl(docu_nr:string, user_init:string, dept_nr:int):

    prepare_cache ([Htparam, Bediener, Parameters, Waehrung, Mathis])

    enforce_rflag = False
    show_price = False
    price_decimal = 0
    billdate = None
    add_first_waehrung_wabkurz = ""
    exchg_rate = 0
    tot_amount = to_decimal("0.0")
    pr_21 = 0
    pr_973 = False
    t_faordheader_list = []
    tfa_order_list = []
    t_lieferant_list = []
    t_parameters_list = []
    fa_ordheader = l_lieferant = fa_order = htparam = bediener = parameters = waehrung = mathis = None

    t_faordheader = t_lieferant = tfa_order = t_parameters = None

    t_faordheader_list, T_faordheader = create_model_like(Fa_ordheader)
    t_lieferant_list, T_lieferant = create_model_like(L_lieferant)
    tfa_order_list, Tfa_order = create_model_like(Fa_order, {"nr":int, "name":string, "asset":string, "price":Decimal})
    t_parameters_list, T_parameters = create_model("T_parameters", {"varname":string, "vstring":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal enforce_rflag, show_price, price_decimal, billdate, add_first_waehrung_wabkurz, exchg_rate, tot_amount, pr_21, pr_973, t_faordheader_list, tfa_order_list, t_lieferant_list, t_parameters_list, fa_ordheader, l_lieferant, fa_order, htparam, bediener, parameters, waehrung, mathis
        nonlocal docu_nr, user_init, dept_nr


        nonlocal t_faordheader, t_lieferant, tfa_order, t_parameters
        nonlocal t_faordheader_list, t_lieferant_list, tfa_order_list, t_parameters_list

        return {"enforce_rflag": enforce_rflag, "show_price": show_price, "price_decimal": price_decimal, "billdate": billdate, "add_first_waehrung_wabkurz": add_first_waehrung_wabkurz, "exchg_rate": exchg_rate, "tot_amount": tot_amount, "pr_21": pr_21, "pr_973": pr_973, "t-faordheader": t_faordheader_list, "tfa-order": tfa_order_list, "t-lieferant": t_lieferant_list, "t-parameters": t_parameters_list}

    def get_currency():

        nonlocal enforce_rflag, show_price, price_decimal, billdate, add_first_waehrung_wabkurz, exchg_rate, tot_amount, pr_21, pr_973, t_faordheader_list, tfa_order_list, t_lieferant_list, t_parameters_list, fa_ordheader, l_lieferant, fa_order, htparam, bediener, parameters, waehrung, mathis
        nonlocal docu_nr, user_init, dept_nr


        nonlocal t_faordheader, t_lieferant, tfa_order, t_parameters
        nonlocal t_faordheader_list, t_lieferant_list, tfa_order_list, t_parameters_list

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, fa_ordheader.currency)]})

        if waehrung:
            add_first_waehrung_wabkurz = waehrung.wabkurz
            exchg_rate = waehrung.ankauf / waehrung.einheit


    def create_tfa_order():

        nonlocal enforce_rflag, show_price, price_decimal, billdate, add_first_waehrung_wabkurz, exchg_rate, tot_amount, pr_21, pr_973, t_faordheader_list, tfa_order_list, t_lieferant_list, t_parameters_list, fa_ordheader, l_lieferant, fa_order, htparam, bediener, parameters, waehrung, mathis
        nonlocal docu_nr, user_init, dept_nr


        nonlocal t_faordheader, t_lieferant, tfa_order, t_parameters
        nonlocal t_faordheader_list, t_lieferant_list, tfa_order_list, t_parameters_list


        tfa_order_list.clear()

        for fa_order in db_session.query(Fa_order).filter(
                 (Fa_order.order_nr == (docu_nr).lower())).order_by(Fa_order.fa_pos).all():

            mathis = get_cache (Mathis, {"nr": [(eq, fa_order.fa_nr)]})
            tfa_order = Tfa_order()
            tfa_order_list.append(tfa_order)

            buffer_copy(fa_order, tfa_order)
            tfa_order.nr = mathis.nr
            tfa_order.name = mathis.name
            tfa_order.asset = mathis.asset
            tfa_order.price =  to_decimal(mathis.price)


            tot_amount =  to_decimal(tot_amount) + to_decimal(tfa_order.order_amount)

    fa_ordheader = get_cache (Fa_ordheader, {"order_nr": [(eq, docu_nr)]})
    t_faordheader = T_faordheader()
    t_faordheader_list.append(t_faordheader)

    buffer_copy(fa_ordheader, t_faordheader)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 222)]})
    enforce_rflag = htparam.flogical

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != ("0").lower() :
        show_price = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 973)]})
    pr_21 = htparam.paramgruppe
    pr_973 = htparam.flogical

    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower())).order_by(Parameters._recid).all():
        t_parameters = T_parameters()
        t_parameters_list.append(t_parameters)

        t_parameters.varname = parameters.varname
        t_parameters.vstring = parameters.vstring


    get_currency()
    create_tfa_order()

    for l_lieferant in db_session.query(L_lieferant).order_by(L_lieferant._recid).all():
        t_lieferant = T_lieferant()
        t_lieferant_list.append(t_lieferant)

        buffer_copy(l_lieferant, t_lieferant)

    return generate_output()