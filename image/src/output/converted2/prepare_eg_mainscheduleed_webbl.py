#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_location, Zimmer, Queasy, Eg_action, Eg_maintain, Res_line, Guest, Htparam, Bediener, Eg_property, Eg_mobilenr, Eg_mdetail, Eg_alert, Eg_staff

def prepare_eg_mainscheduleed_webbl(pvilanguage:int, mainno:int, user_init:string):

    prepare_cache ([Res_line, Guest, Htparam, Bediener, Eg_property, Eg_mobilenr, Eg_alert, Eg_staff])

    sguestflag = False
    groupid = 0
    engid = 0
    sms_flag = False
    avail_eg_location = False
    h_category = 0
    h_maintask = 0
    h_location = 0
    h_zinr = ""
    str_property = ""
    str_maintask = ""
    str_categ = ""
    ci_date = None
    flag1 = 0
    flag2 = 0
    flag3 = 0
    flag4 = 0
    flag5 = 0
    flag6 = 0
    flag7 = 0
    flag8 = 0
    send_alert_list = []
    his_action_list = []
    mobile_list = []
    action_list = []
    maintain_list = []
    t_eg_location_list = []
    t_zimmer_list = []
    t_queasy_list = []
    t_property_list = []
    tpic_list = []
    lvcarea:string = "eg-mainscheduleEd"
    alert_str:List[string] = create_empty_list(3,"")
    guestname:string = ""
    eg_location = zimmer = queasy = eg_action = eg_maintain = res_line = guest = htparam = bediener = eg_property = eg_mobilenr = eg_mdetail = eg_alert = eg_staff = None

    t_eg_location = t_zimmer = t_queasy = send_alert = his_action = mobile = action = maintain = mbuff = resline1 = guest1 = t_property = tpic = None

    t_eg_location_list, T_eg_location = create_model_like(Eg_location)
    t_zimmer_list, T_zimmer = create_model_like(Zimmer, {"gname_str":string})
    t_queasy_list, T_queasy = create_model_like(Queasy)
    send_alert_list, Send_alert = create_model("Send_alert", {"alert_date":date, "alert_time":int, "alert_str":string, "alert_reqnr":int, "alert_msg":string, "alert_sendto":int, "alert_sendnm":string, "alert_sendnr":string, "alert_msgstatus":int, "alert_mstat":string})
    his_action_list, His_action = create_model("His_action", {"action_mainnr":int, "action_nr":int, "action_nm":string, "create_date":date, "create_time":int, "time_str":string, "create_by":string})
    mobile_list, Mobile = create_model("Mobile", {"nr":int, "name":string, "position":string, "mobilenr":string, "mobile_selected":bool})
    action_list, Action = create_model_like(Eg_action, {"selected":bool})
    maintain_list, Maintain = create_model_like(Eg_maintain)
    t_property_list, T_property = create_model("T_property", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pcateg_nr":int, "pcateg":string, "pmain_nr":int, "pmain":string, "ploc_nr":int, "ploc":string, "pzinr":string})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_dept":int})

    Mbuff = create_buffer("Mbuff",Eg_maintain)
    Resline1 = create_buffer("Resline1",Res_line)
    Guest1 = create_buffer("Guest1",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal pvilanguage, mainno, user_init
        nonlocal mbuff, resline1, guest1


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        return {"sguestflag": sguestflag, "groupid": groupid, "engid": engid, "sms_flag": sms_flag, "avail_eg_location": avail_eg_location, "h_category": h_category, "h_maintask": h_maintask, "h_location": h_location, "h_zinr": h_zinr, "str_property": str_property, "str_maintask": str_maintask, "str_categ": str_categ, "ci_date": ci_date, "flag1": flag1, "flag2": flag2, "flag3": flag3, "flag4": flag4, "flag5": flag5, "flag6": flag6, "flag7": flag7, "flag8": flag8, "send-alert": send_alert_list, "his-action": his_action_list, "mobile": mobile_list, "action": action_list, "maintain": maintain_list, "t-eg-location": t_eg_location_list, "t-zimmer": t_zimmer_list, "t-queasy": t_queasy_list, "t-property": t_property_list, "tpic": tpic_list}

    def define_group():

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal pvilanguage, mainno, user_init
        nonlocal mbuff, resline1, guest1


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def define_engineering():

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal pvilanguage, mainno, user_init
        nonlocal mbuff, resline1, guest1


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            pass


    def getmaintain():

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal pvilanguage, mainno, user_init
        nonlocal mbuff, resline1, guest1


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        bprop = None
        quesbuff = None
        quesbuff1 = None
        Bprop =  create_buffer("Bprop",Eg_property)
        Quesbuff =  create_buffer("Quesbuff",Queasy)
        Quesbuff1 =  create_buffer("Quesbuff1",Queasy)
        maintain_list.clear()

        mbuff = db_session.query(Mbuff).filter(
                 (Mbuff.maintainnr == mainno)).first()

        if not mbuff:

            return
        else:
            buffer_copy(mbuff, maintain)

            if maintain.smsflag :
                sms_flag = True

            bprop = get_cache (Eg_property, {"nr": [(eq, maintain.propertynr)]})

            if bprop:
                h_maintask = bprop.maintask
                h_location = bprop.location
                h_zinr = bprop.zinr
                str_property = bprop.bezeich
                maintain.propertynr = bprop.nr

                quesbuff = db_session.query(Quesbuff).filter(
                         (Quesbuff.key == 133) & (Quesbuff.number1 == bprop.maintask)).first()

                if quesbuff:
                    str_maintask = quesbuff.char1
                    h_maintask = quesbuff.number1

                    action = query(action_list, filters=(lambda action: action.maintask == h_maintask), first=True)

                    if action:
                        flag1 = 1
                    else:
                        flag1 = 2

                    quesbuff1 = db_session.query(Quesbuff1).filter(
                             (Quesbuff1.key == 132) & (Quesbuff1.number1 == quesbuff.number2)).first()

                    if quesbuff1:
                        h_category = quesbuff1.number1
                        str_categ = quesbuff1.char1


                    else:
                        h_category = 0
                        str_categ = ""


                else:
                    h_maintask = 0
                    str_maintask = ""


                flag2 = 1

                eg_location = get_cache (Eg_location, {"nr": [(eq, bprop.location)],"guestflag": [(eq, True)]})

                if eg_location:
                    flag3 = 1
                    sguestflag = True
                    h_location = 0


                else:
                    flag3 = 2
                    sguestflag = False


            else:
                h_maintask = 0
                h_location = 0
                h_zinr = "0"


                flag4 = 1

            if sguestflag == False:
                flag5 = 1
            else:
                flag5 = 2
            flag6 = 1
            getaction(h_maintask)

            if maintain.type == 3:
                flag7 = 1

                return
            else:
                flag7 = 2


    def create_mobile():

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal pvilanguage, mainno, user_init
        nonlocal mbuff, resline1, guest1


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_mobilenr)

        for mobile in query(mobile_list):
            mobile_list.remove(mobile)

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.activeflag) & (Qbuff.mobilenr != "")).order_by(Qbuff._recid).all():
            mobile = Mobile()
            mobile_list.append(mobile)

            mobile.nr = qbuff.nr
            mobile.name = qbuff.name
            mobile.position = qbuff.position
            mobile.mobilenr = qbuff.mobilenr
            mobile.mobile_selected = False


    def getprevaction():

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal pvilanguage, mainno, user_init
        nonlocal mbuff, resline1, guest1


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        dbuff = None
        buff_action = None
        Dbuff =  create_buffer("Dbuff",Eg_mdetail)
        Buff_action =  create_buffer("Buff_action",Eg_action)
        his_action_list.clear()

        dbuff_obj_list = {}
        for dbuff, buff_action in db_session.query(Dbuff, Buff_action).join(Buff_action,(Buff_action.actionnr == Dbuff.nr)).filter(
                 (Dbuff.maintainnr == mainno) & (Dbuff.key == 1)).order_by(Dbuff._recid).all():
            if dbuff_obj_list.get(dbuff._recid):
                continue
            else:
                dbuff_obj_list[dbuff._recid] = True


            his_action = His_action()
            his_action_list.append(his_action)

            his_action.action_mainnr = dbuff.maintainnr
            his_action.action_nr = dbuff.nr
            his_action.action_nm = buff_action.bezeich
            his_action.create_date = dbuff.create_date
            his_action.create_time = dbuff.create_time
            his_action.time_str = to_string(dbuff.create_time , "HH:MM:SS")
            his_action.create_by = dbuff.create_by


    def create_alert():

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal pvilanguage, mainno, user_init
        nonlocal mbuff, resline1, guest1


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        b:string = ""
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_alert)
        send_alert_list.clear()

        for eg_alert in db_session.query(Eg_alert).filter(
                 (Eg_alert.fromfile == ("3").lower()) & (Eg_alert.reqnr == mainno)).order_by(Eg_alert._recid).all():

            eg_mobilenr = get_cache (Eg_mobilenr, {"nr": [(eq, eg_alert.sendto)]})

            if eg_mobilenr:
                b = eg_mobilenr.name
            else:
                b = "Staff Record Not Found"
            send_alert = Send_alert()
            send_alert_list.append(send_alert)

            send_alert.alert_date = eg_alert.create_date
            send_alert.alert_time = eg_alert.create_time
            send_alert.alert_str = to_string(eg_alert.create_time , "HH:MM")
            send_alert.alert_reqnr = eg_alert.reqnr
            send_alert.alert_msg = eg_alert.msg
            send_alert.alert_sendto = eg_alert.sendto
            send_alert.alert_sendnm = b
            send_alert.alert_sendnr = eg_alert.sendnr
            send_alert.alert_msgstatus = eg_alert.msgstatus
            send_alert.alert_mstat = alert_str[eg_alert.msgstatus - 1]


    def getaction(rmaintask:int):

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal pvilanguage, mainno, user_init
        nonlocal mbuff, resline1, guest1


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        qbuff = None
        dbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_action)
        Dbuff =  create_buffer("Dbuff",Eg_mdetail)
        action_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.usefor != 2)).order_by(Qbuff._recid).all():
            action = Action()
            action_list.append(action)

            action.actionnr = qbuff.actionnr
            action.bezeich = qbuff.bezeich
            action.maintask = qbuff.maintask
            action.selected = False


    def get_guestname(h_zinr:string):

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal pvilanguage, mainno, user_init
        nonlocal mbuff, resline1, guest1


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        resline1 = get_cache (Res_line, {"active_flag": [(eq, 1)],"zinr": [(eq, h_zinr)],"resstatus": [(ne, 13)]})

        if resline1:

            guest1 = get_cache (Guest, {"gastnr": [(eq, resline1.gastnrmember)]})

            if guest1:
                guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
        else:

            resline1 = get_cache (Res_line, {"active_flag": [(eq, 0)],"zinr": [(eq, h_zinr)],"resstatus": [(ne, 13)]})

            if resline1:

                guest1 = get_cache (Guest, {"gastnr": [(eq, resline1.gastnrmember)]})

                if guest1:
                    guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
            else:
                guestname = ""


    def create_property():

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal pvilanguage, mainno, user_init
        nonlocal mbuff, resline1, guest1


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        ques = None
        Ques =  create_buffer("Ques",Queasy)

        for eg_property in db_session.query(Eg_property).order_by(Eg_property._recid).all():
            t_property = T_property()
            t_property_list.append(t_property)

            t_property.prop_nr = eg_property.nr
            t_property.prop_nm = eg_property.bezeich
            t_property.pzinr = eg_property.zinr
            t_property.pmain_nr = eg_property.maintask
            t_property.ploc_nr = eg_property.location

            queasy = get_cache (Queasy, {"key": [(eq, 133)],"number1": [(eq, eg_property.maintask)]})

            if queasy:
                t_property.pmain = queasy.char1
                t_property.pcateg_nr = queasy.number2

                ques = db_session.query(Ques).filter(
                         (Ques.key == 132) & (Ques.number1 == queasy.number2)).first()

                if ques:
                    t_property.pcateg = ques.char1

            eg_location = get_cache (Eg_location, {"nr": [(eq, eg_property.location)]})

            if eg_location:
                t_property.ploc = eg_location.bezeich


    def create_pic():

        nonlocal sguestflag, groupid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal pvilanguage, mainno, user_init
        nonlocal mbuff, resline1, guest1


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        qbuff = None
        engid:int = 0
        Qbuff =  create_buffer("Qbuff",Eg_staff)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.usergroup == engid) & (Qbuff.activeflag)).order_by(Qbuff.nr).all():
            tpic = Tpic()
            tpic_list.append(tpic)

            tpic.pic_nr = qbuff.nr
            tpic.pic_nm = qbuff.name
            tpic.pic_dept = qbuff.usergroup


    alert_str[0] = translateExtended ("Successfully", lvcarea, "")
    alert_str[1] = translateExtended ("Failed", lvcarea, "")
    alert_str[2] = translateExtended ("Pending", lvcarea, "")

    eg_location = get_cache (Eg_location, {"guestflag": [(eq, True)]})

    if eg_location:
        avail_eg_location = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate
    define_group()
    define_engineering()
    getmaintain()
    create_mobile()
    getprevaction()
    create_alert()
    create_property()
    create_pic()

    eg_maintain = get_cache (Eg_maintain, {"maintainnr": [(eq, mainno)]})

    if eg_maintain:

        if eg_maintain.type == 1 or eg_maintain.type == 2:
            flag8 = 1

    for eg_location in db_session.query(Eg_location).order_by(Eg_location._recid).all():
        t_eg_location = T_eg_location()
        t_eg_location_list.append(t_eg_location)

        buffer_copy(eg_location, t_eg_location)

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
        get_guestname(zimmer.zinr)
        t_zimmer = T_zimmer()
        t_zimmer_list.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)
        t_zimmer.gname_str = guestname

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 135)).order_by(Queasy._recid).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    return generate_output()