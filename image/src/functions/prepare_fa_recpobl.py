from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Fa_ordheader, L_lieferant, Fa_order, Htparam, Bediener, Parameters, Waehrung, Mathis

def prepare_fa_recpobl(docu_nr:str, user_init:str, dept_nr:int):
    enforce_rflag = False
    show_price = False
    price_decimal = 0
    billdate = None
    add_first_waehrung_wabkurz = ""
    exchg_rate = 0
    tot_amount = 0
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
    tfa_order_list, Tfa_order = create_model_like(Fa_order, {"nr":int, "name":str, "asset":str, "price":decimal})
    t_parameters_list, T_parameters = create_model("T_parameters", {"varname":str, "vstring":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal enforce_rflag, show_price, price_decimal, billdate, add_first_waehrung_wabkurz, exchg_rate, tot_amount, pr_21, pr_973, t_faordheader_list, tfa_order_list, t_lieferant_list, t_parameters_list, fa_ordheader, l_lieferant, fa_order, htparam, bediener, parameters, waehrung, mathis


        nonlocal t_faordheader, t_lieferant, tfa_order, t_parameters
        nonlocal t_faordheader_list, t_lieferant_list, tfa_order_list, t_parameters_list
        return {"enforce_rflag": enforce_rflag, "show_price": show_price, "price_decimal": price_decimal, "billdate": billdate, "add_first_waehrung_wabkurz": add_first_waehrung_wabkurz, "exchg_rate": exchg_rate, "tot_amount": tot_amount, "pr_21": pr_21, "pr_973": pr_973, "t-faordheader": t_faordheader_list, "tfa-order": tfa_order_list, "t-lieferant": t_lieferant_list, "t-parameters": t_parameters_list}

    def get_currency():

        nonlocal enforce_rflag, show_price, price_decimal, billdate, add_first_waehrung_wabkurz, exchg_rate, tot_amount, pr_21, pr_973, t_faordheader_list, tfa_order_list, t_lieferant_list, t_parameters_list, fa_ordheader, l_lieferant, fa_order, htparam, bediener, parameters, waehrung, mathis


        nonlocal t_faordheader, t_lieferant, tfa_order, t_parameters
        nonlocal t_faordheader_list, t_lieferant_list, tfa_order_list, t_parameters_list

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == fa_ordheader.currency)).first()

        if waehrung:
            add_first_waehrung_wabkurz = waehrung.wabkurz
            exchg_rate = waehrung.ankauf / waehrung.einheit

    def create_tfa_order():

        nonlocal enforce_rflag, show_price, price_decimal, billdate, add_first_waehrung_wabkurz, exchg_rate, tot_amount, pr_21, pr_973, t_faordheader_list, tfa_order_list, t_lieferant_list, t_parameters_list, fa_ordheader, l_lieferant, fa_order, htparam, bediener, parameters, waehrung, mathis


        nonlocal t_faordheader, t_lieferant, tfa_order, t_parameters
        nonlocal t_faordheader_list, t_lieferant_list, tfa_order_list, t_parameters_list


        tfa_order_list.clear()

        for fa_order in db_session.query(Fa_order).filter(
                (func.lower(Fa_order.order_nr) == (docu_nr).lower())).all():

            mathis = db_session.query(Mathis).filter(
                    (Mathis.nr == fa_order.fa_nr)).first()
            tfa_order = Tfa_order()
            tfa_order_list.append(tfa_order)

            buffer_copy(fa_order, tfa_order)
            tfa_order.nr = mathis.nr
            tfa_order.name = mathis.name
            tfa_order.asset = mathis.asset
            tfa_order.price = mathis.price


            tot_amount = tot_amount + tfa_order.order_amount


    fa_ordheader = db_session.query(Fa_ordheader).filter(
            (func.lower(Fa_ordheader.order_nr) == (docu_nr).lower())).first()
    t_faordheader = T_faordheader()
    t_faordheader_list.append(t_faordheader)

    buffer_copy(fa_ordheader, t_faordheader)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 222)).first()
    enforce_rflag = flogical

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != "0":
        show_price = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    billdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 973)).first()
    pr_21 = htparam.paramgr
    pr_973 = htparam.flogical

    for parameters in db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name")).all():
        t_parameters = T_parameters()
        t_parameters_list.append(t_parameters)

        t_parameters.varname = parameters.varname
        t_parameters.vstring = parameters.vstring


    get_currency()
    create_tfa_order()

    for l_lieferant in db_session.query(L_lieferant).all():
        t_lieferant = T_lieferant()
        t_lieferant_list.append(t_lieferant)

        buffer_copy(l_lieferant, t_lieferant)

    return generate_output()