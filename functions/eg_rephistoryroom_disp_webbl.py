#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, Eg_request, Eg_property, Eg_subtask, Eg_queasy, Eg_vperform, Eg_vendor

def eg_rephistoryroom_disp_webbl(room_nr:string, fdate:date, tdate:date, prop_nr:int):

    prepare_cache ([L_artikel, Eg_request, Eg_property, Eg_subtask, Eg_queasy, Eg_vperform, Eg_vendor])

    gtotal = ""
    tot_cost = ""
    tot_vend = ""
    t_hisroom_head_data = []
    t_hisroom_line_data = []
    t_hisroom_line_cost_data = []
    t_hisroom_line_vendor_data = []
    tprop_data = []
    tot:Decimal = to_decimal("0.0")
    curr_tot1:Decimal = to_decimal("0.0")
    curr_tot2:Decimal = to_decimal("0.0")
    curr_gtotal:Decimal = to_decimal("0.0")
    int_str:List[string] = ["New", "Processed", "Done", "Postponed", "Closed"]
    l_artikel = eg_request = eg_property = eg_subtask = eg_queasy = eg_vperform = eg_vendor = None

    t_hisroom_head = t_hisroom_line = t_hisroom_line_cost = t_hisroom_line_vendor = tprop = tbuff = None

    t_hisroom_head_data, T_hisroom_head = create_model("T_hisroom_head", {"itemno":string, "bezeich":string, "flag":string})
    t_hisroom_line_data, T_hisroom_line = create_model("T_hisroom_line", {"itemno":string, "bezeich":string, "reqno":string, "opend":string, "processd":string, "doned":string, "subtask":string, "reqstat":string, "flag":string})
    t_hisroom_line_cost_data, T_hisroom_line_cost = create_model("T_hisroom_line_cost", {"itemno":string, "bezeich":string, "reqno":string, "flag":string, "artno":string, "bezeich2":string, "qty":string, "price":string, "tot_dtl":string})
    t_hisroom_line_vendor_data, T_hisroom_line_vendor = create_model("T_hisroom_line_vendor", {"itemno":string, "bezeich":string, "reqno":string, "flag":string, "outsource":string, "vendor_nm":string, "startdate":string, "finishdate":string, "price":string, "tot_dtl":string})
    tprop_data, Tprop = create_model("Tprop", {"nr":int, "nm":string})

    Tbuff = create_buffer("Tbuff",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gtotal, tot_cost, tot_vend, t_hisroom_head_data, t_hisroom_line_data, t_hisroom_line_cost_data, t_hisroom_line_vendor_data, tprop_data, tot, curr_tot1, curr_tot2, curr_gtotal, int_str, l_artikel, eg_request, eg_property, eg_subtask, eg_queasy, eg_vperform, eg_vendor
        nonlocal room_nr, fdate, tdate, prop_nr
        nonlocal tbuff


        nonlocal t_hisroom_head, t_hisroom_line, t_hisroom_line_cost, t_hisroom_line_vendor, tprop, tbuff
        nonlocal t_hisroom_head_data, t_hisroom_line_data, t_hisroom_line_cost_data, t_hisroom_line_vendor_data, tprop_data

        return {"gtotal": gtotal, "tot_cost": tot_cost, "tot_vend": tot_vend, "t-hisroom-head": t_hisroom_head_data, "t-hisroom-line": t_hisroom_line_data, "t-hisroom-line-cost": t_hisroom_line_cost_data, "t-hisroom-line-vendor": t_hisroom_line_vendor_data, "tprop": tprop_data}

    def create_history():

        nonlocal gtotal, tot_cost, tot_vend, t_hisroom_head_data, t_hisroom_line_data, t_hisroom_line_cost_data, t_hisroom_line_vendor_data, tprop_data, tot, curr_tot1, curr_tot2, curr_gtotal, int_str, l_artikel, eg_request, eg_property, eg_subtask, eg_queasy, eg_vperform, eg_vendor
        nonlocal room_nr, fdate, tdate, prop_nr
        nonlocal tbuff


        nonlocal t_hisroom_head, t_hisroom_line, t_hisroom_line_cost, t_hisroom_line_vendor, tprop, tbuff
        nonlocal t_hisroom_head_data, t_hisroom_line_data, t_hisroom_line_cost_data, t_hisroom_line_vendor_data, tprop_data

        char4:string = ""
        a:string = ""
        b:string = ""
        c:string = ""
        vendo_nm:string = ""
        itotal:Decimal = to_decimal("0.0")
        nm_prop1:string = ""
        nm_prop2:string = ""
        nm_prop3:string = ""
        nm_prop4:string = ""
        t_hisroom_head_data.clear()
        t_hisroom_line_data.clear()
        t_hisroom_line_cost_data.clear()
        t_hisroom_line_vendor_data.clear()
        tprop_data.clear()

        for eg_request in db_session.query(Eg_request).filter(
                 (Eg_request.zinr == (room_nr).lower()) & (Eg_request.opened_date >= fdate) & (Eg_request.opened_date <= tdate) | (Eg_request.propertynr == prop_nr) & (Eg_request.closed_date >= fdate) & (Eg_request.closed_date <= tdate) | (Eg_request.propertynr == prop_nr) & (Eg_request.process_date >= fdate) & (Eg_request.process_date <= tdate)).order_by(Eg_request._recid).all():

            tprop = query(tprop_data, filters=(lambda tprop: tprop.nr == eg_request.propertynr), first=True)

            if not tprop:

                eg_property = get_cache (Eg_property, {"nr": [(eq, eg_request.propertynr)]})

                if eg_property:
                    nm_prop1 = eg_property.bezeich
                else:
                    nm_prop1 = ""
                tprop = Tprop()
                tprop_data.append(tprop)

                tprop.nr = eg_request.propertynr
                tprop.nm = nm_prop1


                t_hisroom_head = T_hisroom_head()
                t_hisroom_head_data.append(t_hisroom_head)

                t_hisroom_head.itemno = to_string(eg_request.propertynr, "->>>>>>9")
                t_hisroom_head.bezeich = nm_prop1
                t_hisroom_head.flag = "0"

            if eg_request.opened_date == None:
                a = ""
            else:
                a = to_string(eg_request.opened_date , "99/99/99")

            if eg_request.closed_date == None:
                b = ""
            else:
                b = to_string(eg_request.closed_date , "99/99/99")

            if eg_request.done_date == None:
                c = ""
            else:
                c = to_string(eg_request.done_date , "99/99/99")

            eg_subtask = get_cache (Eg_subtask, {"sub_code": [(eq, eg_request.sub_task)]})

            if eg_subtask:
                char4 = to_string(eg_subtask.bezeich)
            else:
                char4 = ""
            t_hisroom_line = T_hisroom_line()
            t_hisroom_line_data.append(t_hisroom_line)

            t_hisroom_line.itemno = to_string(eg_request.propertynr, "->>>>>>9")
            t_hisroom_line.bezeich = nm_prop1
            t_hisroom_line.reqno = to_string(eg_request.reqnr , "->>>>>>9")
            t_hisroom_line.opend = a
            t_hisroom_line.processd = b
            t_hisroom_line.doned = c
            t_hisroom_line.subtask = char4
            t_hisroom_line.reqstat = int_str[eg_request.reqstatus - 1]
            t_hisroom_line.flag = "1"

            eg_queasy = get_cache (Eg_queasy, {"key": [(eq, 1)],"reqnr": [(eq, eg_request.reqnr)]})

            if eg_queasy:
                curr_tot1 =  to_decimal("0")

                for eg_queasy in db_session.query(Eg_queasy).filter(
                         (Eg_queasy.key == 1) & (Eg_queasy.reqnr == eg_request.reqnr)).order_by(Eg_queasy._recid).all():

                    tbuff = get_cache (L_artikel, {"artnr": [(eq, eg_queasy.stock_nr)]})

                    if tbuff:
                        itotal =  to_decimal(eg_queasy.deci1) * to_decimal(eg_queasy.price)
                        t_hisroom_line_cost = T_hisroom_line_cost()
                        t_hisroom_line_cost_data.append(t_hisroom_line_cost)

                        t_hisroom_line_cost.itemno = to_string(eg_request.propertynr, "->>>>>>9")
                        t_hisroom_line_cost.bezeich = nm_prop1
                        t_hisroom_line_cost.reqno = to_string(eg_request.reqnr , "->>>>>>9")
                        t_hisroom_line_cost.flag = "1"
                        t_hisroom_line_cost.artno = to_string(eg_queasy.stock_nr, "9999999")
                        t_hisroom_line_cost.bezeich2 = tbuff.bezeich
                        t_hisroom_line_cost.qty = to_string(eg_queasy.deci1 , "->>>>>>9")
                        t_hisroom_line_cost.price = to_string(eg_queasy.price, "->>>,>>>,>>>,>>9.99")
                        t_hisroom_line_cost.tot_dtl = to_string(itotal , "->>>,>>>,>>>,>>9.99")


                    tot =  to_decimal(tot) + to_decimal(itotal)
                    curr_tot1 =  to_decimal(curr_tot1) + to_decimal(itotal)

                if curr_tot1 != 0:
                    tot_cost = to_string(curr_tot1 , "->>>,>>>,>>>,>>9.99")

            eg_vperform = get_cache (Eg_vperform, {"reqnr": [(eq, eg_request.reqnr)]})

            if eg_vperform:
                curr_tot2 =  to_decimal("0")

                for eg_vperform in db_session.query(Eg_vperform).filter(
                         (Eg_vperform.reqnr == eg_request.reqnr)).order_by(Eg_vperform._recid).all():

                    eg_vendor = get_cache (Eg_vendor, {"vendor_nr": [(eq, eg_vperform.vendor_nr)]})

                    if eg_vendor:
                        vendo_nm = eg_vendor.bezeich
                    else:
                        vendo_nm = "Undefine"

                    if eg_vperform.startdate == None:
                        a = ""
                    else:
                        a = to_string(eg_vperform.startdate , "99/99/99")

                    if eg_vperform.finishdate == None:
                        b = ""
                    else:
                        b = to_string(eg_vperform.finishdate , "99/99/99")
                    t_hisroom_line_vendor = T_hisroom_line_vendor()
                    t_hisroom_line_vendor_data.append(t_hisroom_line_vendor)

                    t_hisroom_line_vendor.itemno = to_string(eg_request.propertynr, "->>>>>>9")
                    t_hisroom_line_vendor.bezeich = nm_prop1
                    t_hisroom_line_vendor.reqno = to_string(eg_request.reqnr , "->>>>>>9")
                    t_hisroom_line_vendor.flag = "0"
                    t_hisroom_line_vendor.outsource = to_string(eg_vperform.perform_nr, "9999999")
                    t_hisroom_line_vendor.vendor_nm = vendo_nm
                    t_hisroom_line_vendor.startdate = a
                    t_hisroom_line_vendor.finishdate = b
                    t_hisroom_line_vendor.price = to_string(eg_vperform.price , "->>>,>>>,>>>,>>9.99")
                    t_hisroom_line_vendor.tot_dtl = t_hisroom_line_vendor.tot_dtl + to_string(eg_vperform.price , "->>>,>>>,>>>,>>9.99")


                    tot =  to_decimal(tot) + to_decimal(eg_vperform.price)
                    curr_tot2 =  to_decimal(curr_tot2) + to_decimal(eg_vperform.price)

                if curr_tot2 != 0:
                    tot_vend = to_string(curr_tot2, "->>>,>>>,>>>,>>9.99")

            if tot != 0:
                curr_gtotal =  to_decimal(curr_gtotal) + to_decimal(tot)
                tot =  to_decimal("0")

        if curr_gtotal != 0:
            gtotal = to_string(curr_gtotal, "->>>,>>>,>>>,>>9.99")

    create_history()

    return generate_output()