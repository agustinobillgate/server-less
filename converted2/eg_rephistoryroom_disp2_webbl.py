#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, Eg_request, Eg_property, Eg_subtask, Eg_queasy, Eg_vperform

def eg_rephistoryroom_disp2_webbl(room_nr:string, fdate:date, tdate:date, prop_nr:int):

    prepare_cache ([Eg_request, Eg_property, Eg_subtask, Eg_queasy, Eg_vperform])

    gtotal = ""
    t_hisroom_data = []
    tprop_data = []
    tot:Decimal = to_decimal("0.0")
    curr_gtotal:Decimal = to_decimal("0.0")
    int_str:List[string] = ["New", "Processed", "Done", "Postponed", "Closed"]
    l_artikel = eg_request = eg_property = eg_subtask = eg_queasy = eg_vperform = None

    t_hisroom = tprop = tbuff = None

    t_hisroom_data, T_hisroom = create_model("T_hisroom", {"itemno":string, "bezeich":string, "reqno":string, "opend":string, "processd":string, "doned":string, "subtask":string, "reqstat":string, "flag":string})
    tprop_data, Tprop = create_model("Tprop", {"nr":int, "nm":string})

    Tbuff = create_buffer("Tbuff",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gtotal, t_hisroom_data, tprop_data, tot, curr_gtotal, int_str, l_artikel, eg_request, eg_property, eg_subtask, eg_queasy, eg_vperform
        nonlocal room_nr, fdate, tdate, prop_nr
        nonlocal tbuff


        nonlocal t_hisroom, tprop, tbuff
        nonlocal t_hisroom_data, tprop_data

        return {"gtotal": gtotal, "t-hisroom": t_hisroom_data, "tprop": tprop_data}

    def create_history():

        nonlocal gtotal, t_hisroom_data, tprop_data, tot, curr_gtotal, int_str, l_artikel, eg_request, eg_property, eg_subtask, eg_queasy, eg_vperform
        nonlocal room_nr, fdate, tdate, prop_nr
        nonlocal tbuff


        nonlocal t_hisroom, tprop, tbuff
        nonlocal t_hisroom_data, tprop_data

        char4:string = ""
        a:string = ""
        b:string = ""
        c:string = ""
        itotal:Decimal = to_decimal("0.0")
        nm_prop1:string = ""
        t_hisroom_data.clear()
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


                t_hisroom = T_hisroom()
                t_hisroom_data.append(t_hisroom)

                t_hisroom.itemno = to_string(eg_request.propertynr, "->>>>>>9")
                t_hisroom.bezeich = nm_prop1
                t_hisroom.flag = "0"

            if eg_request.opened_date == None:
                a = "-"
            else:
                a = to_string(eg_request.opened_date , "99/99/99")

            if eg_request.closed_date == None:
                b = "-"
            else:
                b = to_string(eg_request.closed_date , "99/99/99")

            if eg_request.done_date == None:
                c = "-"
            else:
                c = to_string(eg_request.done_date , "99/99/99")

            eg_subtask = get_cache (Eg_subtask, {"sub_code": [(eq, eg_request.sub_task)]})

            if eg_subtask:
                char4 = to_string(eg_subtask.bezeich)
            else:
                char4 = ""
            t_hisroom = T_hisroom()
            t_hisroom_data.append(t_hisroom)

            t_hisroom.itemno = to_string(eg_request.propertynr, "->>>>>>9")
            t_hisroom.bezeich = nm_prop1
            t_hisroom.reqno = to_string(eg_request.reqnr , "->>>>>>9")
            t_hisroom.opend = a
            t_hisroom.processd = b
            t_hisroom.doned = c
            t_hisroom.subtask = char4
            t_hisroom.reqstat = int_str[eg_request.reqstatus - 1]
            t_hisroom.flag = "1"

            eg_queasy = get_cache (Eg_queasy, {"key": [(eq, 1)],"reqnr": [(eq, eg_request.reqnr)]})

            if eg_queasy:

                for eg_queasy in db_session.query(Eg_queasy).filter(
                         (Eg_queasy.key == 1) & (Eg_queasy.reqnr == eg_request.reqnr)).order_by(Eg_queasy._recid).all():

                    tbuff = db_session.query(Tbuff).filter(
                             (Tbuff.artnr == eg_queasy.stock_nr)).first()

                    if tbuff:
                        itotal =  to_decimal(eg_queasy.deci1) * to_decimal(eg_queasy.price)
                    tot =  to_decimal(tot) + to_decimal(itotal)

            eg_vperform = get_cache (Eg_vperform, {"reqnr": [(eq, eg_request.reqnr)]})

            if eg_vperform:

                for eg_vperform in db_session.query(Eg_vperform).filter(
                         (Eg_vperform.reqnr == eg_request.reqnr)).order_by(Eg_vperform._recid).all():
                    tot =  to_decimal(tot) + to_decimal(eg_vperform.price)

            if tot != 0:
                curr_gtotal =  to_decimal(curr_gtotal) + to_decimal(tot)
                tot =  to_decimal("0")

        if curr_gtotal != 0:
            gtotal = to_string(curr_gtotal, "->>>,>>>,>>>,>>9.99")


    create_history()

    return generate_output()