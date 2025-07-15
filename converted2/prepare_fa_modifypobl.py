#using conversion tools version: 1.0.0.117

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
    t_fa_ordheader_data = []
    tfa_order_data = []
    disclist_data = []
    t_add_last_data = []
    t_waehrung_data = []
    t_mathis_data = []
    t_lief_list_data = []
    t_dept_list_data = []
    mtd_budget:Decimal = to_decimal("0.0")
    mtd_balance:Decimal = to_decimal("0.0")
    t_warenwert:Decimal = to_decimal("0.0")
    remain_budget:Decimal = to_decimal("0.0")
    order_date:date = None
    fa_ordheader = fa_order = htparam = waehrung = bediener = queasy = fa_op = l_lieferant = mathis = parameters = None

    t_fa_ordheader = t_add_last = tfa_order = t_waehrung = disclist = t_mathis = t_lief_list = t_dept_list = budget_fix_asset_list = b_fa_order = None

    t_fa_ordheader_data, T_fa_ordheader = create_model_like(Fa_ordheader)
    t_add_last_data, T_add_last = create_model("T_add_last", {"wabkurz":string})
    tfa_order_data, Tfa_order = create_model_like(Fa_order, {"desc_budget":string, "date_budget":date, "amount_budget":Decimal, "remain_budget":Decimal})
    t_waehrung_data, T_waehrung = create_model("T_waehrung", {"wabkurz":string, "waehrungsnr":int})
    disclist_data, Disclist = create_model("Disclist", {"fa_recid":int, "fa_pos":int, "price0":Decimal, "brutto":Decimal, "disc":Decimal, "disc2":Decimal, "vat":Decimal})
    t_mathis_data, T_mathis = create_model("T_mathis", {"artnr":int, "asset_name":string, "asset_number":string, "remain_budget":Decimal, "init_budget":Decimal})
    t_lief_list_data, T_lief_list = create_model("T_lief_list", {"firma":string, "lief_nr":int})
    t_dept_list_data, T_dept_list = create_model("T_dept_list", {"name":string, "nr":int})
    budget_fix_asset_list_data, Budget_fix_asset_list = create_model("Budget_fix_asset_list", {"nr_budget":int, "desc_budget":string, "date_budget":date, "amount_budget":Decimal, "remain_budget":Decimal})

    B_fa_order = create_buffer("B_fa_order",Fa_order)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_no, local_nr, str_approved1, enforce_rflag, deptname, billdate, t_amount, add_first_waehrung_wabkurz, add_last_waehrung_wabkurz, p_464, p_1093, p_220, t_fa_ordheader_data, tfa_order_data, disclist_data, t_add_last_data, t_waehrung_data, t_mathis_data, t_lief_list_data, t_dept_list_data, mtd_budget, mtd_balance, t_warenwert, remain_budget, order_date, fa_ordheader, fa_order, htparam, waehrung, bediener, queasy, fa_op, l_lieferant, mathis, parameters
        nonlocal docu_nr
        nonlocal b_fa_order


        nonlocal t_fa_ordheader, t_add_last, tfa_order, t_waehrung, disclist, t_mathis, t_lief_list, t_dept_list, budget_fix_asset_list, b_fa_order
        nonlocal t_fa_ordheader_data, t_add_last_data, tfa_order_data, t_waehrung_data, disclist_data, t_mathis_data, t_lief_list_data, t_dept_list_data, budget_fix_asset_list_data

        return {"err_no": err_no, "local_nr": local_nr, "str_approved1": str_approved1, "enforce_rflag": enforce_rflag, "deptname": deptname, "billdate": billdate, "t_amount": t_amount, "add_first_waehrung_wabkurz": add_first_waehrung_wabkurz, "add_last_waehrung_wabkurz": add_last_waehrung_wabkurz, "p_464": p_464, "p_1093": p_1093, "p_220": p_220, "t-fa-ordheader": t_fa_ordheader_data, "tfa-order": tfa_order_data, "disclist": disclist_data, "t-add-last": t_add_last_data, "t-waehrung": t_waehrung_data, "t-mathis": t_mathis_data, "t-lief-list": t_lief_list_data, "t-dept-list": t_dept_list_data}

    def call_tamount():

        nonlocal err_no, local_nr, str_approved1, enforce_rflag, deptname, billdate, t_amount, add_first_waehrung_wabkurz, add_last_waehrung_wabkurz, p_464, p_1093, p_220, t_fa_ordheader_data, tfa_order_data, disclist_data, t_add_last_data, t_waehrung_data, t_mathis_data, t_lief_list_data, t_dept_list_data, mtd_budget, mtd_balance, t_warenwert, remain_budget, order_date, fa_ordheader, fa_order, htparam, waehrung, bediener, queasy, fa_op, l_lieferant, mathis, parameters
        nonlocal docu_nr
        nonlocal b_fa_order


        nonlocal t_fa_ordheader, t_add_last, tfa_order, t_waehrung, disclist, t_mathis, t_lief_list, t_dept_list, budget_fix_asset_list, b_fa_order
        nonlocal t_fa_ordheader_data, t_add_last_data, tfa_order_data, t_waehrung_data, disclist_data, t_mathis_data, t_lief_list_data, t_dept_list_data, budget_fix_asset_list_data


        t_amount =  to_decimal("0")

        fa_order_obj_list = {}
        fa_order = Fa_order()
        mathis = Mathis()
        for fa_order.order_amount, fa_order.order_nr, fa_order._recid, fa_order.fa_nr, fa_order.order_qty, fa_order.activeflag, fa_order.order_price, fa_order.activereason, fa_order.fa_pos, fa_order.fa_remarks, fa_order.discount1, fa_order.discount2, fa_order.vat, mathis.nr, mathis.name, mathis.asset, mathis._recid in db_session.query(Fa_order.order_amount, Fa_order.order_nr, Fa_order._recid, Fa_order.fa_nr, Fa_order.order_qty, Fa_order.activeflag, Fa_order.order_price, Fa_order.activereason, Fa_order.fa_pos, Fa_order.fa_remarks, Fa_order.discount1, Fa_order.discount2, Fa_order.vat, Mathis.nr, Mathis.name, Mathis.asset, Mathis._recid).join(Mathis,(Mathis.nr == Fa_order.fa_nr)).filter(
                 (Fa_order.order_nr == (docu_nr).lower()) & (Fa_order.fa_pos > 0) & (Fa_order.activeflag == 0)).order_by(Fa_order._recid).all():
            if fa_order_obj_list.get(fa_order._recid):
                continue
            else:
                fa_order_obj_list[fa_order._recid] = True


            t_amount =  to_decimal(t_amount) + to_decimal(fa_order.order_amount)
            tfa_order = Tfa_order()
            tfa_order_data.append(tfa_order)

            tfa_order.order_nr = fa_order.order_nr
            tfa_order.statflag = fa_order._recid
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

            budget_fix_asset_list = query(budget_fix_asset_list_data, filters=(lambda budget_fix_asset_list: budget_fix_asset_list.to_string(budget_fix_asset_list.nr_budget) == fa_order.activereason), first=True)

            if budget_fix_asset_list:
                tfa_order.desc_budget = budget_fix_asset_list.desc_budget
                tfa_order.date_budget = budget_fix_asset_list.date_budget
                tfa_order.amount_budget =  to_decimal(budget_fix_asset_list.amount_budget)
                tfa_order.remain_budget =  to_decimal(budget_fix_asset_list.remain_budget)
            disclist = Disclist()
            disclist_data.append(disclist)

            disclist.fa_recid = fa_order.fa_nr
            disclist.fa_pos = fa_order.fa_pos
            disclist.price0 =  to_decimal(fa_order.order_price) / to_decimal((1) - to_decimal(fa_order.discount1) * to_decimal(0.01)) /\
                    (1 - to_decimal(fa_order.discount2) * to_decimal(0.01)) / to_decimal((1) + to_decimal(fa_order.vat) * to_decimal(0.01) )
            disclist.brutto =  to_decimal(disclist.price0) * to_decimal(fa_order.order_qty)


    def currency_list():

        nonlocal err_no, local_nr, str_approved1, enforce_rflag, deptname, billdate, t_amount, add_first_waehrung_wabkurz, add_last_waehrung_wabkurz, p_464, p_1093, p_220, t_fa_ordheader_data, tfa_order_data, disclist_data, t_add_last_data, t_waehrung_data, t_mathis_data, t_lief_list_data, t_dept_list_data, mtd_budget, mtd_balance, t_warenwert, remain_budget, order_date, fa_ordheader, fa_order, htparam, waehrung, bediener, queasy, fa_op, l_lieferant, mathis, parameters
        nonlocal docu_nr
        nonlocal b_fa_order


        nonlocal t_fa_ordheader, t_add_last, tfa_order, t_waehrung, disclist, t_mathis, t_lief_list, t_dept_list, budget_fix_asset_list, b_fa_order
        nonlocal t_fa_ordheader_data, t_add_last_data, tfa_order_data, t_waehrung_data, disclist_data, t_mathis_data, t_lief_list_data, t_dept_list_data, budget_fix_asset_list_data

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
            t_add_last_data.append(t_add_last)

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

    if fa_ordheader:
        pass
        t_fa_ordheader = T_fa_ordheader()
        t_fa_ordheader_data.append(t_fa_ordheader)

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

        for tfa_order in query(tfa_order_data, filters=(lambda tfa_order: tfa_order.order_nr.lower()  == (docu_nr).lower())):
            tfa_order_data.remove(tfa_order)
        disclist_data.clear()
        t_mathis_data.clear()

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 324)).order_by(Queasy._recid).all():
            t_warenwert =  to_decimal(0.0)
            budget_fix_asset_list = Budget_fix_asset_list()
            budget_fix_asset_list_data.append(budget_fix_asset_list)

            budget_fix_asset_list.nr_budget = queasy.number1
            budget_fix_asset_list.desc_budget = queasy.char1
            budget_fix_asset_list.date_budget = queasy.date1
            budget_fix_asset_list.amount_budget =  to_decimal(queasy.deci1)

            for fa_order in db_session.query(Fa_order).filter(
                     (Fa_order.activereason == to_string(queasy.number1))).order_by(Fa_order._recid).all():

                fa_op = get_cache (Fa_op, {"loeschflag": [(le, 1)],"opart": [(eq, 1)],"anzahl": [(gt, 0)],"docu_nr": [(eq, fa_order.order_nr)]})

                if fa_op:
                    t_warenwert =  to_decimal(t_warenwert) + to_decimal(fa_op.warenwert)
            budget_fix_asset_list.remain_budget =  to_decimal(queasy.deci1) - to_decimal(t_warenwert)
        call_tamount()
        currency_list()

        for waehrung in db_session.query(Waehrung).order_by(Waehrung._recid).all():
            t_waehrung = T_waehrung()
            t_waehrung_data.append(t_waehrung)

            t_waehrung.wabkurz = waehrung.wabkurz
            t_waehrung.waehrungsnr = waehrung.waehrungsnr

        for l_lieferant in db_session.query(L_lieferant).order_by(L_lieferant._recid).all():
            t_lief_list = T_lief_list()
            t_lief_list_data.append(t_lief_list)

            t_lief_list.firma = l_lieferant.firma
            t_lief_list.lief_nr = l_lieferant.lief_nr

        for mathis in db_session.query(Mathis).order_by(Mathis._recid).all():
            t_mathis = T_mathis()
            t_mathis_data.append(t_mathis)

            t_mathis.artnr = mathis.nr
            t_mathis.asset_name = mathis.name
            t_mathis.asset_number = mathis.asset

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("CostCenter").lower()) & (Parameters.SECTION == ("Name").lower())).order_by(Parameters._recid).all():
            t_dept_list = T_dept_list()
            t_dept_list_data.append(t_dept_list)

            t_dept_list.name = parameters.vstring
            t_dept_list.nr = to_int(parameters.varname)


        pass
        pass

    return generate_output()