from functions.additional_functions import *
import decimal
from models import L_artikel, Eg_queasy, Eg_vperform, Eg_vendor

def eg_rephistoryprop_detail_webbl(case_type:int, reqno:int):
    tot_artcost = ""
    tot_vendcost = ""
    t_artikel_cost_list = []
    t_vendor_cost_list = []
    atotal:int = 0
    btotal:int = 0
    tot:decimal = 0
    l_artikel = eg_queasy = eg_vperform = eg_vendor = None

    t_artikel_cost = t_vendor_cost = tbuff = None

    t_artikel_cost_list, T_artikel_cost = create_model("T_artikel_cost", {"reqno":str, "art_no":str, "art_desc":str, "art_qty":str, "art_price":str, "art_total":str, "tflag":str})
    t_vendor_cost_list, T_vendor_cost = create_model("T_vendor_cost", {"reqno":str, "vend_no":str, "vend_desc":str, "vend_start":str, "vend_finish":str, "vend_price":str, "tflag":str})

    Tbuff = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_artcost, tot_vendcost, t_artikel_cost_list, t_vendor_cost_list, atotal, btotal, tot, l_artikel, eg_queasy, eg_vperform, eg_vendor
        nonlocal tbuff


        nonlocal t_artikel_cost, t_vendor_cost, tbuff
        nonlocal t_artikel_cost_list, t_vendor_cost_list
        return {"tot_artcost": tot_artcost, "tot_vendcost": tot_vendcost, "t-artikel-cost": t_artikel_cost_list, "t-vendor-cost": t_vendor_cost_list}

    def create_artikel_cost():

        nonlocal tot_artcost, tot_vendcost, t_artikel_cost_list, t_vendor_cost_list, atotal, btotal, tot, l_artikel, eg_queasy, eg_vperform, eg_vendor
        nonlocal tbuff


        nonlocal t_artikel_cost, t_vendor_cost, tbuff
        nonlocal t_artikel_cost_list, t_vendor_cost_list

        itotal:decimal = 0
        t_artikel_cost_list.clear()

        eg_queasy = db_session.query(Eg_queasy).filter(
                (Eg_queasy.key == 1) &  (Eg_queasy.reqnr == reqno)).first()

        if eg_queasy:

            for eg_queasy in db_session.query(Eg_queasy).filter(
                    (Eg_queasy.key == 1) &  (Eg_queasy.reqnr == reqno)).all():

                tbuff = db_session.query(Tbuff).filter(
                        (Tbuff.artnr == eg_queasy.stock_nr)).first()

                if tbuff:
                    itotal = eg_queasy.deci1 * eg_queasy.price
                    t_artikel_cost = T_artikel_cost()
                    t_artikel_cost_list.append(t_artikel_cost)

                    t_artikel_cost.reqno = to_string(reqno, "->>>>>>>>9")
                    t_artikel_cost.art_no = to_string(eg_queasy.stock_nr, "9999999")
                    t_artikel_cost.art_desc = tbuff.bezeich
                    t_artikel_cost.art_qty = to_string(eg_queasy.deci1 , "->>>,>>9.99")
                    t_artikel_cost.art_price = to_string(eg_queasy.price, "->>>,>>>,>>>,>>9.99")
                    t_artikel_cost.art_total = to_string(itotal, "->>>,>>>,>>>,>>9.99")
                    t_artikel_cost.tFlag = "1"


                tot = tot + itotal

        if tot != 0:
            tot_artcost = to_string(tot, "->>>,>>>,>>>,>>9.99")
            tot = 0

    def create_vendor_cost():

        nonlocal tot_artcost, tot_vendcost, t_artikel_cost_list, t_vendor_cost_list, atotal, btotal, tot, l_artikel, eg_queasy, eg_vperform, eg_vendor
        nonlocal tbuff


        nonlocal t_artikel_cost, t_vendor_cost, tbuff
        nonlocal t_artikel_cost_list, t_vendor_cost_list

        vendo_nm:str = ""
        start_date:str = ""
        finish_date:str = ""
        itotal:decimal = 0
        t_vendor_cost_list.clear()

        eg_vperform = db_session.query(Eg_vperform).filter(
                (Eg_vperform.reqnr == reqno)).first()

        if eg_vperform:

            for eg_vperform in db_session.query(Eg_vperform).filter(
                    (Eg_vperform.reqnr == reqno)).all():

                eg_vendor = db_session.query(Eg_vendor).filter(
                        (Eg_vendor.vendor_nr == eg_vperform.vendor_nr)).first()

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
                t_vendor_cost_list.append(t_vendor_cost)

                t_vendor_cost.reqno = to_string(reqno, "->>>>>>>>9")
                t_vendor_cost.vend_no = to_string(eg_vperform.perform_nr, "9999999")
                t_vendor_cost.vend_desc = vendo_nm
                t_vendor_cost.vend_start = start_date
                t_vendor_cost.vend_finish = finish_date
                t_vendor_cost.vend_price = to_string(eg_vperform.price, "->>>,>>>,>>>,>>9.99")
                t_vendor_cost.tFlag = "2"


                tot = tot + eg_vperform.price

        if tot != 0:
            tot_vendcost = to_string(tot, "->>>,>>>,>>>,>>9.99")
            tot = 0


    if case_type == 1:
        create_artikel_cost()
    else:
        create_vendor_cost()

    return generate_output()