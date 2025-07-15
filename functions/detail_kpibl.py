#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_request, Eg_location, Eg_staff, Bediener, Queasy

def detail_kpibl(nr:int, displayby:int):

    prepare_cache ([Eg_request, Eg_location, Eg_staff, Queasy])

    b2_list_data = []
    eg_request = eg_location = eg_staff = bediener = queasy = None

    b2_list = tpic = tcategory = tmaintask = None

    b2_list_data, B2_list = create_model("B2_list", {"urgency":string, "urgency_desc":string, "stat":string, "stat_desc":string, "created_date":date, "stat_open_date":date, "stat_finish_date":date, "location":string, "location_desc":string, "pic_nr":int, "pic_nm":string, "roomno":string})
    tpic_data, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
    tcategory_data, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})
    tmaintask_data, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b2_list_data, eg_request, eg_location, eg_staff, bediener, queasy
        nonlocal nr, displayby


        nonlocal b2_list, tpic, tcategory, tmaintask
        nonlocal b2_list_data, tpic_data, tcategory_data, tmaintask_data

        return {"b2-list": b2_list_data}

    def create_pic():

        nonlocal b2_list_data, eg_request, eg_location, eg_staff, bediener, queasy
        nonlocal nr, displayby


        nonlocal b2_list, tpic, tcategory, tmaintask
        nonlocal b2_list_data, tpic_data, tcategory_data, tmaintask_data

        qbuff = None
        qbuff1 = None
        Qbuff =  create_buffer("Qbuff",Eg_staff)
        Qbuff1 =  create_buffer("Qbuff1",Bediener)
        tpic_data.clear()
        tpic = Tpic()
        tpic_data.append(tpic)

        tpic.pic_nr = 0
        tpic.pic_nm = ""
        tpic.pic_selected = False

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.activeflag)).order_by(Qbuff.nr).all():
            tpic = Tpic()
            tpic_data.append(tpic)

            tpic.pic_nr = qbuff.nr
            tpic.pic_nm = qbuff.name
            tpic.pic_dept = qbuff.usergroup
            tpic.pic_selected = False


    def create_category():

        nonlocal b2_list_data, eg_request, eg_location, eg_staff, bediener, queasy
        nonlocal nr, displayby


        nonlocal b2_list, tpic, tcategory, tmaintask
        nonlocal b2_list_data, tpic_data, tcategory_data, tmaintask_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        tcategory_data.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 132)).order_by(Qbuff._recid).all():
            tcategory = Tcategory()
            tcategory_data.append(tcategory)

            tcategory.categ_nr = qbuff.number1
            tcategory.categ_nm = qbuff.char1
            tcategory.categ_selected = False


    def create_maintask():

        nonlocal b2_list_data, eg_request, eg_location, eg_staff, bediener, queasy
        nonlocal nr, displayby


        nonlocal b2_list, tpic, tcategory, tmaintask
        nonlocal b2_list_data, tpic_data, tcategory_data, tmaintask_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        tmaintask_data.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 133)).order_by(Qbuff._recid).all():
            tmaintask = Tmaintask()
            tmaintask_data.append(tmaintask)

            tmaintask.main_nr = qbuff.number1
            tmaintask.main_nm = qbuff.char1
            tmaintask.main_selected = False


    create_pic()
    create_category()
    create_maintask()

    if displayby == 1:

        for eg_request in db_session.query(Eg_request).filter(
                 (Eg_request.assign_to == nr)).order_by(Eg_request._recid).all():
            b2_list = B2_list()
            b2_list_data.append(b2_list)

            b2_list.urgency = to_string(eg_request.urgency)

            if b2_list.urgency.lower()  == ("1").lower() :
                b2_list.urgency_desc = "Low"

            if b2_list.urgency.lower()  == ("2").lower() :
                b2_list.urgency_desc = "Medium"

            if b2_list.urgency.lower()  == ("3").lower() :
                b2_list.urgency_desc = "High"
            b2_list.stat = to_string(eg_request.reqstatus)

            if b2_list.stat.lower()  == ("1").lower() :
                b2_list.stat_desc = "New"

            if b2_list.stat.lower()  == ("2").lower() :
                b2_list.stat_desc = "Processed"

            if b2_list.stat.lower()  == ("3").lower() :
                b2_list.stat_desc = "Done"

            if b2_list.stat.lower()  == ("4").lower() :
                b2_list.stat_desc = "Postpone"

            if b2_list.stat.lower()  == ("5").lower() :
                b2_list.stat_desc = "Closed"
            b2_list.created_date = eg_request.created_date
            b2_list.stat_open_date = eg_request.opened_date
            b2_list.stat_finish_date = eg_request.ex_finishdate
            b2_list.location = to_string(eg_request.location)

            eg_location = get_cache (Eg_location, {"nr": [(eq, eg_request.reserve_int)]})

            if eg_location:
                b2_list.location_desc = eg_location.bezeich

    if displayby == 2:

        for eg_request in db_session.query(Eg_request).filter(
                 (Eg_request.location == nr)).order_by(Eg_request._recid).all():
            b2_list = B2_list()
            b2_list_data.append(b2_list)

            b2_list.urgency = to_string(eg_request.urgency)

            if b2_list.urgency.lower()  == ("1").lower() :
                b2_list.urgency_desc = "Low"

            if b2_list.urgency.lower()  == ("2").lower() :
                b2_list.urgency_desc = "Medium"

            if b2_list.urgency.lower()  == ("3").lower() :
                b2_list.urgency_desc = "High"
            b2_list.stat = to_string(eg_request.reqstatus)

            if b2_list.stat.lower()  == ("1").lower() :
                b2_list.stat_desc = "New"

            if b2_list.stat.lower()  == ("2").lower() :
                b2_list.stat_desc = "Processed"

            if b2_list.stat.lower()  == ("3").lower() :
                b2_list.stat_desc = "Done"

            if b2_list.stat.lower()  == ("4").lower() :
                b2_list.stat_desc = "Postpone"

            if b2_list.stat.lower()  == ("5").lower() :
                b2_list.stat_desc = "Closed"
            b2_list.created_date = eg_request.created_date
            b2_list.stat_open_date = eg_request.opened_date
            b2_list.stat_finish_date = eg_request.ex_finishdate
            b2_list.roomno = eg_request.zinr

            for tpic in query(tpic_data, filters=(lambda tpic: tpic.pic_nr == eg_request.assign_to)):

                if tpic:
                    b2_list.pic_nm = tpic.pic_nm

    if displayby == 3:

        for eg_request in db_session.query(Eg_request).filter(
                 (Eg_request.category == nr)).order_by(Eg_request._recid).all():
            b2_list = B2_list()
            b2_list_data.append(b2_list)

            b2_list.urgency = to_string(eg_request.urgency)

            if b2_list.urgency.lower()  == ("1").lower() :
                b2_list.urgency_desc = "Low"

            if b2_list.urgency.lower()  == ("2").lower() :
                b2_list.urgency_desc = "Medium"

            if b2_list.urgency.lower()  == ("3").lower() :
                b2_list.urgency_desc = "High"
            b2_list.stat = to_string(eg_request.reqstatus)

            if b2_list.stat.lower()  == ("1").lower() :
                b2_list.stat_desc = "New"

            if b2_list.stat.lower()  == ("2").lower() :
                b2_list.stat_desc = "Processed"

            if b2_list.stat.lower()  == ("3").lower() :
                b2_list.stat_desc = "Done"

            if b2_list.stat.lower()  == ("4").lower() :
                b2_list.stat_desc = "Postpone"

            if b2_list.stat.lower()  == ("5").lower() :
                b2_list.stat_desc = "Closed"
            b2_list.created_date = eg_request.created_date
            b2_list.stat_open_date = eg_request.opened_date
            b2_list.stat_finish_date = eg_request.ex_finishdate
            b2_list.roomno = eg_request.zinr

            for tpic in query(tpic_data, filters=(lambda tpic: tpic.pic_nr == eg_request.assign_to)):

                if tpic:
                    b2_list.pic_nm = tpic.pic_nm

            eg_location = get_cache (Eg_location, {"nr": [(eq, eg_request.reserve_int)]})

            if eg_location:
                b2_list.location_desc = eg_location.bezeich

    if displayby == 4:

        for eg_request in db_session.query(Eg_request).filter(
                 (Eg_request.maintask == nr)).order_by(Eg_request._recid).all():
            b2_list = B2_list()
            b2_list_data.append(b2_list)

            b2_list.urgency = to_string(eg_request.urgency)

            if b2_list.urgency.lower()  == ("1").lower() :
                b2_list.urgency_desc = "Low"

            if b2_list.urgency.lower()  == ("2").lower() :
                b2_list.urgency_desc = "Medium"

            if b2_list.urgency.lower()  == ("3").lower() :
                b2_list.urgency_desc = "High"
            b2_list.stat = to_string(eg_request.reqstatus)

            if b2_list.stat.lower()  == ("1").lower() :
                b2_list.stat_desc = "New"

            if b2_list.stat.lower()  == ("2").lower() :
                b2_list.stat_desc = "Processed"

            if b2_list.stat.lower()  == ("3").lower() :
                b2_list.stat_desc = "Done"

            if b2_list.stat.lower()  == ("4").lower() :
                b2_list.stat_desc = "Postpone"

            if b2_list.stat.lower()  == ("5").lower() :
                b2_list.stat_desc = "Closed"
            b2_list.created_date = eg_request.created_date
            b2_list.stat_open_date = eg_request.opened_date
            b2_list.stat_finish_date = eg_request.ex_finishdate
            b2_list.roomno = eg_request.zinr

            eg_staff = get_cache (Eg_staff, {"nr": [(eq, eg_request.assign_to)]})

            if eg_staff:
                b2_list.pic_nm = eg_staff.name

            eg_location = get_cache (Eg_location, {"nr": [(eq, eg_request.reserve_int)]})

            if eg_location:
                b2_list.location_desc = eg_location.bezeich

            for tpic in query(tpic_data, filters=(lambda tpic: tpic.pic_nr == eg_request.assign_to)):

                if tpic:
                    b2_list.pic_nm = tpic.pic_nm

    return generate_output()