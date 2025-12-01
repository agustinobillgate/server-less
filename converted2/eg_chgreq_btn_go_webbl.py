#using conversion tools version: 1.0.0.117

# ==================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# ==================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_request, Bediener, Eg_property, Eg_location, Eg_reqdetail, Eg_vperform, Res_history, Eg_staff, Queasy, Eg_subtask, Eg_queasy, L_artikel, Eg_vendor

treqdetail_data, Treqdetail = create_model("Treqdetail", {"reqnr":int, "actionnr":int, "action":string, "create_date":date, "create_time":int, "create_str":string, "create_by":string, "flag":bool})
request1_data, Request1 = create_model_like(Eg_request)
stock_data, Stock = create_model("Stock", {"nr":int, "stock_nr":int, "stock_nm":string, "stock_qty":Decimal, "stock_price":int, "stock_total":int})
attchment_data, Attchment = create_model("Attchment", {"nr":int, "att_file":string, "bezeich":string})
svendor_data, Svendor = create_model("Svendor", {"nr":string, "vendor_nr":int, "docno":string, "reqnr":int, "startdate":date, "estfinishdate":date, "finishdate":date, "price":Decimal, "bezeich":string, "pic":string, "created_by":string, "created_date":date, "created_time":int, "perform_nr":string, "stat":string})

