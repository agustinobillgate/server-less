from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_artikel, Eg_request, Eg_property, Eg_subtask, Eg_queasy, Eg_vperform

def eg_rephistoryroom_disp2_webbl(room_nr:str, fdate:date, tdate:date, prop_nr:int):
    gtotal = ""
    t_hisroom_list = []
    tprop_list = []
    tot:decimal = 0
    curr_gtotal:decimal = 0
    int_str:[str] = ["", "", "", "", "", ""]
    l_artikel = eg_request = eg_property = eg_subtask = eg_queasy = eg_vperform = None

    t_hisroom = tprop = tbuff = None

    t_hisroom_list, T_hisroom = create_model("T_hisroom", {"itemno":str, "bezeich":str, "reqno":str, "opend":str, "processd":str, "doned":str, "subtask":str, "reqstat":str, "flag":str})
    tprop_list, Tprop = create_model("Tprop", {"nr":int, "nm":str})

    Tbuff = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gtotal, t_hisroom_list, tprop_list, tot, curr_gtotal, int_str, l_artikel, eg_request, eg_property, eg_subtask, eg_queasy, eg_vperform
        nonlocal tbuff


        nonlocal t_hisroom, tprop, tbuff
        nonlocal t_hisroom_list, tprop_list
        return {"gtotal": gtotal, "t-hisroom": t_hisroom_list, "tprop": tprop_list}

    def create_history():

        nonlocal gtotal, t_hisroom_list, tprop_list, tot, curr_gtotal, int_str, l_artikel, eg_request, eg_property, eg_subtask, eg_queasy, eg_vperform
        nonlocal tbuff


        nonlocal t_hisroom, tprop, tbuff
        nonlocal t_hisroom_list, tprop_list

        char4:str = ""
        a:str = ""
        b:str = ""
        c:str = ""
        itotal:decimal = 0
        nm_prop1:str = ""
        t_hisroom_list.clear()
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


                t_hisroom = T_hisroom()
                t_hisroom_list.append(t_hisroom)

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

            eg_subtask = db_session.query(Eg_subtask).filter(
                    (Eg_subtask.sub_CODE == eg_request.sub_task)).first()

            if eg_subtask:
                char4 = to_string(eg_subtask.bezeich)
            else:
                char4 = ""
            t_hisroom = T_hisroom()
            t_hisroom_list.append(t_hisroom)

            t_hisroom.itemno = to_string(eg_request.propertynr, "->>>>>>9")
            t_hisroom.bezeich = nm_prop1
            t_hisroom.reqno = to_string(eg_request.reqnr , "->>>>>>9")
            t_hisroom.opend = a
            t_hisroom.processd = b
            t_hisroom.doned = c
            t_hisroom.subtask = char4
            t_hisroom.reqstat = int_str[eg_request.reqstatus - 1]
            t_hisroom.flag = "1"

            eg_queasy = db_session.query(Eg_queasy).filter(
                    (Eg_queasy.key == 1) &  (Eg_queasy.reqnr == eg_request.reqnr)).first()

            if eg_queasy:

                for eg_queasy in db_session.query(Eg_queasy).filter(
                        (Eg_queasy.key == 1) &  (Eg_queasy.reqnr == eg_request.reqnr)).all():

                    tbuff = db_session.query(Tbuff).filter(
                            (Tbuff.artnr == eg_queasy.stock_nr)).first()

                    if tbuff:
                        itotal = eg_queasy.deci1 * eg_queasy.price
                    tot = tot + itotal

            eg_vperform = db_session.query(Eg_vperform).filter(
                    (Eg_vperform.reqnr == eg_request.reqnr)).first()

            if eg_vperform:

                for eg_vperform in db_session.query(Eg_vperform).filter(
                        (Eg_vperform.reqnr == eg_request.reqnr)).all():
                    tot = tot + eg_vperform.price

            if tot != 0:
                curr_gtotal = curr_gtotal + tot
                tot = 0

        if curr_gtotal != 0:
            gtotal = to_string(curr_gtotal, "->>>,>>>,>>>,>>9.99")

    create_history()

    return generate_output()