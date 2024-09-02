from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy, Eg_location, Zimmer, Eg_property, Eg_staff, Bediener, Eg_maintain

def eg_maincalendar_set_mainbl(all_room:bool, engid:int):
    troom_list = []
    tproperty_list = []
    tstatus_list = []
    tcategory_list = []
    maintain_list = []
    tpic_list = []
    tlocation_list = []
    tmaintask_list = []
    queasy = eg_location = zimmer = eg_property = eg_staff = bediener = eg_maintain = None

    maintain = tpic = tproperty = troom = tcategory = tlocation = tstatus = tmaintask = qbuff = comcategory = qbuff1 = comlocat = commain = comroom = ques = None

    maintain_list, Maintain = create_model("Maintain", {"maintainnr":int, "workdate":date, "estworkdate":date, "donedate":date, "type":int, "maintask":int, "location":int, "zinr":str, "propertynr":int, "pic":int})
    tpic_list, Tpic = create_model("Tpic", {"pic_nr":int, "pic_nm":str, "pic_selected":bool, "pic_dept":int})
    tproperty_list, Tproperty = create_model("Tproperty", {"prop_nr":int, "prop_nm":str, "prop_selected":bool, "pcateg_nr":int, "pcateg":str, "pmain_nr":int, "pmain":str, "ploc_nr":int, "ploc":str, "pzinr":str})
    troom_list, Troom = create_model("Troom", {"room_nm":str, "room_selected":bool})
    tcategory_list, Tcategory = create_model("Tcategory", {"categ_nr":int, "categ_nm":str, "categ_selected":bool})
    tlocation_list, Tlocation = create_model("Tlocation", {"loc_nr":int, "loc_nm":str, "loc_selected":bool, "loc_guest":bool})
    tstatus_list, Tstatus = create_model("Tstatus", {"stat_nr":int, "stat_nm":str, "stat_selected":bool})
    tmaintask_list, Tmaintask = create_model("Tmaintask", {"main_nr":int, "main_nm":str, "main_selected":bool})

    Qbuff = Eg_maintain
    Comcategory = Tcategory
    comcategory_list = tcategory_list

    Qbuff1 = Bediener
    Comlocat = Tlocation
    comlocat_list = tlocation_list

    Commain = Tmaintask
    commain_list = tmaintask_list

    Comroom = Troom
    comroom_list = troom_list

    Ques = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list
        return {"troom": troom_list, "tproperty": tproperty_list, "tStatus": tstatus_list, "tcategory": tcategory_list, "maintain": maintain_list, "tpic": tpic_list, "tLocation": tlocation_list, "tMaintask": tmaintask_list}

    def create_status():

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list


        tStatus_list.clear()
        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 1
        tStatus.stat_nm = "Scheduled"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 2
        tStatus.stat_nm = "Processed"
        tstatus.stat_selected = False


        tstatus = Tstatus()
        tstatus_list.append(tstatus)

        tStatus.stat_nr = 3
        tStatus.stat_nm = "Done"
        tstatus.stat_selected = False

    def create_category():

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list


        Qbuff = Queasy
        tcategory_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 132)).all():
            tcategory = Tcategory()
            tcategory_list.append(tcategory)

            tcategory.categ_nr = qbuff.number1
            tcategory.categ_nm = qbuff.char1
            tcategory.categ_selected = False

    def create_maintask():

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list


        Qbuff = Queasy
        Comcategory = Tcategory
        tMaintask_list.clear()

        for comcategory in query(comcategory_list, filters=(lambda comcategory :comCategory.categ_SELECTED)):

            for qbuff in db_session.query(Qbuff).filter(
                    (Qbuff.key == 133) &  (Qbuff.number2 == comcategory.categ_nr)).all():
                tmaintask = Tmaintask()
                tmaintask_list.append(tmaintask)

                tMaintask.Main_nr = qbuff.number1
                tMaintask.Main_nm = qbuff.char1
                tmaintask.main_selected = True

    def create_location():

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list


        Qbuff = Eg_location
        tLocation_list.clear()
        tlocation = Tlocation()
        tlocation_list.append(tlocation)

        tlocation.loc_nr = 0
        tlocation.loc_nm = "Undefine"
        tlocation.loc_guest = False

        for qbuff in db_session.query(Qbuff).all():

            if qbuff.guestflag :
                tlocation = Tlocation()
                tlocation_list.append(tlocation)

                tLocation.loc_nr = qbuff.nr
                tLocation.loc_nm = qbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = True


            else:
                tlocation = Tlocation()
                tlocation_list.append(tlocation)

                tLocation.loc_nr = qbuff.nr
                tLocation.loc_nm = qbuff.bezeich
                tlocation.loc_selected = True
                tlocation.loc_guest = False

    def create_room():

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list

        i:int = 0
        Qbuff = Zimmer
        Qbuff1 = Tlocation
        troom_list.clear()

        qbuff1 = query(qbuff1_list, filters=(lambda qbuff1 :qbuff1.loc_selected  and qbuff1.loc_guest), first=True)

        if qbuff1:

            for qbuff in db_session.query(Qbuff).all():
                troom = Troom()
                troom_list.append(troom)

                troom.room_nm = qbuff.zinr
                troom.room_SELECTED = False


        else:
            pass

    def create_property():

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list


        Qbuff = Eg_property
        Comlocat = Tlocation
        Commain = Tmaintask
        Comroom = Troom
        Ques = Queasy
        tproperty_list.clear()

        if all_room:

            for troom in query(troom_list):
                troom.room_selected = True

        tproperty = Tproperty()
        tproperty_list.append(tproperty)

        tproperty.prop_nr = 0
        tproperty.prop_nm = "Undefine"

        for comlocat in query(comlocat_list, filters=(lambda comlocat :comlocat.loc_selected)):

            if comlocat.loc_guest :

                qbuff_obj_list = []
                for qbuff, commain, comroom in db_session.query(Qbuff, Commain, Comroom).join(Commain,(Commain.main_nr == Qbuff.maintask) &  (Commain.main_selected)).join(Comroom,(Comroom.room_nm == Qbuff.zinr) &  (Comroom.room_selected)).filter(
                        (Qbuff.location == comlocat.loc_nr)).all():
                    if qbuff._recid in qbuff_obj_list:
                        continue
                    else:
                        qbuff_obj_list.append(qbuff._recid)


                    tproperty = Tproperty()
                    tproperty_list.append(tproperty)

                    tproperty.prop_nr = qbuff.nr
                    tproperty.prop_nm = qbuff.bezeich + "(" + trim (to_string(qbuff.nr , ">>>>>>9")) + ")"
                    tproperty.pzinr = qbuff.zinr
                    tproperty.pmain_nr = qbuff.maintask
                    tproperty.ploc_nr = qbuff.location

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.KEY == 133) &  (Queasy.number1 == qbuff.maintask)).first()

                    if queasy:
                        tproperty.pmain = queasy.char1
                        tproperty.pcateg_nr = queasy.number2

                        ques = db_session.query(Ques).filter(
                                (Ques.key == 132) &  (Ques.number1 == queasy.number2)).first()

                        if ques:
                            tproperty.pcateg = ques.char1


                    else:
                        tproperty.pmain = ""
                        tproperty.pcateg_nr = 0
                        tproperty.pcateg = ""

                    eg_location = db_session.query(Eg_location).filter(
                            (Eg_location.nr == qbuff.location)).first()

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""


            else:

                qbuff_obj_list = []
                for qbuff, commain in db_session.query(Qbuff, Commain).join(Commain,(Commain.main_nr == Qbuff.maintask) &  (Commain.main_selected)).filter(
                        (Qbuff.location == comlocat.loc_nr)).all():
                    if qbuff._recid in qbuff_obj_list:
                        continue
                    else:
                        qbuff_obj_list.append(qbuff._recid)


                    tproperty = Tproperty()
                    tproperty_list.append(tproperty)

                    tproperty.prop_nr = qbuff.nr
                    tproperty.prop_nm = qbuff.bezeich
                    tproperty.pzinr = qbuff.zinr
                    tproperty.pmain_nr = qbuff.maintask
                    tproperty.ploc_nr = qbuff.location

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.KEY == 133) &  (Queasy.number1 == qbuff.maintask)).first()

                    if queasy:
                        tproperty.pmain = queasy.char1
                        tproperty.pcateg_nr = queasy.number2

                        ques = db_session.query(Ques).filter(
                                (Ques.key == 132) &  (Ques.number1 == queasy.number2)).first()

                        if ques:
                            tproperty.pcateg = ques.char1


                    else:
                        tproperty.pmain = ""
                        tproperty.pcateg_nr = 0
                        tproperty.pcateg = ""

                    eg_location = db_session.query(Eg_location).filter(
                            (Eg_location.nr == qbuff.location)).first()

                    if eg_location:
                        tproperty.ploc = eg_location.bezeich


                    else:
                        tproperty.ploc = ""

    def create_pic():

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list


        Qbuff = Eg_staff
        Qbuff1 = Bediener
        tpic_list.clear()
        tpic = Tpic()
        tpic_list.append(tpic)

        tpic.pic_nr = 0
        tpic.pic_nm = ""
        tpic.pic_selected = False

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.usergroup == engid) &  (Qbuff.activeflag)).all():
            tpic = Tpic()
            tpic_list.append(tpic)

            tpic.pic_nr = qbuff.nr
            tpic.pic_nm = qbuff.name
            tpic.pic_dept = qbuff.usergroup
            tpic.pic_selected = False

    def create_maintain():

        nonlocal troom_list, tproperty_list, tstatus_list, tcategory_list, maintain_list, tpic_list, tlocation_list, tmaintask_list, queasy, eg_location, zimmer, eg_property, eg_staff, bediener, eg_maintain
        nonlocal qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques


        nonlocal maintain, tpic, tproperty, troom, tcategory, tlocation, tstatus, tmaintask, qbuff, comcategory, qbuff1, comlocat, commain, comroom, ques
        nonlocal maintain_list, tpic_list, tproperty_list, troom_list, tcategory_list, tlocation_list, tstatus_list, tmaintask_list


        Qbuff = Eg_maintain
        maintain_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.delete_flag == False)).all():

            if qbuff.propertynr != 0:

                eg_property = db_session.query(Eg_property).filter(
                        (Eg_property.nr == qbuff.propertynr)).first()

                if eg_property:
                    maintain = Maintain()
                    maintain_list.append(maintain)

                    maintain.maintainnr = qbuff.maintainnr
                    maintain.workdate = qbuff.workdate
                    maintain.estworkdate = qbuff.estworkdate
                    maintain.donedate = qbuff.donedate
                    maintain.TYPE = qbuff.TYPE
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
                maintain.TYPE = qbuff.TYPE
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