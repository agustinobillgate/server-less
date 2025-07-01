#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Eg_location, Zimmer, Eg_property, Eg_staff, Bediener, Eg_maintain

def eg_maincalendar_set_mainbl(all_room:bool, engid:int):

    prepare_cache ([Queasy, Eg_location, Eg_property, Eg_maintain])

    troom_list = []
    tproperty_list = []
    tstatus_list = []
    tcategory_list = []
    maintain_list = []
    tpic_list = []
    tlocation_list = []
    tmaintask_list = []
    queasy = eg_location = zimmer = eg_property = eg_staff = bediener = eg_maintain = None

    maintain = tpic = tproperty = troom = tcategory = tlocation = tstatus = tmaintask = comcategory = qbuff1 = comlocat = commain = comroom = None

    maintain_list, Maintain = create_model("Maintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "donedate":date, "type":int, "maintask":int, "location":int, "zinr":string, "propertynr":int, "pic":int})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":string, "pic_selected":bool, "pic_dept":int})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":string, "prop_selected":bool, "pcateg_nr":int, "pcateg":string, "pmain_nr":int, "pmain":string, "ploc_nr":int, "ploc":string, "pzinr":string})
    troom_list, Troom = create_model("Troom", {"room_nm":string, "room_selected":bool})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":string, "categ_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":string, "loc_selected":bool, "loc_guest":bool})
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":string, "stat_selected":bool})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":string, "main_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list

        return {"troom": troom_list, "tproperty": tproperty_list, "tStatus": tstatus_list, "tcategory": tcategory_list, "maintain": maintain_list, "tpic": tpic_list, "tLocation": tlocation_list, "tMaintask": tmaintask_list}

    def create_status():

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list


        tstatus_list.clear()
        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tstatus.stat_nr = 1
        tstatus.stat_nm = "Scheduled"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tstatus.stat_nr = 2
        tstatus.stat_nm = "Processed"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tstatus.stat_nr = 3
        tstatus.stat_nm = "Done"
        tstatus.stat_selected = False


    def create_category():

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        tcategory_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 132)).order_by(Qbuff._recid).all():
            tcategory = Tcategory()
            tcategory_list.append(tcategory)

            tcategory.categ_nr = qbuff.number1
            tcategory.categ_nm = qbuff.char1
            tcategory.categ_selected = False


    def create_maintask():

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        Comcategory = Tcategory
        comcategory_list = tcategory_list
        tmaintask_list.clear()

        for comcategory in query(comcategory_list, filters=(lambda comcategory: comcategory.categ_selected)):

            for qbuff in db_session.query(Qbuff).filter(
                     (Qbuff.key == 133) & (Qbuff.number2 == comcategory.categ_nr)).order_by(Qbuff._recid).all():
                tmaintask = Tmaintask()
                tmaintask_list.append(tmaintask)

                tmaintask.main_nr = qbuff.number1
                tmaintask.main_nm = qbuff.char1
                tmaintask.main_selected = True


    def create_location():

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_location)
        tlocation_list.clear()
        tlocation = Tlocation()
        tlocation_list.append(tlocation)

        tlocation.loc_nr = 0
        tlocation.loc_nm = "Undefine"
        tlocation.loc_guest = False

        for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():

            if qbuff.guestflag :
                tlocation = Tlocation()
                tlocation_list.append(tlocation)

                tlocation.loc_nr = qbuff.nr
                tlocation.loc_nm = qbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = True


            else:
                tlocation = Tlocation()
                tlocation_list.append(tlocation)

                tlocation.loc_nr = qbuff.nr
                tlocation.loc_nm = qbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = False


    def create_room():

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list

        i:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Zimmer)
        Qbuff1 = Tlocation
        qbuff1_list = tlocation_list
        troom_list.clear()

        qbuff1 = query(qbuff1_list, filters=(lambda qbuff1: qbuff1.loc_selected  and qbuff1.loc_guest), first=True)

        if qbuff1:

            for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():
                troom = Troom()
                troom_list.append(troom)

                troom.room_nm = qbuff.zinr
                troom.room_selected = False


        else:
            pass


    def create_property():

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list

        qbuff = None
        ques = None
        Qbuff =  create_buffer("Qbuff",Eg_property)
        Comlocat = Tlocation
        comlocat_list = tlocation_list
        Commain = Tmaintask
        commain_list = tmaintask_list
        Comroom = Troom
        comroom_list = troom_list
        Ques =  create_buffer("Ques",Queasy)
        tproperty_list.clear()

        if all_room:

            for troom in query(troom_list):
                troom.room_selected = True

        tproperty = Tproperty()
        tproperty_list.append(tproperty)

        tproperty.prop_nr = 0
        tproperty.prop_nm = "Undefine"

        for comlocat in query(comlocat_list, filters=(lambda comlocat: comlocat.loc_selected)):

            if comlocat.loc_guest :

                qbuff_obj_list = {}
                for qbuff in db_session.query(Qbuff).filter(
                         (Qbuff.location == comlocat.loc_nr)).order_by(Qbuff._recid).all():
                    commain = query(commain_list, (lambda commain: commain.main_nr == qbuff.maintask and commain.main_selected), first=True)
                    if not commain:
                        continue

                    comroom = query(comroom_list, (lambda comroom: comroom.room_nm == qbuff.zinr and comroom.room_selected), first=True)
                    if not comroom:
                        continue

                    if qbuff_obj_list.get(qbuff._recid):
                        continue
                    else:
                        qbuff_obj_list[qbuff._recid] = True


                    tproperty = Tproperty()
                    tproperty_list.append(tproperty)

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
                    commain = query(commain_list, (lambda commain: commain.main_nr == qbuff.maintask and commain.main_selected), first=True)
                    if not commain:
                        continue

                    if qbuff_obj_list.get(qbuff._recid):
                        continue
                    else:
                        qbuff_obj_list[qbuff._recid] = True


                    tproperty = Tproperty()
                    tproperty_list.append(tproperty)

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

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list

        qbuff = None
        qbuff1 = None
        Qbuff =  create_buffer("Qbuff",Eg_staff)
        Qbuff1 =  create_buffer("Qbuff1",Bediener)
        tpic_list.clear()
        tpic = Tpic()
        tpic_list.append(tpic)

        tpic.pic_nr = 0
        tpic.pic_nm = ""
        tpic.pic_selected = False

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.usergroup == engid) & (Qbuff.activeflag)).order_by(Qbuff.nr).all():
            tpic = Tpic()
            tpic_list.append(tpic)

            tpic.pic_nr = qbuff.nr
            tpic.pic_nm = qbuff.name
            tpic.pic_dept = qbuff.usergroup
            tpic.pic_selected = False


    def create_maintain():

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal all_room, engid


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, comcategory, qbuff1, comlocat, commain, comroom
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_maintain)
        maintain_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.delete_flag == False)).order_by(Qbuff._recid).all():

            if qbuff.propertynr != 0:

                eg_property = get_cache (Eg_property, {"nr": [(eq, qbuff.propertynr)]})

                if eg_property:
                    maintain = Maintain()
                    maintain_list.append(maintain)

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
                maintain_list.append(maintain)

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

    for tcategory in query(tcategory_list):
        tcategory.categ_selected = True


    create_maintask()

    for tlocation in query(tlocation_list):
        tlocation.loc_selected = True


    create_room()
    create_property()
    create_maintain()

    return generate_output()