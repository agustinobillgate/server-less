from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Zimmer, Queasy, Eg_property, Eg_request, Eg_location, Eg_subtask, Res_line, Guest, Htparam, Bediener, Eg_vendor, Eg_alert, Eg_staff, Eg_vperform, Eg_action, Eg_reqdetail

def prepare_eg_chgreq_webbl(pvilanguage:int, reqno:int, view_first:bool, user_init:str):
    groupid = 0
    engid = 0
    source_str = ""
    dept_str = ""
    strproperty = ""
    main_str = ""
    categ_str = ""
    sub_str = ""
    usr_str = ""
    guestname = ""
    sguestflag = False
    flag1 = 0
    flag2 = 0
    flag3 = 0
    s_othersflag = False
    subtask_bez = ""
    avail_eg_request = False
    avail_eg_subtask = False
    avail_subtask = False
    t_fstat = 0
    svendor_list = []
    request1_list = []
    send_alert_list = []
    tvendor_list = []
    t_eg_location_list = []
    treqdetail_list = []
    t_eg_request_list = []
    t_eg_property_list = []
    t_queasy130_list = []
    t_queasy_list = []
    t_zimmer_list = []
    lvcarea:str = "eg_chgreq"
    alert_str:str = ""
    zimmer = queasy = eg_property = eg_request = eg_location = eg_subtask = res_line = guest = htparam = bediener = eg_vendor = eg_alert = eg_staff = eg_vperform = eg_action = eg_reqdetail = None

    t_zimmer = t_queasy = t_queasy130 = t_eg_property = t_eg_request = treqdetail = svendor = rbuff = request1 = send_alert = tvendor = t_eg_location = subtask1 = resline1 = guest1 = qbuff = queasy1 = queasy2 = sbuff = usr = gbuff = vbuff = actbuff = None

    t_zimmer_list, T_zimmer = create_model_like(Zimmer, {"gname_str":str})
    t_queasy_list, T_queasy = create_model_like(Queasy)
    t_queasy130_list, T_queasy130 = create_model_like(Queasy)
    t_eg_property_list, T_eg_property = create_model_like(Eg_property)
    t_eg_request_list, T_eg_request = create_model_like(Eg_request)
    treqdetail_list, Treqdetail = create_model("Treqdetail", {"reqnr":int, "actionnr":int, "action":str, "create_date":date, "create_time":int, "create_str":str, "create_by":str, "flag":bool})
    svendor_list, Svendor = create_model("Svendor", {"nr":str, "vendor_nr":int, "docno":str, "reqnr":int, "startdate":date, "estfinishdate":date, "finishdate":date, "price":decimal, "bezeich":str, "pic":str, "created_by":str, "created_date":date, "created_time":int, "perform_nr":str, "stat":str})
    request1_list, Request1 = create_model_like(Eg_request)
    send_alert_list, Send_alert = create_model("Send_alert", {"alert_date":date, "alert_time":int, "alert_str":str, "alert_reqnr":int, "alert_msg":str, "alert_sendto":int, "alert_sendnm":str, "alert_sendnr":str, "alert_msgstatus":int, "alert_mstat":str})
    tvendor_list, Tvendor = create_model("Tvendor", {"ven_nr":int, "ven_nm":str})
    t_eg_location_list, T_eg_location = create_model_like(Eg_location)

    Rbuff = Eg_request
    Subtask1 = Eg_subtask
    Resline1 = Res_line
    Guest1 = Guest
    Qbuff = Eg_vendor
    Queasy1 = Queasy
    Queasy2 = Queasy
    Sbuff = Eg_subtask
    Usr = Eg_staff
    Gbuff = Guest
    Vbuff = Eg_vperform
    Actbuff = Eg_action

    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list, treqdetail_list, t_eg_request_list, t_eg_property_list, t_queasy130_list, t_queasy_list, t_zimmer_list, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, res_line, guest, htparam, bediener, eg_vendor, eg_alert, eg_staff, eg_vperform, eg_action, eg_reqdetail
        nonlocal rbuff, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff
        nonlocal t_zimmer_list, t_queasy_list, t_queasy130_list, t_eg_property_list, t_eg_request_list, treqdetail_list, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list
        return {"groupid": groupid, "engid": engid, "source_str": source_str, "dept_str": dept_str, "strproperty": strproperty, "main_str": main_str, "categ_str": categ_str, "sub_str": sub_str, "usr_str": usr_str, "guestname": guestname, "sguestflag": sguestflag, "flag1": flag1, "flag2": flag2, "flag3": flag3, "s_othersflag": s_othersflag, "subtask_bez": subtask_bez, "avail_eg_request": avail_eg_request, "avail_eg_subtask": avail_eg_subtask, "avail_subtask": avail_subtask, "t_fstat": t_fstat, "sVendor": svendor_list, "request1": request1_list, "send-alert": send_alert_list, "tvendor": tvendor_list, "t-eg-location": t_eg_location_list, "treqdetail": treqdetail_list, "t-eg-request": t_eg_request_list, "t-eg-property": t_eg_property_list, "t-queasy130": t_queasy130_list, "t-queasy": t_queasy_list, "t-zimmer": t_zimmer_list}

    def define_sms():

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list, treqdetail_list, t_eg_request_list, t_eg_property_list, t_queasy130_list, t_queasy_list, t_zimmer_list, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, res_line, guest, htparam, bediener, eg_vendor, eg_alert, eg_staff, eg_vperform, eg_action, eg_reqdetail
        nonlocal rbuff, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff
        nonlocal t_zimmer_list, t_queasy_list, t_queasy130_list, t_eg_property_list, t_eg_request_list, treqdetail_list, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list

    def define_engineering():

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list, treqdetail_list, t_eg_request_list, t_eg_property_list, t_queasy130_list, t_queasy_list, t_zimmer_list, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, res_line, guest, htparam, bediener, eg_vendor, eg_alert, eg_staff, eg_vperform, eg_action, eg_reqdetail
        nonlocal rbuff, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff
        nonlocal t_zimmer_list, t_queasy_list, t_queasy130_list, t_eg_property_list, t_eg_request_list, treqdetail_list, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            pass

    def define_group():

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list, treqdetail_list, t_eg_request_list, t_eg_property_list, t_queasy130_list, t_queasy_list, t_zimmer_list, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, res_line, guest, htparam, bediener, eg_vendor, eg_alert, eg_staff, eg_vperform, eg_action, eg_reqdetail
        nonlocal rbuff, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff
        nonlocal t_zimmer_list, t_queasy_list, t_queasy130_list, t_eg_property_list, t_eg_request_list, treqdetail_list, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def create_tvendor():

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list, treqdetail_list, t_eg_request_list, t_eg_property_list, t_queasy130_list, t_queasy_list, t_zimmer_list, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, res_line, guest, htparam, bediener, eg_vendor, eg_alert, eg_staff, eg_vperform, eg_action, eg_reqdetail
        nonlocal rbuff, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff
        nonlocal t_zimmer_list, t_queasy_list, t_queasy130_list, t_eg_property_list, t_eg_request_list, treqdetail_list, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list


        tvendor_list.clear()

        for eg_vendor in db_session.query(Eg_vendor).all():
            tvendor = Tvendor()
            tvendor_list.append(tvendor)

            tvendor.ven_nr = eg_vendor.vendor_nr
            tvendor.ven_nm = eg_vendor.bezeich

    def create_alert():

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list, treqdetail_list, t_eg_request_list, t_eg_property_list, t_queasy130_list, t_queasy_list, t_zimmer_list, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, res_line, guest, htparam, bediener, eg_vendor, eg_alert, eg_staff, eg_vperform, eg_action, eg_reqdetail
        nonlocal rbuff, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff
        nonlocal t_zimmer_list, t_queasy_list, t_queasy130_list, t_eg_property_list, t_eg_request_list, treqdetail_list, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list

        b:str = ""
        Qbuff = Eg_alert
        send_alert_list.clear()

        for eg_alert in db_session.query(Eg_alert).filter(
                (func.lower(Eg_alert.fromfile) == "1") &  (Eg_alert.reqnr == reqno) |  (func.lower(Eg_alert.fromfile) == "2") &  (Eg_alert.reqnr == reqno)).all():

            eg_staff = db_session.query(Eg_staff).filter(
                    (Eg_staff.nr == eg_alert.sendto)).first()

            if eg_staff:
                b = eg_staff.name
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

    def create_request():

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list, treqdetail_list, t_eg_request_list, t_eg_property_list, t_queasy130_list, t_queasy_list, t_zimmer_list, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, res_line, guest, htparam, bediener, eg_vendor, eg_alert, eg_staff, eg_vperform, eg_action, eg_reqdetail
        nonlocal rbuff, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff
        nonlocal t_zimmer_list, t_queasy_list, t_queasy130_list, t_eg_property_list, t_eg_request_list, treqdetail_list, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list

        blzin:int = 0
        Queasy1 = Queasy
        Queasy2 = Queasy
        Sbuff = Eg_subtask
        Usr = Eg_staff
        Gbuff = Guest
        request1_list.clear()
        request1 = Request1()
        request1_list.append(request1)


        rbuff = db_session.query(Rbuff).filter(
                (Rbuff.reqnr == reqno)).first()

        if not rbuff:

            return
        else:
            buffer_copy(rbuff, request1)

            queasy1 = db_session.query(Queasy1).filter(
                    (Queasy1.key == 130) &  (Queasy1.number1 == request1.SOURCE) &  (Queasy1.char1 != "") &  (Queasy1.logi1 == False) &  (Queasy1.deci1 == 0) &  (Queasy1.date1 == None)).first()

            if queasy1:
                source_str = queasy1.char1

            queasy1 = db_session.query(Queasy1).filter(
                    (Queasy1.key == 19) &  (Queasy1.number1 == request1.deptnum)).first()

            if queasy1:
                dept_str = queasy1.char3

            eg_property = db_session.query(Eg_property).filter(
                    (Eg_property.nr == request1.propertynr)).first()

            if eg_property:
                strproperty = eg_property.bezeich
                request1.maintask = eg_property.maintask

                queasy1 = db_session.query(Queasy1).filter(
                        (Queasy1.key == 133) &  (Queasy1.number1 == eg_property.maintask) &  (Queasy1.char1 != "") &  (Queasy1.logi1 == False) &  (Queasy1.deci1 == 0) &  (Queasy1.date1 == None)).first()

                if queasy1:
                    main_str = queasy1.char1

                    queasy2 = db_session.query(Queasy2).filter(
                            (Queasy2.key == 132) &  (Queasy2.number1 == queasy1.number2) &  (Queasy2.char1 != "") &  (Queasy2.logi1 == False) &  (Queasy2.deci1 == 0) &  (Queasy2.date1 == None)).first()

                    if queasy2:
                        request1.category = queasy2.number1
                        categ_str = queasy2.char1
            else:
                strproperty = ""
                main_str = ""

                queasy1 = db_session.query(Queasy1).filter(
                        (Queasy1.key == 133) &  (Queasy1.number1 == request1.maintask) &  (Queasy1.char1 != "") &  (Queasy1.logi1 == False) &  (Queasy1.deci1 == 0) &  (Queasy1.date1 == None)).first()

                if queasy1:
                    main_str = queasy1.char1

                    queasy2 = db_session.query(Queasy2).filter(
                            (Queasy2.key == 132) &  (Queasy2.number1 == queasy1.number2) &  (Queasy2.char1 != "") &  (Queasy2.logi1 == False) &  (Queasy2.deci1 == 0) &  (Queasy2.date1 == None)).first()

                    if queasy2:
                        request1.category = queasy2.number1
                        categ_str = queasy2.char1
                flag1 = 1
            flag2 = 1

            eg_location = db_session.query(Eg_location).filter(
                    (Eg_location.nr == request1.reserve_int) &  (Eg_location.guestflag)).first()

            if eg_location:
                sguestflag = True
                request1.reserve_int = 0


                flag3 = 1
            else:
                sguestflag = False


                flag3 = 2

            sbuff = db_session.query(Sbuff).filter(
                    (Sbuff.sub_code == request1.sub_task)).first()

            if sbuff:

                if sbuff.othersflag :
                    sub_str = rbuff.subtask_bezeich
                else:
                    sub_str = sbuff.bezeich

            usr = db_session.query(Usr).filter(
                    (Usr.nr == request1.assign_to)).first()

            if usr:
                usr_str = usr.name

            gbuff = db_session.query(Gbuff).filter(
                    (Gbuff.gastnr == request1.gastnr)).first()

            if gbuff:
                guestname = gbuff.name + " " + gbuff.vorname1 + ", " + gbuff.anrede1 + gbuff.anredefirma

    def getvendor():

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list, treqdetail_list, t_eg_request_list, t_eg_property_list, t_queasy130_list, t_queasy_list, t_zimmer_list, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, res_line, guest, htparam, bediener, eg_vendor, eg_alert, eg_staff, eg_vperform, eg_action, eg_reqdetail
        nonlocal rbuff, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff
        nonlocal t_zimmer_list, t_queasy_list, t_queasy130_list, t_eg_property_list, t_eg_request_list, treqdetail_list, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list


        Vbuff = Eg_vperform
        Qbuff = Eg_vendor

        for vbuff in db_session.query(Vbuff).filter(
                (Vbuff.reqnr == request1.reqnr) &  (Vbuff.logi1 == False)).all():
            svendor = Svendor()
            svendor_list.append(svendor)

            svendor.reqnr = reqno
            svendor.vendor_nr = vbuff.vendor_nr
            svendor.docno = vbuff.DOcumentno
            svendor.startdate = vbuff.startdate
            svendor.estfinishdate = vbuff.estfinishdate
            svendor.finishdate = vbuff.finishdate
            svendor.price = vbuff.price
            svendor.bezeich = vbuff.bezeich
            svendor.pic = vbuff.pic
            svendor.perform_nr = vbuff.perform_nr
            svendor.stat = "1"

    def create_reqdetail():

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list, treqdetail_list, t_eg_request_list, t_eg_property_list, t_queasy130_list, t_queasy_list, t_zimmer_list, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, res_line, guest, htparam, bediener, eg_vendor, eg_alert, eg_staff, eg_vperform, eg_action, eg_reqdetail
        nonlocal rbuff, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff
        nonlocal t_zimmer_list, t_queasy_list, t_queasy130_list, t_eg_property_list, t_eg_request_list, treqdetail_list, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list

        str:str = ""
        Actbuff = Eg_action
        treqdetail_list.clear()

        for eg_reqdetail in db_session.query(Eg_reqdetail).filter(
                (Eg_reqdetail.reqnr == reqno) &  (Eg_reqdetail.action != "")).all():
            treqdetail = Treqdetail()
            treqdetail_list.append(treqdetail)

            treqdetail.reqnr = eg_reqdetail.reqnr
            treqdetail.actionnr = eg_reqdetail.actionnr
            treqdetail.action = eg_reqdetail.action
            treqdetail.create_date = eg_reqdetail.create_date
            treqdetail.create_time = eg_reqdetail.create_time
            treqdetail.create_str = to_string(eg_reqdetail.create_time, "HH:MM:SS")
            treqdetail.create_by = eg_reqdetail.create_by
            treqdetail.flag = True

    def get_guestname(h_zinr:str):

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list, treqdetail_list, t_eg_request_list, t_eg_property_list, t_queasy130_list, t_queasy_list, t_zimmer_list, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, res_line, guest, htparam, bediener, eg_vendor, eg_alert, eg_staff, eg_vperform, eg_action, eg_reqdetail
        nonlocal rbuff, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1, resline1, guest1, qbuff, queasy1, queasy2, sbuff, usr, gbuff, vbuff, actbuff
        nonlocal t_zimmer_list, t_queasy_list, t_queasy130_list, t_eg_property_list, t_eg_request_list, treqdetail_list, svendor_list, request1_list, send_alert_list, tvendor_list, t_eg_location_list

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


    alert_str[0] = translateextended ("Successfully", lvcarea, "")
    alert_str[1] = translateextended ("Failed", lvcarea, "")
    alert_str[2] = translateextended ("Pending", lvcarea, "")
    define_group()
    define_engineering()
    define_sms()

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


    create_tvendor()
    create_alert()
    create_request()
    getvendor()
    create_reqdetail()

    request1 = query(request1_list, first=True)

    if view_first == False:

        eg_request = db_session.query(Eg_request).filter(
                (Eg_request.reqnr == reqno) &  (Eg_request.reqstatus == 1)).first()

        if eg_request:
            t_eg_request = T_eg_request()
            t_eg_request_list.append(t_eg_request)

            buffer_copy(eg_request, t_eg_request)
            avail_eg_request = True

        eg_subtask = db_session.query(Eg_subtask).filter(
                (Eg_subtask.sub_code == request1.sub_task)).first()

        if eg_subtask:
            s_othersflag = eg_subtask.othersflag
            avail_eg_subtask = True

    for eg_property in db_session.query(Eg_property).all():
        t_eg_property = T_eg_property()
        t_eg_property_list.append(t_eg_property)

        buffer_copy(eg_property, t_eg_property)

    for queasy in db_session.query(Queasy).filter(
            (Queasy.KEY == 130)).all():
        t_queasy130 = T_queasy130()
        t_queasy130_list.append(t_queasy130)

        buffer_copy(queasy, t_queasy130)

    for queasy in db_session.query(Queasy).filter(
            (Queasy.KEY == 132) |  (Queasy.KEY == 19) |  (Queasy.KEY == 135)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    request1 = query(request1_list, first=True)

    subtask1 = db_session.query(Subtask1).filter(
            (Subtask1.dept_nr == request1.deptnum) &  (Subtask1.main_nr == request1.maintask) &  (Subtask1.sub_code == request1.sub_task)).first()

    if subtask1:
        avail_subtask = True
        subtask_bez = subtask1.bezeich

    eg_request = db_session.query(Eg_request).filter(
            (Eg_request.reqnr == reqno)).first()

    if eg_request:
        t_fstat = eg_request.reqstatus
    else:
        t_fstat = 0

    return generate_output()