def eg_chgreq_btn_go_webbl(treqdetail_data:[Treqdetail], request1_data:[Request1], stock_data:[Stock], attchment_data:[Attchment], svendor_data:[Svendor], pvilanguage:int, sub_str:string, solution:string, estfin_str:string, a:int, blout:int, reqno:int, user_init:string, prop_bezeich:string, sguestflag:bool):

    prepare_cache ([Eg_request, Bediener, Eg_property, Eg_location, Eg_vperform, Res_history, Queasy, Eg_subtask, L_artikel, Eg_vendor])

    blrange = 0
    avail_eg_staff = False
    usrnr:int = 0
    char1:string = ""
    prop_nr:int = 0
    lvcarea:string = "eg-chgreq"
    urgstr:List[string] = create_empty_list(10,"")
    statstr:List[string] = create_empty_list(5,"")
    eg_request = bediener = eg_property = eg_location = eg_reqdetail = eg_vperform = res_history = eg_staff = queasy = eg_subtask = eg_queasy = l_artikel = eg_vendor = None

    svendor = attchment = stock = request1 = treqdetail = usr = buff_property = sbuff = None

    Usr = create_buffer("Usr",Bediener)
    Buff_property = create_buffer("Buff_property",Eg_property)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal blrange, avail_eg_staff, usrnr, char1, prop_nr, lvcarea, urgstr, statstr, eg_request, bediener, eg_property, eg_location, eg_reqdetail, eg_vperform, res_history, eg_staff, queasy, eg_subtask, eg_queasy, l_artikel, eg_vendor
        nonlocal request1_data, pvilanguage, sub_str, solution, estfin_str, a, blout, reqno, user_init, prop_bezeich, sguestflag
        nonlocal usr, buff_property


        nonlocal svendor, attchment, stock, request1, treqdetail, usr, buff_property, sbuff

        return {"request1": request1_data, "blrange": blrange, "avail_eg_staff": avail_eg_staff}

    def create_log():

        nonlocal blrange, avail_eg_staff, prop_nr, lvcarea, urgstr, statstr, eg_request, bediener, eg_property, eg_location, eg_reqdetail, eg_vperform, res_history, eg_staff, queasy, eg_subtask, eg_queasy, l_artikel, eg_vendor
        nonlocal request1_data, pvilanguage, sub_str, solution, estfin_str, a, blout, reqno, user_init, prop_bezeich, sguestflag
        nonlocal usr, buff_property


        nonlocal svendor, attchment, stock, request1, treqdetail, usr, buff_property, sbuff

        usr = None
        usrnr:int = 0
        char1:string = ""
        char2:string = ""
        hour:int = 0
        minute:int = 0
        timeest:int = 0
        Usr =  create_buffer("Usr",Bediener)

        usr = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if usr:
            usrnr = usr.nr

        eg_request = get_cache (Eg_request, {"reqnr": [(eq, reqno)]})

        if eg_request:

            if eg_request.reqstatus != request1.reqstatus:

                if eg_request.reqstatus == 3 and request1.reqstatus == 2:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering"
                    res_history.aenderung = "Change Status reqno " + to_string(reqno) +\
                            ": " + statstr[eg_request.reqstatus - 1] + " To " + statstr[request1.reqstatus - 1] +\
                            " record status done by : " + eg_request.done_by + " date : " + to_string(eg_request.done_date, "99/99/99") +\
                            " time : "+ to_string(eg_request.done_time, "->,>>>,>>9")


                else:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering"
                    res_history.aenderung = "Change Status reqno " + to_string(reqno) +\
                            ": " + statstr[eg_request.reqstatus - 1] + " To " + statstr[request1.reqstatus - 1]

            if eg_request.source != request1.source:

                queasy = get_cache (Queasy, {"key": [(eq, 130)],"number1": [(eq, eg_request.source)]})

                if queasy:
                    char1 = queasy.char1

                queasy = get_cache (Queasy, {"key": [(eq, 130)],"number1": [(eq, request1.source)]})

                if queasy:
                    char2 = queasy.char1
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Engineering"
                res_history.aenderung = "Change Source reqno " + to_string(reqno) +\
                        ": " + char1 + " To " + char2

            if eg_request.deptnum != request1.deptnum:

                queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, eg_request.deptnum)]})

                if queasy:
                    char1 = queasy.char1

                queasy = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, request1.deptnum)]})

                if queasy:
                    char2 = queasy.char1
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Engineering"
                res_history.aenderung = "Change Dept In Charge reqno " + to_string(reqno) +\
                        ": " + char1 + " To " + char2

            if eg_request.source_name != request1.source_name:

                if eg_request.source_name == "":
                    char1 = ''

                if request1.source_name == "":
                    char2 = ''
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Engineering"
                res_history.aenderung = "Change Source-name reqno " + to_string(reqno) +\
                        ": " + char1 + " To " + char2

            if eg_request.propertynr == 0:

                if request1.maintask != eg_request.maintask:

                    queasy = get_cache (Queasy, {"key": [(eq, 133)],"number1": [(eq, eg_request.maintask)]})

                    if queasy:
                        char1 = queasy.char1

                    queasy = get_cache (Queasy, {"key": [(eq, 133)],"number1": [(eq, request1.maintask)]})

                    if queasy:
                        char2 = queasy.char1
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering"
                    res_history.aenderung = "Change Sub Group reqno " + to_string(reqno) +\
                            ": " + char1 + " To " + char2

                if request1.category != eg_request.category:

                    queasy = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, eg_request.category)]})

                    if queasy:
                        char1 = queasy.char1

                    queasy = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, request1.category)]})

                    if queasy:
                        char2 = queasy.char1
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering"
                    res_history.aenderung = "Change Main Group reqno " + to_string(reqno) +\
                            ": " + char1 + " To " + char2


            else:

                if eg_request.propertynr != request1.propertynr and request1.propertynr != 0:
                    char1 = to_string(eg_request.propertynr, ">,>>>,>>9")
                    char2 = to_string(request1.propertynr, ">,>>>,>>9")
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering"
                    res_history.aenderung = "Change Article reqno " + to_string(reqno) +\
                            ": " + char1 + " To " + char2


                else:
                    pass

            if request1.sub_task != eg_request.sub_task:

                eg_subtask = get_cache (Eg_subtask, {"sub_code": [(eq, eg_request.sub_task)]})

                if eg_subtask:
                    char1 = eg_subtask.bezeich

                eg_subtask = get_cache (Eg_subtask, {"sub_code": [(eq, request1.sub_task)]})

                if eg_subtask:
                    char2 = eg_subtask.bezeich
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Engineering"
                res_history.aenderung = "Change Sub Task reqno " + to_string(reqno) +\
                        ": " + char1 + " To " + char2

            if sub_str != eg_request.subtask_bezeich:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Engineering"
                res_history.aenderung = "Change Sub Task reqno " + to_string(reqno) +\
                        ": " + eg_request.subtask_bezeich + " To " + sub_str

            if request1.assign_to != eg_request.assign_to:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Engineering"
                res_history.aenderung = "Change PIC reqno " + to_string(reqno) +\
                        ": " + to_string(eg_request.assign_to) + " To " + to_string(request1.assign_to)

            if request1.zinr != eg_request.zinr:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Engineering"
                res_history.aenderung = "Change RmNo reqno " + to_string(reqno) +\
                        ": " + eg_request.zinr + " To " + request1.zinr

            if solution != "":
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Engineering"
                res_history.aenderung = "Add solution reqno " + to_string(reqno) +\
                        ": " + solution


            if eg_request.urgency != request1.urgency:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Engineering"
                res_history.aenderung = "Change Urgency reqno " + to_string(reqno) +\
                        ": " + urgstr[eg_request.urgency - 1] + " To " + urgstr[request1.urgency - 1]


            if eg_request.ex_finishdate != None:

                if eg_request.ex_finishdate != request1.ex_finishdate:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering"
                    res_history.aenderung = "Change Ex Finish Date reqno " + to_string(reqno) +\
                            ": " + to_string(eg_request.ex_finishdate, "99/99/99") + " To " +\
                            to_string(request1.ex_finishdate, "99/99/99")


                    eg_reqdetail = Eg_reqdetail()
                    db_session.add(eg_reqdetail)

                    eg_reqdetail.reqnr = reqno
                    eg_reqdetail.estfinishdate = request1.ex_finishdate
                    eg_reqdetail.estfinishtime = request1.ex_finishtime
                    eg_reqdetail.create_date = get_current_date()
                    eg_reqdetail.create_time = get_current_time_in_seconds()
                    eg_reqdetail.create_by = user_init


                else:

                    if eg_request.ex_finishtime != request1.ex_finishtime:
                        res_history = Res_history()
                        db_session.add(res_history)

                        res_history.nr = usrnr
                        res_history.datum = get_current_date()
                        res_history.zeit = get_current_time_in_seconds()
                        res_history.action = "Engineering"
                        res_history.aenderung = "Change Ex Finish Time reqno " + to_string(reqno) +\
                                ": " + to_string(eg_request.ex_finishtime, "HH:MM") + " To " +\
                                to_string(request1.ex_finishtime, "HH:MM")


                        eg_reqdetail = Eg_reqdetail()
                        db_session.add(eg_reqdetail)

                        eg_reqdetail.reqnr = reqno
                        eg_reqdetail.estfinishdate = request1.ex_finishdate
                        eg_reqdetail.estfinishtime = request1.ex_finishtime
                        eg_reqdetail.create_date = get_current_date()
                        eg_reqdetail.create_time = get_current_time_in_seconds()
                        eg_reqdetail.create_by = user_init


                    else:

                        if trim (replace (estfin_str, ":", "")) != "":
                            hour = (to_int(estfin_str) / 100)
                            minute = (to_int(estfin_str) - (hour * 100))
                            timeest = (hour * 3600) + (minute * 60)

                        if eg_request.ex_finishtime != timeest:
                            res_history = Res_history()
                            db_session.add(res_history)

                            res_history.nr = usrnr
                            res_history.datum = get_current_date()
                            res_history.zeit = get_current_time_in_seconds()
                            res_history.action = "Engineering"
                            res_history.aenderung = "Change Ex Finish Time reqno " + to_string(reqno) +\
                                    ": " + to_string(eg_request.ex_finishtime, "HH:MM") + " To " +\
                                    to_string(timeest , "HH:MM")

        for eg_queasy in db_session.query(Eg_queasy).filter(
                 (Eg_queasy.key == 1) & (Eg_queasy.reqnr == reqno)).order_by(Eg_queasy._recid).all():
            char1 = ""

            stock = query(stock_data, filters=(lambda stock: stock.stock_nr == eg_queasy.stock_nr), first=True)

            if not stock:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, eg_queasy.stock_nr)]})

                if l_artikel:
                    char1 = l_artikel.bezeich
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Engineering"
                res_history.aenderung = "Delete Stock reqno " + to_string(reqno) +\
                        ": " + char1


            else:

                if stock.stock_qty != eg_queasy.deci1:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering"
                    res_history.aenderung = "Change Stock Qty reqno " + to_string(reqno) +\
                            ": " + to_string(eg_queasy.deci1) + " To " +\
                            to_string(stock.stock_qty)

        for stock in query(stock_data):

            if stock.stock_nr != 0:

                eg_queasy = get_cache (Eg_queasy, {"key": [(eq, 1)],"reqnr": [(eq, reqno)],"stock_nr": [(eq, stock.stock_nr)]})

                if not eg_queasy:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering"
                    res_history.aenderung = "Add Stock reqno " + to_string(reqno) +\
                            ": " + stock.stock_nm + " Qty: " + to_string(stock.stock_qty)

        for attchment in query(attchment_data):

            if attchment.att_file != "":

                eg_queasy = get_cache (Eg_queasy, {"key": [(eq, 2)],"reqnr": [(eq, reqno)],"number1": [(eq, attchment.nr)]})

                if not eg_queasy:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering"
                    res_history.aenderung = "Add Attachment reqno " + to_string(reqno) +\
                            ": " + attchment.att_file


                else:

                    if attchment.att_file != eg_queasy.ATTACHMENT:
                        res_history = Res_history()
                        db_session.add(res_history)

                        res_history.nr = usrnr
                        res_history.datum = get_current_date()
                        res_history.zeit = get_current_time_in_seconds()
                        res_history.action = "Engineering"
                        res_history.aenderung = "Chg Attachment's reqno " + to_string(reqno) +\
                                ": " + eg_queasy.ATTACHMENT + " To " + attchment.att_file

                    if attchment.bezeich != eg_queasy.att_desc:
                        res_history = Res_history()
                        db_session.add(res_history)

                        res_history.nr = usrnr
                        res_history.datum = get_current_date()
                        res_history.zeit = get_current_time_in_seconds()
                        res_history.action = "Engineering"
                        res_history.aenderung = "Chg Attachment's desc reqno " + to_string(reqno) +\
                                ": " + eg_queasy.att_desc + " To " + attchment.bezeich

        for eg_queasy in db_session.query(Eg_queasy).filter(
                 (Eg_queasy.key == 2) & (Eg_queasy.reqnr == reqno)).order_by(Eg_queasy._recid).all():

            attchment = query(attchment_data, filters=(lambda attchment: attchment.nr == eg_queasy.number1), first=True)

            if not attchment or attchment.att_file == "":
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = usrnr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Engineering"
                res_history.aenderung = "Delete Attachment reqno " + to_string(reqno) +\
                        ": " + eg_queasy.ATTACHMENT


    def execute_it():

        nonlocal blrange, avail_eg_staff, usrnr, char1, prop_nr, lvcarea, urgstr, statstr, eg_request, bediener, eg_property, eg_location, eg_reqdetail, eg_vperform, res_history, eg_staff, queasy, eg_subtask, eg_queasy, l_artikel, eg_vendor
        nonlocal request1_data, pvilanguage, sub_str, solution, estfin_str, a, blout, reqno, user_init, prop_bezeich, sguestflag
        nonlocal usr, buff_property


        nonlocal svendor, attchment, stock, request1, treqdetail, usr, buff_property, sbuff

        timestr:string = ""
        number1:int = 0
        hist_ctr:int = 0
        hour:int = 0
        minute:int = 0
        timeest:int = 0
        usr = None
        Usr =  create_buffer("Usr",Eg_staff)

        for eg_queasy in db_session.query(Eg_queasy).filter(
                 (Eg_queasy.key == 3) & (Eg_queasy.reqnr == reqno)).order_by(Eg_queasy._recid).all():

            if eg_queasy.hist_nr > hist_ctr:
                hist_ctr = eg_queasy.hist_nr
        hist_ctr = hist_ctr + 1

        if request1.assign_to != eg_request.assign_to:

            usr = get_cache (Bediener, {"nr": [(eq, request1.assign_to)]})

            if usr:
                number1 = usr.nr
            eg_queasy = Eg_queasy()
            db_session.add(eg_queasy)

            eg_queasy.key = 3
            eg_queasy.reqnr = reqno
            eg_queasy.hist_nr = hist_ctr
            eg_queasy.hist_time = get_current_time_in_seconds()
            eg_queasy.hist_fdate = get_current_date()
            eg_queasy.usr_nr = number1


            pass

        if request1.reqstatus == 5 and eg_request.reqstatus != 5:
            request1.closed_date = get_current_date()
            request1.closed_by = user_init
            request1.closed_time = get_current_time_in_seconds()

        elif request1.reqstatus == 2 and eg_request.reqstatus != 2:
            request1.done_by = ""
            request1.done_date = None
            request1.done_time = 0
            request1.process_date = get_current_date()
            request1.process_by = user_init
            request1.process_time = get_current_time_in_seconds()

        elif request1.reqstatus == 3 and eg_request.reqstatus != 3:
            request1.done_date = get_current_date()
            request1.done_by = user_init
            request1.done_time = get_current_time_in_seconds()

            if eg_request.ex_finishdate != None:

                if eg_request.ex_finishdate == get_current_date():

                    if eg_request.ex_finishtime < get_current_time_in_seconds():
                        blrange = 1

                elif eg_request.ex_finishdate < get_current_date():
                    blrange = 1
            else:
                request1.ex_finishdate = request1.done_date
                request1.ex_finishtime = request1.done_time


        request1.subtask_bezeich = sub_str


        pass

        if request1.propertynr != 0:
            request1.maintask = 0
            request1.category = 0

        if trim (replace (estfin_str, ":", "")) != "":
            hour = (to_int(estfin_str) / 100)
            minute = (to_int(estfin_str) - (hour * 100))
            timeest = (hour * 3600) + (minute * 60)
            request1.ex_finishtime = timeest
        buffer_copy(request1, eg_request)

        if solution != "":
            eg_request.task_solv = eg_request.task_solv + solution + chr_unicode(10) + to_string(get_current_date(), "99/99/9999") + " - " + to_string(get_current_time_in_seconds(), "HH:MM:SS") + chr_unicode(10)
        pass

        for eg_queasy in db_session.query(Eg_queasy).filter(
                 (Eg_queasy.key == 1) & (Eg_queasy.reqnr == reqno)).order_by(Eg_queasy._recid).all():
            db_session.delete(eg_queasy)
        Sbuff = Stock
        sbuff_data = stock_data

        for sbuff in query(sbuff_data, sort_by=[("stock_nr",False)]):

            if sbuff.stock_nr != 0:
                eg_queasy = Eg_queasy()
                db_session.add(eg_queasy)

                eg_queasy.key = 1
                eg_queasy.reqnr = reqno
                eg_queasy.stock_nr = sbuff.stock_nr
                eg_queasy.deci1 =  to_decimal(sbuff.stock_qty)
                eg_queasy.price =  to_decimal(sbuff.stock_price)

        for eg_queasy in db_session.query(Eg_queasy).filter(
                 (Eg_queasy.key == 2) & (Eg_queasy.reqnr == reqno)).order_by(Eg_queasy._recid).all():
            db_session.delete(eg_queasy)

        for attchment in query(attchment_data):

            if attchment.att_file != "":
                eg_queasy = Eg_queasy()
                db_session.add(eg_queasy)

                eg_queasy.key = 2
                eg_queasy.reqnr = reqno
                eg_queasy.number1 = attchment.nr
                eg_queasy.attachment = attchment.att_file
                eg_queasy.att_desc = attchment.bezeich


    def save_vendor():

        nonlocal blrange, avail_eg_staff, prop_nr, lvcarea, urgstr, statstr, eg_request, bediener, eg_property, eg_location, eg_reqdetail, eg_vperform, res_history, eg_staff, queasy, eg_subtask, eg_queasy, l_artikel, eg_vendor
        nonlocal request1_data, pvilanguage, sub_str, solution, estfin_str, a, blout, reqno, user_init, prop_bezeich, sguestflag
        nonlocal usr, buff_property


        nonlocal svendor, attchment, stock, request1, treqdetail, usr, buff_property, sbuff

        usr = None
        usrnr:int = 0
        char1:string = ""
        char2:string = ""
        pbuff = None
        vbuff = None
        strvendor:string = ""
        strfull:string = ""
        startc:int = 0
        Usr =  create_buffer("Usr",Bediener)
        Pbuff =  create_buffer("Pbuff",Eg_vperform)
        Vbuff =  create_buffer("Vbuff",Eg_request)

        for svendor in query(svendor_data, filters=(lambda svendor: svendor.stat.lower()  == ("0").lower())):

            eg_vperform = get_cache (Eg_vperform, {"reqnr": [(eq, reqno)],"perform_nr": [(eq, svendor.perform_nr)]})

            if eg_vperform:
                eg_vperform.logi1 = True

        pbuff = get_cache (Eg_vperform, {"reqnr": [(eq, request1.reqnr)],"logi1": [(eq, False)]})

        if pbuff:

            eg_vendor = get_cache (Eg_vendor, {"vendor_nr": [(eq, pbuff.vendor_nr)]})

            if eg_vendor:
                char1 = eg_vendor.bezeich

            eg_vendor = get_cache (Eg_vendor, {"vendor_nr": [(eq, svendor.vendor_nr)]})

            if eg_vendor:
                char2 = eg_vendor.bezeich

            svendor = query(svendor_data, filters=(lambda svendor: svendor.reqnr == reqno and svendor.perform_nr == pbuff.perform_nr), first=True)

            if svendor:

                if pbuff.vendor_nr != svendor.vendor_nr:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering Vendor Perform"
                    res_history.aenderung = "Chg vendor reqno " + to_string(reqno) +\
                            ": " + char1 + " To " + char2

                if pbuff.documentno != svendor.docno:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering Vendor Perform"
                    res_history.aenderung = "Chg vendor reqno " + to_string(reqno) +\
                            ": " + pbuff.documentno + " To " + svendor.docno

                if pbuff.startdate != svendor.startdate:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering Vendor Perform"
                    res_history.aenderung = "Chg vendor start-date reqno " + to_string(reqno) +\
                            ": " + to_string(pbuff.startdate , "99/99/99") + " To " + to_string(svendor.startdate , "99/99/99")

                if pbuff.estfinishdate != svendor.estfinishdate:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering Vendor Perform"
                    res_history.aenderung = "Chg vendor estfinishdate reqno " + to_string(reqno) +\
                            ": " + to_string(pbuff.estfinishdate , "99/99/99") + " To " + to_string(svendor.estfinishdate , "99/99/99")

                if pbuff.finishdate != svendor.finishdate:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering Vendor Perform"
                    res_history.aenderung = "Chg vendor finishdate reqno " + to_string(reqno) +\
                            ": " + to_string(pbuff.finishdate , "99/99/99") + " To " + to_string(svendor.finishdate , "99/99/99")

                if pbuff.price != svendor.price:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering Vendor Perform"
                    res_history.aenderung = "Chg vendor Reparation Fee reqno " + to_string(reqno) +\
                            ": " + to_string(pbuff.price , "->>,>>>,>>>,>>9.99") + " To " + to_string(svendor.price , "->>,>>>,>>>,>>9.99")

                if pbuff.pic != svendor.pic:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = usrnr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Engineering Vendor Perform"
                    res_history.aenderung = "Chg vendor Reparation Fee reqno " + to_string(reqno) +\
                            ": " + pbuff.pic + " To " + svendor.pic

        eg_vperform = db_session.query(Eg_vperform).filter(
                 (Eg_vperform.reqnr == reqno)).order_by(Eg_vperform._recid.desc()).first()

        if eg_vperform:
            startc = int (eg_vperform.perform_nr) + 1
        else:
            startc = 1

        for svendor in query(svendor_data, filters=(lambda svendor: svendor.stat.lower()  == ("1").lower())):

            if substring(sVendor.perform_nr, 0, 1) != ("n").lower() :

                eg_vperform = get_cache (Eg_vperform, {"reqnr": [(eq, reqno)],"perform_nr": [(eq, svendor.perform_nr)]})

                if eg_vperform:
                    eg_vperform.reqnr = reqno
                    eg_vperform.created_by = user_init
                    eg_vperform.created_date = get_current_date()
                    eg_vperform.created_time = get_current_time_in_seconds()
                    eg_vperform.documentno = svendor.docno
                    eg_vperform.vendor_nr = svendor.vendor_nr
                    eg_vperform.startdate = svendor.startdate
                    eg_vperform.estfinishdate = svendor.estfinishdate
                    eg_vperform.finishdate = svendor.finishdate
                    eg_vperform.price =  to_decimal(svendor.price)
                    eg_vperform.bezeich = svendor.bezeich
                    eg_vperform.pic = svendor.pic


                else:
                    pass
            else:
                eg_vperform = Eg_vperform()
                db_session.add(eg_vperform)

                eg_vperform.reqnr = reqno
                eg_vperform.created_by = user_init
                eg_vperform.created_date = get_current_date()
                eg_vperform.created_time = get_current_time_in_seconds()
                eg_vperform.documentno = svendor.docno
                eg_vperform.vendor_nr = svendor.vendor_nr
                eg_vperform.startdate = svendor.startdate
                eg_vperform.estfinishdate = svendor.estfinishdate
                eg_vperform.finishdate = svendor.finishdate
                eg_vperform.price =  to_decimal(svendor.price)
                eg_vperform.bezeich = svendor.bezeich
                eg_vperform.pic = svendor.pic
                eg_vperform.perform_nr = to_string(startc)


                startc = startc + 1

    urgstr[0] = translateExtended ("Low", lvcarea, "")
    urgstr[1] = translateExtended ("Medium", lvcarea, "")
    urgstr[2] = translateExtended ("High", lvcarea, "")
    statstr[0] = translateExtended ("New", lvcarea, "")
    statstr[1] = translateExtended ("Processed", lvcarea, "")
    statstr[2] = translateExtended ("Done", lvcarea, "")
    statstr[3] = translateExtended ("Postponed", lvcarea, "")
    statstr[4] = translateExtended ("Closed", lvcarea, "")

    request1 = query(request1_data, first=True)

    if request1.propertynr == 0:

        for buff_property in db_session.query(Buff_property).order_by(Buff_property.nr.desc()).yield_per(100):
            prop_nr = buff_property.nr
            break
        prop_nr = prop_nr + 1
        eg_property = Eg_property()
        db_session.add(eg_property)

        eg_property.nr = prop_nr
        eg_property.bezeich = prop_bezeich
        eg_property.maintask = request1.maintask
        eg_property.zinr = request1.zinr
        eg_property.datum = get_current_date()

        if sguestflag :

            eg_location = get_cache (Eg_location, {"guestflag": [(eq, True)]})

            if eg_location:
                eg_property.location = eg_location.nr
        else:
            eg_property.location = request1.reserve_int
        request1.propertynr = prop_nr
    create_log()
    execute_it()

    for treqdetail in query(treqdetail_data, filters=(lambda treqdetail: treqdetail.flag == False and treqdetail.action != "")):
        eg_reqdetail = Eg_reqdetail()
        db_session.add(eg_reqdetail)

        eg_reqdetail.reqnr = treqdetail.reqnr
        eg_reqdetail.actionnr = treqdetail.actionnr
        eg_reqdetail.action = treqdetail.action
        eg_reqdetail.create_date = treqdetail.create_date
        eg_reqdetail.create_time = treqdetail.create_time
        eg_reqdetail.create_by = treqdetail.create_by

    for eg_reqdetail in db_session.query(Eg_reqdetail).order_by(Eg_reqdetail._recid).all():

        if eg_reqdetail.actionnr == 0:

            treqdetail = query(treqdetail_data, filters=(lambda treqdetail: treqdetail.action == eg_reqdetail.action), first=True)

            if not treqdetail:
                db_session.delete(eg_reqdetail)
        else:

            treqdetail = query(treqdetail_data, filters=(lambda treqdetail: treqdetail.actionnr == eg_reqdetail.actionnr), first=True)

            if not treqdetail:
                db_session.delete(eg_reqdetail)

    if blout == 2:

        usr = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if usr:
            usrnr = usr.nr

        eg_vperform = get_cache (Eg_vperform, {"reqnr": [(eq, reqno)]})

        if eg_vperform:
            char1 = to_string(eg_vperform.reqnr, "->,>>>,>>9") + ";" + to_string(eg_vperform.created_by) + ";" + to_string(eg_vperform.created_date, "99/99/99") + ";" + to_string(eg_vperform.created_time, "->,>>>,>>9") + ";" + to_string(eg_vperform.vendor_nr, "->,>>>,>>9") + ";" + to_string(eg_vperform.startdate, "99/99/99") + ";" + to_string(eg_vperform.estfinishdate, "99/99/99") + ";" + to_string(eg_vperform.finishdate, "99/99/99") + ";" + to_string(eg_vperform.price, "->>,>>>,>>>,>>9.99") + ";" + eg_vperform.bezeich + ";" + eg_vperform.pic
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = usrnr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Engineering Vendor Perform"
            res_history.aenderung = "Delete outsource reqno " + to_string(reqno) +\
                    ": " + char1


            eg_vperform.logi1 = True


    save_vendor()

    eg_staff = get_cache (Eg_staff, {"nr": [(eq, request1.assign_to)],"mobile": [(ne, "")]})

    if eg_staff:
        avail_eg_staff = True

    return generate_output()