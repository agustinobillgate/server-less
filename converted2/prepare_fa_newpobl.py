#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lieferant, Mathis, Parameters, Htparam, Waehrung, Fa_ordheader, Fa_counter

def prepare_fa_newpobl(order_nr:string):

    prepare_cache ([L_lieferant, Mathis, Parameters, Htparam, Waehrung, Fa_counter])

    err_no = 0
    local_nr = 0
    billdate = None
    add_first_waehrung_wabkurz = ""
    t_add_last_data = []
    t_mathis_data = []
    t_lief_list_data = []
    t_dept_list_data = []
    l_lieferant = mathis = parameters = htparam = waehrung = fa_ordheader = fa_counter = None

    t_add_last = t_mathis = t_lief_list = t_dept_list = None

    t_add_last_data, T_add_last = create_model("T_add_last", {"wabkurz":string})
    t_mathis_data, T_mathis = create_model("T_mathis", {"artnr":int, "asset_name":string, "asset_number":string})
    t_lief_list_data, T_lief_list = create_model("T_lief_list", {"firma":string, "lief_nr":int})
    t_dept_list_data, T_dept_list = create_model("T_dept_list", {"name":string, "nr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_no, local_nr, billdate, add_first_waehrung_wabkurz, t_add_last_data, t_mathis_data, t_lief_list_data, t_dept_list_data, l_lieferant, mathis, parameters, htparam, waehrung, fa_ordheader, fa_counter
        nonlocal order_nr


        nonlocal t_add_last, t_mathis, t_lief_list, t_dept_list
        nonlocal t_add_last_data, t_mathis_data, t_lief_list_data, t_dept_list_data

        return {"order_nr": order_nr, "err_no": err_no, "local_nr": local_nr, "billdate": billdate, "add_first_waehrung_wabkurz": add_first_waehrung_wabkurz, "t-add-last": t_add_last_data, "t-mathis": t_mathis_data, "t-lief-list": t_lief_list_data, "t-dept-list": t_dept_list_data}

    def new_fapo_number():

        nonlocal err_no, local_nr, billdate, add_first_waehrung_wabkurz, t_add_last_data, t_mathis_data, t_lief_list_data, t_dept_list_data, l_lieferant, mathis, parameters, htparam, waehrung, fa_ordheader, fa_counter
        nonlocal order_nr


        nonlocal t_add_last, t_mathis, t_lief_list, t_dept_list
        nonlocal t_add_last_data, t_mathis_data, t_lief_list_data, t_dept_list_data

        fa_orderhdr1 = None
        s:string = ""
        i:int = 1
        mm:int = 0
        yy:int = 0
        dd:int = 0
        docu_nr:string = ""
        a:bool = False
        Fa_orderhdr1 =  create_buffer("Fa_orderhdr1",Fa_ordheader)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 973)]})

        if htparam.paramgruppe == 21:
            mm = get_month(billdate)
            yy = get_year(billdate)
            dd = get_day(billdate)
            s = "F" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99")

            if htparam.flogical:

                fa_counter = get_cache (Fa_counter, {"count_type": [(eq, 0)],"yy": [(eq, yy)],"mm": [(eq, mm)],"dd": [(eq, dd)],"docu_type": [(eq, 0)]})

                if not fa_counter:
                    fa_counter = Fa_counter()
                    db_session.add(fa_counter)

                    fa_counter.count_type = 0
                    fa_counter.yy = yy
                    fa_counter.mm = mm
                    fa_counter.dd = dd
                    fa_counter.counters = 0
                    fa_counter.docu_type = 0


                pass
                i = fa_counter.counters + 1
                docu_nr = s + to_string(dd, "99") + to_string(i, "999")
            else:

                fa_counter = get_cache (Fa_counter, {"count_type": [(eq, 1)],"yy": [(eq, yy)],"mm": [(eq, mm)],"docu_type": [(eq, 0)]})

                if not fa_counter:
                    fa_counter = Fa_counter()
                    db_session.add(fa_counter)

                    fa_counter.count_type = 1
                    fa_counter.yy = yy
                    fa_counter.mm = mm
                    fa_counter.dd = 0
                    fa_counter.counters = 0
                    fa_counter.docu_type = 0


                pass
                i = fa_counter.counters + 1
                docu_nr = s + to_string(i, "99999")
        order_nr = docu_nr


    def currency_list():

        nonlocal err_no, local_nr, billdate, add_first_waehrung_wabkurz, t_add_last_data, t_mathis_data, t_lief_list_data, t_dept_list_data, l_lieferant, mathis, parameters, htparam, waehrung, fa_ordheader, fa_counter
        nonlocal order_nr


        nonlocal t_add_last, t_mathis, t_lief_list, t_dept_list
        nonlocal t_add_last_data, t_mathis_data, t_lief_list_data, t_dept_list_data

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, local_nr)]})
        add_first_waehrung_wabkurz = waehrung.wabkurz

        for waehrung in db_session.query(Waehrung).filter(
                 (Waehrung.waehrungsnr != local_nr) & (Waehrung.ankauf > 0) & (Waehrung.betriebsnr != 0)).order_by(Waehrung.wabkurz).all():
            t_add_last = T_add_last()
            t_add_last_data.append(t_add_last)

            t_add_last.wabkurz = waehrung.wabkurz

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
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower())).order_by(Parameters._recid).all():
        t_dept_list = T_dept_list()
        t_dept_list_data.append(t_dept_list)

        t_dept_list.name = parameters.vstring
        t_dept_list.nr = to_int(parameters.varname)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if not waehrung:
        err_no = 1

        return generate_output()
    local_nr = waehrung.waehrungsnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})

    if htparam.finteger != 1 and htparam.finteger != 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        billdate = htparam.fdate
    else:
        billdate = get_current_date()

    if order_nr == "":
        new_fapo_number()
    currency_list()

    return generate_output()