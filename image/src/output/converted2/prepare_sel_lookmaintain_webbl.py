#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_location, L_artikel, Eg_moveproperty, Eg_property, Eg_request, Eg_subtask, Eg_queasy, Eg_vperform, Eg_maintain, Eg_mdetail, Eg_action, Eg_staff, Eg_propmeter

def prepare_sel_lookmaintain_webbl(pvilanguage:int, prop_nr:int):

    prepare_cache ([Eg_location, Eg_moveproperty, Eg_property, Eg_request, Eg_subtask, Eg_queasy, Eg_vperform, Eg_staff, Eg_propmeter])

    e_price = to_decimal("0.0")
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
    btotal:Decimal = to_decimal("0.0")
    int_str:List[string] = ["New", "Processed", "Done", "Postponed", "Closed"]
    lvcarea:string = "sel-lookMaintain-web"
    typestr:List[string] = create_empty_list(3,"")
    typeworkstr:List[string] = create_empty_list(6,"")
    eg_location = l_artikel = eg_moveproperty = eg_property = eg_request = eg_subtask = eg_queasy = eg_vperform = eg_maintain = eg_mdetail = eg_action = eg_staff = eg_propmeter = None

    t_head = t_line_cost = t_line_vendor = mainaction = tmaintain = flocation = tlocation = q1_list = qbuff = tbuff = None

    t_head_list, T_head = create_model("T_head", {"reqno":string, "datum":string, "task":string, "str_stat":string})
    t_line_cost_list, T_line_cost = create_model("T_line_cost", {"reqno":string, "artno":string, "bezeich2":string, "qty":string, "price":string, "tot_dtl":string})
    t_line_vendor_list, T_line_vendor = create_model("T_line_vendor", {"reqno":string, "outsource":string, "vendor_nm":string, "startdate":string, "finishdate":string, "price":string, "tot_dtl":string})
    mainaction_list, Mainaction = create_model("Mainaction", {"maintainnr":int, "action_nr":int, "action_nm":string, "create_date":date, "create_time":int, "time_str":string, "create_by":string})
    tmaintain_list, Tmaintain = create_model("Tmaintain", {"maintainnr":int, "workdate":date, "donedate":date, "estworkdate":date, "type":int, "type_nm":string, "typework":int, "typework_nm":string, "location":int, "location_nm":string, "zinr":string, "propertynr":int, "property_nm":string, "maintask":int, "maintask_nm":string, "category":int, "category_nm":string, "pic":int, "pic_nm":string, "comments":string, "create_by":string, "create_date":date, "memo":string})
    flocation_list, Flocation = create_model("Flocation", {"loc_nr":int, "loc_nm":string})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string})
    q1_list_list, Q1_list = create_model("Q1_list", {"datum":date, "fr_room":string, "f_loc_nm":string, "t_loc_nm":string, "to_room":string})

    Qbuff = create_buffer("Qbuff",Eg_location)
    Tbuff = create_buffer("Tbuff",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal e_price, e_datum, avail_eg_property, rec_meter, rec_hour, rec_date, rec_time, tot_cost, tot_vend, t_head_list, t_line_cost_list, t_line_vendor_list, q1_list_list, tmaintain_list, mainaction_list, atotal, tot, btotal, int_str, lvcarea, typestr, typeworkstr, eg_location, l_artikel, eg_moveproperty, eg_property, eg_request, eg_subtask, eg_queasy, eg_vperform, eg_maintain, eg_mdetail, eg_action, eg_staff, eg_propmeter
        nonlocal pvilanguage, prop_nr
        nonlocal qbuff, tbuff


        nonlocal t_head, t_line_cost, t_line_vendor, mainaction, tmaintain, flocation, tlocation, q1_list, qbuff, tbuff
        nonlocal t_head_list, t_line_cost_list, t_line_vendor_list, mainaction_list, tmaintain_list, flocation_list, tlocation_list, q1_list_list

        return {"e_price": e_price, "e_datum": e_datum, "avail_eg_property": avail_eg_property, "rec_meter": rec_meter, "rec_hour": rec_hour, "rec_date": rec_date, "rec_time": rec_time, "tot_cost": tot_cost, "tot_vend": tot_vend, "t-head": t_head_list, "t-line-cost": t_line_cost_list, "t-line-vendor": t_line_vendor_list, "q1-list": q1_list_list, "tMaintain": tmaintain_list, "MainAction": mainaction_list}

    def create_history():

        nonlocal e_price, e_datum, avail_eg_property, rec_meter, rec_hour, rec_date, rec_time, tot_cost, tot_vend, t_head_list, t_line_cost_list, t_line_vendor_list, q1_list_list, tmaintain_list, mainaction_list, atotal, tot, btotal, int_str, lvcarea, typestr, typeworkstr, eg_location, l_artikel, eg_moveproperty, eg_property, eg_request, eg_subtask, eg_queasy, eg_vperform, eg_maintain, eg_mdetail, eg_action, eg_staff, eg_propmeter
        nonlocal pvilanguage, prop_nr
        nonlocal qbuff, tbuff


        nonlocal t_head, t_line_cost, t_line_vendor, mainaction, tmaintain, flocation, tlocation, q1_list, qbuff, tbuff
        nonlocal t_head_list, t_line_cost_list, t_line_vendor_list, mainaction_list, tmaintain_list, flocation_list, tlocation_list, q1_list_list

        str_date1:string = ""
        str_date2:string = ""
        char4:string = ""
        a:string = ""
        b:string = ""
        vendo_nm:string = ""
        itotal:Decimal = to_decimal("0.0")

        for eg_request in db_session.query(Eg_request).filter(
                 (Eg_request.propertynr == prop_nr)).order_by(Eg_request.opened_date, Eg_request.reqnr).all():

            if eg_request.opened_date == None:
                a = ""
            else:
                a = to_string(eg_request.opened_date , "99/99/99")

            eg_subtask = get_cache (Eg_subtask, {"sub_code": [(eq, eg_request.sub_task)]})

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

            eg_queasy = get_cache (Eg_queasy, {"key": [(eq, 1)],"reqnr": [(eq, eg_request.reqnr)]})

            if eg_queasy:

                for eg_queasy in db_session.query(Eg_queasy).filter(
                         (Eg_queasy.key == 1) & (Eg_queasy.reqnr == eg_request.reqnr)).order_by(Eg_queasy._recid).all():

                    tbuff = db_session.query(Tbuff).filter(
                             (Tbuff.artnr == eg_queasy.stock_nr)).first()

                    if tbuff:
                        itotal =  to_decimal(eg_queasy.deci1) * to_decimal(eg_queasy.price)
                    tot = tot + itotal

            eg_vperform = get_cache (Eg_vperform, {"reqnr": [(eq, eg_request.reqnr)]})

            if eg_vperform:

                for eg_vperform in db_session.query(Eg_vperform).filter(
                         (Eg_vperform.reqnr == eg_request.reqnr)).order_by(Eg_vperform._recid).all():
                    tot = tot + eg_vperform.price

            if tot != 0:
                btotal =  to_decimal(btotal) + to_decimal(tot)
                tot = 0

        if btotal != 0:
            tot_cost = to_string(btotal, "->>>,>>>,>>>,>>9.99")


    def create_maintain():

        nonlocal e_price, e_datum, avail_eg_property, rec_meter, rec_hour, rec_date, rec_time, tot_cost, tot_vend, t_head_list, t_line_cost_list, t_line_vendor_list, q1_list_list, tmaintain_list, mainaction_list, atotal, tot, btotal, int_str, lvcarea, typestr, typeworkstr, eg_location, l_artikel, eg_moveproperty, eg_property, eg_request, eg_subtask, eg_queasy, eg_vperform, eg_maintain, eg_mdetail, eg_action, eg_staff, eg_propmeter
        nonlocal pvilanguage, prop_nr
        nonlocal qbuff, tbuff


        nonlocal t_head, t_line_cost, t_line_vendor, mainaction, tmaintain, flocation, tlocation, q1_list, qbuff, tbuff
        nonlocal t_head_list, t_line_cost_list, t_line_vendor_list, mainaction_list, tmaintain_list, flocation_list, tlocation_list, q1_list_list

        mainbuff = None
        mdetailbuff = None
        actionbuff = None
        pic_nm:string = ""
        type_nm:string = ""
        typework_nm:string = ""
        action_nm:string = ""
        Mainbuff =  create_buffer("Mainbuff",Eg_maintain)
        Mdetailbuff =  create_buffer("Mdetailbuff",Eg_mdetail)
        Actionbuff =  create_buffer("Actionbuff",Eg_action)

        for mainbuff in db_session.query(Mainbuff).filter(
                 (Mainbuff.propertynr == prop_nr)).order_by(Mainbuff._recid).all():

            eg_staff = get_cache (Eg_staff, {"nr": [(eq, mainbuff.pic)]})

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
            tmaintain.type = mainbuff.type
            tmaintain.type_nm = typestr[mainbuff.type - 1]
            tmaintain.typework = mainbuff.typework
            tmaintain.typework_nm = typeworkstr[mainbuff.typework - 1]
            tmaintain.pic = mainbuff.pic
            tmaintain.pic_nm = pic_nm
            tmaintain.comments = mainbuff.comments

            for mdetailbuff in db_session.query(Mdetailbuff).filter(
                     (Mdetailbuff.key == 1) & (Mdetailbuff.maintainnr == mainbuff.maintainnr)).order_by(Mdetailbuff._recid).all():

                actionbuff = db_session.query(Actionbuff).filter(
                         (Actionbuff.actionnr == mdetailbuff.nr)).first()

                if actionbuff:
                    action_nm = actionbuff.bezeich
                else:
                    action_nm = ""
                mainaction = Mainaction()
                mainaction_list.append(mainaction)

                mainaction.maintainnr = mdetailbuff.maintainnr
                mainaction.action_nr = mdetailbuff.nr
                mainaction.action_nm = action_nm
                mainaction.create_date = mdetailbuff.create_date
                mainaction.create_time = mdetailbuff.create_time
                mainaction.time_str = to_string(mdetailbuff.create_time , "HH:MM:SS")
                mainaction.create_by = mdetailbuff.create_by


    def if_meter():

        nonlocal e_price, e_datum, avail_eg_property, rec_meter, rec_hour, rec_date, rec_time, tot_cost, tot_vend, t_head_list, t_line_cost_list, t_line_vendor_list, q1_list_list, tmaintain_list, mainaction_list, atotal, tot, btotal, int_str, lvcarea, typestr, typeworkstr, eg_location, l_artikel, eg_moveproperty, eg_property, eg_request, eg_subtask, eg_queasy, eg_vperform, eg_maintain, eg_mdetail, eg_action, eg_staff, eg_propmeter
        nonlocal pvilanguage, prop_nr
        nonlocal qbuff, tbuff


        nonlocal t_head, t_line_cost, t_line_vendor, mainaction, tmaintain, flocation, tlocation, q1_list, qbuff, tbuff
        nonlocal t_head_list, t_line_cost_list, t_line_vendor_list, mainaction_list, tmaintain_list, flocation_list, tlocation_list, q1_list_list

        eg_property = get_cache (Eg_property, {"nr": [(eq, prop_nr)],"meterrec": [(eq, True)]})

        if eg_property:

            eg_propmeter = db_session.query(Eg_propmeter).filter(
                     (Eg_propmeter.propertynr == prop_nr)).order_by(Eg_propmeter._recid.desc()).first()

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
    flocation_list.clear()
    tlocation_list.clear()

    for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():
        tlocation = Tlocation()
        tlocation_list.append(tlocation)

        tlocation.loc_nr = qbuff.nr
        tlocation.loc_nm = qbuff.bezeich


        flocation = Flocation()
        flocation_list.append(flocation)

        flocation.loc_nr = qbuff.nr
        flocation.loc_nm = qbuff.bezeich

    eg_moveproperty_obj_list = {}
    for eg_moveproperty in db_session.query(Eg_moveproperty).filter(
             (Eg_moveproperty.property_nr == prop_nr)).order_by(Eg_moveproperty._recid).all():
        flocation = query(flocation_list, (lambda flocation: flocation.loc_nr == eg_moveproperty.fr_location), first=True)
        if not flocation:
            continue

        tlocation = query(tlocation_list, (lambda tlocation: tlocation.loc_nr == eg_moveproperty.to_location), first=True)
        if not tlocation:
            continue

        if eg_moveproperty_obj_list.get(eg_moveproperty._recid):
            continue
        else:
            eg_moveproperty_obj_list[eg_moveproperty._recid] = True


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.datum = eg_moveproperty.datum
        q1_list.f_loc_nm = flocation.loc_nm
        q1_list.fr_room = eg_moveproperty.fr_room
        q1_list.t_loc_nm = tlocation.loc_nm
        q1_list.to_room = eg_moveproperty.to_room

    eg_property = get_cache (Eg_property, {"nr": [(eq, prop_nr)]})

    if eg_property:
        avail_eg_property = True
        e_price =  to_decimal(eg_property.price)
        e_datum = eg_property.datum


    create_history()
    create_maintain()
    if_meter()

    return generate_output()