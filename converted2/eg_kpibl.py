#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Bediener, Eg_request, Eg_location, Eg_staff

def eg_kpibl(from_date:date, to_date:date):

    prepare_cache ([Queasy, Eg_request, Eg_location])

    counter:int = 0
    counter1:int = 0
    counter2:int = 0
    counter3:int = 0
    counter4:int = 0
    pic_list_data = []
    location_list_data = []
    category_list_data = []
    object_list_data = []
    queasy = bediener = eg_request = eg_location = eg_staff = None

    pic_list = location_list = category_list = object_list = tpic = tlocation = tmaintask = tcategory = troom = t_queasy = t_bediener = None

    pic_list_data, Pic_list = create_model("Pic_list", {"name1":string, "new1":int, "processed1":int, "done1":int, "postponed1":int, "closed1":int, "nr":int})
    location_list_data, Location_list = create_model("Location_list", {"name1":string, "new1":int, "processed1":int, "done1":int, "postponed1":int, "closed1":int, "nr":int})
    category_list_data, Category_list = create_model("Category_list", {"name1":string, "new1":int, "processed1":int, "done1":int, "postponed1":int, "closed1":int, "sub_code":int})
    object_list_data, Object_list = create_model("Object_list", {"name1":string, "new1":int, "processed1":int, "done1":int, "postponed1":int, "closed1":int, "sub_code":int})
    tpic_data, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
    tlocation_data, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
    tmaintask_data, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})
    tcategory_data, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})
    troom_data, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
    t_queasy_data, T_queasy = create_model_like(Queasy)
    t_bediener_data, T_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal counter, counter1, counter2, counter3, counter4, pic_list_data, location_list_data, category_list_data, object_list_data, queasy, bediener, eg_request, eg_location, eg_staff
        nonlocal from_date, to_date


        nonlocal pic_list, location_list, category_list, object_list, tpic, tlocation, tmaintask, tcategory, troom, t_queasy, t_bediener
        nonlocal pic_list_data, location_list_data, category_list_data, object_list_data, tpic_data, tlocation_data, tmaintask_data, tcategory_data, troom_data, t_queasy_data, t_bediener_data

        return {"pic-list": pic_list_data, "location-list": location_list_data, "category-list": category_list_data, "object-list": object_list_data}

    def define_group():

        nonlocal counter, counter1, counter2, counter3, counter4, pic_list_data, location_list_data, category_list_data, object_list_data, queasy, bediener, eg_request, eg_location, eg_staff
        nonlocal from_date, to_date


        nonlocal pic_list, location_list, category_list, object_list, tpic, tlocation, tmaintask, tcategory, troom, t_queasy, t_bediener
        nonlocal pic_list_data, location_list_data, category_list_data, object_list_data, tpic_data, tlocation_data, tmaintask_data, tcategory_data, troom_data, t_queasy_data, t_bediener_data

        for bediener in db_session.query(Bediener).order_by(Bediener._recid).all():
            t_bediener = T_bediener()
            t_bediener_data.append(t_bediener)

            buffer_copy(bediener, t_bediener)


    def create_pic():

        nonlocal counter, counter1, counter2, counter3, counter4, pic_list_data, location_list_data, category_list_data, object_list_data, queasy, bediener, eg_request, eg_location, eg_staff
        nonlocal from_date, to_date


        nonlocal pic_list, location_list, category_list, object_list, tpic, tlocation, tmaintask, tcategory, troom, t_queasy, t_bediener
        nonlocal pic_list_data, location_list_data, category_list_data, object_list_data, tpic_data, tlocation_data, tmaintask_data, tcategory_data, troom_data, t_queasy_data, t_bediener_data

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


    def create_maintask():

        nonlocal counter, counter1, counter2, counter3, counter4, pic_list_data, location_list_data, category_list_data, object_list_data, queasy, bediener, eg_request, eg_location, eg_staff
        nonlocal from_date, to_date


        nonlocal pic_list, location_list, category_list, object_list, tpic, tlocation, tmaintask, tcategory, troom, t_queasy, t_bediener
        nonlocal pic_list_data, location_list_data, category_list_data, object_list_data, tpic_data, tlocation_data, tmaintask_data, tcategory_data, troom_data, t_queasy_data, t_bediener_data

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


    def create_category():

        nonlocal counter, counter1, counter2, counter3, counter4, pic_list_data, location_list_data, category_list_data, object_list_data, queasy, bediener, eg_request, eg_location, eg_staff
        nonlocal from_date, to_date


        nonlocal pic_list, location_list, category_list, object_list, tpic, tlocation, tmaintask, tcategory, troom, t_queasy, t_bediener
        nonlocal pic_list_data, location_list_data, category_list_data, object_list_data, tpic_data, tlocation_data, tmaintask_data, tcategory_data, troom_data, t_queasy_data, t_bediener_data

        qbuff1 = None
        Qbuff1 =  create_buffer("Qbuff1",Queasy)
        tcategory_data.clear()

        for qbuff1 in db_session.query(Qbuff1).filter(
                 (Qbuff1.key == 132)).order_by(Qbuff1._recid).all():
            tcategory = Tcategory()
            tcategory_data.append(tcategory)

            tcategory.categ_nr = qbuff1.number1
            tcategory.categ_nm = qbuff1.char1
            tcategory.categ_selected = False

    define_group()
    create_pic()
    create_category()
    create_maintask()

    for eg_request in db_session.query(Eg_request).filter(
             (Eg_request.opened_date >= from_date) & (Eg_request.opened_date <= to_date) & (Eg_request.deptnum >= 0)).order_by(Eg_request._recid).all():

        for tpic in query(tpic_data, filters=(lambda tpic: tpic.pic_nr == eg_request.assign_to)):

            if eg_request:

                pic_list = query(pic_list_data, filters=(lambda pic_list: pic_list.name1 == tpic.pic_nm), first=True)

                if pic_list:
                    pic_list.name1 = tpic.pic_nm

                    if eg_request.reqStatus == 1:
                        pic_list.new1 = pic_list.new1 + 1

                    if eg_request.reqStatus == 2:
                        pic_list.processed1 = pic_list.processed1 + 1

                    if eg_request.reqStatus == 3:
                        pic_list.done1 = pic_list.done1 + 1

                    if eg_request.reqStatus == 4:
                        pic_list.postponed1 = pic_list.postponed1 + 1

                    if eg_request.reqStatus == 5:
                        pic_list.closed = pic_list.closed + 1

            if not pic_list:
                pic_list = Pic_list()
                pic_list_data.append(pic_list)

                pic_list.name1 = tpic.pic_nm

                if eg_request.reqStatus == 1:
                    pic_list.new1 = 1

                if eg_request.reqStatus == 2:
                    pic_list.processed1 = 1

                if eg_request.reqStatus == 3:
                    pic_list.done1 = 1

                if eg_request.reqStatus == 4:
                    pic_list.postponed1 = 1

                if eg_request.reqStatus == 5:
                    pic_list.closed1 = 1

        for eg_location in db_session.query(Eg_location).filter(
                 (Eg_location.nr == eg_request.location)).order_by(Eg_location._recid).all():

            if eg_request:

                location_list = query(location_list_data, filters=(lambda location_list: location_list.nr == eg_location.nr), first=True)

                if location_list:
                    location_list.name1 = eg_location.bezeich


                    location_list.nr = eg_location.nr

                    if eg_request.reqStatus == 1:
                        location_list.new1 = location_list.new1 + 1

                    if eg_request.reqStatus == 2:
                        location_list.processed1 = location_list.processed1 + 1

                    if eg_request.reqStatus == 3:
                        location_list.done1 = location_list.done1 + 1

                    if eg_request.reqStatus == 4:
                        location_list.postponed1 = location_list.postponed1 + 1

                    if eg_request.reqStatus == 5:
                        location_list.closed = location_list.closed + 1

                if not location_list:
                    location_list = Location_list()
                    location_list_data.append(location_list)


                    if eg_request.reqStatus == 1:
                        location_list.new1 = 1

                    if eg_request.reqStatus == 2:
                        location_list.processed1 = 1

                    if eg_request.reqStatus == 3:
                        location_list.done1 = 1

                    if eg_request.reqStatus == 4:
                        location_list.postponed1 = 1

                    if eg_request.reqStatus == 5:
                        location_list.closed = 1

        for tmaintask in query(tmaintask_data, filters=(lambda tmaintask: tmaintask.tMaintask.main_nr == eg_request.maintask)):

            if eg_request:

                object_list = query(object_list_data, filters=(lambda object_list: object_list.sub_code == tMaintask.main_nr), first=True)

                if object_list:
                    object_list.name1 = tmaintask.main_nm


                    object_list.sub_code = tmaintask.main_nr

                    if eg_request.reqStatus == 1:
                        object_list.new1 = object_list.new1 + 1
                    counter = 0

                    if eg_request.reqStatus == 2:
                        object_list.processed1 = object_list.processed1 + 1
                    counter1 = 0

                    if eg_request.reqStatus == 3:
                        object_list.done1 = object_list.done1 + 1
                counter2 = 0

                if eg_request.reqStatus == 4:
                    object_list.postponed1 = object_list.postponed1 + 1
                counter3 = 0

                if eg_request.reqStatus == 5:
                    object_list.closed = object_list.closed + 1
                counter4 = 0

            if not object_list:
                object_list = Object_list()
                object_list_data.append(object_list)

                object_list.name1 = tmaintask.main_nm


                object_list.sub_code = tmaintask.main_nr

                if eg_request.reqStatus == 1:
                    object_list.new1 = 1
                counter = 0

                if eg_request.reqStatus == 2:
                    object_list.processed1 = 1

                if eg_request.reqStatus == 3:
                    object_list.done1 = 1

                if eg_request.reqStatus == 4:
                    object_list.postponed1 = 1

                if eg_request.reqStatus == 5:
                    object_list.closed = 1

    for tcategory in query(tcategory_data):

        category_list = query(category_list_data, filters=(lambda category_list: category_list.sub_code == tcategory.categ_nr), first=True)

        if category_list:
            category_list.name1 = tmaintask.main_nm


            category_list.sub_code = tmaintask.main_nr

            if eg_request.reqStatus == 1:
                category_list.new1 = category_list.new1 + 1

            if eg_request.reqStatus == 2:
                category_list.processed1 = category_list.processed1 + 1

            if eg_request.reqStatus == 3:
                category_list.done1 = category_list.done1 + 1

            if eg_request.reqStatus == 4:
                category_list.postponed1 = category_list.postponed1 + 1

            if eg_request.reqStatus == 5:
                category_list.closed = category_list.closed + 1

        if not category_list:
            category_list = Category_list()
            category_list_data.append(category_list)

            category_list.name1 = tmaintask.main_nm


            category_list.sub_code = tmaintask.main_nr

            if eg_request.reqStatus == 1:
                category_list.new1 = 1

            if eg_request.reqStatus == 2:
                category_list.processed1 = 1

            if eg_request.reqStatus == 3:
                category_list.done1 = 1

            if eg_request.reqStatus == 4:
                category_list.postponed1 = 1

            if eg_request.reqStatus == 5:
                category_list.closed = 1

        for category_list in query(category_list_data):
            pass

    return generate_output()