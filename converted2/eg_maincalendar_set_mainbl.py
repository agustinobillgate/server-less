#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Eg_location, Zimmer, Eg_property, Eg_staff, Bediener, Eg_maintain

def eg_maincalendar_set_mainbl(all_room:bool, engid:int):

    prepare_cache ([Queasy, Eg_location, Eg_property, Eg_maintain])

    troom_data = []
    tproperty_data = []
    tstatus_data = []
    tcategory_data = []
    maintain_data = []
    tpic_data = []
    tlocation_data = []
    tmaintask_data = []
    queasy = eg_location = zimmer = eg_property = eg_staff = bediener = eg_maintain = None

    maintain = tpic = tproperty = troom = tcategory = tlocation = tstatus = tmaintask = comcategory = qbuff1 = comlocat = commain = comroom = None

    maintain_data, Maintain = create_model("Maintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "donedate":date, "type":int, "maintask":int, "location":int, "zinr":string, "propertynr":int, "pic":int})
    tpic_data, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
    tproperty_data, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pcateg_nr":int, "pcateg":string, "pmain_nr":int, "pmain":string, "ploc_nr":int, "ploc":string, "pzinr":string})
    troom_data, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
    tcategory_data, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})
    tlocation_data, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
    tstatus_data, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":string, "stat_selected":bool})
    tmaintask_data, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal troom_data, tproperty_data, tstatus_data, tcategory_data, maintain_data, tpic_data, tlocation_data, tmaintask_data, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_data, tpic_data, tproperty_data, troom_data, tcategory_data, tlocation_data, tstatus_data, tmaintask_data

        return {"troom": troom_data, "tproperty": tproperty_data, "tStatus": tstatus_data, "tcategory": tcategory_data, "maintain": maintain_data, "tpic": tpic_data, "tLocation": tlocation_data, "tMaintask": tmaintask_data}

    def create_status():

        nonlocal troom_data, tproperty_data, tstatus_data, tcategory_data, maintain_data, tpic_data, tlocation_data, tmaintask_data, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_data, tpic_data, tproperty_data, troom_data, tcategory_data, tlocation_data, tstatus_data, tmaintask_data


        tstatus_data.clear()
        tstatus = Tstatus()
        tstatus_data.append(tstatus)

        tstatus.stat_nr = 1
        tstatus.stat_nm = "Scheduled"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_data.append(tstatus)

        tstatus.stat_nr = 2
        tstatus.stat_nm = "Processed"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_data.append(tstatus)

        tstatus.stat_nr = 3
        tstatus.stat_nm = "Done"
        tstatus.stat_selected = False


    def create_category():

        nonlocal troom_data, tproperty_data, tstatus_data, tcategory_data, maintain_data, tpic_data, tlocation_data, tmaintask_data, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_data, tpic_data, tproperty_data, troom_data, tcategory_data, tlocation_data, tstatus_data, tmaintask_data

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

        nonlocal troom_data, tproperty_data, tstatus_data, tcategory_data, maintain_data, tpic_data, tlocation_data, tmaintask_data, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_data, tpic_data, tproperty_data, troom_data, tcategory_data, tlocation_data, tstatus_data, tmaintask_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        Comcategory = Tcategory
        comcategory_data = tcategory_data
        tmaintask_data.clear()

        for comcategory in query(comcategory_data, filters=(lambda comcategory: comcategory.categ_selected)):

            for qbuff in db_session.query(Qbuff).filter(
                     (Qbuff.key == 133) & (Qbuff.number2 == comcategory.categ_nr)).order_by(Qbuff._recid).all():
                tmaintask = Tmaintask()
                tmaintask_data.append(tmaintask)

                tmaintask.main_nr = qbuff.number1
                tmaintask.main_nm = qbuff.char1
                tmaintask.main_selected = True


    def create_location():

        nonlocal troom_data, tproperty_data, tstatus_data, tcategory_data, maintain_data, tpic_data, tlocation_data, tmaintask_data, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_data, tpic_data, tproperty_data, troom_data, tcategory_data, tlocation_data, tstatus_data, tmaintask_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_location)
        tlocation_data.clear()
        tlocation = Tlocation()
        tlocation_data.append(tlocation)

        tlocation.loc_nr = 0
        tlocation.loc_nm = "Undefine"
        tlocation.loc_guest = False

        for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():

            if qbuff.guestflag :
                tlocation = Tlocation()
                tlocation_data.append(tlocation)

                tlocation.loc_nr = qbuff.nr
                tlocation.loc_nm = qbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = True


            else:
                tlocation = Tlocation()
                tlocation_data.append(tlocation)

                tlocation.loc_nr = qbuff.nr
                tlocation.loc_nm = qbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = False


    def create_room():

        nonlocal troom_data, tproperty_data, tstatus_data, tcategory_data, maintain_data, tpic_data, tlocation_data, tmaintask_data, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_data, tpic_data, tproperty_data, troom_data, tcategory_data, tlocation_data, tstatus_data, tmaintask_data

        i:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Zimmer)
        Qbuff1 = Tlocation
        qbuff1_data = tlocation_data
        troom_data.clear()

        qbuff1 = query(qbuff1_data, filters=(lambda qbuff1: qbuff1.loc_selected  and qbuff1.loc_guest), first=True)

        if qbuff1:

            for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():
                troom = Troom()
                troom_data.append(troom)

                troom.room_nm = qbuff.zinr
                troom.room_selected = False


        else:
            pass


    def create_property():

        nonlocal troom_data, tproperty_data, tstatus_data, tcategory_data, maintain_data, tpic_data, tlocation_data, tmaintask_data, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_data, tpic_data, tproperty_data, troom_data, tcategory_data, tlocation_data, tstatus_data, tmaintask_data

        qbuff = None
        ques = None
        Qbuff =  create_buffer("Qbuff",Eg_property)
        Comlocat = Tlocation
        comlocat_data = tlocation_data
        Commain = Tmaintask
        commain_data = tmaintask_data
        Comroom = Troom
        comroom_data = troom_data
        Ques =  create_buffer("Ques",Queasy)
        tproperty_data.clear()

        if all_room:

            for troom in query(troom_data):
                troom.room_selected = True

        tproperty = Tproperty()
        tproperty_data.append(tproperty)

        tproperty.prop_nr = 0
        tproperty.prop_nm = "Undefine"

        for comlocat in query(comlocat_data, filters=(lambda comlocat: comlocat.loc_selected)):

            if comlocat.loc_guest :

                qbuff_obj_list = {}
                for qbuff in db_session.query(Qbuff).filter(
                         (Qbuff.location == comlocat.loc_nr)).order_by(Qbuff._recid).all():
                    commain = query(commain_data, (lambda commain: commain.main_nr == qbuff.maintask and commain.main_selected), first=True)
                    if not commain:
                        continue

                    comroom = query(comroom_data, (lambda comroom: comroom.room_nm == qbuff.zinr and comroom.room_selected), first=True)
                    if not comroom:
                        continue

                    if qbuff_obj_list.get(qbuff._recid):
                        continue
                    else:
                        qbuff_obj_list[qbuff._recid] = True


                    tproperty = Tproperty()
                    tproperty_data.append(tproperty)

                    tproperty.prop_nr = qbuff.nr
                    tproperty.prop_nm = qbuff.bezeich + "(" + trim (to_string(qbuff.nr , ">>>>>>9")) + ")"
                    tproperty.pzinr = qbuff.zinr
                    tproperty.pmain_nr = qbuff.maintask
                    tproperty.ploc_nr = qbuff.location

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 133) & (Queasy.number1 == qbuff.maintask)).first()

                    if queasy:
                        tproperty.pmain = queasy.char1
                        tproperty.pcateg_nr = queasy.number2

                        ques = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, queasy.number2)]})

                        if ques:
                            tproperty.pcateg = ques.char1


                    else:
                        tproperty.pmain = ""
                        tproperty.pcateg_nr = 0
                        tproperty.pcateg = ""

                    eg_location = get_cache (Eg_location, {"nr": [(eq, qbuff.location)]})

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""


            else:

                qbuff_obj_list = {}
                for qbuff in db_session.query(Qbuff).filter(
                         (Qbuff.location == comlocat.loc_nr)).order_by(Qbuff._recid).all():
                    commain = query(commain_data, (lambda commain: commain.main_nr == qbuff.maintask and commain.main_selected), first=True)
                    if not commain:
                        continue

                    if qbuff_obj_list.get(qbuff._recid):
                        continue
                    else:
                        qbuff_obj_list[qbuff._recid] = True


                    tproperty = Tproperty()
                    tproperty_data.append(tproperty)

                    tproperty.prop_nr = qbuff.nr
                    tproperty.prop_nm = qbuff.bezeich
                    tproperty.pzinr = qbuff.zinr
                    tproperty.pmain_nr = qbuff.maintask
                    tproperty.ploc_nr = qbuff.location

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 133) & (Queasy.number1 == qbuff.maintask)).first()

                    if queasy:
                        tproperty.pmain = queasy.char1
                        tproperty.pcateg_nr = queasy.number2

                        ques = get_cache (Queasy, {"key": [(eq, 132)],"number1": [(eq, queasy.number2)]})

                        if ques:
                            tproperty.pcateg = ques.char1


                    else:
                        tproperty.pmain = ""
                        tproperty.pcateg_nr = 0
                        tproperty.pcateg = ""

                    eg_location = get_cache (Eg_location, {"nr": [(eq, qbuff.location)]})

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""


    def create_pic():

        nonlocal troom_data, tproperty_data, tstatus_data, tcategory_data, maintain_data, tpic_data, tlocation_data, tmaintask_data, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_data, tpic_data, tproperty_data, troom_data, tcategory_data, tlocation_data, tstatus_data, tmaintask_data

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
                 (Qbuff.usergroup == engid) & (Qbuff.activeflag)).order_by(Qbuff.nr).all():
            tpic = Tpic()
            tpic_data.append(tpic)

            tpic.pic_nr = qbuff.nr
            tpic.pic_nm = qbuff.name
            tpic.pic_dept = qbuff.usergroup
            tpic.pic_selected = False


    def create_maintain():

        nonlocal troom_data, tproperty_data, tstatus_data, tcategory_data, maintain_data, tpic_data, tlocation_data, tmaintask_data, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_data, tpic_data, tproperty_data, troom_data, tcategory_data, tlocation_data, tstatus_data, tmaintask_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_maintain)
        maintain_data.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.delete_flag == False)).order_by(Qbuff._recid).all():

            if qbuff.propertynr != 0:

                eg_property = get_cache (Eg_property, {"nr": [(eq, qbuff.propertynr)]})

                if eg_property:
                    maintain = Maintain()
                    maintain_data.append(maintain)

                    maintain.maintainnr = qbuff.maintainnr
                    maintain.workdate = qbuff.workdate
                    maintain.estworkdate = qbuff.estworkdate
                    maintain.donedate = qbuff.donedate
                    maintain.type = qbuff.type
                    maintain.maintask = eg_property.maintask
                    maintain.location = qbuff.location
                    maintain.zinr = qbuff.zinr
                    maintain.propertynr = qbuff.propertynr
                    maintain.pic = qbuff.pic


                else:
                    pass
            else:
                maintain = Maintain()
                maintain_data.append(maintain)

                maintain.maintainnr = qbuff.maintainnr
                maintain.workdate = qbuff.workdate
                maintain.estworkdate = qbuff.estworkdate
                maintain.donedate = qbuff.donedate
                maintain.type = qbuff.type
                maintain.maintask = eg_property.maintask
                maintain.location = qbuff.location
                maintain.zinr = qbuff.zinr
                maintain.propertynr = qbuff.propertynr
                maintain.pic = qbuff.pic


    create_status()
    create_category()
    create_pic()
    create_location()

    for tcategory in query(tcategory_data):
        tcategory.categ_selected = True


    create_maintask()

    for tlocation in query(tlocation_data):
        tlocation.loc_selected = True


    create_room()
    create_property()
    create_maintain()

    return generate_output()