#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, Eg_queasy, Eg_vperform, Eg_vendor

def eg_rephistoryprop_detail_webbl(case_type:int, reqno:int):

    prepare_cache ([L_artikel, Eg_queasy, Eg_vperform, Eg_vendor])

    tot_artcost = ""
    tot_vendcost = ""
    t_artikel_cost_data = []
    t_vendor_cost_data = []
    atotal:int = 0
    btotal:int = 0
    tot:Decimal = to_decimal("0.0")
    l_artikel = eg_queasy = eg_vperform = eg_vendor = None

    t_artikel_cost = t_vendor_cost = tbuff = None

    t_artikel_cost_data, T_artikel_cost = create_model("T_artikel_cost", {"reqno":string, "art_no":string, "art_desc":string, "art_qty":string, "art_price":string, "art_total":string, "tflag":string})
    t_vendor_cost_data, T_vendor_cost = create_model("T_vendor_cost", {"reqno":string, "vend_no":string, "vend_desc":string, "vend_start":string, "vend_finish":string, "vend_price":string, "tflag":string})

    Tbuff = create_buffer("Tbuff",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_artcost, tot_vendcost, t_artikel_cost_data, t_vendor_cost_data, atotal, btotal, tot, l_artikel, eg_queasy, eg_vperform, eg_vendor
        nonlocal case_type, reqno
        nonlocal tbuff


        nonlocal t_artikel_cost, t_vendor_cost, tbuff
        nonlocal t_artikel_cost_data, t_vendor_cost_data

        return {"tot_artcost": tot_artcost, "tot_vendcost": tot_vendcost, "t-artikel-cost": t_artikel_cost_data, "t-vendor-cost": t_vendor_cost_data}

    def create_artikel_cost():

        nonlocal tot_artcost, tot_vendcost, t_artikel_cost_data, t_vendor_cost_data, atotal, btotal, tot, l_artikel, eg_queasy, eg_vperform, eg_vendor
        nonlocal case_type, reqno
        nonlocal tbuff


        nonlocal t_artikel_cost, t_vendor_cost, tbuff
        nonlocal t_artikel_cost_data, t_vendor_cost_data

        itotal:Decimal = to_decimal("0.0")
        t_artikel_cost_data.clear()

        eg_queasy = get_cache (Eg_queasy, {"key": [(eq, 1)],"reqnr": [(eq, reqno)]})

        if eg_queasy:

            for eg_queasy in db_session.query(Eg_queasy).filter(
                     (Eg_queasy.key == 1) & (Eg_queasy.reqnr == reqno)).order_by(Eg_queasy.stock_nr).all():

                tbuff = get_cache (L_artikel, {"artnr": [(eq, eg_queasy.stock_nr)]})

                if tbuff:
                    itotal =  to_decimal(eg_queasy.deci1) * to_decimal(eg_queasy.price)
                    t_artikel_cost = T_artikel_cost()
                    t_artikel_cost_data.append(t_artikel_cost)

                    t_artikel_cost.reqno = to_string(reqno, "->>>>>>>>9")
                    t_artikel_cost.art_no = to_string(eg_queasy.stock_nr, "9999999")
                    t_artikel_cost.art_desc = tbuff.bezeich
                    t_artikel_cost.art_qty = to_string(eg_queasy.deci1 , "->>>,>>9.99")
                    t_artikel_cost.art_price = to_string(eg_queasy.price, "->>>,>>>,>>>,>>9.99")
                    t_artikel_cost.art_total = to_string(itotal, "->>>,>>>,>>>,>>9.99")
                    t_artikel_cost.tflag = "1"


                tot =  to_decimal(tot) + to_decimal(itotal)

        if tot != 0:
            tot_artcost = to_string(tot, "->>>,>>>,>>>,>>9.99")
            tot =  to_decimal("0")


    def create_vendor_cost():

        nonlocal tot_artcost, tot_vendcost, t_artikel_cost_data, t_vendor_cost_data, atotal, btotal, tot, l_artikel, eg_queasy, eg_vperform, eg_vendor
        nonlocal case_type, reqno
        nonlocal tbuff


        nonlocal t_artikel_cost, t_vendor_cost, tbuff
        nonlocal t_artikel_cost_data, t_vendor_cost_data

        vendo_nm:string = ""
        start_date:string = ""
        finish_date:string = ""
        itotal:Decimal = to_decimal("0.0")
        t_vendor_cost_data.clear()

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
                t_vendor_cost = T_vendor_cost()
                t_vendor_cost_data.append(t_vendor_cost)

                t_vendor_cost.reqno = to_string(reqno, "->>>>>>>>9")
                t_vendor_cost.vend_no = to_string(eg_vperform.perform_nr, "9999999")
                t_vendor_cost.vend_desc = vendo_nm
                t_vendor_cost.vend_start = start_date
                t_vendor_cost.vend_finish = finish_date
                t_vendor_cost.vend_price = to_string(eg_vperform.price, "->>>,>>>,>>>,>>9.99")
                t_vendor_cost.tflag = "2"


                tot =  to_decimal(tot) + to_decimal(eg_vperform.price)

        if tot != 0:
            tot_vendcost = to_string(tot, "->>>,>>>,>>>,>>9.99")
            tot =  to_decimal("0")

    if case_type == 1:
        create_artikel_cost()
    else:
        create_vendor_cost()

    return generate_output()