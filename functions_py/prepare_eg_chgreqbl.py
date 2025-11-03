#using conversion tools version: 1.0.0.117

# =============================
# Rulita, 03-11-2025 | 0644BD
# - New compline program
# =============================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimmer, Queasy, Eg_property, Eg_request, Eg_location, Eg_subtask, Htparam, Bediener, Eg_vendor, Eg_alert, Eg_staff, Guest, Eg_vperform, Eg_action, Eg_reqdetail

def prepare_eg_chgreqbl(pvilanguage:int, reqno:int, view_first:bool, user_init:string):

    prepare_cache ([Eg_subtask, Htparam, Bediener, Eg_vendor, Eg_alert, Eg_staff, Eg_reqdetail])

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
    svendor_data = []
    request1_data = []
    send_alert_data = []
    tvendor_data = []
    t_eg_location_data = []
    treqdetail_data = []
    t_eg_request_data = []
    t_eg_property_data = []
    t_queasy130_data = []
    t_queasy_data = []
    t_zimmer_data = []
    lvcarea:string = "eg-chgreq"
    alert_str:List[string] = create_empty_list(3,"")
    zimmer = queasy = eg_property = eg_request = eg_location = eg_subtask = htparam = bediener = eg_vendor = eg_alert = eg_staff = guest = eg_vperform = eg_action = eg_reqdetail = None

    t_zimmer = t_queasy = t_queasy130 = t_eg_property = t_eg_request = treqdetail = svendor = rbuff = request1 = send_alert = tvendor = t_eg_location = subtask1 = None

    t_zimmer_data, T_zimmer = create_model_like(Zimmer)
    t_queasy_data, T_queasy = create_model_like(Queasy)
    t_queasy130_data, T_queasy130 = create_model_like(Queasy)
    t_eg_property_data, T_eg_property = create_model_like(Eg_property)
    t_eg_request_data, T_eg_request = create_model_like(Eg_request)
    treqdetail_data, Treqdetail = create_model("Treqdetail", {"reqnr":int, "actionnr":int, "action":string, "create_date":date, "create_time":int, "create_str":string, "create_by":string, "flag":bool})
    svendor_data, Svendor = create_model("Svendor", {"nr":string, "vendor_nr":int, "docno":string, "reqnr":int, "startdate":date, "estfinishdate":date, "finishdate":date, "price":Decimal, "bezeich":string, "pic":string, "created_by":string, "created_date":date, "created_time":int, "perform_nr":string, "stat":string})
    request1_data, Request1 = create_model_like(Eg_request)
    send_alert_data, Send_alert = create_model("Send_alert", {"alert_date":date, "alert_time":int, "alert_str":string, "alert_reqnr":int, "alert_msg":string, "alert_sendto":int, "alert_sendnm":string, "alert_sendnr":string, "alert_msgstatus":int, "alert_mstat":string})
    tvendor_data, Tvendor = create_model("Tvendor", {"ven_nr":int, "ven_nm":string})
    t_eg_location_data, T_eg_location = create_model_like(Eg_location)

    Rbuff = create_buffer("Rbuff",Eg_request)
    Subtask1 = create_buffer("Subtask1",Eg_subtask)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data, treqdetail_data, t_eg_request_data, t_eg_property_data, t_queasy130_data, t_queasy_data, t_zimmer_data, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, htparam, bediener, eg_vendor, eg_alert, eg_staff, guest, eg_vperform, eg_action, eg_reqdetail
        nonlocal pvilanguage, reqno, view_first, user_init
        nonlocal rbuff, subtask1


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1
        nonlocal t_zimmer_data, t_queasy_data, t_queasy130_data, t_eg_property_data, t_eg_request_data, treqdetail_data, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data

        return {"groupid": groupid, "engid": engid, "source_str": source_str, "dept_str": dept_str, "strproperty": strproperty, "main_str": main_str, "categ_str": categ_str, "sub_str": sub_str, "usr_str": usr_str, "guestname": guestname, "sguestflag": sguestflag, "flag1": flag1, "flag2": flag2, "flag3": flag3, "s_othersflag": s_othersflag, "subtask_bez": subtask_bez, "avail_eg_request": avail_eg_request, "avail_eg_subtask": avail_eg_subtask, "avail_subtask": avail_subtask, "t_fstat": t_fstat, "sVendor": svendor_data, "request1": request1_data, "send-alert": send_alert_data, "tvendor": tvendor_data, "t-eg-location": t_eg_location_data, "treqdetail": treqdetail_data, "t-eg-request": t_eg_request_data, "t-eg-property": t_eg_property_data, "t-queasy130": t_queasy130_data, "t-queasy": t_queasy_data, "t-zimmer": t_zimmer_data}

    def define_sms():

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data, treqdetail_data, t_eg_request_data, t_eg_property_data, t_queasy130_data, t_queasy_data, t_zimmer_data, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, htparam, bediener, eg_vendor, eg_alert, eg_staff, guest, eg_vperform, eg_action, eg_reqdetail
        nonlocal pvilanguage, reqno, view_first, user_init
        nonlocal rbuff, subtask1


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1
        nonlocal t_zimmer_data, t_queasy_data, t_queasy130_data, t_eg_property_data, t_eg_request_data, treqdetail_data, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data


    def define_engineering():

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data, treqdetail_data, t_eg_request_data, t_eg_property_data, t_queasy130_data, t_queasy_data, t_zimmer_data, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, htparam, bediener, eg_vendor, eg_alert, eg_staff, guest, eg_vperform, eg_action, eg_reqdetail
        nonlocal pvilanguage, reqno, view_first, user_init
        nonlocal rbuff, subtask1


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1
        nonlocal t_zimmer_data, t_queasy_data, t_queasy130_data, t_eg_property_data, t_eg_request_data, treqdetail_data, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            pass


    def define_group():

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data, treqdetail_data, t_eg_request_data, t_eg_property_data, t_queasy130_data, t_queasy_data, t_zimmer_data, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, htparam, bediener, eg_vendor, eg_alert, eg_staff, guest, eg_vperform, eg_action, eg_reqdetail
        nonlocal pvilanguage, reqno, view_first, user_init
        nonlocal rbuff, subtask1


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1
        nonlocal t_zimmer_data, t_queasy_data, t_queasy130_data, t_eg_property_data, t_eg_request_data, treqdetail_data, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def create_tvendor():

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data, treqdetail_data, t_eg_request_data, t_eg_property_data, t_queasy130_data, t_queasy_data, t_zimmer_data, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, htparam, bediener, eg_vendor, eg_alert, eg_staff, guest, eg_vperform, eg_action, eg_reqdetail
        nonlocal pvilanguage, reqno, view_first, user_init
        nonlocal rbuff, subtask1


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1
        nonlocal t_zimmer_data, t_queasy_data, t_queasy130_data, t_eg_property_data, t_eg_request_data, treqdetail_data, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data


        tvendor_data.clear()

        for eg_vendor in db_session.query(Eg_vendor).order_by(Eg_vendor._recid).all():
            tvendor = Tvendor()
            tvendor_data.append(tvendor)

            tvendor.ven_nr = eg_vendor.vendor_nr
            tvendor.ven_nm = eg_vendor.bezeich


    def create_alert():

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data, treqdetail_data, t_eg_request_data, t_eg_property_data, t_queasy130_data, t_queasy_data, t_zimmer_data, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, htparam, bediener, eg_vendor, eg_alert, eg_staff, guest, eg_vperform, eg_action, eg_reqdetail
        nonlocal pvilanguage, reqno, view_first, user_init
        nonlocal rbuff, subtask1


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1
        nonlocal t_zimmer_data, t_queasy_data, t_queasy130_data, t_eg_property_data, t_eg_request_data, treqdetail_data, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data

        b:string = ""
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_alert)
        send_alert_data.clear()

        for eg_alert in db_session.query(Eg_alert).filter(
                 (Eg_alert.fromfile == ("1").lower()) & (Eg_alert.reqnr == reqno) | (Eg_alert.fromfile == ("2").lower()) & (Eg_alert.reqnr == reqno)).order_by(Eg_alert._recid).all():

            eg_staff = get_cache (Eg_staff, {"nr": [(eq, eg_alert.sendto)]})

            if eg_staff:
                b = eg_staff.name
            else:
                b = "Staff Record Not Found"
            send_alert = Send_alert()
            send_alert_data.append(send_alert)

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

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data, treqdetail_data, t_eg_request_data, t_eg_property_data, t_queasy130_data, t_queasy_data, t_zimmer_data, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, htparam, bediener, eg_vendor, eg_alert, eg_staff, guest, eg_vperform, eg_action, eg_reqdetail
        nonlocal pvilanguage, reqno, view_first, user_init
        nonlocal rbuff, subtask1


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1
        nonlocal t_zimmer_data, t_queasy_data, t_queasy130_data, t_eg_property_data, t_eg_request_data, treqdetail_data, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data

        blzin:int = 0
        queasy1 = None
        queasy2 = None
        sbuff = None
        usr = None
        gbuff = None
        Queasy1 =  create_buffer("Queasy1",Queasy)
        Queasy2 =  create_buffer("Queasy2",Queasy)
        Sbuff =  create_buffer("Sbuff",Eg_subtask)
        Usr =  create_buffer("Usr",Eg_staff)
        Gbuff =  create_buffer("Gbuff",Guest)
        request1_data.clear()
        request1 = Request1()
        request1_data.append(request1)


        rbuff = db_session.query(Rbuff).filter(
                 (Rbuff.reqnr == reqno)).first()

        if not rbuff:

            return
        else:
            buffer_copy(rbuff, request1)

            queasy1 = db_session.query(Queasy1).filter(
                     (Queasy1.key == 130) & (Queasy1.number1 == request1.source) & (Queasy1.char1 != "") & (Queasy1.logi1 == False) & (Queasy1.deci1 == 0) & (Queasy1.date1 == None)).first()

            if queasy1:
                source_str = queasy1.char1

            queasy1 = db_session.query(Queasy1).filter(
                     (Queasy1.key == 19) & (Queasy1.number1 == request1.deptnum)).first()

            if queasy1:
                dept_str = queasy1.char3

            eg_property = get_cache (Eg_property, {"nr": [(eq, request1.propertynr)]})

            if eg_property and request1.propertynr != 0:
                strproperty = eg_property.bezeich
                request1.maintask = eg_property.maintask

                queasy1 = db_session.query(Queasy1).filter(
                         (Queasy1.key == 133) & (Queasy1.number1 == eg_property.maintask) & (Queasy1.char1 != "") & (Queasy1.logi1 == False) & (Queasy1.deci1 == 0) & (Queasy1.date1 == None)).first()

                if queasy1:
                    main_str = queasy1.char1

                    queasy2 = db_session.query(Queasy2).filter(
                             (Queasy2.key == 132) & (Queasy2.number1 == queasy1.number2) & (Queasy2.char1 != "") & (Queasy2.logi1 == False) & (Queasy2.deci1 == 0) & (Queasy2.date1 == None)).first()

                    if queasy2:
                        request1.category = queasy2.number1
                        categ_str = queasy2.char1
            else:
                strproperty = ""
                main_str = ""

                queasy1 = db_session.query(Queasy1).filter(
                         (Queasy1.key == 133) & (Queasy1.number1 == request1.maintask) & (Queasy1.char1 != "") & (Queasy1.logi1 == False) & (Queasy1.deci1 == 0) & (Queasy1.date1 == None)).first()

                if queasy1:
                    main_str = queasy1.char1

                    queasy2 = db_session.query(Queasy2).filter(
                             (Queasy2.key == 132) & (Queasy2.number1 == queasy1.number2) & (Queasy2.char1 != "") & (Queasy2.logi1 == False) & (Queasy2.deci1 == 0) & (Queasy2.date1 == None)).first()

                    if queasy2:
                        request1.category = queasy2.number1
                        categ_str = queasy2.char1
                flag1 = 1
            flag2 = 1

            eg_location = get_cache (Eg_location, {"nr": [(eq, request1.reserve_int)],"guestflag": [(eq, True)]})

            if eg_location:
                sguestflag = True
                request1.reserve_int = 0


                flag3 = 1
            else:
                sguestflag = False


                flag3 = 2

            sbuff = get_cache (Eg_subtask, {"sub_code": [(eq, request1.sub_task)]})

            if sbuff:

                if sbuff.othersflag :
                    sub_str = rbuff.subtask_bezeich
                else:
                    sub_str = sbuff.bezeich

            usr = get_cache (Eg_staff, {"nr": [(eq, request1.assign_to)]})

            if usr:
                usr_str = usr.name

            gbuff = db_session.query(Gbuff).filter(
                     (Gbuff.gastnr == request1.gastnr)).first()

            if gbuff:
                guestname = gbuff.name + " " + gbuff.vorname1 + ", " + gbuff.anrede1 + gbuff.anredefirma


    def getvendor():

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data, treqdetail_data, t_eg_request_data, t_eg_property_data, t_queasy130_data, t_queasy_data, t_zimmer_data, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, htparam, bediener, eg_vendor, eg_alert, eg_staff, guest, eg_vperform, eg_action, eg_reqdetail
        nonlocal pvilanguage, reqno, view_first, user_init
        nonlocal rbuff, subtask1


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1
        nonlocal t_zimmer_data, t_queasy_data, t_queasy130_data, t_eg_property_data, t_eg_request_data, treqdetail_data, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data

        vbuff = None
        qbuff = None
        Vbuff =  create_buffer("Vbuff",Eg_vperform)
        Qbuff =  create_buffer("Qbuff",Eg_vendor)

        for vbuff in db_session.query(Vbuff).filter(
                 (Vbuff.reqnr == request1.reqnr) & (Vbuff.logi1 == False)).order_by(Vbuff._recid).all():
            svendor = Svendor()
            svendor_data.append(svendor)

            svendor.reqnr = reqno
            svendor.vendor_nr = vbuff.vendor_nr
            svendor.docno = vbuff.DOcumentno
            svendor.startdate = vbuff.startdate
            svendor.estfinishdate = vbuff.estfinishdate
            svendor.finishdate = vbuff.finishdate
            svendor.price =  to_decimal(vbuff.price)
            svendor.bezeich = vbuff.bezeich
            svendor.pic = vbuff.pic
            svendor.perform_nr = vbuff.perform_nr
            svendor.stat = "1"


    def create_reqdetail():

        nonlocal groupid, engid, source_str, dept_str, strproperty, main_str, categ_str, sub_str, usr_str, guestname, sguestflag, flag1, flag2, flag3, s_othersflag, subtask_bez, avail_eg_request, avail_eg_subtask, avail_subtask, t_fstat, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data, treqdetail_data, t_eg_request_data, t_eg_property_data, t_queasy130_data, t_queasy_data, t_zimmer_data, lvcarea, alert_str, zimmer, queasy, eg_property, eg_request, eg_location, eg_subtask, htparam, bediener, eg_vendor, eg_alert, eg_staff, guest, eg_vperform, eg_action, eg_reqdetail
        nonlocal pvilanguage, reqno, view_first, user_init
        nonlocal rbuff, subtask1


        nonlocal t_zimmer, t_queasy, t_queasy130, t_eg_property, t_eg_request, treqdetail, svendor, rbuff, request1, send_alert, tvendor, t_eg_location, subtask1
        nonlocal t_zimmer_data, t_queasy_data, t_queasy130_data, t_eg_property_data, t_eg_request_data, treqdetail_data, svendor_data, request1_data, send_alert_data, tvendor_data, t_eg_location_data

        actbuff = None
        str:string = ""
        Actbuff =  create_buffer("Actbuff",Eg_action)
        treqdetail_data.clear()

        for eg_reqdetail in db_session.query(Eg_reqdetail).filter(
                 (Eg_reqdetail.reqnr == reqno) & (Eg_reqdetail.action != "")).order_by(Eg_reqdetail._recid).all():
            treqdetail = Treqdetail()
            treqdetail_data.append(treqdetail)

            treqdetail.reqnr = eg_reqdetail.reqnr
            treqdetail.actionnr = eg_reqdetail.actionnr
            treqdetail.action = eg_reqdetail.action
            treqdetail.create_date = eg_reqdetail.create_date
            treqdetail.create_time = eg_reqdetail.create_time
            treqdetail.create_str = to_string(eg_reqdetail.create_time, "HH:MM:SS")
            treqdetail.create_by = eg_reqdetail.create_by
            treqdetail.flag = True

    alert_str[0] = translateExtended ("Successfully", lvcarea, "")
    alert_str[1] = translateExtended ("Failed", lvcarea, "")
    alert_str[2] = translateExtended ("Pending", lvcarea, "")
    define_group()
    define_engineering()
    define_sms()

    for eg_location in db_session.query(Eg_location).order_by(Eg_location._recid).all():
        t_eg_location = T_eg_location()
        t_eg_location_data.append(t_eg_location)

        buffer_copy(eg_location, t_eg_location)

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
        t_zimmer = T_zimmer()
        t_zimmer_data.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)
    create_tvendor()
    create_alert()
    create_request()
    getvendor()
    create_reqdetail()

    request1 = query(request1_data, first=True)

    if view_first == False:

        eg_request = get_cache (Eg_request, {"reqnr": [(eq, reqno)],"reqstatus": [(eq, 1)]})

        if eg_request:
            t_eg_request = T_eg_request()
            t_eg_request_data.append(t_eg_request)

            buffer_copy(eg_request, t_eg_request)
            avail_eg_request = True

        eg_subtask = get_cache (Eg_subtask, {"sub_code": [(eq, request1.sub_task)]})

        if eg_subtask:
            s_othersflag = eg_subtask.othersflag
            avail_eg_subtask = True

    for eg_property in db_session.query(Eg_property).order_by(Eg_property._recid).all():
        t_eg_property = T_eg_property()
        t_eg_property_data.append(t_eg_property)

        buffer_copy(eg_property, t_eg_property)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 130)).order_by(Queasy._recid).all():
        t_queasy130 = T_queasy130()
        t_queasy130_data.append(t_queasy130)

        buffer_copy(queasy, t_queasy130)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 132) | (Queasy.key == 19)).order_by(Queasy._recid).all():
        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    request1 = query(request1_data, first=True)

    subtask1 = get_cache (Eg_subtask, {"dept_nr": [(eq, request1.deptnum)],"main_nr": [(eq, request1.maintask)],"sub_code": [(eq, request1.sub_task)]})

    if subtask1:
        avail_subtask = True
        subtask_bez = subtask1.bezeich

    eg_request = get_cache (Eg_request, {"reqnr": [(eq, reqno)]})

    if eg_request:
        t_fstat = eg_request.reqstatus
    else:
        t_fstat = 0

    return generate_output()