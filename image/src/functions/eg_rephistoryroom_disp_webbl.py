from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_artikel, Eg_request, Eg_property, Eg_subtask, Eg_queasy, Eg_vperform, Eg_vendor

def eg_rephistoryroom_disp_webbl(room_nr:str, fdate:date, tdate:date, prop_nr:int):
    gtotal = ""
    tot_cost = ""
    tot_vend = ""
    t_hisroom_head_list = []
    t_hisroom_line_list = []
    t_hisroom_line_cost_list = []
    t_hisroom_line_vendor_list = []
    tprop_list = []
    tot:decimal = 0
    curr_tot1:decimal = 0
    curr_tot2:decimal = 0
    curr_gtotal:decimal = 0
    int_str:[str] = ["", "", "", "", "", ""]
    l_artikel = eg_request = eg_property = eg_subtask = eg_queasy = eg_vperform = eg_vendor = None

    t_hisroom_head = t_hisroom_line = t_hisroom_line_cost = t_hisroom_line_vendor = tprop = tbuff = None

    t_hisroom_head_list, T_hisroom_head = create_model("T_hisroom_head", {"itemno":str, "bezeich":str, "flag":str})
    t_hisroom_line_list, T_hisroom_line = create_model("T_hisroom_line", {"itemno":str, "bezeich":str, "reqno":str, "opend":str, "processd":str, "doned":str, "subtask":str, "reqstat":str, "flag":str})
    t_hisroom_line_cost_list, T_hisroom_line_cost = create_model("T_hisroom_line_cost", {"itemno":str, "bezeich":str, "reqno":str, "flag":str, "artno":str, "bezeich2":str, "qty":str, "price":str, "tot_dtl":str})
    t_hisroom_line_vendor_list, T_hisroom_line_vendor = create_model("T_hisroom_line_vendor", {"itemno":str, "bezeich":str, "reqno":str, "flag":str, "outsource":str, "vendor_nm":str, "startdate":str, "finishdate":str, "price":str, "tot_dtl":str})
    tprop_list, Tprop = create_model("Tprop", {"nr":int, "nm":str})

    Tbuff = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gtotal, tot_cost, tot_vend, t_hisroom_head_list, t_hisroom_line_list, t_hisroom_line_cost_list, t_hisroom_line_vendor_list, tprop_list, tot, curr_tot1, curr_tot2, curr_gtotal, int_str, l_artikel, eg_request, eg_property, eg_subtask, eg_queasy, eg_vperform, eg_vendor
        nonlocal tbuff


        nonlocal t_hisroom_head, t_hisroom_line, t_hisroom_line_cost, t_hisroom_line_vendor, tprop, tbuff
        nonlocal t_hisroom_head_list, t_hisroom_line_list, t_hisroom_line_cost_list, t_hisroom_line_vendor_list, tprop_list
        return {"gtotal": gtotal, "tot_cost": tot_cost, "tot_vend": tot_vend, "t-hisroom-head": t_hisroom_head_list, "t-hisroom-line": t_hisroom_line_list, "t-hisroom-line-cost": t_hisroom_line_cost_list, "t-hisroom-line-vendor": t_hisroom_line_vendor_list, "tprop": tprop_list}

    def create_history():

        nonlocal gtotal, tot_cost, tot_vend, t_hisroom_head_list, t_hisroom_line_list, t_hisroom_line_cost_list, t_hisroom_line_vendor_list, tprop_list, tot, curr_tot1, curr_tot2, curr_gtotal, int_str, l_artikel, eg_request, eg_property, eg_subtask, eg_queasy, eg_vperform, eg_vendor
        nonlocal tbuff


        nonlocal t_hisroom_head, t_hisroom_line, t_hisroom_line_cost, t_hisroom_line_vendor, tprop, tbuff
        nonlocal t_hisroom_head_list, t_hisroom_line_list, t_hisroom_line_cost_list, t_hisroom_line_vendor_list, tprop_list

        char4:str = ""
        a:str = ""
        b:str = ""
        c:str = ""
        vendo_nm:str = ""
        itotal:decimal = 0
        nm_prop1:str = ""
        nm_prop2:str = ""
        nm_prop3:str = ""
        nm_prop4:str = ""
        t_hisroom_head_list.clear()
        t_hisroom_line_list.clear()
        t_hisroom_line_cost_list.clear()
        t_hisroom_line_vendor_list.clear()
        tprop_list.clear()

        for eg_request in db_session.query(Eg_request).filter(
                (func.lower(Eg_request.zinr) == (room_nr).lower()) &  (Eg_request.opened_date >= fdate) &  (Eg_request.opened_date <= tdate) |  (Eg_request.propertynr == prop_nr) &  (Eg_request.closed_date >= fdate) &  (Eg_request.closed_date <= tdate) |  (Eg_request.propertynr == prop_nr) &  (Eg_request.process_date >= fdate) &  (Eg_request.process_date <= tdate)).all():

            tprop = query(tprop_list, filters=(lambda tprop :tprop.nr == eg_request.propertynr), first=True)

            if not tprop:

                eg_property = db_session.query(Eg_property).filter(
                        (Eg_property.nr == eg_request.propertynr)).first()

                if eg_property:
                    nm_prop1 = eg_property.bezeich
                else:
                    nm_prop1 = ""
                tprop = Tprop()
                tprop_list.append(tprop)

                tprop.nr = eg_request.propertynr
                tprop.nm = nm_prop1


                t_hisroom_head = T_hisroom_head()
                t_hisroom_head_list.append(t_hisroom_head)

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

            eg_subtask = db_session.query(Eg_subtask).filter(
                    (Eg_subtask.sub_CODE == eg_request.sub_task)).first()

            if eg_subtask:
                char4 = to_string(eg_subtask.bezeich)
            else:
                char4 = ""
            t_hisroom_line = T_hisroom_line()
            t_hisroom_line_list.append(t_hisroom_line)

            t_hisroom_line.itemno = to_string(eg_request.propertynr, "->>>>>>9")
            t_hisroom_line.bezeich = nm_prop1
            t_hisroom_line.reqno = to_string(eg_request.reqnr , "->>>>>>9")
            t_hisroom_line.opend = a
            t_hisroom_line.processd = b
            t_hisroom_line.doned = c
            t_hisroom_line.subtask = char4
            t_hisroom_line.reqstat = int_str[eg_request.reqstatus - 1]
            t_hisroom_line.flag = "1"

            eg_queasy = db_session.query(Eg_queasy).filter(
                    (Eg_queasy.key == 1) &  (Eg_queasy.reqnr == eg_request.reqnr)).first()

            if eg_queasy:
                curr_tot1 = 0

                for eg_queasy in db_session.query(Eg_queasy).filter(
                        (Eg_queasy.key == 1) &  (Eg_queasy.reqnr == eg_request.reqnr)).all():

                    tbuff = db_session.query(Tbuff).filter(
                            (Tbuff.artnr == eg_queasy.stock_nr)).first()

                    if tbuff:
                        itotal = eg_queasy.deci1 * eg_queasy.price
                        t_hisroom_line_cost = T_hisroom_line_cost()
                        t_hisroom_line_cost_list.append(t_hisroom_line_cost)

                        t_hisroom_line_cost.itemno = to_string(eg_request.propertynr, "->>>>>>9")
                        t_hisroom_line_cost.bezeich = nm_prop1
                        t_hisroom_line_cost.reqno = to_string(eg_request.reqnr , "->>>>>>9")
                        t_hisroom_line_cost.flag = "1"
                        t_hisroom_line_cost.artno = to_string(eg_queasy.stock_nr, "9999999")
                        t_hisroom_line_cost.bezeich2 = tbuff.bezeich
                        t_hisroom_line_cost.qty = to_string(eg_queasy.deci1 , "->>>>>>9")
                        t_hisroom_line_cost.price = to_string(eg_queasy.price, "->>>,>>>,>>>,>>9.99")
                        t_hisroom_line_cost.tot_dtl = to_string(itotal , "->>>,>>>,>>>,>>9.99")


                    tot = tot + itotal
                    curr_tot1 = curr_tot1 + itotal

                if curr_tot1 != 0:
                    tot_cost = to_string(curr_tot1 , "->>>,>>>,>>>,>>9.99")

            eg_vperform = db_session.query(Eg_vperform).filter(
                    (Eg_vperform.reqnr == eg_request.reqnr)).first()

            if eg_vperform:
                curr_tot2 = 0

                for eg_vperform in db_session.query(Eg_vperform).filter(
                        (Eg_vperform.reqnr == eg_request.reqnr)).all():

                    eg_vendor = db_session.query(Eg_vendor).filter(
                            (Eg_vendor.vendor_nr == eg_vperform.vendor_nr)).first()

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
                    t_hisroom_line_vendor_list.append(t_hisroom_line_vendor)

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


                    tot = tot + eg_vperform.price
                    curr_tot2 = curr_tot2 + eg_vperform.price

                if curr_tot2 != 0:
                    tot_vend = to_string(curr_tot2, "->>>,>>>,>>>,>>9.99")

            if tot != 0:
                curr_gtotal = curr_gtotal + tot
                tot = 0

        if curr_gtotal != 0:
            gtotal = to_string(curr_gtotal, "->>>,>>>,>>>,>>9.99")


    create_history()

    return generate_output()