from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Eg_location, Zimmer, Queasy, Eg_action, Eg_maintain, Res_line, Guest, Htparam, Bediener, Eg_property, Eg_mobilenr, Eg_mdetail, Eg_alert, Eg_staff

def prepare_eg_mainscheduleed_webbl(pvilanguage:int, mainno:int, user_init:str):
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
    lvcarea:str = "eg_mainscheduleEd"
    alert_str:str = ""
    guestname:str = ""
    eg_location = zimmer = queasy = eg_action = eg_maintain = res_line = guest = htparam = bediener = eg_property = eg_mobilenr = eg_mdetail = eg_alert = eg_staff = None

    t_eg_location = t_zimmer = t_queasy = send_alert = his_action = mobile = action = maintain = mbuff = resline1 = guest1 = t_property = tpic = bprop = quesbuff = quesbuff1 = qbuff = dbuff = buff_action = ques = None

    t_eg_location_list, T_eg_location = create_model_like(Eg_location)
    t_zimmer_list, T_zimmer = create_model_like(Zimmer, {"gname_str":str})
    t_queasy_list, T_queasy = create_model_like(Queasy)
    send_alert_list, Send_alert = create_model("Send_alert", {"alert_date":date, "alert_time":int, "alert_str":str, "alert_reqnr":int, "alert_msg":str, "alert_sendto":int, "alert_sendnm":str, "alert_sendnr":str, "alert_msgstatus":int, "alert_mstat":str})
    his_action_list, His_action = create_model("His_action", {"action_mainnr":int, "action_nr":int, "action_nm":str, "create_date":date, "create_time":int, "time_str":str, "create_by":str})
    mobile_list, Mobile = create_model("Mobile", {"nr":int, "name":str, "position":str, "mobilenr":str, "mobile_selected":bool})
    action_list, Action = create_model_like(Eg_action, {"selected":bool})
    maintain_list, Maintain = create_model_like(Eg_maintain)
    t_property_list, T_property = create_model("T_property", {"prop_nr":int, "prop_nm":str, "prop_selected":bool, "pcateg_nr":int, "pcateg":str, "pmain_nr":int, "pmain":str, "ploc_nr":int, "ploc":str, "pzinr":str})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":str, "pic_dept":int})

    Mbuff = Eg_maintain
    Resline1 = Res_line
    Guest1 = Guest
    Bprop = Eg_property
    Quesbuff = Queasy
    Quesbuff1 = Queasy
    Qbuff = Eg_staff
    Dbuff = Eg_mdetail
    Buff_action = Eg_action
    Ques = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal mbuff, resline1, guest1, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list
        return {"sguestflag": sguestflag, "groupid": groupid, "engid": engid, "sms_flag": sms_flag, "avail_eg_location": avail_eg_location, "h_category": h_category, "h_maintask": h_maintask, "h_location": h_location, "h_zinr": h_zinr, "str_property": str_property, "str_maintask": str_maintask, "str_categ": str_categ, "ci_date": ci_date, "flag1": flag1, "flag2": flag2, "flag3": flag3, "flag4": flag4, "flag5": flag5, "flag6": flag6, "flag7": flag7, "flag8": flag8, "send-alert": send_alert_list, "his-action": his_action_list, "mobile": mobile_list, "action": action_list, "maintain": maintain_list, "t-eg-location": t_eg_location_list, "t-zimmer": t_zimmer_list, "t-queasy": t_queasy_list, "t-property": t_property_list, "tpic": tpic_list}

    def define_group():

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal mbuff, resline1, guest1, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def define_engineering():

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal mbuff, resline1, guest1, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            pass

    def getmaintain():

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal mbuff, resline1, guest1, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list


        Bprop = Eg_property
        Quesbuff = Queasy
        Quesbuff1 = Queasy
        maintain_list.clear()

        mbuff = db_session.query(Mbuff).filter(
                (Mbuff.maintainnr == mainno)).first()

        if not mbuff:

            return
        else:
            buffer_copy(mbuff, maintain)

            if maintain.smsflag :
                sms_flag = True

            bprop = db_session.query(Bprop).filter(
                    (bProp.nr == maintain.propertynr)).first()

            if bprop:
                h_maintask = bprop.maintask
                h_location = bprop.location
                h_zinr = bprop.zinr
                str_property = bprop.bezeich
                maintain.propertynr = bprop.nr

                quesbuff = db_session.query(Quesbuff).filter(
                        (Quesbuff.key == 133) &  (Quesbuff.number1 == bprop.maintask)).first()

                if quesbuff:
                    str_maintask = quesbuff.char1
                    h_maintask = quesbuff.number1

                    action = query(action_list, filters=(lambda action :action.maintask == h_maintask), first=True)

                    if action:
                        flag1 = 1
                    else:
                        flag1 = 2

                    quesbuff1 = db_session.query(Quesbuff1).filter(
                            (Quesbuff1.key == 132) &  (Quesbuff1.number1 == quesbuff.number2)).first()

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

                eg_location = db_session.query(Eg_location).filter(
                        (Eg_location.nr == bprop.location) &  (Eg_location.guestflag)).first()

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

            if maintain.TYPE == 3:
                flag7 = 1

                return
            else:
                flag7 = 2

    def create_mobile():

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal mbuff, resline1, guest1, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list


        Qbuff = Eg_mobilenr

        for mobile in query(mobile_list):
            mobile_list.remove(mobile)

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.activeflag) &  (Qbuff.mobile != "")).all():
            mobile = Mobile()
            mobile_list.append(mobile)

            mobile.nr = qbuff.nr
            mobile.name = qbuff.name
            mobile.POSITION = qbuff.POSITION
            mobile.mobilenr = qbuff.mobilenr
            mobile.mobile_SELECTED = False

    def getprevaction():

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal mbuff, resline1, guest1, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list


        Dbuff = Eg_mdetail
        Buff_action = Eg_action
        his_action_list.clear()

        dbuff_obj_list = []
        for dbuff, buff_action in db_session.query(Dbuff, Buff_action).join(Buff_action,(Buff_action.actionnr == Dbuff.nr)).filter(
                (Dbuff.maintainnr == mainno) &  (Dbuff.key == 1)).all():
            if dbuff._recid in dbuff_obj_list:
                continue
            else:
                dbuff_obj_list.append(dbuff._recid)


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
        nonlocal mbuff, resline1, guest1, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        b:str = ""
        Qbuff = Eg_alert
        send_alert_list.clear()

        for eg_alert in db_session.query(Eg_alert).filter(
                (func.lower(Eg_alert.fromfile) == "3") &  (Eg_alert.reqnr == mainno)).all():

            eg_mobilenr = db_session.query(Eg_mobilenr).filter(
                    (Eg_mobilenr.nr == eg_alert.sendto)).first()

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
        nonlocal mbuff, resline1, guest1, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list


        Qbuff = Eg_action
        Dbuff = Eg_mdetail
        action_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.usefor != 2)).all():
            action = Action()
            action_list.append(action)

            action.actionnr = qbuff.actionnr
            action.bezeich = qbuff.bezeich
            action.maintask = qbuff.maintask
            action.SELECTED = False

    def get_guestname(h_zinr:str):

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal mbuff, resline1, guest1, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        resline1 = db_session.query(Resline1).filter(
                (Resline1.active_flag == 1) &  (func.lower(Resline1.zinr) == (h_zinr).lower()) &  (Resline1.resstatus != 13)).first()

        if resline1:

            guest1 = db_session.query(Guest1).filter(
                    (Guest1.gastnr == resline1.gastnrmember)).first()

            if guest1:
                guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
        else:

            resline1 = db_session.query(Resline1).filter(
                    (Resline1.active_flag == 0) &  (func.lower(Resline1.zinr) == (h_zinr).lower()) &  (Resline1.resstatus != 13)).first()

            if resline1:

                guest1 = db_session.query(Guest1).filter(
                        (Guest1.gastnr == resline1.gastnrmember)).first()

                if guest1:
                    guestname = guest1.name + " " + guest1.vorname1 + ", " + guest1.anrede1 + guest1.anredefirma
            else:
                guestname = ""

    def create_property():

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal mbuff, resline1, guest1, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list


        Ques = Queasy

        for eg_property in db_session.query(Eg_property).all():
            t_property = T_property()
            t_property_list.append(t_property)

            t_property.prop_nr = eg_property.nr
            t_property.prop_nm = eg_property.bezeich
            t_property.pzinr = eg_property.zinr
            t_property.pmain_nr = eg_property.maintask
            t_property.ploc_nr = eg_property.location

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 133) &  (Queasy.number1 == eg_property.maintask)).first()

            if queasy:
                t_property.pmain = queasy.char1
                t_property.pcateg_nr = queasy.number2

            ques = db_session.query(Ques).filter(
                    (Ques.key == 132) &  (Ques.number1 == queasy.number2)).first()

            if ques:
                t_property.pcateg = ques.char1

            eg_location = db_session.query(Eg_location).filter(
                    (Eg_location.nr == eg_property.location)).first()

            if eg_location:
                t_property.ploc = eg_location.bezeich

    def create_pic():

        nonlocal sguestflag, groupid, engid, sms_flag, avail_eg_location, h_category, h_maintask, h_location, h_zinr, str_property, str_maintask, str_categ, ci_date, flag1, flag2, flag3, flag4, flag5, flag6, flag7, flag8, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_eg_location_list, t_zimmer_list, t_queasy_list, t_property_list, tpic_list, lvcarea, alert_str, guestname, eg_location, zimmer, queasy, eg_action, eg_maintain, res_line, guest, htparam, bediener, eg_property, eg_mobilenr, eg_mdetail, eg_alert, eg_staff
        nonlocal mbuff, resline1, guest1, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques


        nonlocal t_eg_location, t_zimmer, t_queasy, send_alert, his_action, mobile, action, maintain, mbuff, resline1, guest1, t_property, tpic, bprop, quesbuff, quesbuff1, qbuff, dbuff, buff_action, ques
        nonlocal t_eg_location_list, t_zimmer_list, t_queasy_list, send_alert_list, his_action_list, mobile_list, action_list, maintain_list, t_property_list, tpic_list

        engid:int = 0
        Qbuff = Eg_staff

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.usergroup == engid) &  (Qbuff.activeflag)).all():
            tpic = Tpic()
            tpic_list.append(tpic)

            tpic.pic_nr = qbuff.nr
            tpic.pic_nm = qbuff.name
            tpic.pic_dept = qbuff.usergroup

    alert_str[0] = translateextended ("Successfully", lvcarea, "")
    alert_str[1] = translateextended ("Failed", lvcarea, "")
    alert_str[2] = translateextended ("Pending", lvcarea, "")

    eg_location = db_session.query(Eg_location).filter(
            (Eg_location.guestflag)).first()

    if eg_location:
        avail_eg_location = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = fdate
    define_group()
    define_engineering()
    getmaintain()
    create_mobile()
    getprevaction()
    create_alert()
    create_property()
    create_pic()

    eg_maintain = db_session.query(Eg_maintain).filter(
            (Eg_maintain.maintainnr == mainno)).first()

    if eg_maintain:

        if eg_maintain.TYPE == 1 or eg_maintain.TYPE == 2:
            flag8 = 1

    for eg_location in db_session.query(Eg_location).all():
        t_eg_location = T_eg_location()
        t_eg_location_list.append(t_eg_location)

        buffer_copy(eg_location, t_eg_location)

    for zimmer in db_session.query(Zimmer).all():
        get_guestname(zimmer.zinr)
        t_zimmer = T_zimmer()
        t_zimmer_list.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)
        t_zimmer.gname_str = guestname

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 135)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    return generate_output()