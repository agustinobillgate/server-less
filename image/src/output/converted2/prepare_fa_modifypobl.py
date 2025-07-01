#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from models import Fa_ordheader, Fa_order, Htparam, Waehrung, Bediener, Queasy, Fa_op, L_lieferant, Mathis, Parameters

def prepare_fa_modifypobl(docu_nr:string):

    prepare_cache ([Fa_order, Htparam, Waehrung, Bediener, Queasy, Fa_op, L_lieferant, Mathis, Parameters])

    err_no = 0
    local_nr = 0
    str_approved1 = ""
    enforce_rflag = False
    deptname = ""
    billdate = None
    t_amount = to_decimal("0.0")
    add_first_waehrung_wabkurz = ""
    add_last_waehrung_wabkurz = ""
    p_464 = 0
    p_1093 = 0
    p_220 = 0
    t_fa_ordheader_list = []
    tfa_order_list = []
    disclist_list = []
    t_add_last_list = []
    t_waehrung_list = []
    t_mathis_list = []
    t_lief_list_list = []
    t_dept_list_list = []
    mtd_budget:Decimal = to_decimal("0.0")
    mtd_balance:Decimal = to_decimal("0.0")
    t_warenwert:Decimal = to_decimal("0.0")
    remain_budget:Decimal = to_decimal("0.0")
    order_date:date = None
    fa_ordheader = fa_order = htparam = waehrung = bediener = queasy = fa_op = l_lieferant = mathis = parameters = None

    t_fa_ordheader = t_add_last = tfa_order = t_waehrung = disclist = t_mathis = t_lief_list = t_dept_list = budget_fix_asset_list = b_fa_order = None

    t_fa_ordheader_list, T_fa_ordheader = create_model_like(Fa_ordheader)
    t_add_last_list, T_add_last = create_model("T_add_last", {"wabkurz":string})
    tfa_order_list, Tfa_order = create_model_like(Fa_order, {"desc_budget":string, "date_budget":date, "amount_budget":Decimal, "remain_budget":Decimal})
    t_waehrung_list, T_waehrung = create_model("T_waehrung", {"wabkurz":string, "waehrungsnr":int})
    disclist_list, Disclist = create_model("Disclist", {"fa_recid":int, "fa_pos":int, "price0":Decimal, "brutto":Decimal, "disc":Decimal, "disc2":Decimal, "vat":Decimal})
    t_mathis_list, T_mathis = create_model("T_mathis", {"artnr":int, "asset_name":string, "asset_number":string, "remain_budget":Decimal, "init_budget":Decimal})
    t_lief_list_list, T_lief_list = create_model("T_lief_list", {"firma":string, "lief_nr":int})
    t_dept_list_list, T_dept_list = create_model("T_dept_list", {"name":string, "nr":int})
    budget_fix_asset_list_list, Budget_fix_asset_list = create_model("Budget_fix_asset_list", {"nr_budget":int, "desc_budget":string, "date_budget":date, "amount_budget":Decimal, "remain_budget":Decimal})

    B_fa_order = create_buffer("B_fa_order",Fa_order)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_no, local_nr, str_approved1, enforce_rflag, deptname, billdate, t_amount, add_first_waehrung_wabkurz, add_last_waehrung_wabkurz, p_464, p_1093, p_220, t_fa_ordheader_list, tfa_order_list, disclist_list, t_add_last_list, t_waehrung_list, t_mathis_list, t_lief_list_list, t_dept_list_list, mtd_budget, mtd_balance, t_warenwert, remain_budget, order_date, fa_ordheader, fa_order, htparam, waehrung, bediener, queasy, fa_op, l_lieferant, mathis, parameters
        nonlocal docu_nr
        nonlocal b_fa_order


        nonlocal t_fa_ordheader, t_add_last, tfa_order, t_waehrung, disclist, t_mathis, t_lief_list, t_dept_list, budget_fix_asset_list, b_fa_order
        nonlocal t_fa_ordheader_list, t_add_last_list, tfa_order_list, t_waehrung_list, disclist_list, t_mathis_list, t_lief_list_list, t_dept_list_list, budget_fix_asset_list_list

        return {"err_no": err_no, "local_nr": local_nr, "str_approved1": str_approved1, "enforce_rflag": enforce_rflag, "deptname": deptname, "billdate": billdate, "t_amount": t_amount, "add_first_waehrung_wabkurz": add_first_waehrung_wabkurz, "add_last_waehrung_wabkurz": add_last_waehrung_wabkurz, "p_464": p_464, "p_1093": p_1093, "p_220": p_220, "t-fa-ordheader": t_fa_ordheader_list, "tfa-order": tfa_order_list, "disclist": disclist_list, "t-add-last": t_add_last_list, "t-waehrung": t_waehrung_list, "t-mathis": t_mathis_list, "t-lief-list": t_lief_list_list, "t-dept-list": t_dept_list_list}

    def call_tamount():

        nonlocal err_no, local_nr, str_approved1, enforce_rflag, deptname, billdate, t_amount, add_first_waehrung_wabkurz, add_last_waehrung_wabkurz, p_464, p_1093, p_220, t_fa_ordheader_list, tfa_order_list, disclist_list, t_add_last_list, t_waehrung_list, t_mathis_list, t_lief_list_list, t_dept_list_list, mtd_budget, mtd_balance, t_warenwert, remain_budget, order_date, fa_ordheader, fa_order, htparam, waehrung, bediener, queasy, fa_op, l_lieferant, mathis, parameters
        nonlocal docu_nr
        nonlocal b_fa_order


        nonlocal t_fa_ordheader, t_add_last, tfa_order, t_waehrung, disclist, t_mathis, t_lief_list, t_dept_list, budget_fix_asset_list, b_fa_order
        nonlocal t_fa_ordheader_list, t_add_last_list, tfa_order_list, t_waehrung_list, disclist_list, t_mathis_list, t_lief_list_list, t_dept_list_list, budget_fix_asset_list_list


        t_amount =  to_decimal("0")

        fa_order_obj_list = {}
        fa_order = Fa_order()
        mathis = Mathis()
        for fa_order.order_amount, fa_order.order_nr, fa_order.fa_nr, fa_order.order_qty, fa_order.activeflag, fa_order.order_price, fa_order.activereason, fa_order.fa_pos, fa_order.fa_remarks, fa_order.discount1, fa_order.discount2, fa_order.vat, fa_order._recid, mathis.nr, mathis.name, mathis.asset, mathis._recid in db_session.query(Fa_order.order_amount, Fa_order.order_nr, Fa_order.fa_nr, Fa_order.order_qty, Fa_order.activeflag, Fa_order.order_price, Fa_order.activereason, Fa_order.fa_pos, Fa_order.fa_remarks, Fa_order.discount1, Fa_order.discount2, Fa_order.vat, Fa_order._recid, Mathis.nr, Mathis.name, Mathis.asset, Mathis._recid).join(Mathis,(Mathis.nr == Fa_order.fa_nr)).filter(
                 (Fa_order.order_nr == (docu_nr).lower()) & (Fa_order.fa_pos > 0) & (Fa_order.activeflag == 0)).order_by(Fa_order._recid).all():
            if fa_order_obj_list.get(fa_order._recid):
                continue
            else:
                fa_order_obj_list[fa_order._recid] = True


            t_amount =  to_decimal(t_amount) + to_decimal(fa_order.order_amount)
            tfa_order = Tfa_order()
            tfa_order_list.append(tfa_order)

            tfa_order.order_nr = fa_order.order_nr
            tfa_order.statflag = l_order._recid
            tfa_order.fa_nr = fa_order.fa_nr
            tfa_order.order_qty = fa_order.order_qty
            tfa_order.activeflag = fa_order.activeflag
            tfa_order.order_price =  to_decimal(fa_order.order_price)
            tfa_order.order_amount =  to_decimal(fa_order.order_amount)
            tfa_order.activereason = fa_order.activereason
            tfa_order.fa_pos = fa_order.fa_pos
            tfa_order.fa_remarks = fa_order.fa_remarks
            tfa_order.discount1 =  to_decimal(fa_order.discount1)
            tfa_order.discount2 =  to_decimal(fa_order.discount2)
            tfa_order.vat =  to_decimal(fa_order.vat)

            budget_fix_asset_list = query(budget_fix_asset_list_list, filters=(lambda budget_fix_asset_list: budget_fix_asset_list.to_string(budget_fix_asset_list.nr_budget) == fa_order.activereason), first=True)

            if budget_fix_asset_list:
                tfa_order.desc_budget = budget_fix_asset_list.desc_budget
                tfa_order.date_budget = budget_fix_asset_list.date_budget
                tfa_order.amount_budget =  to_decimal(budget_fix_asset_list.amount_budget)
                tfa_order.remain_budget =  to_decimal(budget_fix_asset_list.remain_budget)
            disclist = Disclist()
            disclist_list.append(disclist)

            disclist.fa_recid = fa_order.fa_nr
            disclist.fa_pos = fa_order.fa_pos
            disclist.price0 =  to_decimal(fa_order.order_price) / to_decimal((1) - to_decimal(fa_order.discount1) * to_decimal(0.01)) /\
                    (1 - to_decimal(fa_order.discount2) * to_decimal(0.01)) / to_decimal((1) + to_decimal(fa_order.vat) * to_decimal(0.01) )
            disclist.brutto =  to_decimal(disclist.price0) * to_decimal(fa_order.order_qty)


    def currency_list():

        nonlocal err_no, local_nr, str_approved1, enforce_rflag, deptname, billdate, t_amount, add_first_waehrung_wabkurz, add_last_waehrung_wabkurz, p_464, p_1093, p_220, t_fa_ordheader_list, tfa_order_list, disclist_list, t_add_last_list, t_waehrung_list, t_mathis_list, t_lief_list_list, t_dept_list_list, mtd_budget, mtd_balance, t_warenwert, remain_budget, order_date, fa_ordheader, fa_order, htparam, waehrung, bediener, queasy, fa_op, l_lieferant, mathis, parameters
        nonlocal docu_nr
        nonlocal b_fa_order


        nonlocal t_fa_ordheader, t_add_last, tfa_order, t_waehrung, disclist, t_mathis, t_lief_list, t_dept_list, budget_fix_asset_list, b_fa_order
        nonlocal t_fa_ordheader_list, t_add_last_list, tfa_order_list, t_waehrung_list, disclist_list, t_mathis_list, t_lief_list_list, t_dept_list_list, budget_fix_asset_list_list

        strcurr:string = ""

        if fa_ordheader.currency == 0:
            fa_ordheader.currency = local_nr

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, fa_ordheader.currency)]})
        add_first_waehrung_wabkurz = waehrung.wabkurz

        if fa_ordheader.currency != local_nr:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, local_nr)]})

            if waehrung.betriebsnr == 0:
                add_last_waehrung_wabkurz = waehrung.wabkurz

        for waehrung in db_session.query(Waehrung).filter(
                 (Waehrung.ankauf > 0) & (Waehrung.betriebsnr != 0)).order_by(Waehrung.wabkurz).all():
            t_add_last = T_add_last()
            t_add_last_list.append(t_add_last)

            t_add_last.wabkurz = waehrung.wabkurz

    p_1093 = get_output(htpint(1093))
    p_464 = get_output(htpint(464))
    p_220 = get_output(htpint(220))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if not waehrung:
        err_no = 1

        return generate_output()
    local_nr = waehrung.waehrungsnr

    fa_ordheader = get_cache (Fa_ordheader, {"order_nr": [(eq, docu_nr)]})
    t_fa_ordheader = T_fa_ordheader()
    t_fa_ordheader_list.append(t_fa_ordheader)

    buffer_copy(fa_ordheader, t_fa_ordheader)
    order_date = fa_ordheader.order_date

    if fa_ordheader.approved_1 :

        bediener = get_cache (Bediener, {"userinit": [(eq, fa_ordheader.approved_1_by)]})

        if bediener:
            str_approved1 = bediener.username
        else:
            str_approved1 = ""

    htparam = get_cache (Htparam, {"paramnr": [(eq, 222)]})
    enforce_rflag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})

    if htparam.finteger != 1 and htparam.finteger != 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        billdate = htparam.fdate
    else:
        billdate = get_current_date()

    for tfa_order in query(tfa_order_list, filters=(lambda tfa_order: tfa_order.order_nr.lower()  == (docu_nr).lower())):
        tfa_order_list.remove(tfa_order)
    disclist_list.clear()
    t_mathis_list.clear()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 324)).order_by(Queasy._recid).all():
        t_warenwert =  to_decimal(0.0)
        budget_fix_asset_list = Budget_fix_asset_list()
        budget_fix_asset_list_list.append(budget_fix_asset_list)

        budget_fix_asset_list.nr_budget = queasy.number1
        budget_fix_asset_list.desc_budget = queasy.char1
        budget_fix_asset_list.date_budget = queasy.date1
        budget_fix_asset_list.amount_budget =  to_decimal(queasy.deci1)

        for fa_order in db_session.query(Fa_order).filter(
                 (Fa_order.ActiveReason == to_string(queasy.number1))).order_by(Fa_order._recid).all():

            fa_op = get_cache (Fa_op, {"loeschflag": [(le, 1)],"opart": [(eq, 1)],"anzahl": [(gt, 0)],"docu_nr": [(eq, fa_order.order_nr)]})

            if fa_op:
                t_warenwert =  to_decimal(t_warenwert) + to_decimal(fa_op.warenwert)
        budget_fix_asset_list.remain_budget =  to_decimal(queasy.deci1) - to_decimal(t_warenwert)
    call_tamount()
    currency_list()

    for waehrung in db_session.query(Waehrung).order_by(Waehrung._recid).all():
        t_waehrung = T_waehrung()
        t_waehrung_list.append(t_waehrung)

        t_waehrung.wabkurz = waehrung.wabkurz
        t_waehrung.waehrungsnr = waehrung.waehrungsnr

    for l_lieferant in db_session.query(L_lieferant).order_by(L_lieferant._recid).all():
        t_lief_list = T_lief_list()
        t_lief_list_list.append(t_lief_list)

        t_lief_list.firma = l_lieferant.firma
        t_lief_list.lief_nr = l_lieferant.lief_nr

    for mathis in db_session.query(Mathis).order_by(Mathis._recid).all():
        t_mathis = T_mathis()
        t_mathis_list.append(t_mathis)

        t_mathis.artnr = mathis.nr
        t_mathis.asset_name = mathis.name
        t_mathis.asset_number = mathis.asset

    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.SECTION == ("Name").lower())).order_by(Parameters._recid).all():
        t_dept_list = T_dept_list()
        t_dept_list_list.append(t_dept_list)

        t_dept_list.name = parameters.vstring
        t_dept_list.nr = to_int(parameters.varname)

    return generate_output()