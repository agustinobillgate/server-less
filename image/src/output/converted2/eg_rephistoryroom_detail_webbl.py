#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, Eg_queasy, Eg_vperform, Eg_vendor

def eg_rephistoryroom_detail_webbl(case_type:int, reqno:int):

    prepare_cache ([L_artikel, Eg_queasy, Eg_vperform, Eg_vendor])

    tot_cost = ""
    tot_vend = ""
    t_hisroom_line_cost_list = []
    t_hisroom_line_vendor_list = []
    tot:Decimal = to_decimal("0.0")
    curr_tot:Decimal = to_decimal("0.0")
    l_artikel = eg_queasy = eg_vperform = eg_vendor = None

    t_hisroom_line_cost = t_hisroom_line_vendor = tbuff = None

    t_hisroom_line_cost_list, T_hisroom_line_cost = create_model("T_hisroom_line_cost", {"reqno":string, "flag":string, "artno":string, "bezeich":string, "qty":string, "price":string, "tot_price":string})
    t_hisroom_line_vendor_list, T_hisroom_line_vendor = create_model("T_hisroom_line_vendor", {"reqno":string, "flag":string, "outsource":string, "vendor_nm":string, "startdate":string, "finishdate":string, "price":string})

    Tbuff = create_buffer("Tbuff",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_cost, tot_vend, t_hisroom_line_cost_list, t_hisroom_line_vendor_list, tot, curr_tot, l_artikel, eg_queasy, eg_vperform, eg_vendor
        nonlocal case_type, reqno
        nonlocal tbuff


        nonlocal t_hisroom_line_cost, t_hisroom_line_vendor, tbuff
        nonlocal t_hisroom_line_cost_list, t_hisroom_line_vendor_list

        return {"tot_cost": tot_cost, "tot_vend": tot_vend, "t-hisroom-line-cost": t_hisroom_line_cost_list, "t-hisroom-line-vendor": t_hisroom_line_vendor_list}

    def create_artikel_cost():

        nonlocal tot_cost, tot_vend, t_hisroom_line_cost_list, t_hisroom_line_vendor_list, tot, curr_tot, l_artikel, eg_queasy, eg_vperform, eg_vendor
        nonlocal case_type, reqno
        nonlocal tbuff


        nonlocal t_hisroom_line_cost, t_hisroom_line_vendor, tbuff
        nonlocal t_hisroom_line_cost_list, t_hisroom_line_vendor_list

        itotal:Decimal = to_decimal("0.0")
        t_hisroom_line_cost_list.clear()

        eg_queasy = get_cache (Eg_queasy, {"key": [(eq, 1)],"reqnr": [(eq, reqno)]})

        if eg_queasy:

            for eg_queasy in db_session.query(Eg_queasy).filter(
                     (Eg_queasy.key == 1) & (Eg_queasy.reqnr == reqno)).order_by(Eg_queasy.stock_nr).all():

                tbuff = get_cache (L_artikel, {"artnr": [(eq, eg_queasy.stock_nr)]})

                if tbuff:
                    itotal =  to_decimal(eg_queasy.deci1) * to_decimal(eg_queasy.price)
                    t_hisroom_line_cost = T_hisroom_line_cost()
                    t_hisroom_line_cost_list.append(t_hisroom_line_cost)

                    t_hisroom_line_cost.reqno = to_string(reqno, "->>>>>>9")
                    t_hisroom_line_cost.flag = "1"
                    t_hisroom_line_cost.artno = to_string(eg_queasy.stock_nr, "9999999")
                    t_hisroom_line_cost.bezeich = tbuff.bezeich
                    t_hisroom_line_cost.qty = to_string(eg_queasy.deci1 , "->>>>>>9")
                    t_hisroom_line_cost.price = to_string(eg_queasy.price, "->>>,>>>,>>>,>>9.99")
                    t_hisroom_line_cost.tot_price = to_string(itotal , "->>>,>>>,>>>,>>9.99")


                tot =  to_decimal(tot) + to_decimal(itotal)

        if tot != 0:
            tot_cost = to_string(tot, "->>>,>>>,>>>,>>9.99")
            tot =  to_decimal("0")


    def create_vendor_cost():

        nonlocal tot_cost, tot_vend, t_hisroom_line_cost_list, t_hisroom_line_vendor_list, tot, curr_tot, l_artikel, eg_queasy, eg_vperform, eg_vendor
        nonlocal case_type, reqno
        nonlocal tbuff


        nonlocal t_hisroom_line_cost, t_hisroom_line_vendor, tbuff
        nonlocal t_hisroom_line_cost_list, t_hisroom_line_vendor_list

        vendo_nm:string = ""
        start_date:string = ""
        finish_date:string = ""
        itotal:Decimal = to_decimal("0.0")
        t_hisroom_line_vendor_list.clear()

        eg_vperform = get_cache (Eg_vperform, {"reqnr": [(eq, reqno)]})

        if eg_vperform:

            for eg_vperform in db_session.query(Eg_vperform).filter(
                     (Eg_vperform.reqnr == reqno)).order_by(Eg_vperform.perform_nr).all():

                eg_vendor = get_cache (Eg_vendor, {"vendor_nr": [(eq, eg_vperform.vendor_nr)]})

                if eg_vendor:
                    vendo_nm = eg_vendor.bezeich
                else:
                    vendo_nm = "Undefine"

                if eg_vperform.startdate == None:
                    start_date = "-"
                else:
                    start_date = to_string(eg_vperform.startdate, "99/99/99")

                if eg_vperform.finishdate == None:
                    finish_date = "-"
                else:
                    finish_date = to_string(eg_vperform.finishdate, "99/99/99")
                t_hisroom_line_vendor = T_hisroom_line_vendor()
                t_hisroom_line_vendor_list.append(t_hisroom_line_vendor)

                t_hisroom_line_vendor.reqno = to_string(reqno, "->>>>>>9")
                t_hisroom_line_vendor.flag = "2"
                t_hisroom_line_vendor.outsource = to_string(eg_vperform.perform_nr, "9999999")
                t_hisroom_line_vendor.vendor_nm = vendo_nm
                t_hisroom_line_vendor.startdate = start_date
                t_hisroom_line_vendor.finishdate = finish_date
                t_hisroom_line_vendor.price = to_string(eg_vperform.price , "->>>,>>>,>>>,>>9.99")


                tot =  to_decimal(tot) + to_decimal(eg_vperform.price)

        if tot != 0:
            tot_vend = to_string(tot, "->>>,>>>,>>>,>>9.99")
            tot =  to_decimal("0")

    if case_type == 1:
        create_artikel_cost()
    else:
        create_vendor_cost()

    return generate_output()