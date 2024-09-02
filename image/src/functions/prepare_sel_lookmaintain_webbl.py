from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_location, L_artikel, Eg_moveproperty, Eg_property, Eg_request, Eg_subtask, Eg_queasy, Eg_vperform, Eg_maintain, Eg_mdetail, Eg_action, Eg_staff, Eg_propmeter

def prepare_sel_lookmaintain_webbl(pvilanguage:int, prop_nr:int):
    e_price = 0
    e_datum = None
    avail_eg_property = False
    rec_meter = 0
    rec_hour = 0
    rec_date = None
    rec_time = ""
    tot_cost = ""
    tot_vend = ""
    t_head_list = []
    t_line_cost_list = []
    t_line_vendor_list = []
    q1_list_list = []
    tmaintain_list = []
    mainaction_list = []
    atotal:int = 0
    tot:int = 0
    btotal:decimal = 0
    int_str:[str] = ["", "", "", "", "", ""]
    lvcarea:str = "sel_lookMaintain_web"
    typestr:[str] = ["", "", "", ""]
    typeworkstr:[str] = ["", "", "", "", "", "", ""]
    eg_location = l_artikel = eg_moveproperty = eg_property = eg_request = eg_subtask = eg_queasy = eg_vperform = eg_maintain = eg_mdetail = eg_action = eg_staff = eg_propmeter = None

    t_head = t_line_cost = t_line_vendor = mainaction = tmaintain = flocation = tlocation = q1_list = qbuff = tbuff = mainbuff = mdetailbuff = actionbuff = None

    t_head_list, T_head = create_model("T_head", {"reqno":str, "datum":str, "task":str, "str_stat":str})
    t_line_cost_list, T_line_cost = create_model("T_line_cost", {"reqno":str, "artno":str, "bezeich2":str, "qty":str, "price":str, "tot_dtl":str})
    t_line_vendor_list, T_line_vendor = create_model("T_line_vendor", {"reqno":str, "outsource":str, "vendor_nm":str, "startdate":str, "finishdate":str, "price":str, "tot_dtl":str})
    mainaction_list, Mainaction = create_model("Mainaction", {"maintainnr":int, "action_nr":int, "action_nm":str, "create_date":date, "create_time":int, "time_str":str, "create_by":str})
    tmaintain_list, Tmaintain = create_model("Tmaintain", {"maintainnr":int, "workdate":date, "donedate":date, "estworkdate":date, "type":int, "type_nm":str, "typework":int, "typework_nm":str, "location":int, "location_nm":str, "zinr":str, "propertynr":int, "property_nm":str, "maintask":int, "maintask_nm":str, "category":int, "category_nm":str, "pic":int, "pic_nm":str, "comments":str, "create_by":str, "create_date":date, "memo":str})
    flocation_list, Flocation = create_model("Flocation", {"loc_nr":int, "loc_nm":str})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str})
    q1_list_list, Q1_list = create_model("Q1_list", {"datum":date, "fr_room":str, "f_loc_nm":str, "t_loc_nm":str, "to_room":str})

    Qbuff = Eg_location
    Tbuff = L_artikel
    Mainbuff = Eg_maintain
    Mdetailbuff = Eg_mdetail
    Actionbuff = Eg_action

    db_session = local_storage.db_session

    def generate_output():
        nonlocal e_price, e_datum, avail_eg_property, rec_meter, rec_hour, rec_date, rec_time, tot_cost, tot_vend, t_head_list, t_line_cost_list, t_line_vendor_list, q1_list_list, tmaintain_list, mainaction_list, atotal, tot, btotal, int_str, lvcarea, typestr, typeworkstr, eg_location, l_artikel, eg_moveproperty, eg_property, eg_request, eg_subtask, eg_queasy, eg_vperform, eg_maintain, eg_mdetail, eg_action, eg_staff, eg_propmeter
        nonlocal qbuff, tbuff, mainbuff, mdetailbuff, actionbuff


        nonlocal t_head, t_line_cost, t_line_vendor, mainaction, tmaintain, flocation, tlocation, q1_list, qbuff, tbuff, mainbuff, mdetailbuff, actionbuff
        nonlocal t_head_list, t_line_cost_list, t_line_vendor_list, mainaction_list, tmaintain_list, flocation_list, tlocation_list, q1_list_list
        return {"e_price": e_price, "e_datum": e_datum, "avail_eg_property": avail_eg_property, "rec_meter": rec_meter, "rec_hour": rec_hour, "rec_date": rec_date, "rec_time": rec_time, "tot_cost": tot_cost, "tot_vend": tot_vend, "t-head": t_head_list, "t-line-cost": t_line_cost_list, "t-line-vendor": t_line_vendor_list, "q1-list": q1_list_list, "tMaintain": tmaintain_list, "MainAction": mainaction_list}

    def create_history():

        nonlocal e_price, e_datum, avail_eg_property, rec_meter, rec_hour, rec_date, rec_time, tot_cost, tot_vend, t_head_list, t_line_cost_list, t_line_vendor_list, q1_list_list, tmaintain_list, mainaction_list, atotal, tot, btotal, int_str, lvcarea, typestr, typeworkstr, eg_location, l_artikel, eg_moveproperty, eg_property, eg_request, eg_subtask, eg_queasy, eg_vperform, eg_maintain, eg_mdetail, eg_action, eg_staff, eg_propmeter
        nonlocal qbuff, tbuff, mainbuff, mdetailbuff, actionbuff


        nonlocal t_head, t_line_cost, t_line_vendor, mainaction, tmaintain, flocation, tlocation, q1_list, qbuff, tbuff, mainbuff, mdetailbuff, actionbuff
        nonlocal t_head_list, t_line_cost_list, t_line_vendor_list, mainaction_list, tmaintain_list, flocation_list, tlocation_list, q1_list_list

        str_date1:str = ""
        str_date2:str = ""
        char4:str = ""
        a:str = ""
        b:str = ""
        vendo_nm:str = ""
        itotal:decimal = 0

        for eg_request in db_session.query(Eg_request).filter(
                (Eg_request.propertynr == prop_nr)).all():

            if eg_request.opened_date == None:
                a = ""
            else:
                a = to_string(eg_request.opened_date , "99/99/99")

            eg_subtask = db_session.query(Eg_subtask).filter(
                    (Eg_subtask.sub_CODE == eg_request.sub_task)).first()

            if eg_subtask:
                char4 = eg_subtask.bezeich
            else:
                char4 = ""
            t_head = T_head()
            t_head_list.append(t_head)

            t_head.reqno = to_string(eg_request.reqnr , "->>>>>>9")
            t_head.datum = a
            t_head.task = char4
            t_head.str_stat = int_str[eg_request.reqstatus - 1]

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
                btotal = btotal + tot
                tot = 0

        if btotal != 0:
            tot_cost = to_string(btotal, "->>>,>>>,>>>,>>9.99")

    def create_maintain():

        nonlocal e_price, e_datum, avail_eg_property, rec_meter, rec_hour, rec_date, rec_time, tot_cost, tot_vend, t_head_list, t_line_cost_list, t_line_vendor_list, q1_list_list, tmaintain_list, mainaction_list, atotal, tot, btotal, int_str, lvcarea, typestr, typeworkstr, eg_location, l_artikel, eg_moveproperty, eg_property, eg_request, eg_subtask, eg_queasy, eg_vperform, eg_maintain, eg_mdetail, eg_action, eg_staff, eg_propmeter
        nonlocal qbuff, tbuff, mainbuff, mdetailbuff, actionbuff


        nonlocal t_head, t_line_cost, t_line_vendor, mainaction, tmaintain, flocation, tlocation, q1_list, qbuff, tbuff, mainbuff, mdetailbuff, actionbuff
        nonlocal t_head_list, t_line_cost_list, t_line_vendor_list, mainaction_list, tmaintain_list, flocation_list, tlocation_list, q1_list_list

        pic_nm:str = ""
        type_nm:str = ""
        typework_nm:str = ""
        action_nm:str = ""
        Mainbuff = Eg_maintain
        Mdetailbuff = Eg_mdetail
        Actionbuff = Eg_action

        for mainbuff in db_session.query(Mainbuff).filter(
                (Mainbuff.propertynr == prop_nr)).all():

            eg_staff = db_session.query(Eg_staff).filter(
                    (Eg_staff.nr == mainbuff.pic)).first()

            if eg_staff:
                pic_nm = eg_staff.name
            else:
                pic_nm = ""
            tmaintain = Tmaintain()
            tmaintain_list.append(tmaintain)

            tmaintain.maintainnr = mainbuff.maintainnr
            tmaintain.workdate = mainbuff.workdate
            tmaintain.donedate = mainbuff.donedate
            tmaintain.estworkdate = mainbuff.estworkdate
            tmaintain.type = mainbuff.TYPE
            tmaintain.type_nm = typestr[mainbuff.TYPE - 1]
            tmaintain.typework = mainbuff.typework
            tmaintain.typework_nm = typeworkstr[mainbuff.TYPEwork - 1]
            tmaintain.pic = mainbuff.pic
            tmaintain.pic_nm = pic_nm
            tmaintain.comments = mainbuff.comments

            for mdetailbuff in db_session.query(Mdetailbuff).filter(
                    (Mdetailbuff.key == 1) &  (Mdetailbuff.maintainnr == mainbuff.maintainnr)).all():

                actionbuff = db_session.query(Actionbuff).filter(
                        (Actionbuff.actionnr == mdetailbuff.nr)).first()

                if actionBuff:
                    action_nm = actionbuff.bezeich
                else:
                    action_nm = ""
                mainaction = Mainaction()
                mainaction_list.append(mainaction)

                mainaction.Maintainnr = mdetailbuff.maintainnr
                mainaction.action_nr = mdetailbuff.nr
                mainaction.action_nm = action_nm
                mainaction.create_date = mdetailbuff.create_date
                mainaction.create_time = mdetailbuff.create_time
                mainaction.time_str = to_string(mdetailbuff.create_time , "HH:MM:SS")
                mainaction.create_by = mdetailbuff.create_by

    def if_meter():

        nonlocal e_price, e_datum, avail_eg_property, rec_meter, rec_hour, rec_date, rec_time, tot_cost, tot_vend, t_head_list, t_line_cost_list, t_line_vendor_list, q1_list_list, tmaintain_list, mainaction_list, atotal, tot, btotal, int_str, lvcarea, typestr, typeworkstr, eg_location, l_artikel, eg_moveproperty, eg_property, eg_request, eg_subtask, eg_queasy, eg_vperform, eg_maintain, eg_mdetail, eg_action, eg_staff, eg_propmeter
        nonlocal qbuff, tbuff, mainbuff, mdetailbuff, actionbuff


        nonlocal t_head, t_line_cost, t_line_vendor, mainaction, tmaintain, flocation, tlocation, q1_list, qbuff, tbuff, mainbuff, mdetailbuff, actionbuff
        nonlocal t_head_list, t_line_cost_list, t_line_vendor_list, mainaction_list, tmaintain_list, flocation_list, tlocation_list, q1_list_list

        eg_property = db_session.query(Eg_property).filter(
                (Eg_property.nr == prop_nr) &  (Eg_property.meterrec)).first()

        if eg_property:

            eg_propmeter = db_session.query(Eg_propmeter).filter(
                    (Eg_propmeter.propertynr == prop_nr)).first()

            if eg_propmeter:
                rec_meter = eg_propmeter.val_meter
                rec_hour = eg_propmeter.val_hour
                rec_date = eg_propmeter.rec_date
                rec_time = ""


            else:
                rec_meter = 0
                rec_hour = 0
                rec_date = None
                rec_time = ""


        else:
            rec_meter = 0
            rec_hour = 0
            rec_date = None
            rec_time = ""

    typestr[0] = translateExtended ("Scheduled", lvcarea, "")
    typestr[1] = translateExtended ("Processed", lvcarea, "")
    typestr[2] = translateExtended ("Done", lvcarea, "")
    typeworkstr[0] = translateExtended ("Daily", lvcarea, "")
    typeworkstr[1] = translateExtended ("Weekly", lvcarea, "")
    typeworkstr[2] = translateExtended ("Monthly", lvcarea, "")
    typeworkstr[3] = translateExtended ("Quarter", lvcarea, "")
    typeworkstr[4] = translateExtended ("Half Yearly", lvcarea, "")
    typeworkstr[5] = translateExtended ("Yearly", lvcarea, "")
    fLocation_list.clear()
    tLocation_list.clear()

    for qbuff in db_session.query(Qbuff).all():
        tlocation = Tlocation()
        tlocation_list.append(tlocation)

        tLocation.loc_nr = qbuff.nr
        tLocation.loc_nm = qbuff.bezeich


        flocation = Flocation()
        flocation_list.append(flocation)

        fLocation.loc_nr = qbuff.nr
        fLocation.loc_nm = qbuff.bezeich

    eg_moveproperty_obj_list = []
    for eg_moveproperty, flocation, tlocation in db_session.query(Eg_moveproperty, Flocation, Tlocation).join(Flocation,(Flocation.loc_nr == Eg_moveproperty.fr_location)).join(Tlocation,(Tlocation.loc_nr == Eg_moveproperty.to_location)).filter(
            (Eg_moveproperty.property_nr == prop_nr)).all():
        if eg_moveproperty._recid in eg_moveproperty_obj_list:
            continue
        else:
            eg_moveproperty_obj_list.append(eg_moveproperty._recid)


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.datum = eg_moveproperty.datum
        q1_list.f_loc_nm = flocation.loc_nm
        q1_list.fr_room = eg_moveproperty.fr_room
        q1_list.t_loc_nm = tlocation.loc_nm
        q1_list.to_room = eg_moveproperty.to_room

    eg_property = db_session.query(Eg_property).filter(
            (Eg_property.nr == prop_nr)).first()

    if eg_property:
        avail_eg_property = True
        e_price = eg_property.price
        e_datum = eg_property.datum


    create_history()
    create_maintain()
    if_meter()

    return generate_output()